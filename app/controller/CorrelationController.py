# app/controller/CorrelationController.py
from signnet.services.CorrelationService import CorrelationService
from signnet.analysis.correlations.CorrelationRegistry import CorrelationRegistry
from app.controller.AppState import AppState

class CorrelationController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for statistical correlation analysis.
    """
    def __init__(self):
        self.correlation_service = CorrelationService()

    def run_correlation_analysis(self, app_state: AppState) -> None:
        """Validates structural pre-conditions, executes the correlation service, and updates session outputs.

        Args:
            app_state (AppState): The session-isolated state model of the active user session containing 
                configured parameters and pre-computed centrality data matrices.

        Raises:
            ValueError: If workflow pre-conditions (missing centrality data or insufficient metric filters) 
                are not satisfied.
        """
        # Validation
        if app_state.centrality_results is None:
            raise ValueError("No centrality resulsts available.")

        # Validation
        if app_state.centrality_results.shape[1] < 2: # type: ignore
            raise ValueError("There must be at least two centrality measures.")

        app_state.is_loading = True
        
        try:
            # Strategy definition
            metric_name = app_state.selected_correlation_metric
            strategy_class = CorrelationRegistry.get_measure_class(metric_name) # type: ignore
            strategy_instance = strategy_class()

            # Execute service
            df_corr, df_p_values = self.correlation_service.compute_correlations(
                centrality_df=app_state.centrality_results, # type: ignore
                strategy_instance=strategy_instance
            )

            # Update state
            app_state.correlation_matrix = df_corr
            app_state.p_value_matrix = df_p_values

        finally:
            app_state.is_loading = False
