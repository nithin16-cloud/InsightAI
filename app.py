"""
InsightAI - Intelligent Tabular Data Analytics Platform
Deterministic Python execution. Zero hallucinations. ML anomaly detection. Executive HTML reports.
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
from src.executor import DeterministicExecutor, ExecutionResult
from src.planner import QueryPlanner, AnalysisPlan
from src.anomalies import AnomalyDetector, AnomalyDetectionResult
from src.reporter import ExecutiveReporter
import streamlit.components.v1 as components

# --- Page Configuration ---
FAVICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "favicon.png")

st.set_page_config(
    page_title="InsightAI | Tabular Analytics & Intelligence",
    page_icon=FAVICON_PATH if os.path.exists(FAVICON_PATH) else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dynamic Favicon Cache-Buster (guarantees browser tab never displays Streamlit default crown)
components.html(
    """
    <script>
        try {
            const pDoc = window.parent.document;
            const existing = pDoc.querySelectorAll("link[rel*='icon']");
            existing.forEach(el => el.remove());
            const link = pDoc.createElement('link');
            link.rel = 'shortcut icon';
            link.type = 'image/png';
            link.href = '/favicon.png?v=' + Date.now();
            pDoc.getElementsByTagName('head')[0].appendChild(link);
        } catch(e) {}
    </script>
    """,
    height=0,
    width=0,
)

# --- Modern, High-End Design System (Mobile-Responsive & Ultra-Smooth) ---
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography, Touch Resets & Canvas */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0A0D14;
        color: #F8FAFC;
        -webkit-tap-highlight-color: transparent;
        text-rendering: optimizeLegibility;
    }

    /* Hardware Accelerated Smooth Transitions */
    * {
        box-sizing: border-box;
    }
    .posh-card, .stButton > button, .health-container, .narrative-card {
        will-change: transform;
        transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.18s ease, box-shadow 0.18s ease !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0D14;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.35);
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.75rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1300px !important;
    }

    /* Brand Header */
    .brand-hero {
        padding: 0.25rem 0 0.85rem 0;
    }
    .brand-title {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(1.6rem, 3.5vw, 2.35rem);
        font-weight: 800;
        letter-spacing: -0.035em;
        margin-bottom: 0.25rem;
        line-height: 1.2;
        word-break: break-word;
    }
    .brand-tagline {
        color: #94A3B8;
        font-size: clamp(0.85rem, 1.8vw, 0.98rem);
        font-weight: 400;
        margin-bottom: 0.5rem;
        line-height: 1.45;
    }
    .assurance-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34D399;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    /* Luxury Glassmorphic Cards */
    .posh-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
    }
    .posh-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.35);
    }
    .posh-card:active {
        transform: scale(0.98);
    }

    .metric-title {
        color: #94A3B8;
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .metric-num {
        color: #FFFFFF;
        font-size: clamp(1.4rem, 2.5vw, 1.95rem);
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }
    .metric-sub {
        font-size: 0.78rem;
        font-weight: 500;
        color: #94A3B8;
    }

    /* Health Scorecard */
    .health-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.75) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1.1rem 1.35rem;
        margin-bottom: 1.25rem;
    }
    .health-val {
        font-size: clamp(1.75rem, 3.5vw, 2.2rem);
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1;
    }

    /* Status Colors */
    .c-good { color: #10B981 !important; }
    .c-warn { color: #F59E0B !important; }
    .c-bad { color: #F43F5E !important; }
    .c-info { color: #60A5FA !important; }

    /* Pill Badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-numeric { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.25); }
    .badge-categorical { background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.25); }
    .badge-datetime { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.25); }

    /* Narrative Highlight Box */
    .narrative-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 12px;
        padding: 1.15rem 1.35rem;
        margin: 1rem 0;
    }
    .narrative-title {
        color: #A5B4FC;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
    }
    .narrative-body {
        color: #F1F5F9;
        font-size: 1.02rem;
        line-height: 1.55;
        font-weight: 400;
    }

    /* Tabs Styling - Horizontal Swipe Carousel on Mobile */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.45rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.4rem;
        margin-bottom: 1.25rem;
        display: flex;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.48rem 0.95rem;
        white-space: nowrap;
        flex-shrink: 0;
        transition: all 0.18s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.18) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: 1px solid rgba(99, 102, 241, 0.35) !important;
    }

    /* Touch-Ergonomic Buttons (44px Minimum Tap Height) */
    .stButton > button {
        min-height: 44px;
        border-radius: 9px;
        font-weight: 600;
        font-size: 0.92rem;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 0.55rem 1.15rem;
        touch-action: manipulation;
    }
    .stButton > button:hover {
        border-color: #818CF8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* Inputs - Prevent Mobile Auto-Zoom */
    input, select, textarea {
        font-size: 16px !important;
    }

    /* Floating Mobile Sidebar Trigger Enhancement */
    [data-testid="stSidebarCollapsedControl"] {
        top: 0.6rem !important;
        left: 0.6rem !important;
        z-index: 100 !important;
        background: rgba(17, 24, 39, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Dataframe Tables: Smooth Touch Scrolling */
    [data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-radius: 10px !important;
    }

    /* ============================================================== */
    /* RESPONSIVE BREAKPOINT: TABLETS & MOBILE PHONES (<= 768px)      */
    /* Buttery-Smooth, Uncrowded, Native-Feeling Responsive Layout    */
    /* ============================================================== */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1.25rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 100vw !important;
        }

        /* Responsive Grid: Multi-columns wrap gracefully instead of squeezing */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.65rem !important;
            row-gap: 0.75rem !important;
            width: 100% !important;
        }

        /* 2-Column Balanced Grid on Mobile for Metric Cards & Grid Elements */
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex: 1 1 calc(50% - 0.4rem) !important;
            min-width: calc(50% - 0.4rem) !important;
            max-width: 100% !important;
        }

        /* Cards padding calibrated for phone screens */
        .posh-card {
            padding: 0.95rem 1rem !important;
            border-radius: 12px !important;
        }
        .metric-title {
            font-size: 0.68rem !important;
            letter-spacing: 0.05em !important;
        }
        .metric-sub {
            font-size: 0.72rem !important;
        }

        /* Health scorecard on mobile */
        .health-container {
            padding: 0.95rem 1.15rem !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.95rem !important;
        }

        /* Mobile Tab Carousel - Pill Format */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.4rem !important;
            padding-bottom: 0.5rem !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.83rem !important;
            padding: 0.45rem 0.82rem !important;
            border-radius: 9999px !important;
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
        }

        /* Charts: Prevent zoom trap on finger scroll */
        .js-plotly-plot, .plotly {
            touch-action: pan-y !important;
            max-width: 100% !important;
        }
        .modebar-container {
            display: none !important;
        }
    }

    /* ============================================================== */
    /* EXTRA-NARROW PHONE SCREENS (<= 480px)                          */
    /* ============================================================== */
    @media (max-width: 480px) {
        .block-container {
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
        }

        /* Form Controls Full Width on Small Phones */
        .stSelectbox, .stTextInput, .stSlider {
            width: 100% !important;
        }
        .stButton > button {
            width: 100% !important;
        }
    }

    /* Monospace Text */
    code, .font-mono {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --- Plotly Unified Theme ---
def apply_posh_plotly_layout(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply unified luxury dark theme to all Plotly visualizations."""
    fig.update_layout(
        title={
            "text": title,
            "font": {"family": "Plus Jakarta Sans", "size": 14, "color": "#F8FAFC"},
            "x": 0.01,
            "xanchor": "left"
        },
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Plus Jakarta Sans", "color": "#94A3B8"},
        margin=dict(l=15, r=15, t=45, b=25),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont={"size": 10, "color": "#94A3B8"},
            linecolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont={"size": 10, "color": "#94A3B8"},
            linecolor="rgba(255,255,255,0.1)"
        ),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.6)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            font={"size": 10, "color": "#CBD5E1"},
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


