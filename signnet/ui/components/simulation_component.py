# simulation_component.py
import streamlit as st
import pandas as pd

from signnet.ui.components.simulation_parameter_config import configure_topology_parameters
from signnet.ui.components.simulation_topology_selector import simulation_topology_selector
from signnet.ui.components.grayout_stale_df import grayout_df
from signnet.ui.components.grayout_stale_df import is_stale


from signnet.analysis.simulation.SimulationEngine import SimulationEngine
from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry
from signnet.analysis.simulation.NetworkBenchmarker import NetworkBenchmarker

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis
from signnet.models.NetworkGenerator import NetworkGenerator

from signnet.models.SignedNetwork import SignedNetwork

from signnet.utils.StateKeyGenerator import StateKeyGenerator

def render_benchmarking_centrality_analysis(network: SignedNetwork, centrality_df: pd.DataFrame, selected_measures: list, selected_names: list, runtime_parameters: list, current_state_key_centrality: str, expected_state_key_centrality: str, button_centrality_name:str): 
        st.subheader("Simulation Benchmarking")

        simulation_engine = SimulationEngine(analysis_pipeline=CentralityAnalysis(measures=selected_measures).compute, default_index_label="node")

        topology_options = TopologyRegistry.get_available_topologies()

        selected_topology = simulation_topology_selector(available_topologies=topology_options)

        global_parameters, kwargs_parameters = configure_topology_parameters(selected_topology=selected_topology, number_of_nodes=network.number_of_nodes, number_of_edges=network.number_of_edges)
      
        # Base string with original network properties
        expected_state_key_simulation = (
            StateKeyGenerator(prefix="params")
            .add_network(network)
            .add_flat_param("sim_topology", selected_topology)
            # Globale Parameter (n, neg_ratio, n_iterations) direkt aus dem Dict auslesen und sortieren
            .add_dict(global_parameters, prefix="sim")
            # Topologie-spezifische kwargs (m, p, etc.) hinzufügen
            .add_dict(kwargs_parameters, prefix="kw")
            # Centrality Metriken hinzufügen
            .add_measures_with_parameters(selected_names, runtime_parameters)
            .generate()
        )

        button_simulation_name = "Run Simulation Pipeline"

        if st.button(button_simulation_name, type="secondary"):
            # Wrap execution in a native spinner for complex network simulation
            with st.spinner(f"Simulating {global_parameters['n_iterations']} networks..."):
                try:
                    network_generator = NetworkGenerator(
                        topology_name=selected_topology, 
                        n=global_parameters["n"], 
                        neg_ratio=global_parameters["neg_ratio"], 
                        **kwargs_parameters
                    )
                    
                    simulation_result = simulation_engine.run(
                        num_iterations=global_parameters["n_iterations"], 
                        network_provider=network_generator.create_random_signed_network
                    )
                    st.session_state["active_simulation_results"] = simulation_result
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
            current_hash = st.session_state.get("current_param_hash_simulation")
            simulation_result  = st.session_state["active_simulation_results"]

            id_column = simulation_result.columns[1]
            extremes_result = NetworkBenchmarker.analyze_network_extremes(df_raw_results=simulation_result, node_col=id_column)
            gini_result = NetworkBenchmarker.calculate_gini_coefficient(df_raw_results=simulation_result)

            bool_is_stale = is_stale(current_hash=current_hash, expected_hash=expected_state_key_simulation, button=button_simulation_name)

            extremes_styled_df = grayout_df(session_state_df=extremes_result, is_stale=bool_is_stale)
            gini_styled_df = grayout_df(session_state_df=gini_result, is_stale=bool_is_stale)

            # Adding meta-data to the download file
            meta_parts = [
                f"Topo: {selected_topology}",
                f"N: {global_parameters['n']}",
                f"Iter: {global_parameters['n_iterations']}",
                f"Neg_Ratio: {global_parameters['neg_ratio']}"
            ]
            for param_name, param_value in kwargs_parameters.items():
                meta_parts.append(f"{param_name}: {param_value}")
                
            meta_string = " | ".join(meta_parts)

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
                    bool_is_stale = is_stale(current_hash=current_state_key_centrality, expected_hash=expected_state_key_centrality, button=button_centrality_name)

                    # Data loading
                    df_for_benchmarking = centrality_df.copy()

                    # Add an iteration column to use behaviour of the network benchmarker
                    if "iteration" not in df_for_benchmarking.columns:
                        df_for_benchmarking.insert(0, "iteration", 0)

                    # Position iteration in the first column
                    elif df_for_benchmarking.columns[0] != "iteration":
                        cols = ["iteration"] + [col for col in df_for_benchmarking.columns if col != "iteration"]
                        df_for_benchmarking = df_for_benchmarking[cols]

                    # If the node columns misses, we add one to the df
                    if "node" not in df_for_benchmarking.columns:
                        df_for_benchmarking["node"] = df_for_benchmarking.index

                    try:
                        empirical_summary = NetworkBenchmarker.analyze_network_extremes(
                            df_raw_results=df_for_benchmarking, 
                            node_col="node"
                        )
                        
                        empirical_summary.rename(columns={
                            "mean_of_maxima": "maxima",
                            "mean_of_minima": "minima"
                        }, inplace=True)

                        empirical_styled_df = grayout_df(session_state_df=empirical_summary, is_stale=bool_is_stale)

                        st.dataframe(empirical_styled_df, use_container_width=True)

                    except ValueError as e:
                        st.error(f"Calculation Error: {e}")
            
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

                if "active_centrality_results" in st.session_state:                       
                    st.subheader("Empirical Network Metrics Summary")
                    st.caption("Aggregated Gini-Coefficients computed directly on your real input network.")

                    bool_is_stale = is_stale(current_hash=current_state_key_centrality, expected_hash=expected_state_key_centrality, button=button_centrality_name)

                    # Data loading
                    df_for_benchmarking = centrality_df.copy()

                    # Add an iteration column to use behaviour of the network benchmarker
                    if "iteration" not in df_for_benchmarking.columns:
                        df_for_benchmarking.insert(0, "iteration", 0)

                    # Position iteration in the first column
                    elif df_for_benchmarking.columns[0] != "iteration":
                        cols = ["iteration"] + [col for col in df_for_benchmarking.columns if col != "iteration"]
                        df_for_benchmarking = df_for_benchmarking[cols]

                    # If the node columns misses, we add one to the df
                    if "node" not in df_for_benchmarking.columns:
                        df_for_benchmarking["node"] = df_for_benchmarking.index

                    try:
                        empirical_summary = NetworkBenchmarker.calculate_gini_coefficient(
                            df_raw_results=df_for_benchmarking, 
                            node_col="node"
                        )
                        
                        empirical_summary.rename(columns={
                            "mean_gini_coefficient": "gini_coefficient",
                        }, inplace=True)

                        empirical_styled_df = grayout_df(session_state_df=empirical_summary, is_stale=bool_is_stale)

                        st.dataframe(empirical_styled_df, use_container_width=True)

                        chart_df = empirical_summary.reset_index()
                        st.bar_chart(chart_df, x="metric_name", y="gini_coefficient")

                    except ValueError as e:
                        st.error(f"Calculation Error: {e}")

        st.divider()