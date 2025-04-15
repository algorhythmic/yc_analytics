"""
data_transform.py
Cleans and transforms YC company data.
"""
import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Minimal cleaning: drop fully empty columns, strip whitespace from column names."""
    df = df.dropna(axis=1, how='all')
    df.columns = df.columns.str.strip()
    return df

def maybe_persist(df: pd.DataFrame, db_path: str = None, table_name: str = 'yc_companies'):
    """Optionally save to DuckDB if db_path is provided."""
    if db_path:
        import duckdb
        con = duckdb.connect(database=db_path)
        con.register('temp_df', df)
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM temp_df")
        con.close()
