# YC Analytics Dashboard

A Streamlit-based dashboard for exploring and visualizing Y Combinator company data. The dashboard fetches the latest data directly from the official YC OSS API and provides interactive charts, filtering, and analytics for data analysts, internal teams, and external stakeholders.

## Features
- Fetches live YC company data from https://yc-oss.github.io/api/companies/all.json
- Supports CSV upload for custom datasets
- Cleans and normalizes data for analysis
- Loads data into DuckDB for fast SQL analytics
- Interactive table preview and Plotly charts (e.g., company count by batch)

## Local Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/algorhythmic/yc_analytics.git
cd yc_analytics
```

### 2. Create and activate a virtual environment (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

### 3. Install dependencies with UV
```powershell
uv pip install -r pyproject.toml
```

### 4. Run the Streamlit dashboard
```powershell
streamlit run dashboard.py
```

### 5. Using the Dashboard
- By default, the dashboard fetches the latest YC company data from the public API.
- You can also upload your own CSV file for custom exploration.

## Project Structure
- `dashboard.py` — Streamlit app entrypoint
- `data_ingestion.py` — Fetches JSON, saves as CSV, and loads into DuckDB
- `data_transform.py` — Cleans and normalizes data
- `visualization.py` — Chart rendering (Plotly)
- `config.py` — Configuration constants
- `pyproject.toml` — Dependency management (UV/PEP 621)
- `docs/` — PRD, specs, and API documentation

## Requirements
- Python 3.8+
- [UV](https://github.com/astral-sh/uv) (for fast dependency management)
- Streamlit, pandas, plotly, requests, duckdb (auto-installed)

---

For more details on the architecture and features, see `spec.md` and `docs/prd.md`.
