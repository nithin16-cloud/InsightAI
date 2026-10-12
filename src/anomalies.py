"""
InsightAI - Machine Learning Anomaly Detection Module
Uses Scikit-Learn Isolation Forest to detect multivariate outliers,
compute anomaly severity scores, and explain feature-level drivers in plain English.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


@dataclass
class AnomalyDetectionResult:
    """Complete results from an Isolation Forest scan."""
    total_records: int
    outliers_detected: int
    outlier_percentage: float
    contamination: float
    features_used: List[str]
    outlier_df: pd.DataFrame
    full_df_with_scores: pd.DataFrame
    top_anomalies_summary: List[Dict[str, Any]] = field(default_factory=list)
    narrative_summary: str = ""


class AnomalyDetector:
    """Safe, reproducible multivariate anomaly detector."""

    @staticmethod
    def detect_anomalies(
        df: pd.DataFrame,
        feature_columns: Optional[List[str]] = None,
        contamination: float = 0.05,
        random_state: int = 42
    ) -> Tuple[bool, Optional[AnomalyDetectionResult], Optional[str]]:
        """
        Run Isolation Forest on selected or auto-detected numeric columns.
        Returns (success, result, error_message).
        """
        if df is None or df.empty:
            return False, None, "Dataset is empty."

        # Detect numeric columns
        if feature_columns is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Exclude id-like columns (very high cardinality integers that look like row IDs)
            feature_columns = [
                c for c in numeric_cols
                if not (c.lower().endswith("_id") or c.lower() == "id")
            ]

        if len(feature_columns) < 2:
            return False, None, "Anomaly detection requires at least 2 numeric features."

        try:
            # Prepare feature matrix
            X = df[feature_columns].copy()
            # Impute missing values with column median for robustness
            X_imputed = X.fillna(X.median())

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_imputed)

            # Fit Isolation Forest
            model = IsolationForest(
                contamination=contamination,
                random_state=random_state,
                n_estimators=100
            )
            preds = model.fit_predict(X_scaled)  # -1 for anomaly, 1 for normal
            scores = model.decision_function(X_scaled)  # Lower is more abnormal

            df_augmented = df.copy()
            df_augmented["_is_anomaly"] = (preds == -1)
            # Scale decision score into 0 to 100 severity index where 100 is most anomalous
            min_s, max_s = scores.min(), scores.max()
            if max_s > min_s:
                normalized_score = 100 * (1 - (scores - min_s) / (max_s - min_s))
            else:
                normalized_score = np.zeros_like(scores)

            df_augmented["anomaly_score"] = normalized_score.round(1)

            outlier_df = df_augmented[df_augmented["_is_anomaly"]].sort_values(
                by="anomaly_score", ascending=False
            )

            outlier_count = len(outlier_df)
            outlier_pct = round((outlier_count / len(df)) * 100, 2)

            # Compute humanized explanations for top outliers
            z_scores = np.abs(X_scaled)
            top_summaries = []

            for idx, row in outlier_df.head(5).iterrows():
                row_idx = df.index.get_loc(idx)
                row_z = z_scores[row_idx]
                top_deviant_idx = np.argsort(row_z)[::-1]

                drivers = []
                for feat_i in top_deviant_idx[:2]:
                    f_name = feature_columns[feat_i]
                    f_val = row[f_name]
                    f_z = row_z[feat_i]
                    col_mean = X[f_name].mean()
                    dir_str = "above" if f_val > col_mean else "below"
                    drivers.append(f"{f_name}={f_val:,.2f} ({f_z:.1f} sd {dir_str} avg)")

                id_col = next((c for c in df.columns if "id" in c.lower()), None)
                record_id = str(row[id_col]) if id_col else f"Row #{idx}"

                top_summaries.append({
                    "record_id": record_id,
                    "anomaly_score": float(row["anomaly_score"]),
                    "explanation": "; ".join(drivers)
                })

            narrative = (
                f"Scanned {len(df):,} records using Isolation Forest across {len(feature_columns)} "
                f"features. Flagged {outlier_count} anomalous record(s) ({outlier_pct}% of dataset) "
                f"displaying rare multi-feature divergence."
            )

            result = AnomalyDetectionResult(
                total_records=len(df),
                outliers_detected=outlier_count,
                outlier_percentage=outlier_pct,
                contamination=contamination,
                features_used=feature_columns,
                outlier_df=outlier_df,
                full_df_with_scores=df_augmented,
                top_anomalies_summary=top_summaries,
                narrative_summary=narrative
            )
            return True, result, None

        except Exception as e:
            return False, None, f"Anomaly detection encountered an error: {str(e)}"
