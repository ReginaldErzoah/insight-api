import pandas as pd

from insight_api.processing import (
    load_raw_data,
    validate_columns,
    validate_numeric_columns,
    validate_missing_values,
    process_sales_data,
    save_processed_data,
    run_processing_pipeline
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


def test_save_processed_data():
    sales = load_raw_data()
    processed_sales =  process_sales_data(sales)

    processed_path = save_processed_data(processed_sales)

    assert processed_path.exists()


def test_run_processing_pipeline():
    processed_path = run_processing_pipeline()

    assert processed_path.exists()