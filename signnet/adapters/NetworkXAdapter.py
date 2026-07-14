# NetworkXAdapter.py
import networkx as nx

from signnet.models.StaticSignedNetwork import StaticSignedNetwork


class NetworkXAdapter:
    """
    Converts the framework's SignedNetwork domain model into a NetworkX graph.

    The adapter preserves all edge attributes stored in the canonical edge list
    and creates either an undirected Graph or a directed DiGraph depending on
    the network configuration.
    """


    @staticmethod
    def to_networkx(network: StaticSignedNetwork) -> nx.Graph:

        G = nx.DiGraph() if network.directed else nx.Graph()

        return nx.from_pandas_edgelist(
            network.edges,
            source='source',
            target='target',
            edge_attr=True,
            create_using=G
        )
