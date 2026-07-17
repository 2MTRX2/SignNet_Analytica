# NetworkXAdapter.py
import networkx as nx

from signnet.models.SignedNetwork import SignedNetwork


class NetworkXAdapter:
    """
    Converts the framework's SignedNetwork domain model into a NetworkX graph.

    The adapter preserves all edge attributes stored in the canonical edge list
    and creates either an undirected Graph or a directed DiGraph depending on
    the network configuration.
    """


    @staticmethod
    def to_networkx(network: SignedNetwork) -> nx.Graph:

        G = nx.DiGraph() if network.directed else nx.Graph()

        nx.from_pandas_edgelist(
            network.edges,
            source='source',
            target='target',
            edge_attr=True,
            create_using=G
        )

        # add nodes which are not connected to the network but are part of the network
        G.add_nodes_from(network.nodes) 

        return G
