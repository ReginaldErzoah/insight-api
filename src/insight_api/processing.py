from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sales.csv"

PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "sales.parquet"

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
    """Validate numeric columns."""
    for column in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(sales[column]):
            raise ValueError(
                f"Column {column} must contain numeric data."
            )
        

def validate_missing_values(sales):
    """Validate that required sales fields contain no missing values."""
    missing_values = sales.isna().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        raise ValueError(
            f"Missing values found: \n{missing_values}" 
        )


def process_sales_data(sales):
    """Process raw data."""
    sales = sales.copy()

    sales["date"] = pd.to_datetime(sales["date"], format = "%d-%m-%Y")
    sales["month_year"] = sales["date"].dt.to_period("M")

    return sales
