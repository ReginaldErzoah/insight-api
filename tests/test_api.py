from fastapi.testclient import TestClient

from insight_api.main import app

client = TestClient(app)

def test_sales_summary_returns_success():
    response = client.get("/sales/summary")

    assert response.status_code == 200


def test_sales_summary_comtains_expected_metrics():
    response = client.get("/sales/summary")

    data = response.json()

    expected_keys = {
        "total_revenue",
        "total_units_sold",
        "average_revenue_per_record",
        "average_revenue_per_unit"
    }

    assert set(data.keys()) == expected_keys


def test_sales_summary_returns_numeric_values():
    response = client.get("/sales/summary")

    data = response.json()

    assert isinstance(data["total_revenue"], (int, float))
    assert isinstance(data["total_units_sold"], (int, float))
    assert isinstance(data["average_revenue_per_record"], (int, float))
    assert isinstance(data["average_revenue_per_unit"], (int, float))