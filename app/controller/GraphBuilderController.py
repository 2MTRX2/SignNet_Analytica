# GraphBuilderController.py
from typing import Optional
from app.controller.AppState import AppState, NetworkBundle
from signnet.services.GraphBuilderService import GraphBuilderService

class GraphBuilderController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for network visualizations.
    """
    def __init__(self):
        self.graph_builder_service = GraphBuilderService()

    def generate_visualization(self, bundle: Optional[NetworkBundle], app_state: AppState) -> None:
        """Validates pre-conditions, executes the graph visualizer service, and updates the target bundle.

        Args:
            bundle (Optional[NetworkBundle]): The target network bundle (e.g., app_state.loaded or app_state.selected)
                containing the network to visualize and where the HTML output will be stored.
            app_state (AppState): The session-isolated state model for managing global loading flags.

        Raises:
            ValueError: If no valid network bundle is provided.
        """
        # Validation
        if not bundle or not bundle.network:
            raise ValueError("No network available to visualize.")

        app_state.is_loading = True
        
        try:
            # Generate HTML graph
            html_string = self.graph_builder_service.build_network_html(bundle.network)
            
            # Speichert das Ergebnis direkt im übergebenen Bundle (loaded ODER selected)
            bundle.visualization_html = html_string
            
        finally:
            app_state.is_loading = False

