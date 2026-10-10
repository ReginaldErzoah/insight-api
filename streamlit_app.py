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