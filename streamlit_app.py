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


def series_to_dict(data, category_name, value_name):
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