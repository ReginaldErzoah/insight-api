import pandas as pd

from insight_api.data_access.loader import load_processed_data

def test_load_processed_data():
    sales = load_processed_data()

    assert isinstance(sales,pd.DataFrame)

    