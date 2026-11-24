# AppState.py
from dataclasses import dataclass
from typing import Optional
import pandas as pd
from nicegui import app

from signnet.models.SignedNetwork import SignedNetwork

@dataclass
class NetworkStats:
    filename: str
    is_directed: bool
    num_nodes: int
    num_edges: int
    num_components: int
    num_isolated_nodes: int
    negative_edge_ratio: float    
    balanced_triad_ratio: float   
    density: float                

@dataclass
class NetworkBundle:
    network: SignedNetwork
    stats: Optional[NetworkStats] = None
    visualization_html: Optional[str] = None

@dataclass
class AppState:
    """
    Defines the structural schema and lifecycle fields for session-isolated application states.

    This data class serves as the unified, strongly typed state repository for an individual user session 
    within the NiceGUI web ecosystem. It decouples reactive interface components from stateless analytical 
    backends by tracking interactive selection states, raw file configurations, graph domain models, and 
    the resulting multi-variate statistical dataframes. To guarantee safe multi-user execution, instances 
    of this schema are stored inside transient client slots (`app.storage.tab`) on the application server.
    """
    # ==================================================================
    # GENERAL APPLICATION STATE
    # ==================================================================
    is_loading: bool = False
    is_current: bool = True

    # ------------------------------------------------------------------
    # NETWORK
    # ------------------------------------------------------------------
    loaded: Optional[NetworkBundle] = None
    selected: Optional[NetworkBundle] = None

    # ==================================================================
    # FILE LOADING
    # ==================================================================
    selected_file_type: str = 'csv'
    selected_repr_type: str = 'Edge List'
    is_directed: bool = False

    # ------------------------------------------------------------------
    # COLUMN MAPPING
    # ------------------------------------------------------------------
    source_column_name: str = 'source'
    target_column_name: str = 'target'
    sign_column_name: str = 'sign'

    available_columns: Optional[list] = None 

    # ==================================================================
    # CENTRALITY ANALYSIS
    # ==================================================================
    selected_measure_names: Optional[list] = None
    runtime_parameters: Optional[dict] = None

    # Wir benennen das interne Feld um
    centrality_results: Optional[pd.DataFrame] = None

    # ------------------------------------------------------------------
    # CORRELATION ANALYSIS
    # ------------------------------------------------------------------
    selected_correlation_metric: Optional[str] = None
    selected_alpha: Optional[float] = None
    correlation_matrix: Optional[pd.DataFrame] = None
    p_value_matrix: Optional[pd.DataFrame] = None

    # ------------------------------------------------------------------
    # CENTRALITY SIMULATION
    # ------------------------------------------------------------------
    selected_topology: Optional[str] = None
    sim_global_parameters: Optional[dict] = None
    sim_topology_kwargs: Optional[dict] = None

    sim_raw_results: Optional[pd.DataFrame] = None
    sim_extremes_results: Optional[pd.DataFrame] = None
    sim_gini_results: Optional[pd.DataFrame] = None

    sim_empirical_summary: Optional[pd.DataFrame] = None
    sim_empirical_gini: Optional[pd.DataFrame] = None

    # ==================================================================
    # INITALISATION
    # ==================================================================
    def __post_init__(self):
        """Safe initialisation of lists and dictionaries to break class-level reference sharing.

        Enforces individual memory allocation for mutable collections per session instance, 
        preventing state pollution across distinct web clients. It pre-populates default 
        scientific parameters to ensure immediate, error-free data binding to active frontend components.
        """
        if self.selected_measure_names is None:
            self.selected_measure_names = []
        if self.runtime_parameters is None:
            self.runtime_parameters = {}

        if self.sim_global_parameters is None:
            self.sim_global_parameters = {"n": 100, "neg_ratio": 0.2, "n_iterations": 10}
        if self.sim_topology_kwargs is None:
            self.sim_topology_kwargs = {}

def get_session_state() -> AppState:
    """Retrieves or initializes the session-isolated AppState instance for the current browser tab.

    Returns:
        AppState: The unique, strongly typed state repository dedicated exclusively 
            to the active user's web session thread.
    """
    if 'state' not in app.storage.tab:
        app.storage.tab['state'] = AppState()
    return app.storage.tab['state']

