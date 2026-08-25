# test_RepresentationNormaliser.py
import pytest
import pandas as pd
from unittest.mock import MagicMock

from signnet.io.data_representation import RepresentationNormaliser
from signnet.io.data_representation.NetworkData import NetworkData

# =====================================================================
# 1. ABSTRACT BASE CLASS TESTS (The Contract)
# =====================================================================

def test_cannot_instantiate_abstract_base_class():
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        RepresentationNormaliser() 
 
def test_subclass_must_implement_abstract_methods():
    class IncompleteStrategy(RepresentationNormaliser):
        pass
 
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        IncompleteStrategy()

def test_successful_subclass_instantiation():
    # ARRANGE
    class DummyLoader(RepresentationNormaliser):
        def to_network_data(self, df: pd.DataFrame) -> NetworkData:
            mock_network_data = MagicMock(spec=NetworkData)
            return mock_network_data
    # ACT
    instance = DummyLoader()
    mock_df = MagicMock(spec=pd.DataFrame)
    result = instance.to_network_data(mock_df)

    # ASSERT
    assert isinstance(instance, RepresentationNormaliser)
    
    assert isinstance(result, pd.DataFrame)
