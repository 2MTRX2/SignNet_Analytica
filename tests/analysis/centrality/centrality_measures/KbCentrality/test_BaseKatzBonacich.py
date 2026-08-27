# test_BaseKatzBonacich
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
import pandas as pd

from signnet.analysis.centrality.centrality_measures.KbCentrality.BaseKatzBonacich import BaseKatzBonacich
from signnet.models.SignedNetwork import SignedNetwork

# =====================================================================
# 1. INITIALIZATION TESTS (__init__)
# =====================================================================

def test_init_with_valid_delta():
    # ARRANGE & ACT
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        kb = BaseKatzBonacich(delta=0.5)
    
    # ASSERT
    assert kb._custom_delta == 0.5


def test_init_with_invalid_delta_raises_value_error():
    # ARRANGE, ACT & ASSERT
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        with pytest.raises(ValueError, match="delta must be greater than zero."):
            BaseKatzBonacich(delta=0)
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        with pytest.raises(ValueError, match="delta must be greater than zero."):
            BaseKatzBonacich(delta=-1.5)


# =====================================================================
# 2. SYSTEM PREPARATION TESTS (_prepare_core_system)
# =====================================================================

def test_prepare_system_with_directed_network_raises_error():
    # ARRANGE
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        kb = BaseKatzBonacich()
    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.directed = True  
    
    # ACT & ASSERT
    with pytest.raises(NotImplementedError, match="KB-centrality currently supports only undirected networks."):
        kb._prepare_core_system(mock_network)


def test_prepare_system_with_too_few_nodes_raises_error():
    # ARRANGE
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        kb = BaseKatzBonacich()
    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.directed = False
    mock_network.number_of_nodes = 1  
    
    # ACT & ASSERT
    with pytest.raises(ValueError, match="Katz-Bonacich centrality requires a network with at least 2 nodes"):
        kb._prepare_core_system(mock_network)


@patch("signnet.utils.MatrixFactory.MatrixFactory.adjacency")
def test_prepare_system_success(mock_adjacency):
    # ARRANGE
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        kb = BaseKatzBonacich()
    
    # network mock
    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.directed = False
    mock_network.number_of_nodes = 3
    
    # Simple adjacency matrix
    # max_eigenval == 2 in this case
    mock_A = np.array([
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 0]
    ])
    mock_adjacency.return_value = mock_A
    
    # Expected delta: 1.0 / (2 * 3 - 2) = 1.0 / 4 = 0.25
    # stability: max_eigenval (2) * delta (0.25) = 0.5 < 1.0 -> should be successful
    
    # ACT
    A, delta, matrix_to_invert = kb._prepare_core_system(mock_network)
    
    # ASSERT
    assert np.array_equal(A, mock_A)
    assert delta == 0.25
    
    # Check the identity matrix calculation (I - delta * A)
    expected_matrix = np.eye(3) - (0.25 * mock_A)
    assert np.array_equal(matrix_to_invert, expected_matrix)


@patch("signnet.utils.MatrixFactory.MatrixFactory.adjacency")
def test_prepare_system_fails_stability_check(mock_adjacency):
    # ARRANGE
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        kb = BaseKatzBonacich()
    
    # 2 nodes -> Delta = 1.0 / (2 * 2 - 2) = 0.5
    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.directed = False
    mock_network.number_of_nodes = 2
    
    # Adjacency matrix with strong connection (e.g. value 3), Eigen-values are [3, -3]
    # max_eigenval = 3. 
    # Stabilitätsprüfung: delta (0.5) >= 1.0 / 3 (0.333) -> should not work
    mock_A = np.array([
        [3, 0]
    ])
    mock_adjacency.return_value = mock_A
    
    # ACT & ASSERT
    with pytest.raises(ValueError, match="Delta .* is too big for convergence."):
        kb._prepare_core_system(mock_network)

def test_prepare_core_system_with_empty_network_raises_error():
    # ARRANGE
    with patch.object(BaseKatzBonacich, "__abstractmethods__", set()):
        kb = BaseKatzBonacich()
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])
    network = SignedNetwork(edges=empty_edges, nodes=["A", "B"])

    # ACT & ASSERT
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        kb._prepare_core_system(network)
