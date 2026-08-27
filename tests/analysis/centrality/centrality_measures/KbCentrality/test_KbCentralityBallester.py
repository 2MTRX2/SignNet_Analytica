# test_KbCentralityBallester
import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch

from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBallester import KbCentralityBallester
from signnet.models.SignedNetwork import SignedNetwork

# =====================================================================
# 1. PROPERTY TESTS
# =====================================================================

def test_name_property():
    # ARRANGE
    kb_ballester = KbCentralityBallester()
    
    # ACT & ASSERT
    assert kb_ballester.name == "K-B (Ballester, t=0)"


# =====================================================================
# 2. COMPUTATION TESTS (compute)
# =====================================================================

@patch.object(KbCentralityBallester, "_prepare_core_system")
@patch.object(KbCentralityBallester, "_to_dataframe")
def test_compute_success(mock_to_dataframe, mock_prepare_system):
    # ARRANGE
    kb_ballester = KbCentralityBallester()
    
    # Mock for SignedNetwork
    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.number_of_nodes = 3
    mock_network.nodes = ["Node_A", "Node_B", "Node_C"]
    
    # Prepare mock outputs for the core system
    # (I - delta * A) system matrix for 3 nodes
    mock_A = np.array([
        [0, 1, 1], 
        [1, 0, 1], 
        [1, 1, 0]
    ])
    mock_delta = 0.25 # 1/(2n-2)
    mock_matrix_to_invert = np.array([
        [1.0, -0.25, -0.25],
        [-0.25, 1.0, -0.25],
        [-0.25, -0.25, 1.0]
    ])
    mock_prepare_system.return_value = (mock_A, mock_delta, mock_matrix_to_invert)
    
    # Expected scores from np.linalg.solve with rhs_vector = [1, 1, 1]
    # Equation: (1.0 * x) - (0.25 * x) - (0.25 * x) = 1 -> 0.5 * x = 1 -> x = 2.0
    expected_scores = np.array([2.0, 2.0, 2.0])
    
    # Expected final DataFrame format
    expected_df = pd.DataFrame(
        {"centrality": expected_scores}, 
        index=mock_network.nodes
    )
    mock_to_dataframe.return_value = expected_df
    
    # ACT
    result_df = kb_ballester.compute(mock_network)
    
    # ASSERT
    # Verify that the core system calculation was called correctly
    mock_prepare_system.assert_called_once_with(mock_network)
    
    # Verify that data conversion helper was called with calculated scores
    mock_to_dataframe.assert_called_once()
    actual_args = mock_to_dataframe.call_args[0]
    assert actual_args[0] == mock_network.nodes
    assert np.allclose(actual_args[1], expected_scores)
    assert actual_args[2] == "K-B (Ballester, t=0)"
    
    # Verify the output DataFrame matches the mock dataframe
    pd.testing.assert_frame_equal(result_df, expected_df)


@patch.object(KbCentralityBallester, "_prepare_core_system")
def test_compute_propagates_exception_from_preparation(mock_prepare_system):
    # ARRANGE
    kb_ballester = KbCentralityBallester()
    mock_network = MagicMock(spec=SignedNetwork)
    
    # Simulate an error raised in the base class (e.g. directed network)
    mock_prepare_system.side_effect = NotImplementedError("KB-centrality currently supports only undirected networks.")
    
    # ACT & ASSERT
    with pytest.raises(NotImplementedError, match="KB-centrality currently supports only undirected networks."):
        kb_ballester.compute(mock_network)

def test_calculate_with_empty_network_raises_error():
    # ARRANGE
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])
    network = SignedNetwork(edges=empty_edges, nodes=["A", "B"])
    measure = KbCentralityBallester()

    # ACT & ASSERT
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        measure.compute(network)
