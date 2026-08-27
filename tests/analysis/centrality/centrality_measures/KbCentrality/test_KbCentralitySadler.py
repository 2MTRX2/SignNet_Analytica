# test_KbCentralitySadler.py
import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch

from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralitySadler import KbCentralitySadler
from signnet.models.SignedNetwork import SignedNetwork

# =====================================================================
# 1. PROPERTY TESTS
# =====================================================================

def test_name_property():
    # ARRANGE
    kb_sadler = KbCentralitySadler()
    
    # ACT & ASSERT
    assert kb_sadler.name == "K-B (Sadler, t=1 with d=t-1)"

# =====================================================================
# 2. COMPUTATION TESTS (compute)
# =====================================================================

@patch.object(KbCentralitySadler, "_prepare_core_system")
@patch.object(KbCentralitySadler, "_to_dataframe")
def test_compute_success(mock_to_dataframe, mock_prepare_system):
    kb_sadler = KbCentralitySadler()

    # # Mock for SignedNetwork
    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.number_of_nodes = 3
    mock_network.nodes = ["Node_A", "Node_B", "Node_C"]

    # mocked adjacency matrix of network
    mock_A = np.array([
        [0, 1, 1], 
        [1, 0, 1], 
        [1, 1, 0]
    ])

    # mocked delta of network: # 1 / (2*n - 2)
    mock_delta = 0.25 

    # mocked matrix to invert: I - (delta * A)
    mock_matrix_to_invert = np.array([
        [1.0, -0.25, -0.25],
        [-0.25, 1.0, -0.25],
        [-0.25, -0.25, 1.0]
    ])

    mock_prepare_system.return_value = (mock_A, mock_delta, mock_matrix_to_invert)

    # solving the system leads to the following result because the right side of the equation is always equal to 1
    mock_b_scores = np.array([2, 2, 2])

    expected_scores = mock_A @ mock_b_scores

    expected_df = pd.DataFrame(
            {"centrality": expected_scores}, 
            index=mock_network.nodes
        )
    mock_to_dataframe.return_value = expected_df

    # ACT
    result_df = kb_sadler.compute(mock_network)

    # ASSERT
    # Verify that the core system calculation was called correctly
    mock_prepare_system.assert_called_once_with(mock_network)

    # Verify that data conversion helper was called with calculated scores
    mock_to_dataframe.assert_called_once()
    actual_args = mock_to_dataframe.call_args[0]
    assert actual_args[0] == mock_network.nodes
    assert np.allclose(actual_args[1], expected_scores)
    assert actual_args[2] == "K-B (Bloch, t=1 with d=t)"

    # Verify the output DataFrame matches the mock dataframe
    pd.testing.assert_frame_equal(result_df, expected_df)

@patch.object(KbCentralitySadler, "_prepare_core_system")
def test_compute_propagates_exception_from_preparation(mock_prepare_system):
    # ARRANGE
    kb_sadler = KbCentralitySadler()
    
    # Mock for SignedNetwork
    mock_network = MagicMock(spec=SignedNetwork)

    # Simulate an error raised in the base class (e.g. directed network)
    mock_prepare_system.side_effect = NotImplementedError("KB-centrality currently supports only undirected networks.")
    
    # ACT & ASSERT
    with pytest.raises(NotImplementedError, match="KB-centrality currently supports only undirected networks."):
        kb_sadler.compute(mock_network)

def test_calculate_with_empty_network_raises_error():
    # ARRANGE
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])
    network = SignedNetwork(edges=empty_edges, nodes=["A", "B"])
    measure = KbCentralitySadler()

    # ACT & ASSERT - Da der Dekorator jetzt davor sitzt, erwarten wir den Fehler
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        measure.compute(network)  