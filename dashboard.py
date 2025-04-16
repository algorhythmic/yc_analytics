"""
dashboard.py
Streamlit app entrypoint for YC Analytics Dashboard.
"""
import streamlit as st
import pandas as pd
import os
from data_ingestion import get_or_download_json_as_csv, load_csv_to_duckdb
from data_transform import clean_data
import plotly.express as px
from config import DB_PATH

# Config
DEFAULT_JSON_URL = "https://yc-oss.github.io/api/companies/all.json"
LOCAL_CSV_PATH = "./data/yc_companies.csv"
TABLE_NAME = "yc_companies"

def main():
    st.title("YC Analytics Dashboard")
    st.write("Upload a Y Combinator companies CSV or use the latest from the API.")

    # File upload or use default (fetched from JSON API)
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Loaded uploaded CSV.")
    else:
        os.makedirs(os.path.dirname(LOCAL_CSV_PATH), exist_ok=True)
        csv_path = get_or_download_json_as_csv(DEFAULT_JSON_URL, LOCAL_CSV_PATH)
        df = pd.read_csv(csv_path)
        st.info("Loaded latest YC data from API.")

    # Clean data
    df = clean_data(df)

    # Load into DuckDB (persistent file)
    con = load_csv_to_duckdb(csv_path=LOCAL_CSV_PATH, db_path=DB_PATH, table_name=TABLE_NAME)

    # Show table preview
    st.subheader("Data Preview")
    st.dataframe(df.head(20))

    # Simple chart: Number of companies per batch (if 'batch' column exists)
    batch_col = None
    for col in df.columns:
        if col.lower() == 'batch':
            batch_col = col
            break
    if batch_col:
        batch_counts = df[batch_col].value_counts().reset_index()
        batch_counts.columns = ['Batch', 'Company Count']
        fig = px.bar(batch_counts, x='Batch', y='Company Count', title='Company Count by Batch')
        st.plotly_chart(fig)
    else:
        st.warning("No 'batch' column found for chart.")

if __name__ == "__main__":
    main()
