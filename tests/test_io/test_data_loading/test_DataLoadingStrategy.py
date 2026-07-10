# test_DataLoadingStrategy.py
import pytest
from signnet.io.data_loading.DataLoadingStrategy import DataLoadingStrategy


class TestDataLoadingStrategy:
    """Ensures that interfaces cannot be instantiated directly."""
 
    def test_data_loading_strategy_cannot_be_instantiated(self):
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            DataLoadingStrategy()  # type: ignore
 
    def test_subclass_without_implementation_cannot_be_instantiated(self):
        class IncompleteStrategy(DataLoadingStrategy):
            pass
 
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteStrategy()
