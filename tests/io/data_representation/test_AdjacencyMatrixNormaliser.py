# test_AdjacencyMatrixNormaliser.py
import pandas as pd

from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser
from signnet.io.data_representation.NetworkData import NetworkData

# =====================================================================
# 1. TRANSFORM
# =====================================================================

def test_to_network_data_with_default_index():
    # ARRANGE
    normaliser = AdjacencyMatrixNormaliser(directed=True)
    
    matrix_df = pd.DataFrame({
        "node_labels": ["A", "B", "C"],
        "A": [0, 1, -1],
        "B": [1, 0, 0],
        "C": [-1, 0, 0]
    })

    expected_edges = pd.DataFrame({
        "source": ["A", "A", "B", "C"],
        "target": ["B", "C", "A", "A"],
        "sign": [1, -1, 1, -1]
    }).reset_index(drop=True)

    # ACT
    network_data = normaliser.to_network_data(matrix_df)

    # ASSERT
    assert isinstance(network_data, NetworkData)
    pd.testing.assert_frame_equal(network_data.edges, expected_edges, check_like=True)
    assert network_data.nodes == ["A", "B", "C"]


def test_to_network_data_with_int_index():
    # ARRANGE
    normaliser = AdjacencyMatrixNormaliser()
    
    matrix_df = pd.DataFrame({
        "id_column":[1, 2 ,3],
        "1": [0, 1, -1],
        "2": [1, 0, 1],
        "3": [-1, 1, 0]
    })

    expected_edges = pd.DataFrame({
        "source": ["1", "1", "2"],
        "target": ["2", "3", "3"],
        "sign": [1.0, -1.0, 1.0]
    }).reset_index(drop=True)

    # ACT
    network_data = normaliser.to_network_data(matrix_df)

    # ASSERT
    assert isinstance(network_data, NetworkData)
    pd.testing.assert_frame_equal(network_data.edges, expected_edges, check_like=True)
    assert network_data.nodes == ["1", "2", "3"]


def test_to_network_data_with_isolated_node():
    # ARRANGE
    normaliser = AdjacencyMatrixNormaliser()
    
    matrix_df = pd.DataFrame({
        "nodes": ["A", "B", "C"],
        "A": [0, -1, 0],
        "B": [-1, 0, 0],
        "C": [0, 0, 0]
    })

    expected_edges = pd.DataFrame({
        "source": ["A"],
        "target": ["B"],
        "sign": [-1.0]
    }).reset_index(drop=True)

    # ACT
    network_data = normaliser.to_network_data(matrix_df)

    # ASSERT
    assert isinstance(network_data, NetworkData)
    pd.testing.assert_frame_equal(network_data.edges, expected_edges, check_like=True)
    assert network_data.nodes == ["A", "B", "C"]

