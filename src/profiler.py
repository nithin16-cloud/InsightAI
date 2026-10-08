"""
InsightAI - Data Profiler Module
Computes automated comprehensive profiles for datasets:
- Dimension, memory, and duplicate row statistics
- Per-column type classification, missingness, and cardinality
- Numeric distributions (min, max, mean, std, percentiles)
- Categorical frequencies and datetime ranges
- Inter-feature correlation analysis
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


@dataclass
class ColumnProfile:
    """Detailed profile of a single column."""
    name: str
    dtype: str
    semantic_type: str  # 'numeric', 'categorical', 'datetime', 'boolean', 'id_text'
    total_count: int
    non_null_count: int
    missing_count: int
    missing_percentage: float
    unique_count: int
    is_unique: bool
    sample_values: List[Any]
    stats: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DatasetProfile:
    """Complete profile of the dataset."""
    row_count: int
    column_count: int
    memory_usage_bytes: int
    memory_usage_str: str
    duplicate_rows_count: int
    duplicate_rows_percentage: float
    total_cells: int
    total_missing_cells: int
    total_missing_percentage: float
    columns: Dict[str, ColumnProfile] = field(default_factory=dict)
    numeric_columns: List[str] = field(default_factory=list)
    categorical_columns: List[str] = field(default_factory=list)
    datetime_columns: List[str] = field(default_factory=list)
    boolean_columns: List[str] = field(default_factory=list)
    correlation_matrix: Optional[Dict[str, Dict[str, float]]] = None
    has_numeric_columns: bool = False
    has_datetime_columns: bool = False


class DataProfiler:
    """Generates deep, safe metadata profiles of tabular datasets."""

    @staticmethod
    def profile(df: pd.DataFrame) -> DatasetProfile:
        """Analyze a pandas DataFrame and return a DatasetProfile."""
        if df is None or df.empty:
            return DatasetProfile(
                row_count=0,
                column_count=0,
                memory_usage_bytes=0,
                memory_usage_str="0 B",
                duplicate_rows_count=0,
                duplicate_rows_percentage=0.0,
                total_cells=0,
                total_missing_cells=0,
                total_missing_percentage=0.0
            )

        row_count, column_count = df.shape
        total_cells = row_count * column_count

        # Memory usage
        mem_bytes = int(df.memory_usage(deep=True).sum())
        mem_str = DataProfiler._format_memory(mem_bytes)

        # Duplicate rows
        dup_count = int(df.duplicated().sum())
        dup_pct = round((dup_count / row_count) * 100, 2) if row_count > 0 else 0.0

        # Total missing cells
        missing_cells = int(df.isna().sum().sum())
        missing_pct = round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0.0

        col_profiles: Dict[str, ColumnProfile] = {}
        numeric_cols: List[str] = []
        categorical_cols: List[str] = []
        datetime_cols: List[str] = []
        boolean_cols: List[str] = []

        for col in df.columns:
            series = df[col]
            profile = DataProfiler._profile_column(series, row_count)
            col_profiles[col] = profile

            if profile.semantic_type == "numeric":
                numeric_cols.append(col)
            elif profile.semantic_type == "datetime":
                datetime_cols.append(col)
            elif profile.semantic_type == "boolean":
                boolean_cols.append(col)
            else:
                categorical_cols.append(col)

        # Correlation matrix for numeric columns
        corr_matrix = None
        if len(numeric_cols) >= 2:
            try:
                num_df = df[numeric_cols].select_dtypes(include=[np.number])
                if not num_df.empty:
                    corr = num_df.corr().round(3)
                    corr_matrix = corr.to_dict()
            except Exception:
                corr_matrix = None

        return DatasetProfile(
            row_count=row_count,
            column_count=column_count,
            memory_usage_bytes=mem_bytes,
            memory_usage_str=mem_str,
            duplicate_rows_count=dup_count,
            duplicate_rows_percentage=dup_pct,
            total_cells=total_cells,
            total_missing_cells=missing_cells,
            total_missing_percentage=missing_pct,
            columns=col_profiles,
            numeric_columns=numeric_cols,
            categorical_columns=categorical_cols,
            datetime_columns=datetime_cols,
            boolean_columns=boolean_cols,
            correlation_matrix=corr_matrix,
            has_numeric_columns=len(numeric_cols) > 0,
            has_datetime_columns=len(datetime_cols) > 0
        )

    @staticmethod
    def _profile_column(series: pd.Series, total_rows: int) -> ColumnProfile:
        """Compute metrics for an individual column."""
        name = str(series.name)
        dtype_str = str(series.dtype)
        non_null_count = int(series.count())
        missing_count = int(series.isna().sum())
        missing_pct = round((missing_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
        unique_count = int(series.nunique(dropna=True))
        is_unique = (unique_count == non_null_count) and (non_null_count > 0)

        # Clean samples
        samples = series.dropna().unique()[:3].tolist()
        sample_values = [DataProfiler._serialize_val(s) for s in samples]

        # Inferred semantic type
        semantic_type = DataProfiler._infer_semantic_type(series)
        stats: Dict[str, Any] = {}

        if semantic_type == "numeric":
            clean_num = pd.to_numeric(series.dropna(), errors="coerce").dropna()
            if not clean_num.empty:
                stats = {
                    "min": DataProfiler._serialize_val(clean_num.min()),
                    "max": DataProfiler._serialize_val(clean_num.max()),
                    "mean": round(float(clean_num.mean()), 2),
                    "median": round(float(clean_num.median()), 2),
                    "std": round(float(clean_num.std()), 2) if len(clean_num) > 1 else 0.0,
                    "q25": round(float(clean_num.quantile(0.25)), 2),
                    "q75": round(float(clean_num.quantile(0.75)), 2),
                    "zeros_count": int((clean_num == 0).sum()),
                }
        elif semantic_type == "datetime":
            dt_series = pd.to_datetime(series.dropna(), errors="coerce").dropna()
            if not dt_series.empty:
                stats = {
                    "min_date": str(dt_series.min()),
                    "max_date": str(dt_series.max()),
                    "range_days": (dt_series.max() - dt_series.min()).days
                }
        else:
            # Categorical or text
            val_counts = series.value_counts(dropna=True).head(5)
            top_value = val_counts.index[0] if not val_counts.empty else None
            top_freq = int(val_counts.iloc[0]) if not val_counts.empty else 0
            stats = {
                "top_value": DataProfiler._serialize_val(top_value),
                "top_frequency": top_freq,
                "top_percentage": round((top_freq / non_null_count) * 100, 2) if non_null_count > 0 else 0.0,
                "top_categories": {DataProfiler._serialize_val(k): int(v) for k, v in val_counts.items()}
            }

        return ColumnProfile(
            name=name,
            dtype=dtype_str,
            semantic_type=semantic_type,
            total_count=total_rows,
            non_null_count=non_null_count,
            missing_count=missing_count,
            missing_percentage=missing_pct,
            unique_count=unique_count,
            is_unique=is_unique,
            sample_values=sample_values,
            stats=stats
        )

    @staticmethod
    def _infer_semantic_type(series: pd.Series) -> str:
        """Infer semantic type of column."""
        # Check boolean
        if pd.api.types.is_bool_dtype(series):
            return "boolean"

        # Check numeric
        if pd.api.types.is_numeric_dtype(series):
            # If 0 and 1 only, could still be treated as numeric
            return "numeric"

        # Check datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"

        # Check if object can be parsed as datetime (e.g. '2024-01-15')
        if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
            non_null = series.dropna().astype(str).str.strip()
            if not non_null.empty:
                # Test first 10 entries for date patterns
                sample = non_null.head(10)
                try:
                    converted = pd.to_datetime(sample, errors="raise", format="mixed")
                    # If conversion succeeded for all sample items and has date separator
                    if any(sep in sample.iloc[0] for sep in ["-", "/", "."]):
                        return "datetime"
                except Exception:
                    pass

                # Check if it represents boolean string ('yes'/'no', 'true'/'false')
                lower_unique = set(sample.str.lower().unique())
                if lower_unique.issubset({"true", "false", "yes", "no", "0", "1", "t", "f"}):
                    return "boolean"

        return "categorical"

    @staticmethod
    def _format_memory(bytes_val: int) -> str:
        """Format bytes into readable string."""
        if bytes_val < 1024:
            return f"{bytes_val} B"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.1f} KB"
        elif bytes_val < 1024 * 1024 * 1024:
            return f"{bytes_val / (1024 * 1024):.2f} MB"
        else:
            return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"

    @staticmethod
    def _serialize_val(val: Any) -> Any:
        """Convert numpy/pandas types to standard JSON-safe types."""
        if pd.isna(val):
            return None
        if isinstance(val, (np.integer, np.int64, np.int32)):
            return int(val)
        if isinstance(val, (np.floating, np.float64, np.float32)):
            return round(float(val), 4)
        if isinstance(val, (pd.Timestamp, np.datetime64)):
            return str(val)
        return str(val)
