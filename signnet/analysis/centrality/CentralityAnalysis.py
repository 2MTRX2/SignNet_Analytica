# CentralityAnalysis.py
import pandas as pd

from signnet.analysis.centrality.centrality_measures.CentralityMeasure import CentralityMeasure
from signnet.models.SignedNetwork import SignedNetwork


class CentralityAnalysis:
    """
    Orchestrates the computation of multiple centrality measures for a signed network.

    This class serves as the central analysis hub, taking a collection of 
    configured centrality measures and executing them sequentially against 
    a domain network object. It consolidates the distinct result vectors into 
    a single tabular representation optimized for downstream visualization 
    and reporting tools (such as Streamlit dashboards).
    """

    def __init__(self, measures: list[CentralityMeasure]):
        """Initializes the CentralityAnalysis pipeline with a list of measures.

        Args:
            measures (list[CentralityMeasure]): A list of instantiated centrality 
                measure objects (e.g., PiiCentrality, PnCentrality, SignedDegreeCentrality) 
                to be computed for the network.
        """
        self._measures = measures

    def compute(self, network: SignedNetwork) -> pd.DataFrame:
        """Executes all configured centrality measures and aggregates their scores.

        Each individual measure computes its scores for all nodes in the network 
        (including isolated nodes) and returns a DataFrame indexed by node identifiers. 
        This method combines them horizontally by aligning their indexes.

        Args:
            network (SignedNetwork): The canonical domain representation of the 
                signed network to analyze.

        Returns:
            pd.DataFrame: A consolidated table where the rows correspond to unique 
                node identifiers (the index named 'node') and the columns represent 
                the individual metrics named after each centrality measure's identifier.
        """

        results = []

        for measure in self._measures:
            results.append(
                measure.compute(network)
            )

        return pd.concat(results, axis=1)