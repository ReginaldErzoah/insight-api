import pandas as pd
import pytest

from insight_api.data_access.loader import load_processed_data

from insight_api.services.analysis import(
    total_revenue,
    total_units_sold,
    average_revenue_per_record,
    average_revenue_per_unit,
    revenue_by_product,
    units_by_product,
    top_product,
    revenue_by_region,
    units_by_region,
    revenue_by_month,
    units_by_month
)

@pytest.fixture
def sales():
    return load_processed_data()

def test_total_revenue(sales):
    result = total_revenue(sales)

    assert result is not None


def test_total_units_sold(sales):
    result = total_units_sold(sales)

    assert result is not None


def test_average_revenue_per_record(sales):
    result = average_revenue_per_record(sales)

    assert result is not None


def test_average_revenue_per_unit(sales):
    result = average_revenue_per_unit(sales)

    assert result is not None


def test_revenue_by_product(sales):
    result = revenue_by_product(sales)

    assert isinstance(result, pd.Series)


def test_units_by_product(sales):
    result = units_by_product(sales)

    assert isinstance(result, pd.Series)


def test_top_product(sales):
    result = top_product(sales)

    assert result is not None


def test_revenue_by_region(sales):
    result = revenue_by_region(sales)

    assert isinstance(result, pd.Series)


def test_units_by_region(sales):
    result = units_by_region(sales)

    assert isinstance(result, pd.Series)


def test_revenue_by_month(sales):
    result = revenue_by_month(sales)

    assert isinstance(result, pd.Series)


def test_units_by_month(sales):
    result = units_by_month(sales)

    assert isinstance(result, pd.Series)
