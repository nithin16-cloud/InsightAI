"""
InsightAI Day 1 Unit Tests
Validates CSV validation, profiling, and cleaning modules.
"""

import os
import pytest
import pandas as pd
from src.validator import CSVValidator
from src.profiler import DataProfiler
from src.cleaner import DataCleaner


def test_validator_sample_sales():
    validator = CSVValidator()
    path = os.path.join("data", "sample_sales.csv")
    result = validator.validate(path, file_name="sample_sales.csv")
    assert result.is_valid is True
    assert result.df is not None
    assert len(result.df) == 100
    assert "order_id" in result.df.columns
    assert "revenue" in result.df.columns


def test_validator_rejects_non_csv():
    validator = CSVValidator()
    result = validator.validate(b"test data", file_name="notes.pdf")
    assert result.is_valid is False
    assert "Unsupported file format" in result.error_message


def test_validator_empty_data():
    validator = CSVValidator()
    result = validator.validate(b"", file_name="empty.csv")
    assert result.is_valid is False
    assert "empty" in result.error_message.lower()


def test_profiler_statistics():
    df = pd.read_csv(os.path.join("data", "sample_sales.csv"))
    profile = DataProfiler.profile(df)
    assert profile.row_count == 100
    assert profile.column_count == 13
    assert profile.duplicate_rows_count >= 1  # 1 duplicate injected
    assert profile.total_missing_cells >= 2  # 2 missing segments injected
    assert "revenue" in profile.numeric_columns
    assert "region" in profile.categorical_columns

    rev_stats = profile.columns["revenue"].stats
    assert "min" in rev_stats
    assert "max" in rev_stats
    assert "mean" in rev_stats
    assert rev_stats["max"] > 20000


def test_cleaner_deduplication():
    df = pd.read_csv(os.path.join("data", "sample_sales.csv"))
    initial_len = len(df)
    clean_df, removed = DataCleaner.drop_duplicates(df)
    assert removed >= 1
    assert len(clean_df) == initial_len - removed


def test_cleaner_missing_imputation():
    df = pd.DataFrame({
        "num": [1.0, 2.0, None, 4.0],
        "cat": ["A", "B", None, "B"]
    })
    cleaned, imputed_count = DataCleaner.impute_missing(df, numeric_strategy="median", categorical_strategy="mode")
    assert imputed_count == 2
    assert cleaned["num"].isna().sum() == 0
    assert cleaned["cat"].isna().sum() == 0
