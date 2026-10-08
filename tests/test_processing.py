import pandas as pd

from insight_api.processing import (load_raw_data, validate_columns, validate_numeric_columns, validate_missing_values, process_sales_data)


def test_load_raw_data():
    sales = load_raw_data()

    assert isinstance(sales, pd.DataFrame)


def test_validate_columns():

    sales = validate_columns()



def test_validate_numeric_columns():
    sales = validate_numeric_columns()

    assert isinstance(sales,pd.DataFrame)


def test_validate_missing_values():
    sales = validate_missing_values()

    assert isinstance(sales,pd.DataFrame)


def test_process_sales_data():
    sales = process_sales_data()

    assert isinstance(sales,pd.DataFrame)
