# SignedDegreeCentrality.py
import pandas as pd

from .CentralityMeasure import CentralityMeasure
from signnet.models.SignedNetwork import SignedNetwork
from adapters.NetworkXAdapter import NetworkXAdapter
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter

class SignedDegreeCentrality(CentralityMeasure):
    """
    Implements the signed degree centrality

        Δ_i(A, β) = d_i⁺(A) − β d_i⁻(A)

    where

        d_i⁺ = number of positive incident edges
        d_i⁻ = number of negative incident edges
        β > 0

    Setting β = 1 yields the classical net degree.
    
    The implementation currently supports undirected signed networks only.
    """
    
    def __init__(self, beta: float = 1.0):
        """Initializes the centrality measure with a penalization factor for negative edges.

        Args:
            beta (float): Weight factor for negative edges in the net score calculation.
                Must be greater than zero. Defaults to 1.0.
        """
        if beta <= 0:
            raise ValueError("beta must be greater than zero.")
        self.beta = beta

    @property
    def name(self) -> str:
        return f"Signed Degree (β={self.beta})"

    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        """Computes the signed degree metrics and returns them as a structured DataFrame.

        Args:
            network (SignedNetwork): The canonical domain model of the network.

        Returns:
            pd.DataFrame: A table indexed by node identifiers with the columns:
                'pos_degree', 'neg_degree', and 'signed_degree'.
        """
        if network.directed:
            raise NotImplementedError("SignedDegreeCentrality currently supports only undirected networks.")
        
        # Create the NetworkX object via the adapter to handle the network properly and avoid double-counting
        G = NetworkXAdapter.to_networkx(network)
        
        rows: list[dict] = []

        # Loop over all nodes in the network
        for node in network.nodes:
            pos_count = 0
            neg_count = 0
            
            # G[node] delivers all unique neighbors of the node in the undirected graph.
            if node in G:
                for key, attr in G[node].items():
                    sign = attr.get('sign', 0)
                    if sign > 0:
                        pos_count += 1
                    elif sign < 0:
                        neg_count += 1
            
            signed_degree = pos_count - (self.beta * neg_count)
            
            rows.append(
                {
                    "node": node,
                    f"pos_degree (β={self.beta})": pos_count,
                    f"neg_degree (β={self.beta})": neg_count,
                    self.name: signed_degree
                }
            )

        # Result as a structured pandas dataframe
        return CentralityResultFormatter.from_records(rows, index_column="node")
