# PnCentrality.py
import numpy as np
import pandas as pd

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.MatrixFactory import MatrixFactory
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter

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
    @property
    def name(self) -> str:
        return "PN"

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

        if number_of_nodes <= 1:
            raise ValueError("PN-centrality requires a network with at least 2 nodes to calculate alpha.")

        alpha = 1.0 / (2*number_of_nodes - 2)

        eigenvalues = np.linalg.eigvals(A_tilde)
        max_eigenval = np.max(np.abs(eigenvalues))

        if max_eigenval > 0 and alpha >= (1.0 / max_eigenval):
            raise ValueError(
                f"Alpha ({alpha}) is too large for matrix convergence with this specific dataset. "
                f"It must be smaller than 1 / |lambda_max| = {1.0 / max_eigenval:.4f}"
            )

        # apply formula: PN = (I - alpha * A_tilde)^(-1) * 1
        I = np.eye(number_of_nodes) 
        matrix_to_invert = I - (alpha * A_tilde)
        ones_vector = np.ones(number_of_nodes)
        
        try:
            pn_scores = np.linalg.solve(matrix_to_invert, ones_vector)
        except np.linalg.LinAlgError:
            raise ValueError("Matrix is singular and cannot be inverted.")

        # mapping to the pandas dataframe
        return CentralityResultFormatter.from_array(nodes, pn_scores, self.name)
