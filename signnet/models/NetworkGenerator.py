# NetworkGenerator.py
import networkx as nx
import pandas as pd
import random
from typing import Any

from signnet.models.SignedNetwork import SignedNetwork

TOPOLOGY_REGISTRY = {
    "Random network (Erdős-Rényi)": nx.erdos_renyi_graph,
    "Scale-Free (Barabási-Albert)": nx.barabasi_albert_graph,
    "Small-World (Watts-Strogatz)": nx.watts_strogatz_graph,
}

def create_random_signed_network(topology_name: str, n: int, neg_ratio: float, **kwargs: Any) -> SignedNetwork:
    """
    Creates an artificial random network and returns it in the kanonic SignedNetwork object format.
    
    This function works as a fcatory for synthetic graph structures.
    It generates a topology with the according NetworkX-algorithms and translate
    the structure into a canonic network schema (SignedNetwork).

    Args:
        topology_name (str): Name of the topology from `TOPOLOGY_REGISTRY` (e.g. "Small-World (Watts-Strogatz)").
        n (int): Number of nodes in the generated network.
        neg_ratio (float): Relative number of negative edges in the network 
            (value between 0.0 and 1.0u).
        **kwargs (Any): Additional topology-specific parameters for the NetworkX-function (e.g. p, k, m).

    Returns:
        SignedNetwork: A fresh instantiated network of the canonic network modell 

    Raises:
        ValueError: If the topology name doesn't exist in the `TOPOLOGY_REGISTRY`.

        ValueError: If the number of nodes is less than 3.

        ValueError: If the negative ratio is more than 1.0 or less than 0.0.
    """
    if topology_name not in TOPOLOGY_REGISTRY:
        raise ValueError(
            f"Topology '{topology_name}' is not available. "
            f"Available topologies are: {list(TOPOLOGY_REGISTRY.keys())}"
        )
    
    if n < 3:
        raise ValueError("The number of nodes n must be at least 3.")
        
    if not (0.0 <= neg_ratio <= 1.0):
        raise ValueError(f"The conflict rate (neg_ratio) must be inside [0.0, 1.0]. Given: {neg_ratio}")
        
    # 1. temporary topology
    generator_func = TOPOLOGY_REGISTRY[topology_name]
    G: nx.Graph = generator_func(n=n, **kwargs)
    
    # 2. generating edge list
    edge_data = []
    for u, v in G.edges():
        # determination of sign distribution 
        sign_value = -1.0 if random.random() < neg_ratio else 1.0
        edge_data.append({
            "source": u,
            "target": v,
            "sign": sign_value
        })
        
    edges_df = pd.DataFrame(edge_data, columns=["source", "target", "sign"])
    nodes_list = list(range(n))
    
    # 3. returns a kanonic SignedNetwork object
    return SignedNetwork(edges=edges_df, nodes=nodes_list, directed=False)
