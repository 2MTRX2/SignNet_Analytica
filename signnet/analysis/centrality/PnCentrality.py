# PnCentrality.py
import numpy as np
import pandas as pd

from .CentralityMeasure import CentralityMeasure
from models.SignedNetwork import SignedNetwork
from utils.matrix_factory import MatrixFactory

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

        A_tilde = MatrixFactory.tilde(network)

        nodes = network.nodes
        number_of_nodes = network.number_of_nodes

        alpha = 1.0 / (2*number_of_nodes - 2)

        # apply formula: PN = (I - alpha * A_tilde)^(-1) * 1
        I = np.eye(number_of_nodes) 

        matrix_to_invert = I - (alpha * A_tilde)

        ones_vector = np.ones(number_of_nodes)
        
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
