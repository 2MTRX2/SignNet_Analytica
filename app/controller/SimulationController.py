# SimulationController.py
from signnet.services.SimulationService import SimulationService
from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry
from app.controller.AppState import AppState

class SimulationController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for simulation benchmarking.
    """
    def __init__(self):
        self.simulation_service = SimulationService()

    def execute_simulation_pipeline(self, app_state: AppState) -> None:
        """Validates pre-conditions, runs the mathematical simulation service, and updates session outputs.

        Args:
            state (AppState): The session-isolated state model of the active user session containing 
                configured parameters and data repositories.

        Raises:
            ValueError: If workflow pre-conditions (missing network data or metric filters) are not satisfied.
        """
        if not app_state.current_network:
            raise ValueError("No network loaded.")
        if not app_state.selected_measure_names:
            raise ValueError("No selected centrality measures.")

        app_state.is_loading = True

        try:
            # Define centrality measures
            instantiated_measures = []
            for name in app_state.selected_measure_names:
                measure_class = CentralityRegistry.get_measure_class(name)
                kwargs = app_state.runtime_parameters.get(name, {}) # type: ignore
                instantiated_measures.append(measure_class(**kwargs))
            
            analysis_pipeline = CentralityAnalysis(measures=instantiated_measures)

            # Execute Simulation
            df_raw, df_extremes, df_gini = self.simulation_service.run_benchmark_simulation(
                topology_name=app_state.selected_topology, # type: ignore
                global_parameters=app_state.sim_global_parameters, # type: ignore
                kwargs_parameters=app_state.sim_topology_kwargs, # type: ignore
                compute_pipeline=analysis_pipeline.compute
            )

            # Update state
            app_state.sim_raw_results = df_raw
            app_state.sim_extremes_results = df_extremes
            app_state.sim_gini_results = df_gini

            # Empiric baselines
            if app_state.centrality_results is not None:
                # Empirical Extremes
                app_state.sim_empirical_summary = self.simulation_service.compute_empirical_summary(
                    centrality_df=app_state.centrality_results # type: ignore
                )
                
                # Empirical Gini
                app_state.sim_empirical_gini = self.simulation_service.compute_empirical_gini(
                    centrality_df=app_state.centrality_results # type: ignore
                )

        finally:
            app_state.is_loading = False