# --- Session State Management ---
def init_session():
    """Ensure all required session states exist."""
    defaults = {
        "df": None,
        "profile": None,
        "file_name": None,
        "validation_warnings": [],
        "anomaly_result": None,
        "last_query": "",
        "query_history": [],
        "custom_api_key": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session()


# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.2rem;">
            <div style="width: 26px; height: 26px; border-radius: 6px; background: linear-gradient(135deg, #6366F1, #A855F7); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; color: #FFFFFF;">AI</div>
            <span style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">InsightAI</span>
        </div>
        <p style="color: #64748B; font-size: 0.82rem; margin: 0;">Intelligent Tabular Analytics & Profiling</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Ingestion Block
    st.markdown("#### Data Source")
    uploaded = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"],
        help="Upload tabular CSV files up to 50MB. Delimiters and encodings are detected automatically."
    )

    col_demo, col_reset = st.columns([2, 1])
    with col_demo:
        load_demo = st.button("Load Demo Sales", use_container_width=True)
    with col_reset:
        reset_app = st.button("Clear", use_container_width=True)

    if reset_app:
        st.session_state.df = None
        st.session_state.profile = None
        st.session_state.file_name = None
        st.session_state.anomaly_result = None
        st.session_state.validation_warnings = []
        st.rerun()

    sample_sales_path = os.path.join(os.path.dirname(__file__), "data", "sample_sales.csv")

    if load_demo and os.path.exists(sample_sales_path):
        val = CSVValidator()
        res = val.validate(sample_sales_path, file_name="sample_sales.csv")
        if res.is_valid:
            st.session_state.df = res.df
            st.session_state.file_name = "sample_sales.csv"
            st.session_state.profile = DataProfiler.profile(res.df)
            st.session_state.validation_warnings = res.warnings
            st.session_state.anomaly_result = None
            st.toast("Loaded sample_sales.csv successfully.")
            st.rerun()

    if uploaded is not None and (st.session_state.file_name != uploaded.name):
        val = CSVValidator()
        res = val.validate(uploaded, file_name=uploaded.name)
        if res.is_valid:
            st.session_state.df = res.df
            st.session_state.file_name = uploaded.name
            st.session_state.profile = DataProfiler.profile(res.df)
            st.session_state.validation_warnings = res.warnings
            st.session_state.anomaly_result = None
            st.toast(f"Loaded {uploaded.name} successfully.")
            st.rerun()
        else:
            st.error(res.error_message)

    # API Configuration (Optional)
    st.markdown("---")
    with st.expander("OpenAI Configuration (Optional)", expanded=False):
        st.caption("InsightAI operates 100% deterministically offline. Connect an API key for enhanced conversational commentary.")
        api_key_input = st.text_input(
            "OpenAI API Key",
            value=st.session_state.custom_api_key or os.getenv("OPENAI_API_KEY", ""),
            type="password",
            placeholder="sk-..."
        )
        if api_key_input != st.session_state.custom_api_key:
            st.session_state.custom_api_key = api_key_input
            if api_key_input:
                st.success("API key registered.")

    # System Integrity Badges
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.78rem; color: #64748B; display: flex; flex-direction: column; gap: 0.45rem;">
        <div><strong>Deterministic Engine:</strong> Active (Python)</div>
        <div><strong>Execution Safety:</strong> Strict Allow-list</div>
        <div><strong>Hallucination Risk:</strong> Zero (Deterministic)</div>
        <div><strong>Anomaly Algorithm:</strong> Isolation Forest</div>
    </div>
    """, unsafe_allow_html=True)


# --- Main Workspace ---
if st.session_state.df is None:
    # --- Landing Empty State ---
    st.markdown("""
    <div class="brand-hero">
        <div class="assurance-badge">Deterministic Tabular Analytics Engine</div>
        <h1 class="brand-title">Transform Tabular Data into Verified Insights</h1>
        <p class="brand-tagline">
            Deterministic Python calculations guarantee mathematical accuracy. Zero hallucinations, zero arbitrary code execution, clear humanized summaries.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown("""
        <div class="posh-card">
            <div class="metric-title">1. Ingest & Sanitize</div>
            <div class="metric-num" style="font-size: 1.5rem;">Secure CSV</div>
            <div class="metric-sub">Automatic delimiter, encoding detection, malformed line safety up to 50MB.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("""
        <div class="posh-card">
            <div class="metric-title">2. Automated Profiling</div>
            <div class="metric-num" style="font-size: 1.5rem;">Health Score</div>
            <div class="metric-sub">Instant detection of duplicate rows, null cells, numeric skews, and correlations.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_c3:
        st.markdown("""
        <div class="posh-card">
            <div class="metric-title">3. Grounded Intelligence</div>
            <div class="metric-num" style="font-size: 1.5rem;">Plain English</div>
            <div class="metric-sub">Natural language questions execute deterministic pandas aggregations and ML anomaly scans.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Ready to explore? Upload a CSV file in the sidebar or click 'Load Demo Sales' to test the analytics engine immediately.")

else:
    # --- Active Dataset Dashboard ---
    df: pd.DataFrame = st.session_state.df
    profile: DatasetProfile = st.session_state.profile
    api_key_to_use = st.session_state.custom_api_key or os.getenv("OPENAI_API_KEY")

    # Compute overall dataset health
    health_score = ExecutiveReporter.calculate_health_score(profile, st.session_state.anomaly_result)
    health_color = "c-good" if health_score >= 85 else ("c-warn" if health_score >= 65 else "c-bad")
    health_grade = "A+" if health_score >= 95 else ("A" if health_score >= 85 else ("B" if health_score >= 70 else "C"))

    # Top Bar Header
    head_left, head_right = st.columns([3, 1])
    with head_left:
        st.markdown(f"""
        <div class="brand-hero">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span class="badge badge-datetime">ACTIVE DATASET</span>
                <span style="color: #94A3B8; font-size: 0.85rem;">{st.session_state.file_name}</span>
            </div>
            <h1 class="brand-title" style="font-size: 2.1rem; margin-top: 0.2rem;">{st.session_state.file_name}</h1>
            <p class="brand-tagline">
                {profile.row_count:,} records across {profile.column_count} features &mdash; Memory: {profile.memory_usage_str}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with head_right:
        st.markdown(f"""
        <div class="health-container">
            <div>
                <div class="metric-title">Data Health</div>
                <div style="font-size: 0.8rem; color: #94A3B8;">Grade {health_grade} Score</div>
            </div>
            <div class="health-val {health_color}">{health_score}<span style="font-size: 1.1rem; color: #64748B;">/100</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Display Validation Warnings
    for w in st.session_state.validation_warnings:
        st.warning(f"Warning: {w}")

    # --- High-Level Metric Tiles ---
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
        <div class="posh-card">
            <div class="metric-title">Total Records</div>
            <div class="metric-num">{profile.row_count:,}</div>
            <div class="metric-sub">{profile.column_count} Features</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        n_count = len(profile.numeric_columns)
        st.markdown(f"""
        <div class="posh-card">
            <div class="metric-title">Numeric Features</div>
            <div class="metric-num">{n_count}</div>
            <div class="metric-sub">{round((n_count / max(1, profile.column_count)) * 100)}% of schema</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        c_count = len(profile.categorical_columns)
        st.markdown(f"""
        <div class="posh-card">
            <div class="metric-title">Categorical Fields</div>
            <div class="metric-num">{c_count}</div>
            <div class="metric-sub">{len(profile.datetime_columns)} Datetime fields</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        miss_color = "c-good" if profile.total_missing_cells == 0 else "c-warn"
        st.markdown(f"""
        <div class="posh-card">
            <div class="metric-title">Missing Values</div>
            <div class="metric-num {miss_color}">{profile.total_missing_cells:,}</div>
            <div class="metric-sub">{profile.total_missing_percentage}% total cells</div>
        </div>
        """, unsafe_allow_html=True)

    with k5:
        dup_color = "c-good" if profile.duplicate_rows_count == 0 else "c-bad"
        st.markdown(f"""
        <div class="posh-card">
            <div class="metric-title">Duplicate Rows</div>
            <div class="metric-num {dup_color}">{profile.duplicate_rows_count:,}</div>
            <div class="metric-sub">{profile.duplicate_rows_percentage}% redundancy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 6 Humanized, Super Clean Tabs ---
    tab_overview, tab_ask, tab_anomalies, tab_visuals, tab_clean, tab_report = st.tabs([
        "Overview & Health",
        "Ask Analyst",
        "Anomaly Scanner",
        "Visual Studio",
        "Data Studio",
        "Executive Report"
    ])

    # ========================================================
    # TAB 1: Overview & Health
    # ========================================================
    with tab_overview:
        col_ov_left, col_ov_right = st.columns([1, 1])

        with col_ov_left:
            st.subheader("Statistical Summary of Numeric Features")
            if profile.has_numeric_columns:
                num_summary = df[profile.numeric_columns].describe().T
                num_summary = num_summary.rename(columns={
                    "count": "Count", "mean": "Mean", "std": "Std Dev",
                    "min": "Min", "25%": "25th Pct", "50%": "Median",
                    "75%": "75th Pct", "max": "Max"
                })
                def _highlight_range(val):
                    """Highlight cells relative to column max — no matplotlib needed."""
                    return "background-color: rgba(99,102,241,0.15); color: #E2E8F0;"

                styled = num_summary.style.format("{:,.2f}").map(
                    _highlight_range, subset=["Mean", "Median"]
                )
                st.dataframe(styled, use_container_width=True)
            else:
                st.info("No numeric columns found in dataset.")

        with col_ov_right:
            st.subheader("Feature Correlation Heatmap")
            if profile.correlation_matrix and len(profile.numeric_columns) >= 2:
                corr_df = pd.DataFrame(profile.correlation_matrix)
                fig_corr = px.imshow(
                    corr_df,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale="Purples",
                    title="Pearson Correlation Heatmap"
                )
                apply_posh_plotly_layout(fig_corr)
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.info("Need at least 2 numeric features to compute correlation matrix.")

        st.markdown("---")
        st.subheader("Comprehensive Column Schema")
        schema_rows = []
        for col_name, c_prof in profile.columns.items():
            schema_rows.append({
                "Feature Name": col_name,
                "Inferred Type": c_prof.semantic_type.upper(),
                "Non-Null Count": f"{c_prof.non_null_count:,}",
                "Missing Cells": f"{c_prof.missing_count:,} ({c_prof.missing_percentage}%)",
                "Unique Cardinality": f"{c_prof.unique_count:,}",
                "Sample Values": ", ".join(str(s) for s in c_prof.sample_values)
            })
        st.dataframe(pd.DataFrame(schema_rows), use_container_width=True, hide_index=True)

    # ========================================================
    # TAB 2: Ask Analyst (Natural Language Engine)
    # ========================================================
    with tab_ask:
        st.subheader("Plain-English Analytics Engine")
        st.caption("Ask questions about your data in everyday language. Verified deterministic calculations guarantee mathematical accuracy.")

        # Suggestion pills
        suggestions = QueryPlanner.get_suggested_queries(df)
        st.markdown("**Suggested Inquiries:**")

        # Suggestion pills (responsive 2-column layout for touch & desktop)
        sugg_c1, sugg_c2 = st.columns(2)
        selected_suggestion = None
        for i, s_text in enumerate(suggestions):
            target_c = sugg_c1 if (i % 2 == 0) else sugg_c2
            with target_c:
                if st.button(s_text, key=f"sugg_{i}", use_container_width=True):
                    selected_suggestion = s_text

        # Question Input
        default_q = selected_suggestion if selected_suggestion else st.session_state.last_query
        user_query = st.text_input(
            "Enter your question:",
            value=default_q,
            placeholder="e.g. Which region generates the highest revenue?",
            key="nl_query_input"
        )

        run_query = st.button("Run Analysis", type="primary", use_container_width=True)

        if (run_query or selected_suggestion) and user_query.strip():
            st.session_state.last_query = user_query
            planner = QueryPlanner(api_key=api_key_to_use)

            with st.spinner("Translating question into verified deterministic plan..."):
                plan, exec_result = planner.plan_and_execute(user_query, df)

            if exec_result.success:
                # Grounded Narrative Box
                st.markdown(f"""
                <div class="narrative-card">
                    <div class="narrative-title">Verified Executive Insight</div>
                    <div class="narrative-body">{exec_result.narrative}</div>
                </div>
                """, unsafe_allow_html=True)

                # Visual + Table Presentation
                q_col_left, q_col_right = st.columns([1, 1])

                with q_col_left:
                    st.write("#### Visual Representation")
                    if exec_result.result_df is not None and not exec_result.result_df.empty:
                        if exec_result.chart_type == "bar":
                            cfg = exec_result.chart_config
                            fig_q = px.bar(
                                exec_result.result_df,
                                x=cfg.get("x"),
                                y=cfg.get("y"),
                                color=cfg.get("color", cfg.get("y")),
                                color_continuous_scale="Purples",
                                title=cfg.get("title", "Result Breakdown")
                            )
                        elif exec_result.chart_type == "line":
                            cfg = exec_result.chart_config
                            fig_q = px.line(
                                exec_result.result_df,
                                x=cfg.get("x"),
                                y=cfg.get("y"),
                                markers=True,
                                title=cfg.get("title", "Temporal Trend")
                            )
                        else:
                            fig_q = px.bar(
                                exec_result.result_df.head(10),
                                x=exec_result.result_df.columns[0],
                                y=exec_result.result_df.columns[1] if len(exec_result.result_df.columns) > 1 else exec_result.result_df.columns[0]
                            )

                        apply_posh_plotly_layout(fig_q)
                        st.plotly_chart(fig_q, use_container_width=True)

                with q_col_right:
                    st.write("#### Computed Figures")
                    if exec_result.result_df is not None:
                        st.dataframe(exec_result.result_df, use_container_width=True)

                # Inspect Calculation Details
                with st.expander("View Deterministic Calculation Audit", expanded=False):
                    st.markdown(f"""
                    - **Operation Executed:** `{plan.operation}`
                    - **Categorical Dimension:** `{plan.group_col}`
                    - **Metric Field:** `{plan.metric_col}`
                    - **Aggregation Math:** `{plan.agg_func.upper()}`
                    - **Top Limit:** `{plan.top_n}` (Sort Descending: `{plan.sort_desc}`)
                    - **Planner Rationale:** *{plan.rationale}*
                    """)
                    st.json(exec_result.kpis)
            else:
                st.error(f"Analysis could not be computed: {exec_result.error_message}")

    # ========================================================
    # TAB 3: Machine Learning Anomaly Scanner
    # ========================================================
    with tab_anomalies:
        st.subheader("Machine Learning Outlier Detection (Isolation Forest)")
        st.caption(
            "Detects multivariate anomalies where records exhibit unusual cross-feature divergence that traditional single-column thresholds miss."
        )

        anom_c1, anom_c2 = st.columns(2)
        with anom_c1:
            contamination = st.slider(
                "Estimated Outlier Contamination Rate (%):",
                min_value=1.0,
                max_value=15.0,
                value=5.0,
                step=0.5,
                help="The approximate proportion of outliers expected in this dataset."
            ) / 100.0

        with anom_c2:
            num_cols = profile.numeric_columns
            selected_features = st.multiselect(
                "Features to include in model training:",
                options=num_cols,
                default=num_cols[:min(5, len(num_cols))]
            )

        run_anom_btn = st.button("Run Isolation Forest Scan", type="primary", use_container_width=True)

        if run_anom_btn or (st.session_state.anomaly_result is None and profile.has_numeric_columns):
            with st.spinner("Training Isolation Forest and computing anomaly severity scores..."):
                ok, anom_res, err = AnomalyDetector.detect_anomalies(
                    df,
                    feature_columns=selected_features if selected_features else None,
                    contamination=contamination
                )
                if ok:
                    st.session_state.anomaly_result = anom_res
                else:
                    st.error(err)

        if st.session_state.anomaly_result:
            a_res: AnomalyDetectionResult = st.session_state.anomaly_result

            # Top KPI Cards for Anomaly Scan
            ak1, ak2, ak3 = st.columns(3)
            with ak1:
                st.markdown(f"""
                <div class="posh-card">
                    <div class="metric-title">Outliers Flagged</div>
                    <div class="metric-num c-bad">{a_res.outliers_detected}</div>
                    <div class="metric-sub">{a_res.outlier_percentage}% of total dataset</div>
                </div>
                """, unsafe_allow_html=True)
            with ak2:
                st.markdown(f"""
                <div class="posh-card">
                    <div class="metric-title">Features Modeled</div>
                    <div class="metric-num">{len(a_res.features_used)}</div>
                    <div class="metric-sub">{', '.join(a_res.features_used[:3])}...</div>
                </div>
                """, unsafe_allow_html=True)
            with ak3:
                st.markdown(f"""
                <div class="posh-card">
                    <div class="metric-title">Algorithm</div>
                    <div class="metric-num" style="font-size: 1.3rem;">Isolation Forest</div>
                    <div class="metric-sub">Contamination: {int(a_res.contamination*100)}% - n_est: 100</div>
                </div>
                """, unsafe_allow_html=True)

            # Anomaly Scatter Plot
            st.markdown("<br>", unsafe_allow_html=True)
            plot_c1, plot_c2 = st.columns([2, 1])

            with plot_c1:
                st.write("#### Multivariate Scatter Map")
                if len(a_res.features_used) >= 2:
                    feat_x = st.selectbox("X-Axis Feature:", a_res.features_used, index=0, key="anom_x")
                    feat_y = st.selectbox("Y-Axis Feature:", a_res.features_used, index=1, key="anom_y")

                    fig_anom = px.scatter(
                        a_res.full_df_with_scores,
                        x=feat_x,
                        y=feat_y,
                        color="_is_anomaly",
                        color_discrete_map={True: "#F43F5E", False: "#38BDF8"},
                        hover_data=["anomaly_score"] + a_res.features_used[:3],
                        title=f"Outlier Boundary: {feat_y} vs {feat_x}"
                    )
                    apply_posh_plotly_layout(fig_anom)
                    st.plotly_chart(fig_anom, use_container_width=True)

            with plot_c2:
                st.write("#### Key Outlier Factors")
                for item in a_res.top_anomalies_summary:
                    st.markdown(f"""
                    <div style="background: rgba(24, 34, 52, 0.7); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 0.65rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #FFFFFF;">{item['record_id']}</span>
                            <span style="background: rgba(244, 63, 94, 0.15); color: #F43F5E; font-size: 0.72rem; padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 700;">Score {item['anomaly_score']}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #CBD5E1;">{item['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Outlier Table & CSV Download
            st.write("#### Flagged Outlier Records")
            st.dataframe(a_res.outlier_df, use_container_width=True)

            outlier_csv = io.StringIO()
            a_res.outlier_df.to_csv(outlier_csv, index=False)
            st.download_button(
                label="Download Outlier Records (CSV)",
                data=outlier_csv.getvalue(),
                file_name=f"anomalies_{st.session_state.file_name}",
                mime="text/csv"
            )

    # ========================================================
    # TAB 4: Visual Studio
    # ========================================================
    with tab_visuals:
        st.subheader("Interactive Visual Studio")
        st.caption("Construct clean, publication-grade visualizations with unified color palettes.")

        if profile.has_numeric_columns:
            vs_c1, vs_c2, vs_c3 = st.columns(3)
            with vs_c1:
                v_type = st.selectbox("Chart Type:", ["Bar Chart", "Line Trend", "Scatter Plot", "Box Plot", "Histogram"], key="v_type")
            with vs_c2:
                v_x = st.selectbox("X-Axis (Dimension):", df.columns, index=0, key="v_x")
            with vs_c3:
                v_y = st.selectbox("Y-Axis (Numeric Metric):", profile.numeric_columns, index=0, key="v_y")

            vs_c4, vs_c5 = st.columns(2)
            with vs_c4:
                v_color_opts = ["None"] + profile.categorical_columns
                v_color = st.selectbox("Color / Group By (Optional):", v_color_opts, index=0, key="v_color")
                chosen_color = None if v_color == "None" else v_color
            with vs_c5:
                v_agg = st.selectbox("Aggregation Math:", ["Sum", "Average", "Count", "Max", "Min"], index=0, key="v_agg")

            # Generate chart
            if v_type == "Bar Chart":
                if v_x in profile.categorical_columns:
                    func = "mean" if v_agg == "Average" else v_agg.lower()
                    grouped = df.groupby(v_x)[v_y].agg(func).reset_index()
                    fig_v = px.bar(grouped, x=v_x, y=v_y, color=v_y, color_continuous_scale="Purples", title=f"{v_agg} of {v_y} by {v_x}")
                else:
                    fig_v = px.bar(df.head(100), x=v_x, y=v_y, color=chosen_color, title=f"{v_y} vs {v_x}")
            elif v_type == "Line Trend":
                fig_v = px.line(df, x=v_x, y=v_y, color=chosen_color, markers=True, title=f"{v_y} over {v_x}")
            elif v_type == "Scatter Plot":
                fig_v = px.scatter(df, x=v_x, y=v_y, color=chosen_color, hover_data=df.columns[:3], title=f"{v_y} vs {v_x}")
            elif v_type == "Box Plot":
                fig_v = px.box(df, x=v_x if v_x in profile.categorical_columns else None, y=v_y, color=chosen_color, title=f"Distribution of {v_y}")
            else:
                fig_v = px.histogram(df, x=v_y, color=chosen_color, marginal="box", nbins=30, title=f"Histogram of {v_y}")

            apply_posh_plotly_layout(fig_v)
            st.plotly_chart(fig_v, use_container_width=True)
        else:
            st.info("Visual studio requires at least one numeric feature in the dataset.")

    # ========================================================
    # TAB 5: Hygiene & Data Studio
    # ========================================================
    with tab_clean:
        st.subheader("Data Hygiene & Cleaning Utilities")
        st.caption("Apply non-destructive cleaning transformations to improve dataset health.")

        cl_left, cl_right = st.columns(2)

        with cl_left:
            st.write("#### Deduplication")
            st.markdown(f"**Duplicate Rows Detected:** `{profile.duplicate_rows_count}` ({profile.duplicate_rows_percentage}%)")
            if profile.duplicate_rows_count > 0:
                if st.button("Remove Duplicate Rows", key="btn_dedup_action", use_container_width=True):
                    cleaned_df, removed = DataCleaner.drop_duplicates(df)
                    st.session_state.df = cleaned_df
                    st.session_state.profile = DataProfiler.profile(cleaned_df)
                    st.session_state.anomaly_result = None
                    st.success(f"Removed {removed} duplicate rows successfully.")
                    st.rerun()
            else:
                st.success("Dataset contains zero duplicate rows.")

            st.write("#### Header Normalization")
            if st.button("Standardize Column Headers to snake_case", key="btn_snake_action", use_container_width=True):
                cleaned_df, new_cols = DataCleaner.standardize_column_names(df)
                st.session_state.df = cleaned_df
                st.session_state.profile = DataProfiler.profile(cleaned_df)
                st.success("Column headers standardized.")
                st.rerun()

        with cl_right:
            st.write("#### Missing Values Imputation")
            st.markdown(f"**Missing Cells Detected:** `{profile.total_missing_cells}` ({profile.total_missing_percentage}%)")
            if profile.total_missing_cells > 0:
                imp_strategy = st.selectbox(
                    "Numeric Imputation Strategy:",
                    ["median", "mean", "zero"],
                    help="Median is recommended for skewed distributions with outliers."
                )
                if st.button("Impute Missing Cells", key="btn_imp_action", use_container_width=True):
                    cleaned_df, count = DataCleaner.impute_missing(
                        df, numeric_strategy=imp_strategy, categorical_strategy="mode"
                    )
                    st.session_state.df = cleaned_df
                    st.session_state.profile = DataProfiler.profile(cleaned_df)
                    st.session_state.anomaly_result = None
                    st.success(f"Successfully imputed {count} missing value cell(s).")
                    st.rerun()
            else:
                st.success("Dataset contains zero missing cells.")

        st.markdown("---")
        st.subheader("Interactive Dataset Viewer & Export")
        search_kw = st.text_input("Search dataset records by keyword:", "", key="view_search")
        col_limit = st.slider("Max rows to preview:", 10, min(1000, len(df)), 50, step=10)

        view_df = df
        if search_kw.strip():
            mask = view_df.astype(str).apply(lambda row: row.str.contains(search_kw, case=False, na=False).any(), axis=1)
            view_df = view_df[mask]

        st.caption(f"Showing {min(col_limit, len(view_df))} of {len(view_df):,} matching rows")
        st.dataframe(view_df.head(col_limit), use_container_width=True)

        # Export Button
        export_buf = io.StringIO()
        view_df.to_csv(export_buf, index=False)
        st.download_button(
            label="Export Current Dataset as CSV",
            data=export_buf.getvalue(),
            file_name=f"cleaned_{st.session_state.file_name}",
            mime="text/csv"
        )

    # ========================================================
    # TAB 6: Executive Report Generator
    # ========================================================
    with tab_report:
        st.subheader("Executive HTML Report Generator")
        st.caption("Generate a standalone, executive-ready HTML briefing document with 1 click. Zero external dependencies, print-friendly, and beautifully styled.")

        col_rep1, col_rep2 = st.columns([2, 1])
        with col_rep1:
            st.markdown(f"""
            - **Target Dataset:** `{st.session_state.file_name}`
            - **Calculated Health Score:** `{health_score}/100` ({health_grade})
            - **Anomalies Included:** `{'Yes' if st.session_state.anomaly_result else 'Run Anomaly Scan in Tab 3 to include'}`
            - **Format:** Standalone HTML (Works offline in any browser, emailable, printable to PDF)
            """)

        # Generate HTML Report
        report_html = ExecutiveReporter.generate_html_report(
            file_name=st.session_state.file_name,
            profile=profile,
            df=df,
            anomaly_result=st.session_state.anomaly_result
        )

        with col_rep2:
            st.download_button(
                label="Download Executive HTML Report",
                data=report_html,
                file_name=f"Executive_Report_{os.path.splitext(st.session_state.file_name)[0]}.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )

        st.markdown("---")
        st.write("#### Executive Briefing Live Preview")
        st.components.v1.html(report_html, height=650, scrolling=True)
