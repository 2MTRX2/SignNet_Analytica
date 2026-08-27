# test_PiiCentrlity.py
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from signnet.analysis.centrality.centrality_measures.PiiCentrality import PiiCentrality
from signnet.analysis.centrality.centrality_measures.CentralityMeasure import ParameterSpec
from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter

# =====================================================================
# 1. PROPERTY TESTS
# =====================================================================

def test_paramters_property():
    # ARRANGE
    pii_centrality = PiiCentrality(beta=-0.2, max_distance=3)
    
    # ACT & ASSERT
    assert pii_centrality.PARAMETERS[0] == ParameterSpec(name="beta", label="Beta (PII)", type="float", default=-0.20, min_value=None, max_value=-0.00001, step=0.05)
    assert pii_centrality.PARAMETERS[1] == ParameterSpec(name="max_distance", label="Max Distance", type="int", default=3, min_value=0, max_value=None, step=1)

def test_beta_initialisation_error(): 
    with pytest.raises(ValueError, match="beta must be negative."): 
        PiiCentrality(beta=0.2, max_distance=3)

def test_max_distance_initialisation_error(): 
    with pytest.raises(ValueError, match="max_distance must be non-negative."): 
        PiiCentrality(beta=-0.2, max_distance=-3)

def test_name_property(): 
    pii_centrality = PiiCentrality(beta=-0.2, max_distance=3)

    assert pii_centrality.name == "PII (β=-0.2, m_dist=3)"

# =====================================================================
# 2. COMPUTATION TESTS (compute)
# =====================================================================

def test_compute_directed_network_error(): 
    pii_centrality = PiiCentrality(beta=-0.2, max_distance=3)

    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.directed = True

    with pytest.raises(NotImplementedError, match="PII centrality currently supports only undirected networks."):
        pii_centrality.compute(mock_network)

def test_compute_theoretical_constraint_error(): 
    # ARRANGE
    pii_centrality = PiiCentrality(beta=-0.11, max_distance=3)
    
    NUMBER_OF_SATELLITES = 20
    CENTER_NODE = "Center"

    edges_data = {
        "source": [f"Satellite_{i}" for i in range(1, NUMBER_OF_SATELLITES + 1)],
        "target": [CENTER_NODE] * NUMBER_OF_SATELLITES,
        "sign": [1] * NUMBER_OF_SATELLITES  
    }
    df_edges = pd.DataFrame(edges_data)
    
    network = SignedNetwork(edges=df_edges, directed=False)

    max_degree = 20
    max_allowed_beta = 0.1

    # ACT & ASSERT
    with pytest.raises(ValueError, match= f"PII Centrality constraint violated: |beta| * M must be <= 2. "
                    f"With a maximum node degree (M) of {max_degree}, "
                    f"beta must satisfy the condition: -{max_allowed_beta} ≤ beta < 0."): 
        pii_centrality.compute(network)

def test_compute_pii_centrality(): 
    # ARRANGE
    pii_centrality = PiiCentrality(beta=-0.2, max_distance=3)
    
    NUMBER_OF_SATELLITES = 2
    CENTER_NODE = "Center"

    edges_data = pd.DataFrame({
        "source": [f"Satellite_{i}" for i in range(1, NUMBER_OF_SATELLITES + 1)],
        "target": [CENTER_NODE] * NUMBER_OF_SATELLITES,
        "sign": [1] * NUMBER_OF_SATELLITES  
    })
    
    network = SignedNetwork(edges=edges_data, directed=False)

    expected_df = CentralityResultFormatter.from_records([
        {"node": "Satellite_1", pii_centrality.name: 0.8},
        {"node": "Satellite_2", pii_centrality.name: 0.8},
        {"node": "Center",      pii_centrality.name: 2.0}
    ])

    # ACT
    result_df = pii_centrality.compute(network)

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
    measure = PiiCentrality(beta=-0.2, max_distance=3)

    # ACT & ASSERT
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        measure.compute(network)  
