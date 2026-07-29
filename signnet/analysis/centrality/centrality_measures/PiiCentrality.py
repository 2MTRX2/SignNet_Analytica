# PiiCentrality.py
import pandas as pd
import networkx as nx

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import ParameterSpec
from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.adapters.NetworkXAdapter import NetworkXAdapter
from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter


class PiiCentrality(CentralityMeasure):
    """
    Implements the PII centrality.

    PII_i = Σ β^d (P_i(d) - N_i(d))

    where

    P_i(d) = number of positive edges at distance d
    N_i(d) = number of negative edges at distance d

    and

    d(node, edge(u,v)) = min(d(node,u), d(node,v))
    """

    PARAMETERS = [
        ParameterSpec(name="beta", label="Beta (PII)", type="float", default=-0.25, min_value=-1.0, max_value=0.0, step=0.05),
        ParameterSpec(name="max_distance", label="Max Distance", type="int", default=3, min_value=1, max_value=10, step=1)
    ]

    def __init__(self, beta: float, max_distance: int):

        if beta >= 0:
            raise ValueError("beta must be negative.")

        if max_distance < 0:
            raise ValueError("max_distance must be non-negative.")

        self.beta = beta
        self.max_distance = max_distance

    @property
    def name(self) -> str:
        return "PII"

    def compute(self, network: SignedNetwork) -> pd.DataFrame:

        if network.directed:
            raise NotImplementedError(
                "PII centrality currently supports only undirected networks."
            )

        G = NetworkXAdapter.to_networkx(network)

        # ---------- theoretical constraint ----------
        max_degree = max(dict(G.degree()).values(), default=0)

        if abs(self.beta) * max_degree > 2:
            raise ValueError(
                "Constraint violated: |beta| * M must be <= 2."
            )

        rows = []

        for source in network.nodes:

            # shortest path lengths from source to each node
            distances = nx.single_source_shortest_path_length(
                G,
                source,
                cutoff=self.max_distance+1
            )

            pii = 0.0

            for u, v, attr in G.edges(data=True):

                sign = attr["sign"]

                du = distances.get(u)
                dv = distances.get(v)

                if du is None and dv is None:
                    continue

                edge_distance = min(
                    x for x in (du, dv) if x is not None
                )

                if edge_distance > self.max_distance:
                    continue

                weight = self.beta ** edge_distance

                if sign > 0:
                    pii += weight
                elif sign < 0:
                    pii -= weight

            rows.append(
                {
                    "node": source,
                    self.name: pii,
                }
            )

        return CentralityResultFormatter.from_records(rows, index_column="node")
    