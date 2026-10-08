from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sales.csv"

REQUIRED_COLUMNS = ["date","product","region","units_sold","revenue"]

NUMERIC_COLUMNS = ["units_sold","revenue"]

def load_raw_data():
    """Load raw sales data from the CSV file."""
    return pd.read_csv(RAW_DATA_PATH)


def validate_columns(sales):
    """Validate all required columns. """
    missing_columns =[
        column for column in REQUIRED_COLUMNS
        if column not in sales.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def validate_numeric_columns(sales):
    for column in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(sales[column]):
            raise ValueError(
                f"Column {column} must contain numeric data."
            )

def process_sales_data(sales):
    """Process raw data."""
    sales = sales.copy()

    sales["date"] = pd.to_datetime(sales["date"], format = "%d-%m-%Y")

    return sales
