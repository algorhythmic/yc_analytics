"""
data_ingestion.py
Handles downloading and loading YC company data from the YC OSS JSON API.
Integrates with DuckDB for storage and querying.
"""
import pandas as pd
import duckdb
import requests
import os

def fetch_json(url: str) -> list:
    """Fetch JSON data from the given URL and return as a list of dicts."""
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def save_json_to_csv(json_data: list, dest_path: str):
    """Save a list of dicts (JSON) to a CSV file at dest_path."""
    df = pd.DataFrame(json_data)
    df.to_csv(dest_path, index=False)
    return dest_path

def get_or_download_json_as_csv(json_url: str, local_csv_path: str) -> str:
    """Fetch JSON from URL and save as CSV if not present locally."""
    if not os.path.exists(local_csv_path):
        data = fetch_json(json_url)
        save_json_to_csv(data, local_csv_path)
    return local_csv_path

def load_csv_to_duckdb(csv_path: str, db_path: str = ':memory:', table_name: str = 'yc_companies') -> duckdb.DuckDBPyConnection:
    """
    Load CSV into DuckDB and return the connection.
    Args:
        csv_path: Path to the CSV file.
        db_path: Path to DuckDB database (':memory:' for in-memory).
        table_name: Name of the table to create/replace.
    Returns:
        DuckDB connection with data loaded.
    """
    con = duckdb.connect(database=db_path)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}')")
    return con
