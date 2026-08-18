# BaseKatzBonacich.py
import numpy as np
import pandas as pd
from typing import Optional

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.models.SignedNetwork import SignedNetwork
from signnet.utils.MatrixFactory import MatrixFactory
from signnet.utils.CentralityResultFormatter import CentralityResultFormatter

class BaseKatzBonacich(CentralityMeasure):
    """Engine for versions of the Katz-Bonacich-based centralities."""

    def __init__(self, delta: Optional[float] = None):
        if delta is not None and delta <= 0:
            raise ValueError("delta must be greater than zero.")
        self._custom_delta = delta
        self._calculated_delta: Optional[float] = None
    
    def _prepare_core_system(self, network: SignedNetwork):
        if network.directed:
            raise NotImplementedError("KB-centrality currently supports only undirected networks.")
            
        number_of_nodes = network.number_of_nodes
        if number_of_nodes <= 1:
            raise ValueError("Katz-Bonacich centrality requires a network with at least 2 nodes to calculate delta.")

        A = MatrixFactory.adjacency(network)
        
        delta = 1.0 / (2 * number_of_nodes - 2)

        # Stability Test
        eigenvalues = np.linalg.eigvals(A)
        max_eigenval = np.max(np.abs(eigenvalues))
        if max_eigenval > 0 and delta >= (1.0 / max_eigenval):
            raise ValueError(f"Delta ({delta}) ist zu gross für die Matrix-Konvergenz.")
            
        I = np.eye(number_of_nodes)
        matrix_to_invert = I - (delta * A)
        
        return A, delta, matrix_to_invert

    def _to_dataframe(self, nodes, scores, column_name: str) -> pd.DataFrame:
         return CentralityResultFormatter.from_array(nodes, scores, column_name)
