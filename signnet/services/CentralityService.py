# CentralityService.py
import pandas as pd

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.models.SignedNetwork import SignedNetwork

class CentralityService:
    """
    Executes structural centrality pipelines and handles core graph-metric computations.
    """
    def __init__(self):
        pass

    def execute_centrality_analysis(self, network: SignedNetwork, selected_measures: list) -> pd.DataFrame:
        """Executes the configured centrality metrics and aggregates their scores into a single data matrix.

        Args:
            network (SignedNetwork): The canonical domain representation of the signed network to analyze.
            selected_measures (list): A collection of pre-instantiated centrality algorithm classes 
                loaded with their respective runtime parameters.

        Returns:
            pd.DataFrame: A consolidated data matrix where index rows correspond to unique node identifiers 
                and columns represent individual executed metrics named after their registry identifiers.

        Raises:
            ValueError: If mathematical boundaries or matrix compatibility constraints are violated during runtime.
        """
        # Instantiation
        analysis_pipeline = CentralityAnalysis(measures=selected_measures)
        
        # Execution
        results_df = analysis_pipeline.compute(network)
        
        return results_df
