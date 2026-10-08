"""
InsightAI - Data Cleaner Module
Provides non-destructive data hygiene utilities:
- Column header normalization
- Safe missing value handling and imputation
- Duplicate row deduplication
- Type inference and string currency/percentage cleaning
"""

from dataclasses import dataclass
from typing import Tuple, List, Optional
import pandas as pd
import numpy as np


@dataclass
class CleaningReport:
    """Summary of operations performed during dataset cleaning."""
    original_shape: Tuple[int, int]
    new_shape: Tuple[int, int]
    duplicates_removed: int = 0
    missing_imputed_count: int = 0
    columns_standardized: List[str] = None
    converted_types: dict = None


class DataCleaner:
    """Safe, non-destructive tabular cleaner."""

    @staticmethod
    def standardize_column_names(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Normalize column headers to clean snake_case names."""
        df_clean = df.copy()
        new_cols = []
        for c in df_clean.columns:
            clean_name = str(c).strip().replace(" ", "_").replace("-", "_").replace(".", "_")
            # Remove repeated underscores
            while "__" in clean_name:
                clean_name = clean_name.replace("__", "_")
            new_cols.append(clean_name)
        df_clean.columns = new_cols
        return df_clean, new_cols

    @staticmethod
    def drop_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """Remove exact duplicate rows and return new df and count of removed duplicates."""
        initial_count = len(df)
        df_clean = df.drop_duplicates().copy()
        removed = initial_count - len(df_clean)
        return df_clean, removed

    @staticmethod
    def impute_missing(
        df: pd.DataFrame,
        numeric_strategy: str = "median",  # 'median', 'mean', 'zero', 'drop'
        categorical_strategy: str = "mode"  # 'mode', 'unknown', 'drop'
    ) -> Tuple[pd.DataFrame, int]:
        """
        Safely impute missing values based on specified strategy.
        Returns the cleaned DataFrame and count of imputed cells.
        """
        df_clean = df.copy()
        imputed_count = 0

        for col in df_clean.columns:
            missing_in_col = df_clean[col].isna().sum()
            if missing_in_col == 0:
                continue

            if pd.api.types.is_numeric_dtype(df_clean[col]):
                if numeric_strategy == "median":
                    median_val = df_clean[col].median()
                    df_clean[col] = df_clean[col].fillna(median_val)
                    imputed_count += missing_in_col
                elif numeric_strategy == "mean":
                    mean_val = df_clean[col].mean()
                    df_clean[col] = df_clean[col].fillna(mean_val)
                    imputed_count += missing_in_col
                elif numeric_strategy == "zero":
                    df_clean[col] = df_clean[col].fillna(0)
                    imputed_count += missing_in_col
            else:
                if categorical_strategy == "mode":
                    mode_val = df_clean[col].mode()
                    val = mode_val.iloc[0] if not mode_val.empty else "Unknown"
                    df_clean[col] = df_clean[col].fillna(val)
                    imputed_count += missing_in_col
                elif categorical_strategy == "unknown":
                    df_clean[col] = df_clean[col].fillna("Unknown")
                    imputed_count += missing_in_col

        return df_clean, int(imputed_count)

    @staticmethod
    def clean_dataset(
        df: pd.DataFrame,
        deduplicate: bool = True,
        standardize_cols: bool = False,
        handle_missing: bool = False,
        missing_num_strategy: str = "median"
    ) -> Tuple[pd.DataFrame, CleaningReport]:
        """Run standard pipeline and generate structured CleaningReport."""
        original_shape = df.shape
        df_work = df.copy()
        dups_removed = 0
        imputed_cells = 0
        std_cols = list(df.columns)

        if standardize_cols:
            df_work, std_cols = DataCleaner.standardize_column_names(df_work)

        if deduplicate:
            df_work, dups_removed = DataCleaner.drop_duplicates(df_work)

        if handle_missing:
            df_work, imputed_cells = DataCleaner.impute_missing(
                df_work,
                numeric_strategy=missing_num_strategy,
                categorical_strategy="unknown"
            )

        report = CleaningReport(
            original_shape=original_shape,
            new_shape=df_work.shape,
            duplicates_removed=dups_removed,
            missing_imputed_count=imputed_cells,
            columns_standardized=std_cols
        )
        return df_work, report
