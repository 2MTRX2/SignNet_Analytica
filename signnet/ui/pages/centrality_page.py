# centrality_page.py
import streamlit as st

from signnet.ui.components.centrality_selector import centrality_selector
from signnet.ui.components.network_summary import network_summary
from signnet.ui.components.centrality_measure_parameter_config import configure_centrality_measure_parameters
from signnet.ui.components.correlation_component import render_correlation_analysis
from signnet.ui.components.simulation_component import render_benchmarking_centrality_analysis
from signnet.ui.components.grayout_stale_df import grayout_df
from signnet.ui.components.grayout_stale_df import is_stale

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry

from signnet.models.SignedNetwork import SignedNetwork

from signnet.utils.StateKeyGenerator import StateKeyGenerator


def show(network: SignedNetwork):
    """
    Displays the Centrality Analysis section.

    This component provides a sequential workflow allowing the user to:
    1. Inspect the structural metrics of the loaded signed network.
    2. Choose from multiple signed network centrality measures.
    3. Dynamically configure parameters based on the selected measures.
    4. Execute the mathematical analysis using the selected algorithms.
    5. Render and inspect the final data results in a persistent table view.
    6. Perform a correlation analysis including the corresponding p-values.
    7. Perform a benchmark simulation with a given topology as parameters

    Args:
        network (SignedNetwork): The active network domain model containing 
                                 the vertices and edges.
    """
    # ------------------------------------------------------------------
    # RENDER NETWROK STRUCTURAL SUMMARY
    # ------------------------------------------------------------------
    network_summary(network)

    # ------------------------------------------------------------------
    # DEFINE AND COLLECT SELECTED CENTRALITY MEASURES
    # ------------------------------------------------------------------
    measure_options = CentralityRegistry.get_available_names()

    # Display the list and return the selection
    selected_names = centrality_selector(measure_options)

    # Halt execution early if no measures are chosen yet
    if not selected_names:
        st.info("Please select at least one centrality measure to proceed.")
        return

    st.divider()

    # ------------------------------------------------------------------
    # DEFINE DEFAULT PARAMETER VALUES FOR ADVANCED MEASURES
    # ------------------------------------------------------------------
    # Checks if at least one measure has parameters to define
    has_parameters = any(len(CentralityRegistry.get_measure_class(name).PARAMETERS) > 0 for name in selected_names)

    if has_parameters:
        # Sets up the parameter input fields and their borders
        runtime_parameters = configure_centrality_measure_parameters(selected_names)
    else: 
        runtime_parameters = {}

    # ------------------------------------------------------------------
    # MAP SELECTED NAMES TO CONFIGURED CLASS INSTANCES
    # ------------------------------------------------------------------
    selected_measures = []

    # Instantiate the selected centrality measures
    for name in selected_names:
        measure_class = CentralityRegistry.get_measure_class(name)

        kwargs = runtime_parameters.get(name, {}) 
        instance = measure_class(**kwargs)
            
        selected_measures.append(instance)

    # ------------------------------------------------------------------
    # EXECUTE ANALYSIS AND MANAGE SESSION STATE PERSISTANCE
    # ------------------------------------------------------------------
    st.subheader("Run Analysis")

    # Generate a unique hash key containing network numbers of nodes and edges 
    # and the selected centrality measures including their parameters. 
    # This automatically clears old results from the screen if parameters or metrics change.
    expected_state_key_centrality = (
        StateKeyGenerator(prefix="params")
        .add_network(network)
        .add_measures_with_parameters(selected_names, runtime_parameters)
        .generate()
    )

    button_centrality_name = "Run Analysis"

    if st.button(button_centrality_name, type="primary"):
        # Wrap execution in a native spinner for complex network operations
        with st.spinner("Calculating selected metrics..."):
            try:
                analysis = CentralityAnalysis(measures=selected_measures)
                st.session_state["active_centrality_results"] = analysis.compute(network)
                st.session_state["current_param_hash"] = expected_state_key_centrality
            except ValueError as val_ex:
                st.error(f"Mathematical Constraint Error:\n\n{val_ex}")
            except Exception as ex:
                st.error(f"Failed to run analysis:\n\n{ex}")

    # ------------------------------------------------------------------
    # RENDER RESULTS TABLE IF A RESULT IS IN THE CURRENT SESSION STATE
    # ------------------------------------------------------------------
    # If there is any result in the session state, the results get displayed
    if "active_centrality_results" in st.session_state:
        current_hash = st.session_state.get("current_param_hash")
        centrality_df = st.session_state["active_centrality_results"]

        bool_is_stale = is_stale(current_hash=current_hash, expected_hash=expected_state_key_centrality, button=button_centrality_name)
        st.subheader("Results")
        styled_df = grayout_df(session_state_df=centrality_df, is_stale=bool_is_stale)
        
        st.dataframe(
            styled_df,
            use_container_width=True,
        )

        st.divider()

        # ==============================================================
        # CENTRALITY CORRELATION ANALYSIS
        # ==============================================================
        render_correlation_analysis(centrality_df=centrality_df)

        # ==============================================================
        # SIMULATION BENCHMARKING
        # ==============================================================
        render_benchmarking_centrality_analysis(network=network, centrality_df=centrality_df, selected_measures=selected_measures, 
                                                selected_names=selected_names, runtime_parameters=runtime_parameters, current_state_key_centrality=current_hash, 
                                                expected_state_key_centrality=expected_state_key_centrality, button_centrality_name=button_centrality_name)


