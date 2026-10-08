# ⚡ InsightAI — Intelligent Data Analyst & Automated Profiler

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Core Principle:** The LLM plans and explains; Python executes deterministic calculations. Zero hallucinations on verified data.

---

## 🌟 Overview
**InsightAI** is an AI-powered data analysis platform that transforms raw tabular datasets (CSV) into verified insights. Users can upload any CSV, inspect automated profiling metrics, run natural language analysis plans, discover anomalies with Isolation Forest, and download executive HTML reports.

---

## 🏗️ Architecture
```
User (Streamlit UI)
      │
      ▼
CSV Validation & Ingestion (Size & Format Check, Encoding / Delimiter Safety)
      │
      ▼
Automated Data Profiler (Missing Values, Dtypes, Stats, Correlations)
      │
      ▼
Natural Language Query Router
      │
      ▼
Structured LLM Planner (Strict JSON Schema)
      │
      ▼
Plan Validator (Allow-list Check & Column Safety — No Arbitrary Code Execution)
      │
      ▼
Deterministic Pandas Executor
      │
      ├───────────────────────┬───────────────────────┐
      ▼                       ▼                       ▼
Interactive Plotly Charts  Grounded LLM Explanations  Isolation Forest ML Anomalies
      └───────────────────────┬───────────────────────┘
                              ▼
                 Downloadable Executive HTML Report
```

---

## 🚀 Features (Day 1)
- **Robust CSV Validation Engine:**
  - Automatic delimiter detection (`,`, `;`, `\t`, `|`).
  - Encoding detection (`utf-8`, `latin1`, etc.).
  - File size protection (up to 50MB) and malformed record handling.
- **Deep Tabular Profiler:**
  - Full dataset metadata: shape, memory footprint, duplicate rows, missing values.
  - Column-by-column semantic typing (numeric, categorical, datetime, boolean).
  - Descriptive statistics (mean, median, standard deviation, percentiles, min/max).
  - Pearson correlation matrix heatmap for numeric features.
- **Interactive Modern Streamlit UI:**
  - Premium glassmorphic interface with reactive metrics.
  - Interactive distribution histograms, box plots, and bar charts.
  - Built-in data hygiene utilities (deduplication & missing value imputation).
  - Preloaded demo sales analytics dataset (`data/sample_sales.csv`).

---

## 📂 Project Structure
```text
InsightAI/
├── app.py                  # Streamlit web application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Ignored files & secrets
├── README.md               # Project documentation
├── data/
│   ├── sample.csv          # Standard sample dataset
│   └── sample_sales.csv    # 100-row demo sales dataset with outliers & missing values
├── src/
│   ├── __init__.py
│   ├── validator.py        # CSV integrity, encoding, and size validation
│   ├── profiler.py         # Automated data profiling engine
│   └── cleaner.py          # Deduplication & missing value imputation
└── tests/
    └── test_day1.py        # Unit test suite for validation and profiler
```

---

## 🛠️ Local Quickstart

### 1. Clone & Set Up
```bash
git clone https://github.com/nithin16-cloud/InsightAI.git
cd InsightAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Tests
```bash
python -m pytest tests/test_day1.py
```

### 4. Launch Application
```bash
python -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📅 6-Day Development Roadmap
- [x] **Day 1: Project Setup, CSV Ingestion, Profiler & Streamlit Interface**
- [ ] **Day 2: Deterministic Pandas Analysis Engine & Plotly Visualizer**
- [ ] **Day 3: LLM Planning Layer, JSON Schema Validation & Explanations**
- [ ] **Day 4: Isolation Forest Machine Learning Anomaly Detection**
- [ ] **Day 5: Downloadable Executive HTML Reports & Security Hardening**
- [ ] **Day 6: Cloud Deployment, End-to-End Testing & Portfolio Assets**
