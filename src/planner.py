"""
InsightAI - Natural Language Query Planner & Explanation Engine
Translates human questions into deterministic execution plans.
Uses strict schema validation, offline heuristic fallback, and grounded explanations.
Zero hallucinations: calculations are performed by Python, not LLM guesses.
"""

import os
import json
import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from src.executor import DeterministicExecutor, ExecutionResult


@dataclass
class AnalysisPlan:
    """Structured plan for deterministic execution."""
    operation: str  # 'aggregate', 'time_trend', 'top_n', 'correlation', 'unknown'
    group_col: Optional[str] = None
    metric_col: Optional[str] = None
    agg_func: str = "sum"
    top_n: int = 10
    sort_desc: bool = True
    confidence: float = 1.0
    rationale: str = ""


class QueryPlanner:
    """Translates natural language questions to verified execution plans."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def plan_and_execute(self, query: str, df: pd.DataFrame) -> Tuple[AnalysisPlan, ExecutionResult]:
        """
        Takes user question and DataFrame, generates verified plan,
        and deterministically executes it.
        """
        plan = self._generate_plan(query, df)

        # Execute plan safely
        if plan.operation == "aggregate" and plan.group_col and plan.metric_col:
            result = DeterministicExecutor.aggregate_by_category(
                df,
                group_col=plan.group_col,
                metric_col=plan.metric_col,
                agg_func=plan.agg_func,
                top_n=plan.top_n,
                sort_desc=plan.sort_desc
            )
        elif plan.operation == "time_trend" and plan.group_col and plan.metric_col:
            result = DeterministicExecutor.time_trend(
                df,
                date_col=plan.group_col,
                metric_col=plan.metric_col,
                agg_func=plan.agg_func
            )
        elif plan.operation == "top_n" and plan.metric_col:
            result = DeterministicExecutor.top_n_records(
                df,
                metric_col=plan.metric_col,
                n=plan.top_n,
                ascending=not plan.sort_desc
            )
        elif plan.operation == "correlation" and plan.metric_col:
            result = DeterministicExecutor.correlation_drivers(
                df,
                target_col=plan.metric_col,
                top_k=plan.top_n
            )
        else:
            # Fallback to general first numeric column aggregation
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
            if numeric_cols and cat_cols:
                plan.operation = "aggregate"
                plan.group_col = cat_cols[0]
                plan.metric_col = numeric_cols[0]
                result = DeterministicExecutor.aggregate_by_category(
                    df,
                    group_col=plan.group_col,
                    metric_col=plan.metric_col,
                    agg_func="sum",
                    top_n=10
                )
            else:
                return plan, ExecutionResult(
                    success=False,
                    error_message="Could not map question to available numeric and categorical columns."
                )

        # Enhance narrative with LLM if API key available and execution succeeded
        if result.success and self.api_key:
            enhanced_narrative = self._generate_llm_insight(query, plan, result)
            if enhanced_narrative:
                result.narrative = enhanced_narrative

        return plan, result

    def _generate_plan(self, query: str, df: pd.DataFrame) -> AnalysisPlan:
        """Generate structured plan using OpenAI if configured, or robust heuristic parser."""
        if self.api_key:
            try:
                llm_plan = self._plan_with_openai(query, df)
                if llm_plan and self._validate_plan(llm_plan, df):
                    return llm_plan
            except Exception:
                pass  # Graceful fallback to heuristic parser

        return self._heuristic_plan(query, df)

    def _validate_plan(self, plan: AnalysisPlan, df: pd.DataFrame) -> bool:
        """Validate that all columns referenced in the plan actually exist in the dataset."""
        if plan.group_col and plan.group_col not in df.columns:
            return False
        if plan.metric_col and plan.metric_col not in df.columns:
            return False
        return True

    def _plan_with_openai(self, query: str, df: pd.DataFrame) -> Optional[AnalysisPlan]:
        """Use OpenAI structured outputs to build verified execution plan."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)

        columns_info = {
            col: str(dtype)
            for col, dtype in zip(df.columns, df.dtypes)
        }

        system_prompt = (
            "You are a strict data analysis planner for tabular datasets. "
            "You map natural language questions into safe, deterministic execution operations. "
            "Never write code or hallucinate numbers. Output strictly valid JSON."
        )

        user_content = json.dumps({
            "query": query,
            "dataset_columns": columns_info,
            "allowed_operations": ["aggregate", "time_trend", "top_n", "correlation"]
        })

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_analysis_plan",
                    "description": "Construct deterministic plan based only on existing dataset columns.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["aggregate", "time_trend", "top_n", "correlation"]
                            },
                            "group_col": {"type": "string", "description": "Categorical or date column name"},
                            "metric_col": {"type": "string", "description": "Numeric column name"},
                            "agg_func": {
                                "type": "string",
                                "enum": ["sum", "mean", "median", "max", "min", "count"]
                            },
                            "top_n": {"type": "integer", "default": 10},
                            "sort_desc": {"type": "boolean", "default": True},
                            "rationale": {"type": "string"}
                        },
                        "required": ["operation", "metric_col", "rationale"]
                    }
                }
            }
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "create_analysis_plan"}},
            temperature=0.0
        )

        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            args = json.loads(tool_calls[0].function.arguments)
            return AnalysisPlan(
                operation=args.get("operation", "aggregate"),
                group_col=args.get("group_col"),
                metric_col=args.get("metric_col"),
                agg_func=args.get("agg_func", "sum"),
                top_n=args.get("top_n", 10),
                sort_desc=args.get("sort_desc", True),
                rationale=args.get("rationale", "")
            )
        return None

    def _heuristic_plan(self, query: str, df: pd.DataFrame) -> AnalysisPlan:
        """Deterministic fuzzy pattern matching mapping queries to column operations."""
        q = query.lower()
        cols = list(df.columns)
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        non_numeric_cols = [c for c in cols if c not in numeric_cols]

        # 1. Find matched metric column (numeric)
        metric_col = None
        for col in numeric_cols:
            c_norm = col.lower().replace("_", " ")
            if c_norm in q or col.lower() in q:
                metric_col = col
                break
        if not metric_col and numeric_cols:
            metric_col = numeric_cols[0]

        # 2. Find matched group column (categorical or datetime)
        group_col = None
        for col in cols:
            c_norm = col.lower().replace("_", " ")
            if (c_norm in q or col.lower() in q) and col != metric_col:
                group_col = col
                break

        # 3. Determine operation
        op = "aggregate"
        if any(w in q for w in ["trend", "over time", "monthly", "daily", "timeline", "progression", "date"]):
            op = "time_trend"
        elif any(w in q for w in ["correlat", "driver", "relationship", "factor", "impact"]):
            op = "correlation"
        elif any(w in q for w in ["top", "highest", "best", "leading", "worst", "lowest"]) and not group_col and not any(w in q for w in ["by", "per", "across", "which", "each"]):
            op = "top_n"

        # 4. Extract aggregation function
        agg_func = "sum"
        if any(w in q for w in ["average", "avg", "mean"]):
            agg_func = "mean"
        elif any(w in q for w in ["median"]):
            agg_func = "median"
        elif any(w in q for w in ["max", "highest", "peak"]) and op != "top_n":
            agg_func = "sum"  # default to sum ranking for "highest revenue by region"
        elif any(w in q for w in ["min", "lowest"]) and op != "top_n":
            agg_func = "sum"
        elif any(w in q for w in ["count", "number of", "frequency"]):
            agg_func = "count"

        # 5. Detect Top N
        top_n = 10
        match_n = re.search(r"\btop\s+(\d+)\b", q)
        if match_n:
            top_n = int(match_n.group(1))

        # For time trends, find first date-like column if not selected
        if op == "time_trend":
            for col in cols:
                if any(k in col.lower() for k in ["date", "time", "year", "month", "day"]):
                    group_col = col
                    break

        if not group_col and non_numeric_cols:
            group_col = non_numeric_cols[0]

        return AnalysisPlan(
            operation=op,
            group_col=group_col,
            metric_col=metric_col,
            agg_func=agg_func,
            top_n=top_n,
            sort_desc=not any(w in q for w in ["lowest", "bottom", "worst"]),
            confidence=0.9,
            rationale=f"Mapped '{query}' to {op} on {metric_col} grouped by {group_col} ({agg_func})."
        )

    def _generate_llm_insight(self, query: str, plan: AnalysisPlan, result: ExecutionResult) -> Optional[str]:
        """Produce a humanized, concise executive summary grounded in verified calculation."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            sample_data = result.result_df.head(5).to_dict(orient="records") if result.result_df is not None else {}
            prompt = (
                f"User asked: '{query}'\n"
                f"Verified deterministic calculation KPIs: {json.dumps(result.kpis)}\n"
                f"Top results: {json.dumps(sample_data)}\n\n"
                "Write a warm, concise, humanized executive insight (2-3 sentences max). "
                "Quote exact verified figures. Do NOT use buzzwords, corporate fluff, or robot talk."
            )

            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an executive data analyst writing clean, humanized briefs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.3
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            return None

    @staticmethod
    def get_suggested_queries(df: pd.DataFrame) -> List[str]:
        """Generate human-friendly, smart starter questions based on dataset schema."""
        suggestions = []
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

        # Filter out id-like columns from categorical grouping
        meaningful_cat_cols = [
            c for c in cat_cols 
            if not any(k in c.lower() for k in ["id", "uuid", "guid", "hash", "code", "index"])
            and df[c].nunique() < max(2, len(df) * 0.8)
        ]
        if not meaningful_cat_cols:
            meaningful_cat_cols = cat_cols

        # Prioritize key numeric metrics (revenue, sales, profit, amount, price, value, total)
        priority_metrics = [
            c for c in numeric_cols
            if any(k in c.lower() for k in ["revenue", "profit", "sales", "amount", "total", "cost", "price", "score", "value"])
        ]
        chosen_numeric = priority_metrics + [c for c in numeric_cols if c not in priority_metrics]

        date_col = next((c for c in df.columns if any(k in c.lower() for k in ["date", "time", "year"])), None)

        if chosen_numeric and meaningful_cat_cols:
            c_cat = meaningful_cat_cols[0]
            c_num = chosen_numeric[0]
            suggestions.append(f"Which {c_cat} generates the highest {c_num}?")
            if len(meaningful_cat_cols) > 1 and len(chosen_numeric) > 1:
                suggestions.append(f"What is the average {chosen_numeric[1]} by {meaningful_cat_cols[1]}?")
            suggestions.append(f"Top 5 {c_cat} by {c_num}")

        if len(chosen_numeric) >= 2:
            suggestions.append(f"What features correlate most with {chosen_numeric[0]}?")

        if date_col and chosen_numeric:
            suggestions.append(f"Show trend of {chosen_numeric[0]} over {date_col}")

        # Fallbacks if schema is minimal
        if not suggestions:
            suggestions = [
                "Summarize key numeric distributions",
                "Show top records by volume",
                "Breakdown of records across main category"
            ]

        return suggestions[:4]
