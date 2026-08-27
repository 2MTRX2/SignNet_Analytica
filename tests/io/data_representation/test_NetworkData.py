# test_NetworkData.py
import pytest
import pandas as pd
from dataclasses import FrozenInstanceError

from signnet.io.data_representation.NetworkData import NetworkData

# =====================================================================
# NETWORK DATA CONTAINER TESTS
# =====================================================================

def test_network_data_initialization_with_all_arguments():
    # ARRANGE
    edges_df = pd.DataFrame({"source": ["A"], "target": ["B"], "sign": [1]})
    nodes_list = ["A", "B"]

    # ACT
    network_data = NetworkData(edges=edges_df, nodes=nodes_list)

    # ASSERT
    assert network_data.edges is edges_df
    assert network_data.nodes is nodes_list


def test_network_data_initialization_default_nodes():
    edges_df = pd.DataFrame({"source": ["A"], "target": ["B"], "sign": [1]})

    # ACT
    network_data = NetworkData(edges=edges_df)

    # ASSERT
    assert network_data.edges is edges_df
    assert network_data.nodes is None


def test_network_data_is_frozen_and_immutable():
    # ARRANGE
    edges_df = pd.DataFrame({"source": ["A"], "target": ["B"], "sign": [1]})
    network_data = NetworkData(edges=edges_df, nodes=["A", "B"])

    # ACT & ASSERT
    # try to override an attribute
    with pytest.raises(FrozenInstanceError, match="cannot assign to field"):
        network_data.nodes = ["X", "Y"]

    # try to expand with a new attribute
    with pytest.raises(FrozenInstanceError, match="cannot assign to field 'new_attribute'"):
        network_data.new_attribute = "test"
