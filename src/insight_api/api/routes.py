
from fastapi import APIRouter

from insight_api.data_access.loader import load_processed_data
from insight_api.services.analysis import (
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
    units_by_month,
)

router = APIRouter()


def series_to_dict(series, value_type):
    """Convert a Pandas Series into a JSON-friendly dictionary."""
    return {
        str(key): value_type(value)
        for key, value in series.items()
    }


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/sales/summary")
def get_sales_summary():
    sales = load_processed_data()

    return {
        "total_revenue": float(total_revenue(sales)),
        "total_units_sold": int(total_units_sold(sales)),
        "average_revenue_per_record": float(
            average_revenue_per_record(sales)
        ),
        "average_revenue_per_unit": float(
            average_revenue_per_unit(sales)
        ),
    }


@router.get("/sales/by-product")
def get_sales_by_product():
    sales = load_processed_data()

    return {
        "revenue_by_product": series_to_dict(
            revenue_by_product(sales), float
        ),
        "units_by_product": series_to_dict(
            units_by_product(sales), int
        ),
    }


@router.get("/sales/by-region")
def get_sales_by_region():
    sales = load_processed_data()

    return {
        "revenue_by_region": series_to_dict(
            revenue_by_region(sales), float
        ),
        "units_by_region": series_to_dict(
            units_by_region(sales), int
        ),
    }


@router.get("/sales/by-month")
def get_sales_by_month():
    sales = load_processed_data()

    return {
        "revenue_by_month": series_to_dict(
            revenue_by_month(sales), float
        ),
        "units_by_month": series_to_dict(
            units_by_month(sales), int
        ),
    }


@router.get("/sales/top-product")
def get_top_product():
    sales = load_processed_data()

    return {
        "top_product": str(top_product(sales))
    }