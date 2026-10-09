
import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="InsightAPI Dashboard",
    layout="wide",
)


st.title("InsightAPI Sales Dashboard")
st.write("Monitor sales performance and explore key business metrics.")


def get_api_data(endpoint):
    """Fetch JSON data from the FastAPI backend."""
    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(
            "Unable to retrieve data from the API. "
            "Make sure the FastAPI server is running."
        )
        st.caption(f"Technical details: {error}")
        return None


summary = get_api_data("/sales/summary")


if summary is not None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"{summary['total_revenue']:,.2f}",
    )

    col2.metric(
        "Units Sold",
        f"{summary['total_units_sold']:,}",
    )

    col3.metric(
        "Average Revenue per Record",
        f"{summary['average_revenue_per_record']:,.2f}",
    )

    col4.metric(
        "Average Revenue per Unit",
        f"{summary['average_revenue_per_unit']:,.2f}",
    )