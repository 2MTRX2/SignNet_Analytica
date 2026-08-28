# test_PnCentrality
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
import re

from signnet.analysis.centrality.centrality_measures.PnCentrality import PnCentrality
from signnet.analysis.centrality.centrality_measures.CentralityMeasure import ParameterSpec
from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter
from signnet.utils.MatrixFactory import MatrixFactory

# =====================================================================
# 1. PROPERTY TESTS
# =====================================================================

def test_name_property(): 
    pn_centrality = PnCentrality()

    assert pn_centrality.name == "PN"

# =====================================================================
# 2. COMPUTATION TESTS (compute)
# =====================================================================

def test_compute_directed_network_error(): 
    pn_centrality = PnCentrality()
    mock_network = MagicMock(spec=SignedNetwork)

    mock_network.directed = True

    with pytest.raises(NotImplementedError, match="PN-centrality currently supports only undirected networks."): 
        pn_centrality.compute(mock_network)

def test_compute_too_little_number_of_nodes(): 
    pn_centrality = PnCentrality()
    mock_network = MagicMock(spec=SignedNetwork)

    mock_network.directed = False
    mock_network.number_of_nodes = 1

    with pytest.raises(ValueError, match="PN-centrality requires a network with at least 2 nodes to calculate alpha."): 
        pn_centrality.compute(mock_network)

def test_compute_matrix_convergence_error(): 
    pn_centrality = PnCentrality()

    # this network should trigger the constraint since the values grow with a factor of 20 and get discounted with an alpha of 0.25
    edges_data = {
        "source": ["A", "A", "A", "A", "B", "B", "B", "C", "C", "D"],
        "target": ["B", "C", "D", "E", "C", "D", "E", "D", "E", "E"],
        "sign": [-1.0, -5.0, -10.0, -1.0, -2.0, -8.0, -1.0, -1.0, -1.0, -1.0]
    }
    df_edges = pd.DataFrame(edges_data)

    network = SignedNetwork(edges=df_edges, directed=False)

    A_tilde = MatrixFactory.tilde(network)
    eigenvalues = np.linalg.eigvals(A_tilde)
    max_eigenval = np.max(np.abs(eigenvalues))
    alpha = 1.0 / (2 * network.number_of_nodes - 2)

    raw_msg = (
        f"Alpha ({alpha}) is too large for matrix convergence with this specific dataset. "
        f"It must be smaller than 1 / |lambda_max| = {1.0 / max_eigenval:.4f}"
    )

    expected_msg = re.escape(raw_msg)

    with pytest.raises(ValueError, match=expected_msg):
        pn_centrality.compute(network) 

def test_compute_matrix_singularity_error(): 
    pn_centrality = PnCentrality()

    edges_data = {
        "source": ["A"],
        "target": ["B"],
        "sign": [1.0]
    }
    df_edges = pd.DataFrame(edges_data)
    network = SignedNetwork(edges=df_edges, directed=False)

    with patch("numpy.linalg.solve") as mock_solve:
        mock_solve.side_effect = np.linalg.LinAlgError("Matrix is singular.")
        
        with pytest.raises(ValueError, match="Matrix is singular and cannot be inverted."):
            pn_centrality.compute(network)

def test_compute_pn_centrality(): 
    pn_centrality = PnCentrality()

    # this network should trigger the constraint since the values grow with a factor of 20 and get discounted with an alpha of 0.25
    edges_data = {
        "source": ["A", "B", "C"],
        "target": ["B", "C", "A"],
        "sign": [1.0, 1.0, 1.0] 
    }
    df_edges = pd.DataFrame(edges_data)

    network = SignedNetwork(edges=df_edges, directed=False)

    expected_df = CentralityResultFormatter.from_array(["A", "B", "C"], [2.0, 2.0, 2.0], pn_centrality.name)

    
    # ACT
    result_df = pn_centrality.compute(network)
    
    # ASSERT
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    result_df = result_df.sort_index()
    expected_df = expected_df.sort_index()
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_calculate_with_empty_network_raises_error():
    # ARRANGE
    empty_edges = pd.DataFrame(columns=['source', 'target', 'sign'])
    network = SignedNetwork(edges=empty_edges, nodes=["A", "B"])
    measure = PnCentrality()

    # ACT & ASSERT
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        measure.compute(network)  