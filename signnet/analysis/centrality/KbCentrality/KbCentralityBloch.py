# KbCentralityBloch.py
import numpy as np
import pandas as pd

from signnet.models.StaticSignedNetwork import SignedNetwork
from .BaseKatzBonacich import BaseKatzBonacich

class KbCentralityBloch(BaseKatzBonacich):
    """
    Implements the Katz-Bonacich centrality as defined by Bloch et al. (2023).

    This variant excludes the initial identity component (starts the infinite sum at t=1):
    c(A, δ) = δA * (I - δA)^(-1) * 1 = sum_{t=1}^{inf} δ^t * A^t * 1

    Mathematical relation to Ballester (2006):
    c(A, δ) = b(A, δ) + 1 = δA * b(A, δ)
    
    This implementation utilizes NumPy for highly optimized matrix operations.
    """
    
    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        A, delta, matrix_to_invert = self._prepare_core_system(network)
        
        # Calculate vector of Ballester
        rhs_ballester = np.ones(network.number_of_nodes)
        b_scores = np.linalg.solve(matrix_to_invert, rhs_ballester)
        
        # transformation to Bloch
        c_scores = delta * (A @ b_scores)
        return self._to_dataframe(network.nodes, c_scores, "kb_centrality_bloch")