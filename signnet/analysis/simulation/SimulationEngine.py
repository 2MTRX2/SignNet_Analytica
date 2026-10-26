# SimulationEngine.py
from typing import Callable, Union
import pandas as pd

from signnet.models.SignedNetwork import SignedNetwork

class SimulationEngine:
    """Engine to execute a generic Monte-Carlo-simulation.

    Attributes:
        analysis_pipeline (Callable[[SignedNetwork], pd.DataFrame]): Function or bounded method
            to an object (e.g. CentralityAnalysis.compute), which gets executed each iteration. 
    """
    def __init__(self, analysis_pipeline: Callable[[SignedNetwork], pd.DataFrame], default_index_label: str = "node"):
        self.analysis_pipeline = analysis_pipeline
        self.default_index_label = default_index_label

    def run(
        self, 
        num_iterations: int, 
        network_provider: Union[Callable[[], SignedNetwork], SignedNetwork]
    ) -> pd.DataFrame:
        """Executes the simulation iteration.

        The method normalises the `network_provider` at the entry point. Every iteration
        a network is provided and analysed. The result has an iteration identification column.

        Args:
            iterations (int): The number of simulation iterations.
            network_provider (Union[Callable[[], SignedNetwork], SignedNetwork]): Either
                a generator-function that creates at each call a new network, 
                or an existing `SignedNetwork`-object, which is a static basis for each iteration.

        Returns:
            pd.DataFrame: A consolidated raw-data pandas dataframe, which contains the results listed in order. 
                Each row represents a node in a specific iteration.  The first data-column is always an iteration index.

        Raises:
            AttributeError: If a `SignedNetwork`-object is handed over, 
                which doesn't include a working `.copy()`-method.
        """
        
        # 1. Normalisation: If it is an object create a function out of it that can be called 
        if not callable(network_provider):
            # Object gets a local function (closure)
            # .copy() insures that each time a new network gets created
            fixed_network = network_provider
            network_provider = lambda: fixed_network.copy()

        all_iteration_data = []

        # 2. Loop through the simulation
        for iteration in range(num_iterations):
            # network_provider is guranteed a callable
            network = network_provider()
            # analysis pipeline function gets invoked (e.g. CentralityAnalysis calculate)
            df_step = self.analysis_pipeline(network)
            
            df_step = df_step.copy()
            index_label = df_step.index.name or self.default_index_label
            df_step = df_step.reset_index(names=index_label)
            df_step.insert(0, "iteration", iteration)
            all_iteration_data.append(df_step)

        return pd.concat(all_iteration_data, ignore_index=True)
