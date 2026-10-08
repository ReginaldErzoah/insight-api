import pandas as pd
import pytest

from insight_api.processing import (
    load_raw_data,
    validate_columns,
    validate_numeric_columns,
    validate_missing_values,
    process_sales_data,
)


def test_load_raw_data():
    sales = load_raw_data()

    assert isinstance(sales, pd.DataFrame)


def test_validate_columns():
    sales = load_raw_data()

    validate_columns(sales)


def test_validate_numeric_columns():
    sales = load_raw_data()

    validate_numeric_columns(sales)


def test_validate_missing_values():
    sales = load_raw_data()

    validate_missing_values(sales)


def test_process_sales_data():
    sales = load_raw_data()

    processed_sales = process_sales_data(sales)

    assert isinstance(processed_sales, pd.DataFrame)
    assert "month_year" in processed_sales.columns
