# test_MatrixFactory.py
import numpy as np
import pandas as pd
import pytest

from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.MatrixFactory import MatrixFactory

# =====================================================================
# MATRIX FACTORY TESTS
# =====================================================================

@pytest.fixture
def sample_undirected_network():
    data = {
        "source": ["A", "B"],
        "target": ["B", "C"],
        "sign": [1, -1]
    }
    edges_df = pd.DataFrame(data)
   
    return SignedNetwork(edges=edges_df, nodes=["A", "B", "C"], directed=False)


@pytest.fixture
def sample_directed_network():
    data = {
        "source": ["A", "B", "C"],
        "target": ["B", "A", "B"],
        "sign": [1, -1, 1]
    }
    edges_df = pd.DataFrame(data)

    return SignedNetwork(edges=edges_df, nodes=["A", "B", "C"], directed=True)


# ---------------------------------------------------------------------
# UNDIRECTED NETWORK TESTS
# ---------------------------------------------------------------------

def test_adjacency_matrix_undirected(sample_undirected_network):
    # ACT
    result = MatrixFactory.adjacency(sample_undirected_network)

    # ASSERT
    expected = np.array([
        [0.0,  1.0,  0.0],
        [1.0,  0.0, -1.0],
        [0.0, -1.0,  0.0]
    ])
    np.testing.assert_array_equal(result, expected)


def test_positive_matrix_undirected(sample_undirected_network):
    # ACT
    result = MatrixFactory.positive(sample_undirected_network)

    # ASSERT 
    expected = np.array([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ])
    np.testing.assert_array_equal(result, expected)


def test_negative_matrix_undirected(sample_undirected_network):
    # ACT
    result = MatrixFactory.negative(sample_undirected_network)

    # ASSERT
    expected = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0]
    ])
    np.testing.assert_array_equal(result, expected)


def test_tilde_matrix_undirected(sample_undirected_network):
    # ACT
    result = MatrixFactory.tilde(sample_undirected_network)

    # ASSERT - Ã = A⁺ − 2A⁻
    expected = np.array([
        [0.0,  1.0,  0.0],
        [1.0,  0.0, -2.0],
        [0.0, -2.0,  0.0]
    ])
    np.testing.assert_array_equal(result, expected)


# ---------------------------------------------------------------------
# DIRECTED NETWORKS TESTS
# ---------------------------------------------------------------------

def test_adjacency_matrix_directed(sample_directed_network):
    # ACT
    result = MatrixFactory.adjacency(sample_directed_network)

    # ASSERT 
    expected = np.array([
        [ 0.0, 1.0, 0.0],
        [-1.0, 0.0, 0.0],
        [ 0.0, 1.0, 0.0]
    ])
    np.testing.assert_array_equal(result, expected)


def test_tilde_matrix_directed(sample_directed_network):
    # ACT
    result = MatrixFactory.tilde(sample_directed_network)

    # ASSERT 
    expected = np.array([
        [ 0.0, 1.0, 0.0],
        [-2.0, 0.0, 0.0],
        [ 0.0, 1.0, 0.0]
    ])
    np.testing.assert_array_equal(result, expected)


# ---------------------------------------------------------------------
# EDGE-CASE HANDLING
# ---------------------------------------------------------------------

def test_build_matrix_ignores_zero_signs():
    # ARRANGE 
    data = {
        "source": ["A", "B"],
        "target": ["B", "C"],
        "sign": [1, 0] 
    }
    edges_df = pd.DataFrame(data)
    network = SignedNetwork(edges=edges_df, nodes=["A", "B", "C"], directed=False)

    # ACT
    result = MatrixFactory.adjacency(network)

    # ASSERT 
    expected = np.array([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ])
    np.testing.assert_array_equal(result, expected)
