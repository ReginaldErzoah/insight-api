from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sales.csv"

REQUIRED_COLUMNS = ["date","product","region","units_sold","revenue"]

def load_raw_data():
    """Load raw sales data from the CSV file."""
    return pd.read_csv(RAW_DATA_PATH)



def process_sales_data(sales):
    """"Process raw data."""
    sales = sales.copy()

    sales["date"] = pd.to_datetime(sales["date"], format = "%d-%m-%Y")

    return sales
