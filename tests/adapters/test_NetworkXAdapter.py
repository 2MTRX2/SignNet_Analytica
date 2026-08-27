# test_NetworkXAdapter.py
import pytest
import networkx as nx
import pandas as pd

from signnet.models.SignedNetwork import SignedNetwork
from signnet.adapters.NetworkXAdapter import NetworkXAdapter

def test_to_networkx_undirected_with_isolated_nodes():
    # 1. ARRANGE 
    edges_df = pd.DataFrame([
        {'source': 'A', 'target': 'B', 'sign': 1},
        {'source': 'B', 'target': 'C', 'sign': -1},
        {'source': 'C', 'target': 'D', 'sign': -3}
    ])
    nodes_list = ["A", "B", "C", "D", "Isolated_Node"]
    
    network = SignedNetwork(edges=edges_df, nodes=nodes_list, directed=False)

    # 2. ACT 
    graph = NetworkXAdapter.to_networkx(network)

    # 3. ASSERT 
    # Check if the correct instance was instantiated
    assert isinstance(graph, nx.Graph)
    assert not isinstance(graph, nx.DiGraph)

    # Check if all nodes exists
    assert graph.number_of_nodes() == 5
    assert graph.has_node("Isolated_Node")

    # Check if the number of edges is correct
    assert graph.number_of_edges() == 3

    # Check if the signs are correct
    assert graph.has_edge("A", "B")
    assert graph["A"]["B"]["sign"] == 1
    
    assert graph.has_edge("B", "C")
    assert graph["B"]["C"]["sign"] == -1  

    assert graph.has_edge("C", "D")
    assert graph["C"]["D"]["sign"] == -3  


def test_to_networkx_directed():
    # 1. ARRANGE
    edges_df = pd.DataFrame([
        {'source': 'A', 'target': 'B', 'sign': 1}
    ])
    network = SignedNetwork(edges=edges_df, nodes=None, directed=True)

    # 2. ACT
    graph = NetworkXAdapter.to_networkx(network)

    # 3. ASSERT
    # Check if the correct instance was instantiated
    assert isinstance(graph, nx.DiGraph)
    
    # Check if the edge exists only in one direction
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("B", "A")
    assert graph["A"]["B"]["sign"] == 1
