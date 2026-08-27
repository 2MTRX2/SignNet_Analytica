# test_CorrelationStrategy.py
import pytest
from typing import Any
import pandas as pd

from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy

# =====================================================================
# 1. ABSTRACT BASE CLASS TESTS (The Contract)
# =====================================================================

def test_cannot_instantiate_abstract_base_class():
    # ARRANGE, ACT & ASSERT
    # Check if python blocks the intantiation of an abstract base class
    with pytest.raises(TypeError, match="Can't instantiate abstract class CorrelationStrategy"):
        CorrelationStrategy()

def test_subclass_must_implement_abstract_methods():
    # ARRANGE
    # Building an inheriting class which implements no compute
    class IncompleteCorrelationStrategy(CorrelationStrategy):
        pass

    # ACT & ASSERT
    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteCorrelationStrategy without an implementation for abstract method 'calculate'"):
        IncompleteCorrelationStrategy()


def test_successful_subclass_instantiation():
    # ARRANGE
    # A correct implementation of an inheriting class
    class DummyMeasure(CorrelationStrategy):      
        def calculate(self, x: pd.Series, y: pd.Series) -> tuple[float, float]:
            return (1.0, 0.05)

    # ACT
    instance = DummyMeasure()

    series_x = pd.Series([1, 2, 3])
    series_y = pd.Series([2, 4, 6])

    result = instance.calculate(series_x, series_y)

    # ASSERT
    assert result == (1.0, 0.05)