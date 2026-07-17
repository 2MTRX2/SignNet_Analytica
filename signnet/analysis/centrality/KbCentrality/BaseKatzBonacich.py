# BaseKatzBonacich.py
import numpy as np
import pandas as pd

from ..CentralityMeasure import CentralityMeasure
from signnet.models.SignedNetwork import SignedNetwork
from utils.matrix_factory import MatrixFactory

class BaseKatzBonacich(CentralityMeasure):
    """Engine for versions of the Katz-Bonacich-based centralities."""
    
    def _prepare_core_system(self, network: SignedNetwork):
        if network.directed:
            raise NotImplementedError("PN-centrality currently supports only undirected networks.")
            
        A = MatrixFactory.adjacency(network)
        number_of_nodes = network.number_of_nodes
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
        rows = [{"node": node, column_name: score} for node, score in zip(nodes, scores)]
        results = pd.DataFrame(rows)
        results.set_index("node", inplace=True)
        return results


class KbCentralityBallester(BaseKatzBonacich):
    """
    Implements the Katz-Bonacich centrality as defined by Ballester et al. (2006).

    This variant includes the initial identity component (starts the infinite sum at t=0):
    b(A, δ) = (I - δA)^(-1) * 1 = sum_{t=0}^{inf} δ^t * A^t * 1

    where:
        δ (delta) = 1 / (2n - 2) is the discount factor.
        A = The standard adjacency matrix of the network.
    
    This implementation utilizes NumPy for highly optimized matrix operations.
    """
    
    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        A, delta, matrix_to_invert = self._prepare_core_system(network)
        rhs_vector = np.ones(network.number_of_nodes)
        
        scores = np.linalg.solve(matrix_to_invert, rhs_vector)
        return self._to_dataframe(network.nodes, scores, "kb_centrality_ballester")

class KbCentralitySadler(BaseKatzBonacich):
    """
    Implements the Katz-Bonacich centrality as defined by Sadler (2022).

    This variant shifts the attenuation factor by one step relative to the path lengths:
    c(A, δ) = (I - δA)^(-1) * A * 1 = sum_{t=1}^{inf} δ^(t-1) * A^t * 1

    Mathematical relation to Ballester (2006):
    c(A, δ) = A * b(A, δ)
    
    This implementation utilizes NumPy for highly optimized matrix operations.
    """
    
    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        A, delta, matrix_to_invert = self._prepare_core_system(network)
        
        # # Calculate vector of Ballester
        rhs_ballester = np.ones(network.number_of_nodes)
        b_scores = np.linalg.solve(matrix_to_invert, rhs_ballester)
        
        # transformation to Sadler
        c_sadler_scores = A @ b_scores
        return self._to_dataframe(network.nodes, c_sadler_scores, "kb_centrality_sadler")
