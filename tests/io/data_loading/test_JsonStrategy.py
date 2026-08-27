# test_JsonStrategy.py
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

from signnet.io.data_loading.JsonStrategy import JsonStrategy
from signnet.io.data_representation.RepresentationNormaliser import RepresentationNormaliser
from signnet.io.data_representation.NetworkData import NetworkData

# =====================================================================
# 1. FIXURE
# =====================================================================

@pytest.fixture
def mock_representation():
    return MagicMock(spec=RepresentationNormaliser)

@pytest.fixture
def json_strategy(mock_representation):
    return JsonStrategy(representation=mock_representation)

# =====================================================================
# 2. READING
# =====================================================================

def test_read_raw_loads_and_caches_dataframe(json_strategy):
    # ARRANGE
    fake_file = "dummy_network.xlsx"
    fake_df = pd.DataFrame({"source": [1, 2], "target": [3, 4]})

    with patch("pandas.read_json", return_value=fake_df) as mock_read_json:
        # 1. test reading
        result_1 = json_strategy.read_raw(fake_file)
        
        # 2. test caching
        result_2 = json_strategy.read_raw(fake_file)

        # ASSERT
        mock_read_json.assert_called_once_with(fake_file)  # invoked only once
        pd.testing.assert_frame_equal(result_1, fake_df)
        pd.testing.assert_frame_equal(result_2, fake_df)
        assert json_strategy._cached_df is fake_df

def test_load_delegates_to_representation_handler(json_strategy, mock_representation):
    # ARRANGE
    fake_file = "dummy_network.json"
    fake_df = pd.DataFrame({"raw_data": [10, 20]})
    mock_network_data = MagicMock(spec=NetworkData)

    mock_representation.to_network_data.return_value = mock_network_data

    with patch("pandas.read_json", return_value=fake_df):
        # ACT
        result = json_strategy.load(fake_file)

        # ASSERT
        mock_representation.to_network_data.assert_called_once_with(fake_df)
        
        assert result is mock_network_data

def test_is_subclass_of_data_loading_strategy(json_strategy):
    from signnet.io.data_loading.DataLoadingStrategy import DataLoadingStrategy
    assert isinstance(json_strategy, DataLoadingStrategy)
