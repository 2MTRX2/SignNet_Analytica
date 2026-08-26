# test_decorators.py
import pandas as pd
import pytest
from unittest.mock import MagicMock

from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.decorators import require_edges

# =====================================================================
# DECORATOR TESTS
# =====================================================================

@pytest.fixture
def empty_network():
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])
    return SignedNetwork(edges=empty_edges, nodes=["A", "B"])


@pytest.fixture
def valid_network():
    data = {
        "source": ["A"],
        "target": ["B"],
        "sign": [1]
    }
    return SignedNetwork(edges=pd.DataFrame(data=data))


# ---------------------------------------------------------------------
#  TEST 1: WITHOUT INSTANCES   
# ---------------------------------------------------------------------

def test_require_edges_allows_valid_network_as_positional_arg(valid_network):
    # ARRANGE 
    @require_edges
    def dummy_function(network: SignedNetwork):
        return "success"

    # ACT
    result = dummy_function(valid_network)

    # ASSERT 
    assert result == "success"


def test_require_edges_allows_valid_network_as_keyword_arg(valid_network):
    # ARRANGE
    @require_edges
    def dummy_function(network: SignedNetwork):
        return "success"

    # ACT 
    result = dummy_function(network=valid_network)

    # ASSERT
    assert result == "success"


def test_require_edges_blocks_empty_network_as_positional_arg(empty_network):
    # ARRANGE
    @require_edges
    def dummy_function(network: SignedNetwork):
        return "success"

    # ACT & ASSERT 
    with pytest.raises(ValueError, match="Execution blocked for 'dummy_function'"):
        dummy_function(empty_network)


def test_require_edges_blocks_empty_network_as_keyword_arg(empty_network):
    # ARRANGE
    @require_edges
    def dummy_function(network: SignedNetwork):
        return "success"

    # ACT & ASSERT
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        dummy_function(network=empty_network)


# ---------------------------------------------------------------------
# TEST 2: WITH CLASSES
# ---------------------------------------------------------------------

def test_require_edges_works_on_class_methods(valid_network, empty_network):
    # ARRANGE 
    class MockCentralityMeasure:
        @require_edges
        def compute(self, network: SignedNetwork):
            return "computed_successfully"

    measure = MockCentralityMeasure()

    # ACT & ASSERT 1:
    assert measure.compute(valid_network) == "computed_successfully"

    # ACT & ASSERT 2:
    with pytest.raises(ValueError, match="Execution blocked for 'compute'"):
        measure.compute(empty_network)


# ---------------------------------------------------------------------
# TEST 3: META-DATA
# ---------------------------------------------------------------------

def test_require_edges_preserves_function_metadata():
    # ARRANGE 
    @require_edges
    def analytical_calculation(network: SignedNetwork):
        """This is a very important docstring."""
        return "data"

    # ACT & ASSERT 
    assert analytical_calculation.__name__ == "analytical_calculation"
    assert analytical_calculation.__doc__ == "This is a very important docstring."
