"""
InsightAI - CSV Validator Module
Validates uploaded CSV files for security, file type, file size, encoding, and data integrity.
"""

from dataclasses import dataclass, field
import io
import os
from typing import Optional, List, Tuple
import pandas as pd


@dataclass
class ValidationResult:
    """Structured result of CSV file validation."""
    is_valid: bool
    df: Optional[pd.DataFrame] = None
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    file_name: str = ""
    file_size_bytes: int = 0
    delimiter_detected: str = ","
    encoding_detected: str = "utf-8"


class CSVValidator:
    """Validator for uploaded tabular CSV files."""

    ALLOWED_EXTENSIONS = {".csv"}
    DEFAULT_MAX_SIZE_MB = 50.0
    MAX_RECOMMENDED_ROWS = 500_000
    MAX_COLUMNS = 200

    def __init__(self, max_size_mb: float = DEFAULT_MAX_SIZE_MB):
        self.max_size_mb = max_size_mb
        self.max_size_bytes = int(max_size_mb * 1024 * 1024)

    def validate(self, file_input, file_name: str = "uploaded_file.csv") -> ValidationResult:
        """
        Validate file source (BytesIO, string buffer, or file path) and safely parse into DataFrame.
        """
        warnings: List[str] = []

        # 1. Extension check
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Unsupported file format '{ext}'. Please upload a valid CSV file (.csv).",
                file_name=file_name
            )

        # 2. Extract bytes and check file size
        try:
            if hasattr(file_input, "getvalue"):
                raw_bytes = file_input.getvalue()
            elif hasattr(file_input, "read"):
                raw_bytes = file_input.read()
                if hasattr(file_input, "seek"):
                    file_input.seek(0)
            elif isinstance(file_input, str) and os.path.isfile(file_input):
                with open(file_input, "rb") as f:
                    raw_bytes = f.read()
            elif isinstance(file_input, bytes):
                raw_bytes = file_input
            else:
                return ValidationResult(
                    is_valid=False,
                    error_message="Invalid file object provided.",
                    file_name=file_name
                )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Failed to read file buffer: {str(e)}",
                file_name=file_name
            )

        file_size_bytes = len(raw_bytes)
        if file_size_bytes == 0:
            return ValidationResult(
                is_valid=False,
                error_message="The uploaded CSV file is completely empty (0 bytes).",
                file_name=file_name,
                file_size_bytes=0
            )

        if file_size_bytes > self.max_size_bytes:
            return ValidationResult(
                is_valid=False,
                error_message=(
                    f"File size ({file_size_bytes / (1024 * 1024):.2f} MB) exceeds maximum allowed limit "
                    f"of {self.max_size_mb:.1f} MB. Please upload a smaller dataset."
                ),
                file_name=file_name,
                file_size_bytes=file_size_bytes
            )

        # 3. Detect encoding and delimiter
        encoding, delimiter = self._detect_encoding_and_delimiter(raw_bytes)

        # 4. Safe DataFrame Parsing
        try:
            buffer = io.BytesIO(raw_bytes)
            # Use python engine fallback if c-engine encounters unusual quoting
            try:
                df = pd.read_csv(
                    buffer,
                    sep=delimiter,
                    encoding=encoding,
                    on_bad_lines="error"
                )
            except Exception:
                buffer.seek(0)
                df = pd.read_csv(
                    buffer,
                    sep=delimiter,
                    encoding=encoding,
                    engine="python",
                    on_bad_lines="skip"
                )
                warnings.append("Some malformed lines were safely skipped during parsing.")
        except pd.errors.EmptyDataError:
            return ValidationResult(
                is_valid=False,
                error_message="The CSV file has no columns or data records.",
                file_name=file_name,
                file_size_bytes=file_size_bytes,
                encoding_detected=encoding,
                delimiter_detected=delimiter
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Failed to parse CSV file: {str(e)}",
                file_name=file_name,
                file_size_bytes=file_size_bytes,
                encoding_detected=encoding,
                delimiter_detected=delimiter
            )

        # 5. Integrity and bounds validation
        if df.empty or len(df.columns) == 0:
            return ValidationResult(
                is_valid=False,
                error_message="Parsed CSV contains 0 rows or 0 columns.",
                file_name=file_name,
                file_size_bytes=file_size_bytes
            )

        if len(df.columns) > self.MAX_COLUMNS:
            return ValidationResult(
                is_valid=False,
                error_message=(
                    f"Dataset contains {len(df.columns)} columns, exceeding the maximum safe limit "
                    f"of {self.MAX_COLUMNS} columns."
                ),
                file_name=file_name,
                file_size_bytes=file_size_bytes
            )

        if len(df) > self.MAX_RECOMMENDED_ROWS:
            warnings.append(
                f"Dataset contains {len(df):,} rows. Interactive charting may be slower with very large datasets."
            )

        # Check for un-named columns or duplicate column names
        unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed:")]
        if unnamed_cols:
            warnings.append(f"Detected {len(unnamed_cols)} unnamed column(s). Consider cleaning your CSV header.")

        if df.columns.duplicated().any():
            dup_cols = df.columns[df.columns.duplicated()].tolist()
            warnings.append(f"Duplicate column headers found: {dup_cols}. Deduplicating header names.")
            # Deduplicate column names
            df.columns = pd.io.common.dedup_names(df.columns.tolist(), is_potential_multi_index=False)

        return ValidationResult(
            is_valid=True,
            df=df,
            warnings=warnings,
            file_name=file_name,
            file_size_bytes=file_size_bytes,
            delimiter_detected=delimiter,
            encoding_detected=encoding
        )

    def _detect_encoding_and_delimiter(self, raw_bytes: bytes) -> Tuple[str, str]:
        """Detect file encoding and delimiter safely."""
        candidate_encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252", "iso-8859-1"]
        decoded_text = ""
        chosen_encoding = "utf-8"

        for enc in candidate_encodings:
            try:
                # Test first 100KB for encoding
                sample = raw_bytes[:102400].decode(enc)
                decoded_text = sample
                chosen_encoding = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue

        if not decoded_text:
            chosen_encoding = "latin1"
            decoded_text = raw_bytes[:102400].decode("latin1", errors="replace")

        # Delimiter detection
        delimiters = [",", ";", "\t", "|"]
        delimiter_counts = {}
        first_few_lines = [line for line in decoded_text.splitlines()[:5] if line.strip()]

        if first_few_lines:
            for d in delimiters:
                # Count average delimiter occurrences across first few lines
                counts = [line.count(d) for line in first_few_lines]
                if counts and all(c > 0 for c in counts) and len(set(counts)) == 1:
                    delimiter_counts[d] = counts[0] * 10
                else:
                    delimiter_counts[d] = sum(counts)

            chosen_delimiter = max(delimiter_counts, key=delimiter_counts.get) if delimiter_counts else ","
            if delimiter_counts.get(chosen_delimiter, 0) == 0:
                chosen_delimiter = ","
        else:
            chosen_delimiter = ","

        return chosen_encoding, chosen_delimiter
