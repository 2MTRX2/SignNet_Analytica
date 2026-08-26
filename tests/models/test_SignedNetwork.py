import pandas as pd
import pytest

from signnet.models.SignedNetwork import SignedNetwork

# =====================================================================
# INITIALISATION TESTS
# =====================================================================

def test_init_empty_edges_with_isolated_nodes(): 
    # ARRANGE
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])
    nodes = ["A", "B"]

    # ACT
    signed_network = SignedNetwork(edges=empty_edges, nodes=nodes)

    # ASSERT
    assert signed_network.edges.columns.tolist() == ['source', 'target', 'sign']
    assert signed_network.number_of_edges == 0
    assert signed_network.nodes == ("A", "B")


def test_init_many_columns(): 
    # ARRANGE
    data = {
        "weight": [1, 2, -3], 
        "sign": [1, 1, -1], 
        "source": ["A", "A", "B"],
        "target": ["B", "C", "C"]
    }
    edges = pd.DataFrame(data=data)

    # ACT
    signed_network = SignedNetwork(edges=edges)

    # ASSERT 
    assert signed_network.edges.columns.tolist() == ['source', 'target', 'sign']


def test_init_nodes(): 
    # ARRANGE
    data = {
        "weight": [1, 2, -3], 
        "sign": [1, 1, -1], 
        "source": ["A", "A", "B"],
        "target": ["B", "C", "C"]
    }
    edges = pd.DataFrame(data=data)

    # ACT
    signed_network = SignedNetwork(edges=edges)

    # ASSERT 
    assert signed_network.nodes == ("A", "B", "C")


# =====================================================================
# VALIDATION TESTS
# =====================================================================

def test_validate_missing_columns(): 
    # ARRANGE 
    data = {
        "weight": [1, 2, -3], 
        "sign": [1, 1, -1], 
        "source": ["A", "A", "B"],
    }
    edges = pd.DataFrame(data=data)

    # ACT & ASSERT
    with pytest.raises(ValueError, match="Missing required columns:.*target"):
        SignedNetwork(edges=edges)


def test_validate_empty_edges_and_no_nodes(): 
    # ARRANGE 
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])

    # ACT & ASSERT
    with pytest.raises(ValueError, match="Network contains no edges."):
        SignedNetwork(edges=empty_edges, nodes=None)


def test_validate_null_values_in_topology():
    # ARRANGE 
    data = {
        "source": ["A", "B"],
        "target": ["C", None],
        "sign": [1, -1]
    }
    edges = pd.DataFrame(data=data)

    # ACT & ASSERT
    with pytest.raises(ValueError, match="Source and target nodes must not be null."):
        SignedNetwork(edges=edges)


def test_validate_null_values_in_signs():
    # ARRANGE 
    data = {
        "source": ["A", "B"],
        "target": ["C", "A"],
        "sign": [1, None]
    }
    edges = pd.DataFrame(data=data)

    # ACT & ASSERT
    with pytest.raises(ValueError, match="Edge signs must not be null."):
        SignedNetwork(edges=edges)


# =====================================================================
# PROPERTY & MUTABILITY TESTS
# =====================================================================

def test_edges_returns_defensive_copy():
    # ARRANGE
    data = {
        "source": ["A"],
        "target": ["B"],
        "sign": [1]
    }
    signed_network = SignedNetwork(edges=pd.DataFrame(data=data))

    # ACT 
    leaked_edges = signed_network.edges
    leaked_edges.loc[0, "source"] = "MANIPULATED"

    # ASSERT
    assert signed_network.edges.loc[0, "source"] == "A"

def test_network_copy_creates_detached_instance():
    # ARRANGE
    data = {"source": ["A"], "target": ["B"], "sign": [1]}
    original_network = SignedNetwork(edges=pd.DataFrame(data=data))

    # ACT 
    copied_network = original_network.copy()

    # ASSERT 
    assert original_network is not copied_network
    
    assert original_network.nodes == copied_network.nodes
    pd.testing.assert_frame_equal(original_network.edges, copied_network.edges)