# LoadingController.py
from dataclasses import replace

from signnet.services.LoadingService import LoadingService
from signnet.services.NetworkStatsService import NetworkStatsService
from app.controller.AppState import AppState, NetworkBundle, NetworkStats

from signnet.io.DatasetRegistry import DatasetRegistry

class LoadingController:
    """
    Manages session-state boundaries and coordinates lifecycle actions for network data ingestion.
    """
    def __init__(self):
        self.network_service = LoadingService()
        self.stats_service = NetworkStatsService()

    def _create_bundle(self, net, filename: str, is_directed: bool) -> NetworkBundle:
        raw_stats = self.stats_service.compute_stats(net)
        stats = NetworkStats(
            filename=filename,
            is_directed=is_directed,
            **raw_stats
        )
        return NetworkBundle(network=net, stats=stats)

    def process_upload(self, file_buffer, app_state: AppState, filename) -> None:
        """Validates input streams, executes the network parser service, and updates session outputs.

        Args:
            file_buffer (BytesIO | StringIO): Raw file stream from the frontend upload component.
            app_state (AppState): The session-isolated state model of the active user session containing 
                configured column mappings and file definitions.
        """
        app_state.is_loading = True
        
        try:
            # Service Execution
            net = self.network_service.load_and_build_network(
                file_buffer=file_buffer,
                file_type=app_state.selected_file_type,
                representation_type=app_state.selected_repr_type,
                is_directed=app_state.is_directed,
                source_col=app_state.source_column_name,
                target_col=app_state.target_column_name,
                sign_col=app_state.sign_column_name
            )

            app_state.loaded = self._create_bundle(net, filename=filename, is_directed=app_state.is_directed)
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
                net = self.network_service.load_and_build_network(
                    file_buffer=file_buffer,# type: ignore
                    file_type=dataset_info.file_type,
                    representation_type=dataset_info.representation_type,
                    is_directed=False, 
                    source_col='source', 
                    target_col='target',
                    sign_col='sign'
                )

                app_state.loaded = self._create_bundle(net, filename=dataset_name, is_directed=False)
                
                # Update UI-Dropdowns state
                app_state.selected_file_type = dataset_info.file_type
                app_state.selected_repr_type = dataset_info.representation_type
                
        finally:
            app_state.is_loading = False


    def commit_loaded_network(self, app_state: AppState) -> None:
        """The loaded network is selected as the active network."""
        if not app_state.loaded:
            raise ValueError("No loaded network available to select.")
                
        app_state.selected = replace(app_state.loaded)
