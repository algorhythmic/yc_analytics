"""
dashboard.py
Streamlit app entrypoint for YC Analytics Dashboard.
"""
import streamlit as st
import pandas as pd
import os
from ingest import get_or_download_json_as_csv, load_csv_to_duckdb
from transform import clean_data
from config import DB_PATH
import visualization  # new import

# Config
DEFAULT_JSON_URL = "https://yc-oss.github.io/api/companies/all.json"
LOCAL_CSV_PATH = "./data/yc_companies.csv"
TABLE_NAME = "yc_companies"

def main():
    st.title("YC Analytics Dashboard")
    st.write("This dashboard sources all Y Combinator company data directly from the official API.")

    # Always use DuckDB for analytics, not direct CSV
    os.makedirs(os.path.dirname(LOCAL_CSV_PATH), exist_ok=True)
    csv_path = get_or_download_json_as_csv(DEFAULT_JSON_URL, LOCAL_CSV_PATH)
    con = load_csv_to_duckdb(csv_path=LOCAL_CSV_PATH, db_path=DB_PATH, table_name=TABLE_NAME)
    df = con.execute(f"SELECT * FROM {TABLE_NAME}").df()
    st.info("Loaded latest YC data from API.")

    # Clean data
    df = clean_data(df)

    # --- Dashboard Layout ---
    st.markdown("---")

    # batch_year is now persisted in the DuckDB table. Use it directly.
    batch_col = None
    for col in df.columns:
        if col.lower() == 'batch':
            batch_col = col
            break
    if 'batch_year' not in df.columns:
        st.error("batch_year column missing from database. Please re-ingest data.")
        return

    # Year range slider for X-axis span
    min_year = int(df['batch_year'].min())
    max_year = int(df['batch_year'].max())
    default_start = 2012 if min_year <= 2012 <= max_year else min_year
    default_end = 2024 if min_year <= 2024 <= max_year else max_year
    year_range = st.sidebar.slider('Select Year Range', min_year, max_year, (default_start, default_end), step=1)
    df_year = df[(df['batch_year'] >= year_range[0]) & (df['batch_year'] <= year_range[1])]

    # Top N Industries filter (applies to both charts)
    top_n = st.sidebar.slider('Top N Industries', 1, 8, 8)
    if 'industry' in df_year.columns:
        top_industries = df_year['industry'].value_counts().nlargest(top_n).index
        # Multi-select for individual industries
        selected_industries = st.sidebar.multiselect(
            'Select Industries',
            options=list(top_industries),
            default=list(top_industries)
        )
        df_filtered = df_year[df_year['industry'].isin(selected_industries)]
    else:
        df_filtered = df_year

    # Company size slider filter with '10+' upper bound (range 1-10+), exclude companies with team_size < 1
    if 'team_size' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['team_size'] >= 1]
        min_size = 1
        upper_bound = 10
        max_size = int(df_filtered['team_size'].max())
        size_options = list(range(min_size, upper_bound + 1))
        size_labels = [str(s) for s in size_options]
        if max_size > upper_bound:
            size_labels[-1] = '10+'
        size_idx_min = 0
        size_idx_max = len(size_labels) - 1
        # Use st.sidebar.select_slider to show correct labels instead of index-based slider
        size_range = st.sidebar.select_slider(
            'Select Company Size Range',
            options=size_labels,
            value=(size_labels[0], size_labels[-1])
        )
        selected_min = int(size_range[0])
        selected_max = max_size if size_range[1] == '10+' else int(size_range[1])
        df_filtered = df_filtered[(df_filtered['team_size'] >= selected_min) & (df_filtered['team_size'] <= selected_max)]

    # Industry Trends Over Time (full-width)
    if batch_col and 'industry' in df_filtered.columns and df_filtered['batch_year'].notnull().any():
        fig3 = visualization.industry_trends_over_time(df_filtered, top_n=top_n)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No valid industry info for industry trends chart.")
    else:
        st.warning("No valid batch/year or industry info for industry trends chart.")

    st.markdown("---")
    # Batch Over Time (full-width stacked histogram, overlay median team size)
    if batch_col and df_filtered['batch_year'].notnull().any():
        fig = visualization.batch_and_team_size_overlay(df_filtered, batch_col)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No 'batch' column found for chart.")

if __name__ == "__main__":
    main()
