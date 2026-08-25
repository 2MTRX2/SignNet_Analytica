# test_DataLoadingStrategy.py
import pytest
import pandas as pd
from unittest.mock import MagicMock

from signnet.io.data_loading.DataLoadingStrategy import DataLoadingStrategy
from signnet.io.data_representation.NetworkData import NetworkData

# =====================================================================
# 1. ABSTRACT BASE CLASS TESTS (The Contract)
# =====================================================================

def test_cannot_instantiate_abstract_base_class():
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        DataLoadingStrategy() 
 
def test_subclass_must_implement_abstract_methods():
    class IncompleteStrategy(DataLoadingStrategy):
        pass
 
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteStrategy()

def test_successful_subclass_instantiation():
    # ARRANGE
    class DummyLoader(DataLoadingStrategy):
        def read_raw(self, file_source) -> pd.DataFrame:
            return pd.DataFrame({"source": [1], "target": [2]})

        def load(self, file_source) -> NetworkData: 
            mock_network_data = MagicMock(spec=NetworkData)
            return mock_network_data
    # ACT
    instance = DummyLoader()
    raw_result = instance.read_raw("fake_path.csv")
    load_result = instance.load("fake_path.csv")

    # ASSERT
    assert isinstance(instance, DataLoadingStrategy)
    
    assert isinstance(raw_result, pd.DataFrame)
    assert isinstance(load_result, NetworkData)
