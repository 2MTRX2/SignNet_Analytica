# KbCentralitySadler.py
import numpy as np
import pandas as pd

from signnet.models.StaticSignedNetwork import SignedNetwork
from .BaseKatzBonacich import BaseKatzBonacich

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