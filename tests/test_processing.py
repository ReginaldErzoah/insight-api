import pandas as pd

from insight_api.processing import load_raw_data

from insight_api.processing import validate_columns

from insight_api.processing import validate_numeric_columns

from insight_api.processing import validate_missing_values

from insight_api.processing import process_sales_data


def test_load_raw_data():
    sales = load_raw_data()

    assert isinstance(sales, pd.DatFrame)


def test_validate_columns():
    sales = validate_columns()

    assert isinstance(sales,pd.DataFrame)


