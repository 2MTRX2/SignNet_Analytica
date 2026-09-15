# centrality_page.py

import streamlit as st
import pandas as pd

from signnet.ui.components.centrality_selector import centrality_selector
from signnet.ui.components.network_summary import network_summary
from signnet.ui.components.centrality_measure_parameter_config import configure_centrality_measure_parameters
from signnet.ui.components.correlation_component import render_correlation_analysis
from signnet.ui.components.simulation_parameter_config import configure_topology_parameters
from signnet.ui.components.simulation_topology_selector import simulation_topology_selector


from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry
from signnet.analysis.simulation.SimulationEngine import SimulationEngine
from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry
from signnet.analysis.simulation.NetworkBenchmarker import NetworkBenchmarker


from signnet.models.SignedNetwork import SignedNetwork
from signnet.models.NetworkGenerator import NetworkGenerator


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
        render_correlation_analysis(centrality_df=centrality_df)

        # ==============================================================
        # SIMULATION BENCHMARKING
        # ==============================================================
        st.subheader("Simulation Benchmarking")

        simulation_engine = SimulationEngine(analysis_pipeline=CentralityAnalysis(measures=selected_measures).compute)

        topology_options = TopologyRegistry.get_available_topologies()

        selected_topology = simulation_topology_selector(available_topologies=topology_options)

        global_parameters, kwargs_parameters = configure_topology_parameters(selected_topology=selected_topology)

        start_sim = st.button("Run Simulation Pipeline", type="secondary")

        if start_sim or "active_simulation_results" in st.session_state:
            
            if start_sim:
                with st.spinner(f"Simulating {global_parameters['n_iterations']} networks..."):
                    network_generator = NetworkGenerator(
                        topology_name=selected_topology, 
                        n=global_parameters["n"], 
                        neg_ratio=global_parameters["neg_ratio"], 
                        **kwargs_parameters
                    )
                    
                    sim_result = simulation_engine.run(
                        num_iterations=global_parameters["n_iterations"], 
                        network_provider=network_generator.create_random_signed_network
                    )
                    st.session_state["active_simulation_results"] = sim_result
            
            simulation_result = st.session_state["active_simulation_results"]

            actual_node_col = simulation_result.columns[1]
            extremes_result = NetworkBenchmarker.analyze_network_extremes(df_raw_results=simulation_result, node_col=actual_node_col)
            gini_result = NetworkBenchmarker.calculate_gini_coefficient(df_raw_results=simulation_result)

            tab1, tab2 = st.tabs(["📊 Extreme Values Benchmark", "⚖️ Gini-Coefficient"])
            
            with tab1:
                st.caption("Average benchmark values across all iterations (maxima, minima, and general mean).")
                st.dataframe(extremes_result, use_container_width=True)
            
            with tab2:
                st.caption("Average Gini-Coefficient per metric. Higher values indicate higher structural inequality.")
                st.dataframe(gini_result, use_container_width=True)
                
                st.bar_chart(gini_result, x="metric_name", y="mean_gini_coefficient")

        st.divider()
    
