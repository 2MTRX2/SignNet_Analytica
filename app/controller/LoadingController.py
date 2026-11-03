# LoadingController.py
from signnet.services.LoadingService import NetworkService
from app.controller.AppState import AppState

from signnet.io.DatasetRegistry import DatasetRegistry

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


    def process_predefined_upload(self, dataset_name: str, app_state: AppState) -> None:
        """Validates, retrieves, and parses a server-side sample network dataset into the session state.

        Args:
            dataset_name (str): The unique identifier key of the sample dataset registered in the system.
            app_state (AppState): The session-isolated state model of the active user session where 
                the parsed network and format states will be committed.

        Raises:
            FileNotFoundError: If the resolved storage path does not exist on the host system.
            ValueError: If the underlying file parser or topological constraints encounter validation errors.
        """
        app_state.is_loading = True
        
        try:
            # Meta data from registry
            dataset_info = DatasetRegistry.get_info(dataset_name)
            file_path = DatasetRegistry.get_file_path(dataset_name)

            # Open data
            with open(file_path, "rb") as file_buffer:
                # Read file
                app_state.current_network = self.network_service.load_and_build_network(
                    file_buffer=file_buffer,# type: ignore
                    file_type=dataset_info.file_type,
                    representation_type=dataset_info.representation_type,
                    is_directed=False, 
                    source_col='source', 
                    target_col='target',
                    sign_col='sign'
                )
                
                # Update UI-Dropdowns state
                app_state.selected_file_type = dataset_info.file_type
                app_state.selected_repr_type = dataset_info.representation_type
                
        finally:
            app_state.is_loading = False
