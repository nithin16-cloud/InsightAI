"""
Comprehensive Test Suite for InsightAI End-to-End System.
Covers:
- CSV Validation & Ingestion
- Data Profiling & Health Scoring
- Data Cleaning & Imputation
- Deterministic Pandas Analysis Engine
- Natural Language Planning & Heuristic Fallback
- Machine Learning Anomaly Detection (Isolation Forest)
- Executive HTML Report Generator
"""

import os
import pytest
import pandas as pd
import numpy as np

from src.validator import CSVValidator
from src.profiler import DataProfiler
from src.cleaner import DataCleaner
from src.executor import DeterministicExecutor
from src.planner import QueryPlanner
from src.anomalies import AnomalyDetector
from src.reporter import ExecutiveReporter


@pytest.fixture
def sales_df():
    path = os.path.join("data", "sample_sales.csv")
    return pd.read_csv(path)


def test_validator_csv_flow(sales_df):
    validator = CSVValidator()
    path = os.path.join("data", "sample_sales.csv")
    res = validator.validate(path, file_name="sample_sales.csv")
    assert res.is_valid is True
    assert res.df is not None
    assert len(res.df) == 100


def test_executor_aggregation(sales_df):
    res = DeterministicExecutor.aggregate_by_category(
        sales_df,
        group_col="region",
        metric_col="revenue",
        agg_func="sum",
        top_n=5
    )
    assert res.success is True
    assert res.result_df is not None
    assert "region" in res.result_df.columns
    assert "revenue_sum" in res.result_df.columns
    assert "pct_share" in res.result_df.columns
    assert res.kpis["top_category"] in ["North", "South", "East", "West"]
    assert res.kpis["total_categories"] == 4
    assert res.chart_type == "bar"
    assert len(res.narrative) > 10


def test_executor_time_trend(sales_df):
    res = DeterministicExecutor.time_trend(
        sales_df,
        date_col="order_date",
        metric_col="revenue",
        freq="ME",
        agg_func="sum"
    )
    assert res.success is True
    assert res.result_df is not None
    assert res.kpis["periods_tracked"] > 0
    assert res.chart_type == "line"


def test_executor_correlation_drivers(sales_df):
    res = DeterministicExecutor.correlation_drivers(
        sales_df,
        target_col="revenue",
        top_k=3
    )
    assert res.success is True
    assert res.result_df is not None
    assert "Feature" in res.result_df.columns
    assert "Correlation" in res.result_df.columns
    assert len(res.result_df) >= 1


def test_planner_heuristic_and_execution(sales_df):
    planner = QueryPlanner(api_key=None)

    # Question mapping
    plan, res = planner.plan_and_execute("Which region generates the highest revenue?", sales_df)
    assert plan.operation == "aggregate"
    assert plan.group_col == "region"
    assert plan.metric_col == "revenue"
    assert res.success is True
    assert res.result_df is not None

    # Suggested queries
    suggestions = QueryPlanner.get_suggested_queries(sales_df)
    assert len(suggestions) > 0
    assert any("revenue" in s.lower() or "region" in s.lower() for s in suggestions)


def test_anomalies_isolation_forest(sales_df):
    success, result, err = AnomalyDetector.detect_anomalies(
        sales_df,
        feature_columns=["revenue", "unit_price", "units_sold", "profit"],
        contamination=0.05
    )
    assert success is True
    assert result is not None
    assert err is None
    assert result.outliers_detected > 0
    assert result.outlier_percentage > 0
    assert "anomaly_score" in result.outlier_df.columns
    assert len(result.top_anomalies_summary) > 0
    assert "severity" in str(result.top_anomalies_summary).lower() or "score" in str(result.top_anomalies_summary).lower()


def test_reporter_html_generation(sales_df):
    profile = DataProfiler.profile(sales_df)
    success, anomaly_res, _ = AnomalyDetector.detect_anomalies(sales_df, contamination=0.05)

    health_score = ExecutiveReporter.calculate_health_score(profile, anomaly_res)
    assert 0 <= health_score <= 100

    html = ExecutiveReporter.generate_html_report(
        file_name="sample_sales.csv",
        profile=profile,
        df=sales_df,
        anomaly_result=anomaly_res
    )
    assert "<!DOCTYPE html>" in html
    assert "InsightAI Executive Briefing" in html
    assert "sample_sales.csv" in html
    assert "Dataset Health Score" in html
    assert str(health_score) in html
