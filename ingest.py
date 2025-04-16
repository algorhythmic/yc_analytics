"""
ingest.py
Handles downloading and loading YC company data from the YC OSS JSON API.
Integrates with DuckDB for storage and querying.
"""
import pandas as pd
import duckdb
import requests
import os
from config import DB_PATH
import re

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

def batch_to_year(batch):
    match = re.match(r"[SWF](\d{2})", str(batch))
    if match:
        yy = int(match.group(1))
        return 2000 + yy if yy < 100 else None
    return None

def load_csv_to_duckdb(csv_path: str, db_path: str = DB_PATH, table_name: str = 'yc_companies') -> duckdb.DuckDBPyConnection:
    """
    Load CSV into DuckDB, add batch_year column, and return the connection.
    Ensures batch_year is stored as an integer (nullable Int64).
    """
    df = pd.read_csv(csv_path)
    batch_col = None
    for col in df.columns:
        if col.lower() == 'batch':
            batch_col = col
            break
    if batch_col:
        df['batch_year'] = df[batch_col].apply(batch_to_year).astype('Int64')
    else:
        df['batch_year'] = pd.NA
    con = duckdb.connect(database=db_path)
    con.register('df', df)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
    return con
