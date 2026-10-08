from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sales.csv"


def load_raw_data():
    """Load raw sales data from the CSV file."""
    return pd.read_csv(RAW_DATA_PATH)