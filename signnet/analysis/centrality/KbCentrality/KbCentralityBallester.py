# KbCentralityBallester.py
import numpy as np
import pandas as pd

from signnet.models.StaticSignedNetwork import StaticSignedNetwork
from .BaseKatzBonacich import BaseKatzBonacich

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
    
    def compute(self, network: StaticSignedNetwork) -> pd.DataFrame:
        A, delta, matrix_to_invert = self._prepare_core_system(network)
        rhs_vector = np.ones(network.number_of_nodes)
        
        scores = np.linalg.solve(matrix_to_invert, rhs_vector)
        return self._to_dataframe(network.nodes, scores, "kb_centrality_ballester")
