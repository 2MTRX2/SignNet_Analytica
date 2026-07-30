# centrality_page.py

import streamlit as st
import pandas as pd

from signnet.ui.components.centrality_selector import centrality_selector
from signnet.ui.components.network_summary import network_summary
from signnet.ui.components.parameter_config import configure_parameters
from signnet.ui.components.correlation_component import render_correlation_analysis


from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry
from signnet.analysis.correlations.CorrelationAnalysis import CorrelationAnalysis
from signnet.analysis.correlations.CorrelationRegistry import CorrelationRegistry

from signnet.models.SignedNetwork import SignedNetwork


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

    Args:
        network (SignedNetwork): The active network domain model containing 
                                 the vertices and edges.
    """
    # ------------------------------------------------------------------
    # RENDER NETWROK STRUCTURAL SUMMARY
    # ------------------------------------------------------------------
    network_summary(network)

    st.divider()

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
        runtime_parameters = configure_parameters(selected_names)
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
    hash_components = [f"net_nodes_{len(network.nodes)}_edges_{len(network.edges)}"]
    
    for name in sorted(selected_names):
        hash_components.append(name)
       
        if name in runtime_parameters:
            for p_name, p_val in sorted(runtime_parameters[name].items()):
                hash_components.append(f"{p_name}:{p_val}")
                
    expected_state_key = f"params_{'_'.join(hash_components)}"
    
    if st.button("Run Analysis", type="primary"):
        # Wrap execution in a native spinner for complex network operations
        with st.spinner("Calculating selected metrics..."):
            try:
                analysis = CentralityAnalysis(measures=selected_measures)
                st.session_state["active_centrality_results"] = analysis.compute(network)
                st.session_state["current_param_hash"] = expected_state_key
            except ValueError as val_ex:
                st.error(f"Mathematical Constraint Error:\n\n{val_ex}")
            except Exception as ex:
                st.error(f"Failed to run analysis:\n\n{ex}")

    # ------------------------------------------------------------------
    # RENDER RESULTS TABLE IF A RESULT IS IN THE CURRENT SESSION STATE
    # ------------------------------------------------------------------
    # If there is any result in the session state, the results get displayed
    if "active_centrality_results" in st.session_state:
        if st.session_state.get("current_param_hash") != expected_state_key:
            st.warning("You changed parameters above. Click 'Run Analysis' to update the data, or proceed with the current results below.")
            is_stale = True
        else: 
            is_stale = False

        st.subheader("Results")

        centrality_df = st.session_state["active_centrality_results"]

        # If the result doesn't apply to the current parameters, the dataframe is in gray style
        if is_stale:
            styled_df = centrality_df.style.map(lambda _: "color: rgba(120, 120, 120, 0.5);")
        else:
            styled_df = centrality_df

        st.dataframe(
            styled_df,
            use_container_width=True,
        )

        st.divider()
    
        # ==============================================================
        # CENTRALITY CORRELATION ANALYSIS
        # ==============================================================
        render_correlation_analysis(
            centrality_df=centrality_df,
            correlation_registry=CorrelationRegistry,
            analysis_class=CorrelationAnalysis,
        )
