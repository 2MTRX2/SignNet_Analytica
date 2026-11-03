# SimulationService.py
import pandas as pd
from typing import Tuple, Callable, Any

from signnet.analysis.simulation.SimulationEngine import SimulationEngine
from signnet.analysis.simulation.NetworkBenchmarker import NetworkBenchmarker
from signnet.models.NetworkGenerator import NetworkGenerator

class SimulationService:
    """
    Executes multi-iteration network simulations and computes statistical benchmarking metrics.
    """
    def __init__(self):
        pass

    def run_benchmark_simulation(
        self,
        topology_name: str,
        global_parameters: dict,
        kwargs_parameters: dict,
        compute_pipeline: Callable[[Any], pd.DataFrame]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Runs the simulation engine across multiple iterations and computes raw and aggregated benchmarks.

        Args:
            topology_name (str): Identifier of the synthetic network model (e.g., 'Erdos-Renyi').
            global_parameters (dict): Core pipeline parameters containing 'n', 'neg_ratio', and 'n_iterations'.
            kwargs_parameters (dict): Topology-specific parameters parsed dynamically from the registry.
            compute_pipeline (Callable): The structural analysis execution method derived from CentralityAnalysis or other classes.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: A tuple containing three dataframes:
                - df_raw_results: The full unaggregated simulation results across all nodes and iterations.
                - df_extremes: Aggregated benchmark profiles focusing on minima, maxima, and metric means.
                - df_gini: Aggregated structural inequality profiles represented as mean Gini coefficients.

        Raises:
            ValueError: If mathematical boundaries or topology constraints are violated during runtime.
        """
        # SimulationEngine Initialisation
        engine = SimulationEngine(
            analysis_pipeline=compute_pipeline, 
            default_index_label="node"
        )

        # Network Generator Initialisation
        generator = NetworkGenerator(
            topology_name=topology_name,
            n=global_parameters["n"],
            neg_ratio=global_parameters["neg_ratio"],
            **kwargs_parameters
        )

        # Run the simulation
        df_raw_results = engine.run(
            num_iterations=global_parameters["n_iterations"],
            network_provider=generator.create_random_signed_network
        )

        # Aggregate benchmarks
        node_column = df_raw_results.columns[1]
        df_extremes = NetworkBenchmarker.analyze_network_extremes(
            df_raw_results=df_raw_results, 
            node_col=node_column
        )
        df_gini = NetworkBenchmarker.calculate_gini_coefficient(
            df_raw_results=df_raw_results
        )

        return df_raw_results, df_extremes, df_gini

    def compute_empirical_summary(self, centrality_df: pd.DataFrame) -> pd.DataFrame:
        """Computes structural baseline extreme metrics directly on the empirical real-world network.

        Args:
            centrality_df (pd.DataFrame): The pre-computed centrality data matrix from the empirical network.

        Returns:
            pd.DataFrame: A formatted statistical summary of the empirical network's extreme metrics.
        """
        df_empirical = centrality_df.copy()

        # Colmun strcuture
        if "iteration" not in df_empirical.columns:
            df_empirical.insert(0, "iteration", 0)
        elif df_empirical.columns[0] != "iteration":
            cols = ["iteration"] + [c for c in df_empirical.columns if c != "iteration"]
            df_empirical = df_empirical[cols]

        if "node" not in df_empirical.columns:
            df_empirical["node"] = df_empirical.index

        # Execution
        empirical_summary = NetworkBenchmarker.analyze_network_extremes(
            df_raw_results=df_empirical, 
            node_col="node"
        )

        # Adapting column names
        empirical_summary.rename(columns={
            "mean_of_maxima": "maxima",
            "mean_of_minima": "minima"
        }, inplace=True)
        
        return empirical_summary

    def compute_empirical_gini(self, centrality_df: pd.DataFrame) -> pd.DataFrame:
        """Computes baseline structural inequality profiles directly on the empirical real-world network.

        Args:
            centrality_df (pd.DataFrame): The pre-computed centrality data matrix from the empirical network.

        Returns:
            pd.DataFrame: A unified matrix containing the calculated baseline Gini coefficients per metric.
        """
        df_empirical = centrality_df.copy()

        # Colmun strcuture
        if "iteration" not in df_empirical.columns:
            df_empirical.insert(0, "iteration", 0)
        elif df_empirical.columns[0] != "iteration":
            cols = ["iteration"] + [c for c in df_empirical.columns if c != "iteration"]
            df_empirical = df_empirical[cols]

        if "node" not in df_empirical.columns:
            df_empirical["node"] = df_empirical.index

        # Execution
        empirical_gini = NetworkBenchmarker.calculate_gini_coefficient(
            df_raw_results=df_empirical, 
            node_col="node"
        )
        
        # Adapting column names
        empirical_gini.rename(columns={
            "mean_gini_coefficient": "gini_coefficient",
        }, inplace=True)
        
        return empirical_gini
