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


    
def test_sales_by_product_returns_expected_structure():
    response = client.get("/sales/by-product")

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {
        "revenue_by_product",
        "units_by_product",
    }

    assert isinstance(data["revenue_by_product"], dict)
    assert isinstance(data["units_by_product"], dict)


def test_sales_by_region_returns_expected_structure():
    response = client.get("/sales/by-region")

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {
        "revenue_by_region",
        "units_by_region",
    }

    assert isinstance(data["revenue_by_region"], dict)
    assert isinstance(data["units_by_region"], dict)


def test_sales_by_month_returns_expected_structure():
    response = client.get("/sales/by-month")

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {
        "revenue_by_month",
        "units_by_month",
    }

    assert isinstance(data["revenue_by_month"], dict)
    assert isinstance(data["units_by_month"], dict)


def test_top_product_returns_expected_structure():
    response = client.get("/sales/top-product")

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {"top_product"}
    assert isinstance(data["top_product"], str)