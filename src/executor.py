"""
InsightAI - Deterministic Pandas Analysis Engine
Executes structured analytical queries deterministically on tabular data.
Guarantees mathematically verified results with zero hallucinations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import numpy as np


@dataclass
class ExecutionResult:
    """Standardized result returned by the deterministic analysis engine."""
    success: bool
    result_df: Optional[pd.DataFrame] = None
    kpis: Dict[str, Any] = field(default_factory=dict)
    chart_type: str = "bar"  # 'bar', 'line', 'scatter', 'box', 'table'
    chart_config: Dict[str, Any] = field(default_factory=dict)
    narrative: str = ""
    operation_type: str = ""
    error_message: Optional[str] = None


class DeterministicExecutor:
    """Safe, deterministic pandas calculation engine."""

    @staticmethod
    def aggregate_by_category(
        df: pd.DataFrame,
        group_col: str,
        metric_col: str,
        agg_func: str = "sum",
        top_n: Optional[int] = 10,
        sort_desc: bool = True
    ) -> ExecutionResult:
        """
        Group by a categorical column and aggregate a numeric metric.
        Computes total, average, and percentage share.
        """
        if group_col not in df.columns or metric_col not in df.columns:
            return ExecutionResult(
                success=False,
                error_message=f"Columns '{group_col}' or '{metric_col}' not found in dataset."
            )

        if not pd.api.types.is_numeric_dtype(df[metric_col]):
            return ExecutionResult(
                success=False,
                error_message=f"Metric column '{metric_col}' must be numeric."
            )

        agg_map = {
            "sum": "sum",
            "mean": "mean",
            "average": "mean",
            "count": "count",
            "median": "median",
            "max": "max",
            "min": "min"
        }
        func = agg_map.get(agg_func.lower(), "sum")

        try:
            grouped = (
                df.groupby(group_col, dropna=False)[metric_col]
                .agg(func)
                .reset_index()
            )
            agg_col_name = f"{metric_col}_{func}"
            grouped.rename(columns={metric_col: agg_col_name}, inplace=True)
            grouped[group_col] = grouped[group_col].fillna("Unspecified").astype(str)

            grouped.sort_values(by=agg_col_name, ascending=not sort_desc, inplace=True)

            total_val = float(df[metric_col].sum()) if func == "sum" else float(df[metric_col].mean())
            if func == "sum" and total_val != 0:
                grouped["pct_share"] = (grouped[agg_col_name] / total_val * 100).round(2)

            display_df = grouped.head(top_n) if top_n else grouped

            # KPIs
            top_row = grouped.iloc[0] if not grouped.empty else None
            top_category = top_row[group_col] if top_row is not None else "N/A"
            top_val = float(top_row[agg_col_name]) if top_row is not None else 0.0

            kpis = {
                "total_categories": int(grouped[group_col].nunique()),
                "top_category": top_category,
                "top_value": top_val,
                "aggregate_metric": f"{func.upper()}({metric_col})"
            }
            if "pct_share" in grouped.columns and top_row is not None:
                kpis["top_pct_share"] = float(top_row["pct_share"])

            # Human narrative
            human_func = "Total" if func == "sum" else ("Average" if func == "mean" else func.capitalize())
            if "pct_share" in grouped.columns and top_row is not None:
                narrative = (
                    f"{top_category} leads with {human_func.lower()} {metric_col} of "
                    f"{top_val:,.2f}, accounting for {top_row['pct_share']:.1f}% of the overall total "
                    f"across all {kpis['total_categories']} {group_col} segments."
                )
            else:
                narrative = (
                    f"{top_category} ranks highest with an {human_func.lower()} {metric_col} "
                    f"of {top_val:,.2f} across {kpis['total_categories']} {group_col} segments."
                )

            return ExecutionResult(
                success=True,
                result_df=display_df,
                kpis=kpis,
                chart_type="bar",
                chart_config={
                    "x": group_col,
                    "y": agg_col_name,
                    "title": f"{human_func} {metric_col} by {group_col}",
                    "color": agg_col_name
                },
                narrative=narrative,
                operation_type="aggregation"
            )
        except Exception as e:
            return ExecutionResult(success=False, error_message=str(e))

    @staticmethod
    def time_trend(
        df: pd.DataFrame,
        date_col: str,
        metric_col: str,
        freq: str = "M",
        agg_func: str = "sum"
    ) -> ExecutionResult:
        """Analyze temporal progression across date/time periods."""
        if date_col not in df.columns or metric_col not in df.columns:
            return ExecutionResult(
                success=False,
                error_message=f"Columns '{date_col}' or '{metric_col}' not found."
            )

        try:
            df_work = df.copy()
            df_work["_dt"] = pd.to_datetime(df_work[date_col], errors="coerce")
            df_work = df_work.dropna(subset=["_dt", metric_col])

            if df_work.empty:
                return ExecutionResult(success=False, error_message="No valid date records found.")

            resampled = (
                df_work.set_index("_dt")
                .resample(freq)[metric_col]
                .agg(agg_func)
                .reset_index()
            )
            resampled.rename(columns={"_dt": "Period", metric_col: f"{metric_col}_{agg_func}"}, inplace=True)
            resampled["Period_Str"] = resampled["Period"].dt.strftime("%Y-%m-%d" if freq == "D" else "%b %Y")

            val_col = f"{metric_col}_{agg_func}"
            if len(resampled) >= 2:
                growth_rate = ((resampled[val_col].iloc[-1] - resampled[val_col].iloc[0]) / max(1e-6, abs(resampled[val_col].iloc[0]))) * 100
            else:
                growth_rate = 0.0

            peak_period = resampled.loc[resampled[val_col].idxmax()]["Period_Str"]
            peak_val = float(resampled[val_col].max())

            narrative = (
                f"Historical trajectory spans {len(resampled)} periods. Peak activity occurred in "
                f"{peak_period} reaching {peak_val:,.2f} ({agg_func}). Overall period-over-period shift "
                f"was {growth_rate:+.1f}%."
            )

            return ExecutionResult(
                success=True,
                result_df=resampled,
                kpis={
                    "peak_period": peak_period,
                    "peak_value": peak_val,
                    "growth_percentage": round(growth_rate, 2),
                    "periods_tracked": len(resampled)
                },
                chart_type="line",
                chart_config={
                    "x": "Period_Str",
                    "y": val_col,
                    "title": f"{agg_func.capitalize()} {metric_col} Over Time"
                },
                narrative=narrative,
                operation_type="time_trend"
            )
        except Exception as e:
            return ExecutionResult(success=False, error_message=str(e))

    @staticmethod
    def top_n_records(
        df: pd.DataFrame,
        metric_col: str,
        n: int = 5,
        display_cols: Optional[List[str]] = None,
        ascending: bool = False
    ) -> ExecutionResult:
        """Extract top or bottom N records by a numeric metric."""
        if metric_col not in df.columns:
            return ExecutionResult(success=False, error_message=f"Metric '{metric_col}' not found.")

        if not pd.api.types.is_numeric_dtype(df[metric_col]):
            return ExecutionResult(success=False, error_message=f"Column '{metric_col}' is not numeric.")

        try:
            sorted_df = df.sort_values(by=metric_col, ascending=ascending)
            top_df = sorted_df.head(n)

            if display_cols:
                valid_cols = [c for c in display_cols if c in df.columns]
                if metric_col not in valid_cols:
                    valid_cols.append(metric_col)
                top_df = top_df[valid_cols]

            top_val = float(top_df[metric_col].iloc[0]) if not top_df.empty else 0.0
            order_label = "Highest" if not ascending else "Lowest"

            narrative = (
                f"Top {n} {order_label.lower()} records by {metric_col}. The extreme value is {top_val:,.2f}."
            )

            return ExecutionResult(
                success=True,
                result_df=top_df,
                kpis={
                    "record_count": len(top_df),
                    "extreme_value": top_val,
                    "order": order_label
                },
                chart_type="table",
                chart_config={"metric": metric_col},
                narrative=narrative,
                operation_type="top_n"
            )
        except Exception as e:
            return ExecutionResult(success=False, error_message=str(e))

    @staticmethod
    def correlation_drivers(df: pd.DataFrame, target_col: str, top_k: int = 5) -> ExecutionResult:
        """Identify features most strongly correlated with target numeric column."""
        if target_col not in df.columns or not pd.api.types.is_numeric_dtype(df[target_col]):
            return ExecutionResult(success=False, error_message=f"Target '{target_col}' must be a numeric column.")

        try:
            numeric_df = df.select_dtypes(include=[np.number]).dropna()
            if numeric_df.empty or target_col not in numeric_df.columns:
                return ExecutionResult(success=False, error_message="Insufficient numeric data to compute correlations.")

            corrs = numeric_df.corr()[target_col].drop(index=[target_col]).dropna()
            if corrs.empty:
                return ExecutionResult(success=False, error_message="No other numeric features found to correlate with.")

            corr_df = pd.DataFrame({
                "Feature": corrs.index,
                "Correlation": corrs.values,
                "AbsoluteCorrelation": corrs.abs().values
            }).sort_values(by="AbsoluteCorrelation", ascending=False).head(top_k)

            top_driver = corr_df.iloc[0]["Feature"]
            top_strength = corr_df.iloc[0]["Correlation"]
            relationship = "positive" if top_strength > 0 else "negative"

            narrative = (
                f"The strongest statistical driver of {target_col} is '{top_driver}' with a "
                f"{relationship} correlation coefficient of {top_strength:.3f}."
            )

            return ExecutionResult(
                success=True,
                result_df=corr_df[["Feature", "Correlation"]],
                kpis={
                    "top_driver": top_driver,
                    "correlation_coefficient": round(float(top_strength), 3),
                    "driver_direction": relationship
                },
                chart_type="bar",
                chart_config={
                    "x": "Feature",
                    "y": "Correlation",
                    "title": f"Key Correlation Drivers for {target_col}"
                },
                narrative=narrative,
                operation_type="correlation"
            )
        except Exception as e:
            return ExecutionResult(success=False, error_message=str(e))
