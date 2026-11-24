# NetworkStatsService.py
import networkx as nx
from signnet.models.SignedNetwork import SignedNetwork
from signnet.adapters.NetworkXAdapter import NetworkXAdapter 

class NetworkStatsService:
    """
    Computes structural and sign-based summary statistics for a SignedNetwork.
    """

    def __init__(self):
        pass

    def compute_stats(self, network: SignedNetwork) -> dict:
        """Computes topological and signed balance metrics for the given network.

        Args:
            network (SignedNetwork): The initialized signed network domain model.

        Returns:
            dict: Dictionary containing node/edge counts, components, isolates, density,
                negative edge ratio (0-100), and balanced triad ratio (0-100).
        """
        G = NetworkXAdapter.to_networkx(network)

        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()

        # 1. Components & Isolated Nodes
        if num_nodes == 0:
            num_components = 0
        elif G.is_directed():
            num_components = nx.number_weakly_connected_components(G) # type: ignore
        else:
            num_components = nx.number_connected_components(G)

        num_isolated_nodes = nx.number_of_isolates(G)

        # 2. Negative Edge Ratio (%)
        if num_edges > 0:
            neg_edges = sum(1 for _, _, data in G.edges(data=True) if int(data.get('sign', 1)) < 0)
            negative_edge_ratio = (neg_edges / num_edges) * 100.0
        else:
            negative_edge_ratio = 0.0

        # 3. Graph Density (%)
        density = nx.density(G) * 100.0 if num_nodes > 1 else 0.0

        # 4. Balanced Triad Ratio (%) (Heider)
        balanced_triad_ratio = self._compute_balanced_triad_ratio(G)

        return {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "num_components": num_components,
            "num_isolated_nodes": num_isolated_nodes,
            "negative_edge_ratio": negative_edge_ratio,
            "balanced_triad_ratio": balanced_triad_ratio,
            "density": density,
        }

    def _compute_balanced_triad_ratio(self, G: nx.Graph) -> float:
        # Change to undirected if directed
        U = G.to_undirected() if G.is_directed() else G

        total_triads = 0
        balanced_triads = 0

        # Find all cliques (triads)
        for clique in nx.enumerate_all_cliques(U):
            if len(clique) == 3:
                u, v, w = clique
                s1 = int(U[u][v].get('sign', 1))
                s2 = int(U[v][w].get('sign', 1))
                s3 = int(U[u][w].get('sign', 1))

                total_triads += 1
                if (s1 * s2 * s3) > 0:
                    balanced_triads += 1
            elif len(clique) > 3:
                break 

        if total_triads == 0:
            return 0.0

        return (balanced_triads / total_triads) * 100.0
