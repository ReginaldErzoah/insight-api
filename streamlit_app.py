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
