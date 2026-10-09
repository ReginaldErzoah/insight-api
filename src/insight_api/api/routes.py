
from fastapi import APIRouter

from insight_api.data_access.loader import load_processed_data
from insight_api.services.analysis import (
    total_revenue,
    total_units_sold,
    average_revenue_per_record,
    average_revenue_per_unit,
)

router = APIRouter()


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