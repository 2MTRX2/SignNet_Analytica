# UploadController.py
from signnet.services.UploadService import NetworkService
from app.controller.AppState import AppState

class UploadController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for network data ingestion.
    """
    def __init__(self):
        self.network_service = NetworkService()

    def process_upload(self, file_buffer, app_state: AppState) -> None:
        """Validates input streams, executes the network parser service, and updates session outputs.

        Args:
            file_buffer (BytesIO | StringIO): Raw file stream from the frontend upload component.
            app_state (AppState): The session-isolated state model of the active user session containing 
                configured column mappings and file definitions.
        """
        app_state.is_loading = True
        
        try:
            # Service Execution
            app_state.current_network = self.network_service.load_and_build_network(
                file_buffer=file_buffer,
                file_type=app_state.selected_file_type,
                representation_type=app_state.selected_repr_type,
                is_directed=app_state.is_directed,
                source_col=app_state.source_column_name,
                target_col=app_state.target_column_name,
                sign_col=app_state.sign_column_name
            )
        finally:
            app_state.is_loading = False
