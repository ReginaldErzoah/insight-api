import os

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

API_BASE_URL = API_BASE_URL.rstrip("/")
REQUEST_TIMEOUT = 10


st.set_page_config(
    page_title = "InsightAPI Sales Dashboard",
    layout = "wide",
    initial_sidebar_state = "expanded",
)


def get_api_data(endpoint):
    """Fetch JSON data from a FastAPI endpoint"""

    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        return response.json(), None
    
    except requests.RequestException as error:
        return None, str(error)

    except ValueError as error:
        return None, f"Invalaid JSON reponse: {error}"


def check_api_health():
    """Check whether backend is responding."""

    data,error = get_api_data("/health")

    if error:
        return False, error

    if not isinstance(data, dict):
        return False, "The API returned an unexpected health response."

    if data.get("status") != "healthy":
        return False, "The API health check did not report healthy status."

    return True, None


def series_to_dataframe(data, category_name, value_name):
    """Convert an API dictionary into a chart-ready DataFrame."""

    if not isinstance(data,dict) or not data:
        return pd.DataFrame(
            columns = [category_name, value_name]
        )

    frame = pd.DataFrame(
        list(data.items()),
        columns = [category_name, value_name],
    )

    frame[value_name] = pd.to_numeric(
        frame[value_name],
        errors = "coerce"
    )

    frame = frame.dropna(subset=[value_name])

    return frame.sort_values(
        value_name,
        ascending=False,
    ).reset_index(drop=True)


def show_metric(label, value, help_text = None):
    """Dispaly a consistently formatted KPI."""

    st.metric(
        label = label,
        value = value,
        help = help_text,
    )


with st.sidebar:
    st.title("insightAPI")
    st.caption("Sales Analytics Platform")

    st.divider()

    st.subheader("Backend Status")

    api_is_healthy, health_error = check_api_health()

    if api_is_healthy:
        st.success("API is connected")
    else:
        st.error("API unavailable")
        st.caption(
            "Start FastAPI and refresh this page to reconnect."
        )

        with st.expander("Connection details"):
            st.code(health_error or "Unknown connection error")

    st.divider()

    refresh_clicked = st.button(
        "Refresh dashboard",
        use_container_width = True,
    )

    if refresh_clicked:
        st.rerun()


st.title("Sales Performance Analytics")


st.markdown(
    """
    Explore revenue, sales volume, product performance, regional performance, and 
    monthly trends using data supplied by the InsightAPI backend.
    """
)

st.caption("Data Source: FastAPI sales analytics endpoints")


if not api_is_healthy:
    st.error(
        "The dashboard cannot retrieve live data because"
        "the backend health check failed."
    )

    st.info(
        "In another terminal, start the API with:"
        "`uv run uvicorn insight_api.main:app --reload"
    )

    st.stop()


summary, summary_error = get_api_data("/sales/summary")

products, products_error = get_api_data("/sales/by-product")

regions, regions_error = get_api_data("/sales/by-region")

monthly, monthly_error = get_api_data("/sales/by-month")

top_product_data, top_product_error = get_api_data("/sales/top-product")


endpoint_errors = {
    "Sales summary": summary_error,
    "Product analysis": products_error,
    "Regional analysis": regions_error,
    "Monthly analysis": monthly_error,
    "Top product": top_product_error,
}

for endpoint_name, error in endpoint_errors.items():
    if error:
        st.warning(
            f"{endpoint_name} could not be loaded: {error}"
        )


if summary is not None and not isinstance(summary,dict):
    st.warning("The summary endpoint returned an unexpected response.")
    summary = None

if products is not None and not isinstance(products,dict):
    st.warning("The products endpoint returned an unexpected response.")
    products = None

if regions is not None and not isinstance(regions,dict):
    st.warning("The regions endpoint returned an unexpected response.")
    regions = None

if monthly is not None and not isinstance(monthly,dict):
    st.warning("The monthly endpoint returned an unexpected response.")
    monthly = None

if top_product_data is not None and not isinstance(top_product_data,dict):
    st.warning("The top product endpoint returned an unexpected response.")
    top_product_data = None

if (summary is None and products is None and regions is None and monthly is None):
    st.error(
        "No sales data could be loaded. Check the API logs"
        "and try refreshing the dashboard."
    )
    st.stop()


revenue_by_product = pd.DataFrame(
    columns=["Product", "Revenue"]
)

units_by_product = pd.DataFrame(
    columns=["Product", "Units Sold"]
)

revenue_by_region = pd.DataFrame(
    columns=["Region", "Revenue"]
)

units_by_region = pd.DataFrame(
    columns=["Region", "Units Sold"]
)

revenue_by_month = pd.DataFrame(
    columns=["Month", "Revenue"]
)

units_by_month = pd.DataFrame(
    columns=["Month", "Units Sold"]
)


if products is not None:
    revenue_by_product = series_to_dataframe(
        products.get("revenue_by_product", {}),
        "Product",
        "Revenue",
    )

    units_by_product = series_to_dataframe(
        products.get("units_by_product", {}),
        "Product",
        "Units Sold",
    )


if regions is not None:
    revenue_by_region = series_to_dataframe(
        regions.get("revenue_by_region", {}),
        "Region",
        "Revenue",
    )

    units_by_region = series_to_dataframe(
        regions.get("units_by_region", {}),
        "Region",
        "Units Sold",
    )


if monthly is not None:
    revenue_by_month = series_to_dataframe(
        monthly.get("revenue_by_month", {}),
        "Month",
        "Revenue",
    )

    units_by_month = series_to_dataframe(
        monthly.get("units_by_month", {}),
        "Month",
        "Units Sold",
    )

    revenue_by_month = revenue_by_month.sort_values("Month")
    units_by_month = units_by_month.sort_values("Month")


st.subheader("Business Overview")

if summary is not None:
    metric_columns = st.columns(4)

    