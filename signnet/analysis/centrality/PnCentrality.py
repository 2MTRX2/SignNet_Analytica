# PnCentrality.py
import numpy as np
import pandas as pd

from .CentralityMeasure import CentralityMeasure
from models.SignedNetwork import SignedNetwork

class PnCentrality(CentralityMeasure):
    """
    Implements the PN-centrality proposed by

        Everett & Borgatti (2014)

    PN = (I - α Ã)^(-1) 1

    where

        α = 1 / (2n - 2)

        Ã = A+ - 2A-
    
    This implementation utilizes NumPy for highly optimized matrix operations.
    """

    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        """Computes the PN-Centrality vector and returns a structured DataFrame.

        Args:
            network (SignedNetwork): The canonical domain model of the network.

        Returns:
            pd.DataFrame: A table indexed by node identifiers with the column:
                'pn_centrality'.
        """
        if network.directed:
            raise NotImplementedError("PN-centrality currently supports only undirected networks.")

        nodes = network.nodes
        num_nodes = network.number_of_nodes
        alpha = 1.0 / (2*num_nodes - 2)
        
        # create a mapping between nodes and matrix indices (0 to N-1)
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        
        # create the signed adjency matrix filled with 0s
        A_tilde = np.zeros((num_nodes, num_nodes))
        
        # get all the edges of the network
        for source, target, sign in network.edges.itertuples(index=False):
            u_idx = node_to_idx[source]
            v_idx = node_to_idx[target]

            if sign > 0:
                value = 1.0
            elif sign < 0:
                 value = -2.0
            else:
                 continue

            # undirected: both directions
            A_tilde[u_idx, v_idx] = value
            A_tilde[v_idx, u_idx] = value


        # evaluation of the alpha-value that inversion of the matrix converges
        eigenvalues = np.linalg.eigvals(A_tilde)
        max_eigenval = np.max(np.abs(eigenvalues))
        
        if max_eigenval > 0 and alpha >= (1.0 / max_eigenval):
            raise ValueError(
                f"Alpha ({alpha}) is too large for matrix convergence. "
                f"It must be smaller than 1 / |lambda_max| = {1.0 / max_eigenval:.4f}"
            )

        # apply formula: PN = (I - alpha * A_tilde)^(-1) * 1
        I = np.eye(num_nodes)  
        matrix_to_invert = I - (alpha * A_tilde)

        ones_vector = np.ones(num_nodes)
        
        try:
            pn_scores = np.linalg.solve(matrix_to_invert, ones_vector)
        except np.linalg.LinAlgError:
            raise ValueError("Matrix is singular and cannot be inverted.")

        # mapping to the pandas dataframe
        rows = []

        for node, score in zip(nodes, pn_scores):
            rows.append(
                {
                    "node": node,
                    "pn_centrality": score,
                }
            )

        results = pd.DataFrame(rows)
        results.set_index("node", inplace=True)

        return results
