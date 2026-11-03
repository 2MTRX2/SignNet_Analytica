# GraphBuilderController.py
from signnet.services.GraphBuilderService import GraphBuilderService
from app.controller.AppState import AppState

class GraphBuilderController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for network visualizations.
    """
    def __init__(self):
        self.graph_builder_service = GraphBuilderService()

    def generate_visualization(self, app_state: AppState) -> None:
        """Validates pre-conditions, executes the graph visualizer service, and updates session outputs.

        Args:
            app_state (AppState): The session-isolated state model of the active user session containing 
                the target network domain configuration.

        Raises:
            ValueError: If workflow pre-conditions (missing network data) are not satisfied.
        """
        # Validation
        if not app_state.current_network:
            raise ValueError("No network loaded.")

        app_state.is_loading = True
        
        try:
            # Generate HTML graph
            html_string = self.graph_builder_service.build_network_html(app_state.current_network)
            
            # Update state
            app_state.network_visualization_html = html_string
            
        finally:
            app_state.is_loading = False
