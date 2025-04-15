"""
data_transform.py
Cleans and transforms YC company data.
"""
import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize columns, handle types, filter invalid rows."""
    # TODO: Implement cleaning logic
    pass

def maybe_persist(df: pd.DataFrame, db_path: str = None):
    """Optionally save to SQLite for historical analysis."""
    # TODO: Implement persistence logic
    pass
