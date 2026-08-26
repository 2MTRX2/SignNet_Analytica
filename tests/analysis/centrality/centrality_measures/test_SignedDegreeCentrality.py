# test_SignedDegreeCentrality.py
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from signnet.analysis.centrality.centrality_measures.SignedDegreeCentrality import SignedDegreeCentrality
from signnet.analysis.centrality.centrality_measures.CentralityMeasure import ParameterSpec
from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter

# =====================================================================
# 1. PROPERTY TESTS
# =====================================================================

def test_paramters_property():
    # ARRANGE
    sd_centrality = SignedDegreeCentrality()
    
    # ACT & ASSERT
    assert sd_centrality.PARAMETERS[0] == ParameterSpec(name="beta", label="Beta (Signed Degree)", type="float", default=1.0, min_value=0.000001, max_value=None, step=0.05)

def test_beta_initialisation_error(): 
    with pytest.raises(ValueError, match="beta must be greater than zero."): 
        SignedDegreeCentrality(-1.0)

def test_name_property(): 
    sd_centrality = SignedDegreeCentrality(beta=1.0)

    assert sd_centrality.name == "Signed Degree (β=1.0)"

# =====================================================================
# 2. COMPUTATION TESTS (compute)
# =====================================================================

def test_compute_directed_network_error(): 
    sd_centrality = SignedDegreeCentrality()

    mock_network = MagicMock(spec=SignedNetwork)
    mock_network.directed = True

    with pytest.raises(NotImplementedError, match="SignedDegreeCentrality currently supports only undirected networks."):
        sd_centrality.compute(mock_network)

def test_compute_sd_centrality(): 
    # ARRANGE
    sd_centrality = SignedDegreeCentrality(beta=2.0)
    
    NUMBER_OF_SATELLITES = 2
    CENTER_NODE = "Center"

    edges_data = pd.DataFrame({
        "source": [f"Satellite_{i}" for i in range(1, NUMBER_OF_SATELLITES + 1)],
        "target": [CENTER_NODE] * NUMBER_OF_SATELLITES,
        "sign": [1, -1]
    })
    
    network = SignedNetwork(edges=edges_data, directed=False)

    expected_df = CentralityResultFormatter.from_records([
        {"node": "Satellite_1", "pos_degree (β=2.0)": 1,  "neg_degree (β=2.0)": 0, sd_centrality.name: 1.0},
        {"node": "Satellite_2", "pos_degree (β=2.0)": 0,  "neg_degree (β=2.0)": 1, sd_centrality.name: -2.0},
        {"node": "Center", "pos_degree (β=2.0)": 1,  "neg_degree (β=2.0)": 1, sd_centrality.name: -1.0}
    ], index_column="node")

    # ACT
    result_df = sd_centrality.compute(network)

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
    measure = SignedDegreeCentrality()

    # ACT & ASSERT - Da der Dekorator jetzt davor sitzt, erwarten wir den Fehler
    with pytest.raises(ValueError, match="The network topology contains no edges"):
        measure.compute(network)  