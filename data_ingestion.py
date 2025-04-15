"""
data_ingestion.py
Handles downloading and loading YC company data from CSV files.
Integrates with DuckDB for storage and querying.
"""
import pandas as pd
import duckdb

def fetch_csv(url: str, dest_path: str):
    """Download CSV from URL and save to dest_path."""
    # TODO: Implement download logic
    pass

def load_csv(path: str) -> pd.DataFrame:
    """Read CSV into DataFrame, handle missing values."""
    # TODO: Implement CSV loading logic
    pass

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
