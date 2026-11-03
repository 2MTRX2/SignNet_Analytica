# AppState.py
from dataclasses import dataclass
from typing import Optional
import pandas as pd

from signnet.models.SignedNetwork import SignedNetwork

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
    current_network: Optional[SignedNetwork] = None

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

    # ==================================================================
    # CENTRALITY ANALYSIS
    # ==================================================================
    selected_measure_names: Optional[list] = None
    runtime_parameters: Optional[dict] = None
    centrality_results: Optional[object] = None 

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
