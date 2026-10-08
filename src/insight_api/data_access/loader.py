from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]

PROCESSED_DATA_PATH = PROJECT_ROOT/"data"/"processed"/"sales.parquet"

def load_processed_data():
    """Load processed sales data from Parquet file."""
    return pd.read_parquet(PROCESSED_DATA_PATH)