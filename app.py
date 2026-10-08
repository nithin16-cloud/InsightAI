"""
InsightAI - Intelligent Tabular Data Analytics Platform
Day 1: CSV Validation, Automated Profiling & Data Exploration Dashboard
"""

import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.validator import CSVValidator
from src.profiler import DataProfiler, DatasetProfile
from src.cleaner import DataCleaner

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="InsightAI | Automated Data Profiler & Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Modern Styling (Glassmorphism & Vibrant Dark/Light Theme Support) ---
CUSTOM_CSS = """
<style>
    /* Global Font & Smooth Layout */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Gradient Brand Header */
    .brand-title {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.3rem;
        letter-spacing: -0.03em;
        margin-bottom: 0.2rem;
    }

    .brand-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    /* Metric Card Styling */
    .metric-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .metric-label {
        color: #94A3B8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .metric-detail {
        font-size: 0.82rem;
        font-weight: 500;
    }
    .status-good { color: #10B981; }
    .status-warn { color: #F59E0B; }
    .status-bad { color: #EF4444; }

    /* Badge Pills */
    .badge-pill {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-numeric { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-categorical { background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-datetime { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-boolean { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }

    /* Custom Code & Table aesthetic */
    code {
        font-family: 'JetBrains Mono', monospace;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_session_state():
    """Initialize Streamlit session keys."""
    if "df" not in st.session_state:
        st.session_state.df = None
    if "profile" not in st.session_state:
        st.session_state.profile = None
    if "file_name" not in st.session_state:
        st.session_state.file_name = None
    if "validation_warnings" not in st.session_state:
        st.session_state.validation_warnings = []


init_session_state()

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="brand-title">InsightAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Automated Data Analysis Engine</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("📁 Data Ingestion")
    uploaded_file = st.file_uploader(
        "Upload Tabular Dataset",
        type=["csv"],
        help="Upload a CSV file (up to 50MB). Auto-detects delimiters and encodings."
    )

    st.markdown("**— OR —**")
    load_demo = st.button("🚀 Load Demo Dataset (Sales Analytics)", use_container_width=True)

    sample_path = os.path.join(os.path.dirname(__file__), "data", "sample_sales.csv")

    if load_demo and os.path.exists(sample_path):
        validator = CSVValidator()
        res = validator.validate(sample_path, file_name="sample_sales.csv")
        if res.is_valid:
            st.session_state.df = res.df
            st.session_state.file_name = "sample_sales.csv"
            st.session_state.profile = DataProfiler.profile(res.df)
            st.session_state.validation_warnings = res.warnings
            st.toast("Loaded sample_sales.csv successfully!", icon="✅")
            st.rerun()

    if uploaded_file is not None:
        validator = CSVValidator()
        res = validator.validate(uploaded_file, file_name=uploaded_file.name)
        if res.is_valid:
            st.session_state.df = res.df
            st.session_state.file_name = uploaded_file.name
            st.session_state.profile = DataProfiler.profile(res.df)
            st.session_state.validation_warnings = res.warnings
        else:
            st.error(res.error_message)

    st.markdown("---")
    st.subheader("⚙️ Analysis Settings")
    st.caption("Day 1: Data Profiling Engine")
    st.caption("Day 2: Deterministic Executor (Tomorrow)")
    st.caption("Day 3: LLM Structured Planner")
    st.caption("Day 4: Isolation Forest Anomaly Detection")
    st.caption("Day 5: Executive Report Generator")

# --- Main Workspace ---
if st.session_state.df is None:
    # Landing Empty State
    st.markdown('<div class="brand-title">Welcome to InsightAI</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="brand-subtitle">AI-grounded analytics and automated profiling. Python computes the facts; AI explains the insights.</p>',
        unsafe_allow_html=True
    )

    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Step 1 • Ingest & Validate</div>
            <div class="metric-value">Secure CSV</div>
            <div class="metric-detail status-good">Size checks, malformed line safety, auto-delimiter detection.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Step 2 • Automatic Profiling</div>
            <div class="metric-value">Zero Config</div>
            <div class="metric-detail status-good">Missing values, duplicates, numeric distributions & correlations.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_info3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Step 3 • Grounded Intelligence</div>
            <div class="metric-value">Verifiable</div>
            <div class="metric-detail status-good">Deterministic code execution guarantees zero LLM hallucination.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Get started quickly:** Click **'🚀 Load Demo Dataset'** in the sidebar or upload your own `.csv` file.", icon="ℹ️")

else:
    # Active Dataset Dashboard
    df: pd.DataFrame = st.session_state.df
    profile: DatasetProfile = st.session_state.profile

    # Top Header
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(f'<div class="brand-title">Dataset Profile: {st.session_state.file_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="brand-subtitle">Parsed {profile.row_count:,} rows and {profile.column_count} columns • Memory footprint: {profile.memory_usage_str}</div>', unsafe_allow_html=True)
    with header_col2:
        if st.button("🔄 Re-Profile Dataset", use_container_width=True):
            st.session_state.profile = DataProfiler.profile(st.session_state.df)
            st.rerun()

    # Display Validation Warnings if any
    for warn in st.session_state.validation_warnings:
        st.warning(f"⚠️ {warn}")

    # --- High-Level Metric Tiles ---
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Records</div>
            <div class="metric-value">{profile.row_count:,}</div>
            <div class="metric-detail status-good">{profile.column_count} Features</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        num_count = len(profile.numeric_columns)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Numeric Columns</div>
            <div class="metric-value">{num_count}</div>
            <div class="metric-detail status-good">{round((num_count / profile.column_count) * 100)}% of schema</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        cat_count = len(profile.categorical_columns)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Categorical / Text</div>
            <div class="metric-value">{cat_count}</div>
            <div class="metric-detail status-good">{len(profile.datetime_columns)} Datetime fields</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        missing_color = "status-good" if profile.total_missing_cells == 0 else "status-warn"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Missing Values</div>
            <div class="metric-value">{profile.total_missing_cells:,}</div>
            <div class="metric-detail {missing_color}">{profile.total_missing_percentage}% total cells</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        dup_color = "status-good" if profile.duplicate_rows_count == 0 else "status-bad"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Duplicate Rows</div>
            <div class="metric-value">{profile.duplicate_rows_count:,}</div>
            <div class="metric-detail {dup_color}">{profile.duplicate_rows_percentage}% redundancy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Profiling Tabs ---
    tab_overview, tab_schema, tab_explore, tab_charts, tab_clean = st.tabs([
        "📊 Summary & Distributions",
        "📋 Schema & Column Details",
        "🔍 Data Explorer & Raw Records",
        "📈 Instant Visualizations",
        "🧹 Hygiene & Data Cleaning"
    ])

    # TAB 1: Summary & Distributions
    with tab_overview:
        st.subheader("Statistical Summary of Numeric Features")
        if profile.has_numeric_columns:
            num_summary = df[profile.numeric_columns].describe().T
            num_summary = num_summary.rename(columns={
                "count": "Count", "mean": "Mean", "std": "Std Dev",
                "min": "Min", "25%": "25th Pct", "50%": "Median",
                "75%": "75th Pct", "max": "Max"
            })
            st.dataframe(
                num_summary.style.format("{:,.2f}").background_gradient(cmap="Blues", subset=["Mean", "Median"]),
                use_container_width=True
            )
        else:
            st.info("No numeric columns detected in this dataset.")

        st.markdown("---")
        st.subheader("Inter-Feature Correlation Matrix")
        if profile.correlation_matrix and len(profile.numeric_columns) >= 2:
            corr_df = pd.DataFrame(profile.correlation_matrix)
            fig_corr = px.imshow(
                corr_df,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="Viridis",
                title="Pearson Correlation Heatmap"
            )
            fig_corr.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=450)
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("At least two numeric columns are required to compute a correlation heatmap.")

    # TAB 2: Schema & Column Details
    with tab_schema:
        st.subheader("Comprehensive Column Metadata")

        schema_rows = []
        for col_name, c_prof in profile.columns.items():
            schema_rows.append({
                "Column Name": col_name,
                "Inferred Type": c_prof.semantic_type.upper(),
                "Pandas Dtype": c_prof.dtype,
                "Non-Null Count": f"{c_prof.non_null_count:,}",
                "Missing Values": f"{c_prof.missing_count:,} ({c_prof.missing_percentage}%)",
                "Unique Values": f"{c_prof.unique_count:,}",
                "Unique Key": "Yes" if c_prof.is_unique else "No",
                "Sample Values": ", ".join(str(s) for s in c_prof.sample_values)
            })

        schema_df = pd.DataFrame(schema_rows)
        st.dataframe(schema_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Inspect Individual Feature Distribution")
        selected_col = st.selectbox("Select a column to inspect in depth:", df.columns)
        if selected_col:
            col_data = profile.columns[selected_col]
            c_left, c_right = st.columns([1, 2])
            with c_left:
                st.markdown(f"**Semantic Type:** `{col_data.semantic_type}`")
                st.markdown(f"**Missing Count:** `{col_data.missing_count}` (`{col_data.missing_percentage}%`)")
                st.markdown(f"**Unique Values:** `{col_data.unique_count}`")
                if col_data.stats:
                    st.write("**Key Statistics:**")
                    st.json(col_data.stats)
            with c_right:
                if col_data.semantic_type == "numeric":
                    fig_hist = px.histogram(
                        df, x=selected_col, nbins=30,
                        marginal="box",
                        title=f"Distribution of {selected_col}",
                        color_discrete_sequence=["#6366F1"]
                    )
                    fig_hist.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=350)
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    top_cats = df[selected_col].value_counts().head(10).reset_index()
                    top_cats.columns = [selected_col, "Count"]
                    fig_bar = px.bar(
                        top_cats, x=selected_col, y="Count",
                        title=f"Top 10 Categories in {selected_col}",
                        color="Count",
                        color_continuous_scale="Purples"
                    )
                    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=350)
                    st.plotly_chart(fig_bar, use_container_width=True)

    # TAB 3: Data Explorer & Raw Records
    with tab_explore:
        st.subheader("Interactive Dataset Explorer")

        f_col1, f_col2 = st.columns([2, 1])
        with f_col1:
            search_query = st.text_input("🔎 Search dataset rows by text keyword:", "")
        with f_col2:
            row_limit = st.slider("Display row limit:", min_value=10, max_value=min(1000, len(df)), value=50, step=10)

        cols_to_show = st.multiselect("Visible columns:", options=list(df.columns), default=list(df.columns))

        filtered_df = df[cols_to_show] if cols_to_show else df
        if search_query.strip():
            # Search string across all columns
            mask = filtered_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False, na=False).any(), axis=1)
            filtered_df = filtered_df[mask]

        st.caption(f"Showing {min(row_limit, len(filtered_df))} of {len(filtered_df):,} matching rows")
        st.dataframe(filtered_df.head(row_limit), use_container_width=True)

        # Download button for filtered/current data
        csv_buffer = io.StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Visible Rows as CSV",
            data=csv_buffer.getvalue(),
            file_name=f"exported_{st.session_state.file_name}",
            mime="text/csv"
        )

    # TAB 4: Instant Visualizations
    with tab_charts:
        st.subheader("Rapid Visual Exploration")
        v_col1, v_col2 = st.columns(2)

        if profile.has_numeric_columns:
            with v_col1:
                num_x = st.selectbox("X-Axis (Numeric or Categorical):", df.columns, index=0, key="chart_x")
                num_y = st.selectbox("Y-Axis (Numeric Metric):", profile.numeric_columns, index=0, key="chart_y")
                chart_type = st.radio("Chart Type:", ["Bar Chart", "Scatter Plot", "Box Plot"], horizontal=True)

            with v_col2:
                color_by = st.selectbox("Optional Color Grouping:", ["None"] + profile.categorical_columns, index=0)
                color_col = None if color_by == "None" else color_by

            if chart_type == "Bar Chart":
                # Aggregate if categorical x
                if num_x in profile.categorical_columns:
                    grouped = df.groupby(num_x)[num_y].sum().reset_index()
                    fig = px.bar(grouped, x=num_x, y=num_y, color=num_y, color_continuous_scale="Viridis", title=f"Total {num_y} by {num_x}")
                else:
                    fig = px.bar(df.head(50), x=num_x, y=num_y, title=f"{num_y} vs {num_x}")
            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=num_x, y=num_y, color=color_col, hover_data=df.columns[:4], title=f"{num_y} vs {num_x}")
            else:
                fig = px.box(df, x=num_x if num_x in profile.categorical_columns else None, y=num_y, color=color_col, title=f"Distribution of {num_y}")

            fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=460)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available to plot standard metric charts.")

    # TAB 5: Hygiene & Data Cleaning
    with tab_clean:
        st.subheader("Data Hygiene & Cleaning Recommendations")

        st.markdown(f"""
        - **Duplicate Rows:** `{profile.duplicate_rows_count}` row(s) found ({profile.duplicate_rows_percentage}%).
        - **Missing Cells:** `{profile.total_missing_cells}` cell(s) missing across dataset.
        """)

        c_action1, c_action2 = st.columns(2)
        with c_action1:
            st.write("#### Deduplication")
            if profile.duplicate_rows_count > 0:
                if st.button("🗑️ Remove Duplicate Rows", key="btn_dedup", use_container_width=True):
                    cleaned_df, removed = DataCleaner.drop_duplicates(df)
                    st.session_state.df = cleaned_df
                    st.session_state.profile = DataProfiler.profile(cleaned_df)
                    st.success(f"Removed {removed} duplicate row(s)!")
                    st.rerun()
            else:
                st.success("✅ No duplicate rows in dataset.")

        with c_action2:
            st.write("#### Missing Values Imputation")
            if profile.total_missing_cells > 0:
                impute_num_strategy = st.selectbox("Numeric Imputation Strategy:", ["median", "mean", "zero"])
                if st.button("🩹 Impute Missing Values", key="btn_impute", use_container_width=True):
                    cleaned_df, count = DataCleaner.impute_missing(
                        df, numeric_strategy=impute_num_strategy, categorical_strategy="mode"
                    )
                    st.session_state.df = cleaned_df
                    st.session_state.profile = DataProfiler.profile(cleaned_df)
                    st.success(f"Imputed {count} missing value cell(s)!")
                    st.rerun()
            else:
                st.success("✅ No missing values detected in dataset.")
