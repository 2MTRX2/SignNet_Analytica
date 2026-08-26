# KbCentralitySadler.py
import numpy as np
import pandas as pd

from signnet.models.SignedNetwork import SignedNetwork
from signnet.analysis.centrality.centrality_measures.KbCentrality.BaseKatzBonacich import BaseKatzBonacich
from signnet.utils.decorators import require_edges

class KbCentralitySadler(BaseKatzBonacich):
    """
    Implements the Katz-Bonacich centrality as defined by Sadler (2022).

    This variant shifts the attenuation factor by one step relative to the path lengths:
    c(A, δ) = (I - δA)^(-1) * A * 1 = sum_{t=1}^{inf} δ^(t-1) * A^t * 1

    Mathematical relation to Ballester (2006):
    c(A, δ) = A * b(A, δ)
    
    This implementation utilizes NumPy for highly optimized matrix operations.
    """
    @property
    def name(self) -> str:
        return "K-B (Sadler, t=1 with d=t-1)"

    @require_edges
    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        A, delta, matrix_to_invert = self._prepare_core_system(network)
        
        # calculate vector of Ballester
        rhs_ballester = np.ones(network.number_of_nodes)
        b_scores = np.linalg.solve(matrix_to_invert, rhs_ballester)
        
        # transformation to Sadler
        c_sadler_scores = A @ b_scores
        return self._to_dataframe(network.nodes, c_sadler_scores, self.name)