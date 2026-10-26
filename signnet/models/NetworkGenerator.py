# NetworkGenerator.py
import networkx as nx
import pandas as pd
import random
from typing import Any, Dict

from signnet.models.SignedNetwork import SignedNetwork

from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry

class NetworkGenerator: 
    """
    A generator for creating synthetic signed networks based on registered topologies.

    This class acts as a factory for artificial graph structures. It combines 
    unsigned structural topologies from NetworkX with a stochastic distribution 
    of positive and negative edge signs based on a specified conflict ratio.

    Attributes:
        topology_name (str): The name of the network topology to look up in the 
            `TopologyRegistry`.
        n (int): The total number of nodes in the generated network. Must be at 
            least 3.
        neg_ratio (float): The relative fraction of negative edges (conflict rate) 
            in the network. Must be bounded between 0.0 and 1.0.
        kwargs (Dict[str, Any]): Additional topology-specific configuration 
            parameters forwarded directly to the underlying NetworkX generation 
            function (e.g., `p`, `k`, or `m`).

    Raises:
        ValueError: If `topology_name` is not found within the `TopologyRegistry`.
        ValueError: If the number of nodes `n` is less than 3.
        ValueError: If `neg_ratio` falls outside the valid range of [0.0, 1.0].
    """

    def __init__(self, topology_name: str, n: int, neg_ratio: float, **kwargs: Any):
        if topology_name not in TopologyRegistry.get_available_topologies():
            raise ValueError(
                f"Topology '{topology_name}' is not available. "
                f"Available topologies are: {list(TopologyRegistry.get_available_topologies())}"
            )

        if n < 3:
            raise ValueError("The number of nodes n must be at least 3.")

        if not (0.0 <= neg_ratio <= 1.0):
            raise ValueError(f"The conflict rate (neg_ratio) must be inside [0.0, 1.0]. Given: {neg_ratio}")


        self.topology_name = topology_name
        self.n = n
        self.neg_ratio = neg_ratio
        
        self.kwargs = kwargs

    def create_random_signed_network(self) -> SignedNetwork:
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
        """
            
        # 1. unsigned topology
        topology_data = TopologyRegistry.get_topology_data(self.topology_name)
        generator_func = topology_data["func"]
        G: nx.Graph = generator_func(self.n, **self.kwargs)
        
        # 2. generating edge list
        edge_data = []
        for u, v in G.edges():
            # determination of sign distribution 
            sign_value = -1.0 if random.random() < self.neg_ratio else 1.0
            edge_data.append({
                "source": u,
                "target": v,
                "sign": sign_value
            })
            
        edges_df = pd.DataFrame(edge_data, columns=["source", "target", "sign"])
        nodes_list = list(range(self.n))
        
        # 3. returns a kanonic SignedNetwork object
        return SignedNetwork(edges=edges_df, nodes=nodes_list, directed=False)
