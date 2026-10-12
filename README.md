# InsightAI

**Intelligent Tabular Data Analytics Platform**

InsightAI is a production-ready analytics tool that transforms raw CSV files into structured insights without hallucination or black-box guesswork. Every result is produced through deterministic Python execution — no LLM-generated conclusions, no random outputs.

---

## What it Does

- **Automated Data Profiling** — Column-level statistics, missing value rates, cardinality, type inference, and a composite health score in seconds
- **Data Hygiene** — Safe, non-destructive deduplication and imputation; original data is always preserved
- **Natural Language Query Interface** — Ask questions in plain English ("What is the total revenue by region?") and get exact, auditable answers
- **ML Anomaly Detection** — Isolation Forest detects genuine multivariate outliers with per-record explanations
- **Executive HTML Reports** — Download standalone, print-quality HTML reports with full profiling and anomaly summaries

---

## Technology Stack

| Layer | Technology |
|---|---|
| Interface | Streamlit 1.36+ |
| Data | pandas 2.2+ / NumPy 1.26+ |
| Machine Learning | scikit-learn 1.4+ (Isolation Forest) |
| Visualisation | Plotly 5.22+ |
| LLM (optional) | OpenAI API (GPT-4o) for enhanced query planning |
| Fonts | Plus Jakarta Sans, JetBrains Mono via Google Fonts |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/InsightAI.git
cd InsightAI

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables (Optional)

OpenAI integration is entirely optional. The platform runs fully offline without it.

```bash
# Copy the example file
cp .env.example .env

# Then edit .env and paste your key:
# OPENAI_API_KEY=sk-...
```

### Run Locally

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Deployment

### Streamlit Community Cloud (Recommended)

1. Push this repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set the main file to `app.py`
4. Add `OPENAI_API_KEY` to Secrets (optional)

### Render / Heroku

A `Procfile` is included. Connect your repo, set the build command to `pip install -r requirements.txt`, and deploy.

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.headless=true", "--server.address=0.0.0.0"]
```

---

## Project Structure

```
InsightAI/
├── .env.example                # Environment variables template
├── .gitignore                  # Git exclusions
├── .streamlit/
│   └── config.toml             # Streamlit server and theme config
├── Procfile                    # Cloud deployment entry point
├── README.md                   # This file
├── requirements.txt            # Production dependencies
├── setup.cfg                   # Package metadata and test settings
├── app.py                      # Main application entry point
├── data/
│   └── sample_sales.csv        # Demo dataset for testing
├── src/
│   ├── __init__.py             # Package exports
│   ├── validator.py            # CSV integrity and security checks
│   ├── profiler.py             # Automated data profiling engine
│   ├── cleaner.py              # Deduplication and missing value imputation
│   ├── executor.py             # Deterministic pandas query engine
│   ├── planner.py              # Natural language to query router
│   ├── anomalies.py            # Isolation Forest anomaly detection
│   └── reporter.py             # Executive HTML report generator
└── tests/
    ├── test_day1.py            # Validation and profiling unit tests
    └── test_full_suite.py      # End-to-end integration test suite
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

All tests are deterministic and run offline.

---

## Design Principles

- **Zero Hallucinations** — Every number shown is computed directly from your data using pandas. No LLM is asked to guess or summarise results.
- **Non-destructive** — The original uploaded file is never modified. Cleaning steps operate on a copy.
- **Audit-ready** — The query engine logs its exact execution steps, making results fully reproducible.
- **Privacy-first** — Files are held in memory for the session duration only and never written to disk by default.

---

## License

MIT License. See `LICENSE` for details.
