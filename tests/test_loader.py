import pandas as pd

from pathlib import Path

from unittest.mock import patch

import pytest

from insight_api.data_access.loader import load_processed_data

def test_load_processed_data():
    sales = load_processed_data()

    assert isinstance(sales,pd.DataFrame)


def test_load_processed_data_raises_error_when_file_is_missing():
    with patch.object(Path, "exists", return_value=False):
        with pytest.raises(
            FileNotFoundError,
            match="Processed sales data not found",
        ):
            load_processed_data()