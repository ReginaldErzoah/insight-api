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