# test_CentralityRegistry.py
import pytest
from typing import Type

from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry
from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.analysis.centrality.centrality_measures.SignedDegreeCentrality import SignedDegreeCentrality
from signnet.analysis.centrality.centrality_measures.PnCentrality import PnCentrality

# =====================================================================
# 1. TEST FOR AVAILABLE NAMES
# =====================================================================

def test_get_available_names():
    # ACT
    names = CentralityRegistry.get_available_names()

    # ASSERT
    assert isinstance(names, list)
    assert len(names) == 6
    assert "Signed Degree" in names
    assert "PN Centrality" in names
    assert "PII Centrality" in names
    assert "KB Centrality (Ballester)" in names
    assert "KB Centrality (Bloch)" in names
    assert "KB Centrality (Sadler)" in names

# =====================================================================
# 2. TESTS FOR GET MEASURE CLASS
# =====================================================================

def test_get_measure_class_success():
    # ARRANGE
    test_name = "Signed Degree"

    # ACT
    measure_class = CentralityRegistry.get_measure_class(test_name)

    # ASSERT
    assert isinstance(measure_class, type)  # it is a type not an instantiated class
    assert measure_class is SignedDegreeCentrality
    
    # assure that the class inherits from its base class
    assert issubclass(measure_class, CentralityMeasure)

@pytest.mark.parametrize("name, expected_class", [
    ("Signed Degree", SignedDegreeCentrality),
    ("PN Centrality", PnCentrality),
])
def test_get_measure_class_multiple_mappings(name, expected_class):
    # ACT & ASSERT
    assert CentralityRegistry.get_measure_class(name) is expected_class


def test_get_measure_class_raises_value_error_for_unknown_name():
    # ARRANGE
    unknown_name = "Non Existent Centrality"

    # ACT & ASSERT
    expected_msg = f"Centrality measure '{unknown_name}' is not registered."
    
    with pytest.raises(ValueError, match=expected_msg):
        CentralityRegistry.get_measure_class(unknown_name)
