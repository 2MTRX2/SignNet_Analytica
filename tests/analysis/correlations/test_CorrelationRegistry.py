# test_CorrelationRegistry.py
import pytest
from typing import Type

from signnet.analysis.correlations.CorrelationRegistry import CorrelationRegistry
from signnet.analysis.correlations.correlation_measures.CorrelationStrategy import CorrelationStrategy
from signnet.analysis.correlations.correlation_measures.KendallStrategy import KendallStrategy
from signnet.analysis.correlations.correlation_measures.PearsonStrategy import PearsonStrategy
from signnet.analysis.correlations.correlation_measures.SpearmanStrategy import SpearmanStrategy

# =====================================================================
# 1. REGISTRY TESTS
# =====================================================================

def test_get_available_names():
    # ACT
    names = CorrelationRegistry.get_available_names()

    # ASSERT
    expected_names = [
        "Spearman Rank Correlation (Recommended)",
        "Pearson Linear Correlation",
        "Kendall Tau Correlation"
    ]
    assert names == expected_names
    assert len(names) == 3


@pytest.mark.parametrize("name, expected_class", [
    ("Spearman Rank Correlation (Recommended)", SpearmanStrategy),
    ("Pearson Linear Correlation", PearsonStrategy),
    ("Kendall Tau Correlation", KendallStrategy)
])
def test_get_measure_class_success(name, expected_class):
    # ACT
    strategy_class = CorrelationRegistry.get_measure_class(name)

    # ASSERT
    assert strategy_class is expected_class
    
    assert isinstance(strategy_class, type)
    
    instance = strategy_class()
    assert isinstance(instance, CorrelationStrategy)


def test_get_measure_class_raises_value_error():
    unknown_name = "Unknown Fancy Correlation"

    # ACT & ASSERT
    with pytest.raises(ValueError) as exc_info:
        CorrelationRegistry.get_measure_class(unknown_name)
    
    assert str(exc_info.value) == f"Centrality measure '{unknown_name}' is not registered."
