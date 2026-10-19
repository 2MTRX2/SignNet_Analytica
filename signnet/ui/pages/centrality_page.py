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

        global_parameters, kwargs_parameters = configure_topology_parameters(selected_topology=selected_topology, number_of_nodes=network.number_of_nodes, number_of_edges=network.number_of_edges)
      
        # Base string with original network properties
        hash_components_simulation = [
            f"net_nodes_{len(network.nodes)}_edges_{len(network.edges)}",
            f"sim_topology_{selected_topology}",
            f"sim_n_{global_parameters['n']}",
            f"sim_negratio_{global_parameters['neg_ratio']}",
            f"sim_iters_{global_parameters['n_iterations']}"
        ]
        
        # Add topology-specific kwargs to the hash (e.g., m or p values)
        for k_name, k_val in sorted(kwargs_parameters.items()):
            hash_components_simulation.append(f"kw_{k_name}:{k_val}")
        
        # Add metric configurations
        for name in sorted(selected_names):
            hash_components_simulation.append(name)
        
            if name in runtime_parameters:
                for p_name, p_val in sorted(runtime_parameters[name].items()):
                    hash_components_simulation.append(f"{p_name}:{p_val}")
                    
        expected_state_key_simulation = f"params_{'_'.join(hash_components_simulation)}"

        
        if st.button("Run Simulation Pipeline", type="secondary"):
            # Wrap execution in a native spinner for complex network simulation
            with st.spinner(f"Simulating {global_parameters['n_iterations']} networks..."):
                try:
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
                    st.session_state["current_param_hash_simulation"] = expected_state_key_simulation
                except ValueError as val_ex:
                    st.error(f"Mathematical Constraint Error:\n\n{val_ex}")
                except Exception as ex:
                    st.error(f"Failed to run analysis:\n\n{ex}")

        # ------------------------------------------------------------------
        # RENDER RESULTS TABLE IF A RESULT IS IN THE CURRENT SESSION STATE OF THE SIMULATION
        # ------------------------------------------------------------------
        # If there is any result in the session state, the results get displayed
        if "active_simulation_results" in st.session_state:
            if st.session_state.get("current_param_hash_simulation") != expected_state_key_simulation:
                st.warning("You changed parameters above. Click 'Run Simulation Pipeline' to update the data, or proceed with the current results below.")
                is_stale = True
            else: 
                is_stale = False

            # Getting current results
            simulation_result  = st.session_state["active_simulation_results"]

            id_column = simulation_result.columns[1]
            extremes_result = NetworkBenchmarker.analyze_network_extremes(df_raw_results=simulation_result, node_col=id_column)
            gini_result = NetworkBenchmarker.calculate_gini_coefficient(df_raw_results=simulation_result)

            # Dynamic meta-data extraction
            meta_parts = [
                f"Topo: {selected_topology}",
                f"N: {global_parameters['n']}",
                f"Iter: {global_parameters['n_iterations']}",
                f"Neg_Ratio: {global_parameters['neg_ratio']}"
            ]
            for param_name, param_value in kwargs_parameters.items():
                meta_parts.append(f"{param_name}: {param_value}")
                
            meta_string = " | ".join(meta_parts)

            # Greyscaling of result df when current parameters are not coherent with displayed results
            if is_stale:
                extremes_styled_df = extremes_result.style.map(lambda _: "color: rgba(120, 120, 120, 0.5);")
                gini_styled_df = gini_result.style.map(lambda _: "color: rgba(120, 120, 120, 0.5);")
            else:
                extremes_styled_df = extremes_result
                gini_styled_df = gini_result

            # Adding meta-data to the download file
            csv_extremes_bytes = (meta_string + "\n" + extremes_result.reset_index().to_csv(index=False)).encode("utf-8")
            csv_gini_bytes = (meta_string + "\n" + gini_result.reset_index().to_csv(index=False)).encode("utf-8")

            # Ui tabs
            tab1, tab2 = st.tabs(["📊 Extreme Values Benchmark", "⚖️ Gini-Coefficient"])
            
            with tab1:
                st.caption("Average benchmark values across all iterations (maxima, minima, and general mean).")
                st.dataframe(extremes_styled_df, use_container_width=True)

                # Download button to download df inclusive meta-data
                st.download_button(
                    label="Download Extreme Values (CSV) (inclusive Meta-Data)",
                    data=csv_extremes_bytes,
                    file_name=f"sim_extremes_{selected_topology.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    key="download_extremes_btn_final"
                )

                if "active_centrality_results" in st.session_state:
                    st.subheader("Empirical Network Metrics Summary")
                    st.caption("Aggregated baseline values (maximum, minimum, and mean) computed directly on your real input network.")

                    if st.session_state.get("current_param_hash") != expected_state_key:
                        st.warning("You changed parameters above. Click 'Run Analysis' to update the empirical data, or proceed with the current values below.")
                        is_centrality_stale = True
                    else: 
                        is_centrality_stale = False

                    # Data loading
                    centrality_df = st.session_state["active_centrality_results"]

                    numeric_cols = [col for col in centrality_df.columns] 

                    # Calculations of aggregations
                    empirical_summary = pd.DataFrame({
                        "maxima": centrality_df[numeric_cols].max(),
                        "minima": centrality_df[numeric_cols].min(),
                        "mean_of_all_values": centrality_df[numeric_cols].mean()
                    })
                    
                    # Index description
                    empirical_summary.index.name = "metric_name"

                    # Greyscaling of result df when current parameters are not coherent with displayed results
                    if is_centrality_stale:
                        empirical_styled_df = empirical_summary.style.map(lambda _: "color: rgba(120, 120, 120, 0.5);")
                    else:
                        empirical_styled_df = empirical_summary

                    # Display of the df
                    st.dataframe(empirical_styled_df, use_container_width=True)
                    
            
            with tab2:
                st.caption("Average Gini-Coefficient per metric. Higher values indicate higher structural inequality.")
                st.dataframe(gini_styled_df, use_container_width=True)

                # Download button to download df inclusive meta-data
                st.download_button(
                    label="Download Gini Coefficients (CSV) (inclusive Meta-Data)",
                    data=csv_gini_bytes,
                    file_name=f"sim_gini_{selected_topology.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    key="download_gini_btn_final"
                )

                # Column chart of Gini-coefficient
                chart_df = gini_result.reset_index()
                st.bar_chart(chart_df, x="metric_name", y="mean_gini_coefficient")


        st.divider()

