"""
InsightAI - Executive HTML Report Generator
Creates self-contained, executive-grade analytical HTML reports.
Features modern responsive styling, health scorecard, anomaly highlights, and data tables.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
import pandas as pd
from src.profiler import DatasetProfile
from src.anomalies import AnomalyDetectionResult


class ExecutiveReporter:
    """Generates standalone, beautifully formatted executive HTML reports."""

    @staticmethod
    def calculate_health_score(profile: DatasetProfile, anomaly_result: Optional[AnomalyDetectionResult] = None) -> int:
        """Calculate a composite 0-100 data health score."""
        score = 100.0

        # Missing values penalty
        score -= min(30.0, profile.total_missing_percentage * 2.5)

        # Duplicate rows penalty
        score -= min(25.0, profile.duplicate_rows_percentage * 3.0)

        # Anomalies penalty
        if anomaly_result:
            score -= min(15.0, anomaly_result.outlier_percentage * 1.5)

        return max(10, min(100, int(round(score))))

    @staticmethod
    def generate_html_report(
        file_name: str,
        profile: DatasetProfile,
        df: pd.DataFrame,
        anomaly_result: Optional[AnomalyDetectionResult] = None,
        custom_notes: Optional[str] = None
    ) -> str:
        """Generate standalone executive HTML report."""
        now_str = datetime.now().strftime("%B %d, %Y | %H:%M UTC")
        health_score = ExecutiveReporter.calculate_health_score(profile, anomaly_result)

        if health_score >= 90:
            health_badge_class = "health-excellent"
            health_verdict = "Excellent &mdash; Production Ready"
        elif health_score >= 75:
            health_badge_class = "health-good"
            health_verdict = "Good &mdash; Minor Hygiene Recommended"
        elif health_score >= 60:
            health_badge_class = "health-fair"
            health_verdict = "Fair &mdash; Moderate Quality Issues"
        else:
            health_badge_class = "health-poor"
            health_verdict = "Action Required &mdash; High Noise / Missing Data"

        # Numeric stats rows
        stats_rows_html = ""
        if profile.has_numeric_columns:
            desc = df[profile.numeric_columns].describe().T
            for col_name, s in desc.iterrows():
                stats_rows_html += f"""
                <tr>
                    <td class="col-name font-mono">{col_name}</td>
                    <td>{int(s['count']):,}</td>
                    <td>{s['mean']:,.2f}</td>
                    <td>{s['std']:,.2f}</td>
                    <td>{s['min']:,.2f}</td>
                    <td>{s['50%']:,.2f}</td>
                    <td>{s['max']:,.2f}</td>
                </tr>
                """

        # Schema rows
        schema_rows_html = ""
        for col_name, c_prof in profile.columns.items():
            type_badge = f'<span class="badge badge-{c_prof.semantic_type}">{c_prof.semantic_type.upper()}</span>'
            schema_rows_html += f"""
            <tr>
                <td class="col-name font-mono">{col_name}</td>
                <td>{type_badge}</td>
                <td>{c_prof.non_null_count:,}</td>
                <td>{c_prof.missing_count:,} ({c_prof.missing_percentage}%)</td>
                <td>{c_prof.unique_count:,}</td>
            </tr>
            """

        # Anomaly section HTML
        anomaly_section_html = ""
        if anomaly_result and anomaly_result.outliers_detected > 0:
            anomaly_items_html = ""
            for item in anomaly_result.top_anomalies_summary:
                anomaly_items_html += f"""
                <div class="anomaly-item">
                    <div class="anomaly-header">
                        <span class="anomaly-id">{item['record_id']}</span>
                        <span class="anomaly-score">Severity: {item['anomaly_score']}/100</span>
                    </div>
                    <div class="anomaly-desc">{item['explanation']}</div>
                </div>
                """

            anomaly_section_html = f"""
            <div class="card section-card">
                <div class="section-title">Machine Learning Anomaly Detection (Isolation Forest)</div>
                <p class="section-desc">Identified <strong>{anomaly_result.outliers_detected}</strong> anomalous records ({anomaly_result.outlier_percentage}% of dataset) exhibiting rare multi-feature divergence.</p>
                <div class="anomaly-list">
                    {anomaly_items_html}
                </div>
            </div>
            """

        # HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InsightAI Executive Report - {file_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0B0F19;
            --surface: #121826;
            --surface-elevated: #182234;
            --border: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(99, 102, 241, 0.3);
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --accent-primary: #6366F1;
            --accent-gradient: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
            --good: #10B981;
            --warn: #F59E0B;
            --bad: #F43F5E;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background-color: var(--bg);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            padding: 2.5rem 1.5rem;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        
        /* Header */
        .report-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
        }}
        .brand-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #A5B4FC;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.75rem;
        }}
        .report-title {{
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            margin-bottom: 0.3rem;
        }}
        .report-subtitle {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}
        .health-card {{
            text-align: right;
            background: var(--surface);
            padding: 1.25rem 1.75rem;
            border-radius: 14px;
            border: 1px solid var(--border);
        }}
        .health-score-val {{
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.35rem;
        }}
        .health-excellent {{ color: var(--good); }}
        .health-good {{ color: #38BDF8; }}
        .health-fair {{ color: var(--warn); }}
        .health-poor {{ color: var(--bad); }}
        .health-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            font-weight: 600;
        }}
        .health-verdict {{
            font-size: 0.82rem;
            font-weight: 500;
            color: var(--text-secondary);
        }}

        /* KPI Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }}
        .kpi-box {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
        }}
        .kpi-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            font-weight: 600;
            margin-bottom: 0.4rem;
        }}
        .kpi-val {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #FFFFFF;
        }}
        .kpi-sub {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }}

        /* Section Cards */
        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.75rem;
            margin-bottom: 2rem;
        }}
        .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            color: #FFFFFF;
        }}
        .section-desc {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 1.25rem;
        }}

        /* Tables */
        .table-responsive {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }}
        th {{
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
        }}
        td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-secondary);
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-primary);
        }}
        .col-name {{
            font-weight: 600;
            color: #E2E8F0;
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge-numeric {{ background: rgba(59, 130, 246, 0.15); color: #60A5FA; }}
        .badge-categorical {{ background: rgba(168, 85, 247, 0.15); color: #C084FC; }}
        .badge-datetime {{ background: rgba(16, 185, 129, 0.15); color: #34D399; }}
        .badge-boolean {{ background: rgba(245, 158, 11, 0.15); color: #FBBF24; }}

        /* Anomaly Items */
        .anomaly-list {{
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }}
        .anomaly-item {{
            background: var(--surface-elevated);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem 1.25rem;
        }}
        .anomaly-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.35rem;
        }}
        .anomaly-id {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            color: #FFFFFF;
            font-size: 0.92rem;
        }}
        .anomaly-score {{
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--bad);
            background: rgba(244, 63, 94, 0.12);
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
        }}
        .anomaly-desc {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        /* Footer */
        .report-footer {{
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 0.82rem;
        }}

        @media print {{
            body {{ background: #FFFFFF; color: #000000; }}
            .card, .kpi-box, .health-card {{ border: 1px solid #CCCCCC; background: #FAFAFA; }}
            .report-title {{ color: #000000; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="report-header">
            <div>
                <div class="brand-pill">InsightAI Executive Briefing</div>
                <h1 class="report-title">{file_name}</h1>
                <div class="report-subtitle">Generated on {now_str} | Deterministic Verification Engine</div>
            </div>
            <div class="health-card">
                <div class="health-label">Dataset Health Score</div>
                <div class="health-score-val {health_badge_class}">{health_score} / 100</div>
                <div class="health-verdict">{health_verdict}</div>
            </div>
        </header>

        <!-- KPI Grid -->
        <section class="kpi-grid">
            <div class="kpi-box">
                <div class="kpi-label">Total Records</div>
                <div class="kpi-val">{profile.row_count:,}</div>
                <div class="kpi-sub">{profile.column_count} Schema Columns</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">Numeric Features</div>
                <div class="kpi-val">{len(profile.numeric_columns)}</div>
                <div class="kpi-sub">{len(profile.categorical_columns)} Categorical Fields</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">Missing Values</div>
                <div class="kpi-val">{profile.total_missing_cells:,}</div>
                <div class="kpi-sub">{profile.total_missing_percentage}% Total Missing Rate</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">Duplicate Rows</div>
                <div class="kpi-val">{profile.duplicate_rows_count:,}</div>
                <div class="kpi-sub">{profile.duplicate_rows_percentage}% Redundancy</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">Memory Footprint</div>
                <div class="kpi-val">{profile.memory_usage_str}</div>
                <div class="kpi-sub">Optimized in-memory footprint</div>
            </div>
        </section>

        <!-- Anomaly Section -->
        {anomaly_section_html}

        <!-- Statistical Summary -->
        <section class="card">
            <div class="section-title">Numeric Feature Distributions</div>
            <p class="section-desc">Descriptive statistical metrics calculated deterministically on all numeric attributes.</p>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>Column Name</th>
                            <th>Count</th>
                            <th>Mean</th>
                            <th>Std Dev</th>
                            <th>Min</th>
                            <th>Median (50%)</th>
                            <th>Max</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stats_rows_html}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Schema Overview -->
        <section class="card">
            <div class="section-title">Schema & Cardinality Metadata</div>
            <p class="section-desc">Semantic types, missingness, and unique value cardinality breakdown.</p>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Inferred Type</th>
                            <th>Non-Null Rows</th>
                            <th>Missing Cells</th>
                            <th>Cardinality</th>
                        </tr>
                    </thead>
                    <tbody>
                        {schema_rows_html}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Footer -->
        <footer class="report-footer">
            Generated by InsightAI | Zero LLM Hallucinations Guaranteed | Python Deterministic Execution
        </footer>
    </div>
</body>
</html>"""
        return html
