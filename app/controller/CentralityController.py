# app/controller/CentralityController.py
from signnet.services.CentralityService import CentralityService
from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry
from app.controller.AppState import AppState  

class CentralityController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for centrality analysis.
    """
    def __init__(self):
        # Der mathematische Service bleibt zustandslos
        self.centrality_service = CentralityService()

    def run_analysis(self, app_state: AppState) -> None:
        """Validates pre-conditions, executes the centrality service, and updates session outputs.

        Args:
            app_state (AppState): The session-isolated state model of the active user session containing 
                configured parameters, domain models, and data repositories.

        Raises:
            ValueError: If workflow pre-conditions (missing network data or metric filters) are not satisfied.
        """
        # Validation
        if not app_state.current_network:
            raise ValueError("No network loaded.")
            
        if not app_state.selected_measure_names:
            raise ValueError("Choose at least one centrality measure.")

        # Loading State
        app_state.is_loading = True
        
        try:
            # Instatiation
            instantiated_measures = []
            for name in app_state.selected_measure_names:
                measure_class = CentralityRegistry.get_measure_class(name)
                # Paramters for a centrality measure
                kwargs = app_state.runtime_parameters.get(name, {}) # type: ignore
                instantiated_measures.append(measure_class(**kwargs))

            # Service Execution
            df_result = self.centrality_service.execute_centrality_analysis(
                network=app_state.current_network,
                selected_measures=instantiated_measures
            )
            
            # Result written into the state object
            app_state.centrality_results = df_result
            
        finally:
            # Loading State
            app_state.is_loading = False
