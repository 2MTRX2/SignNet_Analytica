# centrality_page.py

import streamlit as st
import pandas as pd

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis

from signnet.ui.components.centrality_selector import centrality_selector
from signnet.ui.components.network_summary import network_summary

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

    Args:
        network (SignedNetwork): The active network domain model containing 
                                 the vertices and edges.
    """
    # ------------------------------------------------------------------
    # Step 1: Render network structural summary
    # ------------------------------------------------------------------
    network_summary(network)

    st.divider()

    # ------------------------------------------------------------------
    # Step 2: Define and collect selected centrality measures
    # ------------------------------------------------------------------
    measure_options = CentralityRegistry.get_available_names()

    # Collect the list of strings representing the selected measures
    selected_names = centrality_selector(measure_options)

    # Halt execution early if no measures are chosen yet
    if not selected_names:
        st.info("Please select at least one centrality measure to proceed.")
        return

    st.divider()

    # ------------------------------------------------------------------
    # Step 3: Define default parameter values for advanced measures
    # ------------------------------------------------------------------
    runtime_arguments = {}

    has_parameters = any(len(CentralityRegistry.get_measure_class(name).PARAMETERS) > 0 for name in selected_names)

    if has_parameters:
        st.subheader("Configure Parameters")
        
        for name in selected_names:
            measure_class = CentralityRegistry.get_measure_class(name)
            
            if measure_class.PARAMETERS:
                st.markdown(f"**{name} Options**")
                runtime_arguments[name] = {}
                
                for param in measure_class.PARAMETERS:
                    if param.type == "float":
                        if param.min_value is None or param.max_value is None:
                            val = st.number_input(
                                param.label,
                                min_value=float(param.min_value) if param.min_value is not None else None,
                                max_value=float(param.max_value) if param.max_value is not None else None,
                                value=float(param.default),
                                step=float(param.step) if param.step else 0.01,
                                key=f"{name}_{param.name}"
                            )

                            if param.min_value is not None and val < param.min_value:
                                st.error(f"{param.label} must be greater than or equal to {param.min_value}.")
                            if param.max_value is not None and val > param.max_value:
                                st.error(f"{param.label} must be less than or equal to {param.max_value}.")
                        else:
                        # Nur wenn beide Grenzen definiert sind, wird ein Slider gerendert
                            val = st.slider(
                                param.label, 
                                min_value=float(param.min_value), 
                                max_value=float(param.max_value), 
                                value=float(param.default), 
                                step=float(param.step),
                                key=f"{name}_{param.name}"
                            )
                        
                    elif param.type == "int":
                        if param.min_value is None or param.max_value is None:
                            val = st.number_input(
                                param.label,
                                min_value=int(param.min_value) if param.min_value is not None else None,
                                max_value=int(param.max_value) if param.max_value is not None else None,
                                value=int(param.default),
                                step=int(param.step) if param.step else 1,
                                key=f"{name}_{param.name}"
                            )
                            if param.min_value is not None and val < param.min_value:
                                st.error(f"{param.label} must be greater than or equal to {param.min_value}.")
                            if param.max_value is not None and val > param.max_value:
                                st.error(f"{param.label} must be less than or equal to {param.max_value}.")
                        else:
                            val = st.slider(
                                param.label, 
                                min_value=int(param.min_value), 
                                max_value=int(param.max_value), 
                                value=int(param.default), 
                                step=int(param.step),
                                key=f"{name}_{param.name}"
                            )

                    runtime_arguments[name][param.name] = val

    # ------------------------------------------------------------------
    # Step 4: Map selected names to configured class instances
    # ------------------------------------------------------------------
    selected_measures = []

    for name in selected_names:
        measure_class = CentralityRegistry.get_measure_class(name)

        kwargs = runtime_arguments.get(name, {}) 
        instance = measure_class(**kwargs)
            
        selected_measures.append(instance)


    # ------------------------------------------------------------------
    # Step 5: Execute analysis and manage session state persistence
    # ------------------------------------------------------------------
    st.subheader("Run Analysis")

    # Generate a unique hash key containing network instance id and all variable settings.
    # This automatically clears old results from the screen if parameters or metrics change.
    hash_components = [f"net_nodes_{len(network.nodes)}_edges_{len(network.edges)}"]
    
    for name in sorted(selected_names):
        hash_components.append(name)
       
        if name in runtime_arguments:
            for p_name, p_val in sorted(runtime_arguments[name].items()):
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
    # Step 6: Render results table if matching state key exists
    # ------------------------------------------------------------------
    if "active_centrality_results" in st.session_state:
        if st.session_state.get("current_param_hash") != expected_state_key:
            st.warning("You changed parameters above. Click 'Run Analysis' to update the data, or proceed with the current results below.")

        st.subheader("Results")

        centrality_df = st.session_state["active_centrality_results"]

        st.dataframe(
            centrality_df,
            use_container_width=True,
        )

        st.divider()
    
        # ==============================================================
        # Step 7: Centrality Correlation Analysis
        # ==============================================================
        st.subheader("Correlation Analysis")
        
        if centrality_df.shape[1] < 2:
            st.warning("Please select at least two centrality measures to perform a correlation analysis.")
            return

        ctrl_col1, ctrl_col2 = st.columns(2)

        with ctrl_col1:
            ui_choice = st.selectbox(
                "Select Correlation Metric:",
                CorrelationRegistry.get_available_names(),
                key="correlation_metric_widget"
            )

        with ctrl_col2:
            alpha = st.selectbox(
                "Select Significance Level (Alpha):",
                [0.05, 0.01, 0.001, 0.10],
                index=0,  
                format_func=lambda x: f"α = {x} ({(1-x)*100:.1f}% Confidence)", 
                key="pvalue_widget"
            )

        corr_strategy = CorrelationRegistry.get_measure_class(ui_choice)()

        analyzer = CorrelationAnalysis(strategy=corr_strategy)
        
        try:
            df_corr, df_p_values = analyzer.analyze_correlations(centrality_df)
            
            tab1, tab2 = st.tabs(["Correlation Coefficients", "p-Values (Significance)"])
            
            with tab1:
                st.caption("Values closer to 1.0 or -1.0 indicate strong positive or negative correlations.")
                st.dataframe(
                    df_corr.style.background_gradient(cmap="coolwarm", vmin=-1.0, vmax=1.0), 
                    use_container_width=True
                )
                
            with tab2:
                st.caption(f"Values below {alpha} indicate that the correlation is statistically significant.")
                
                def highlight_p_values(df, alpha_level):
                    style_df = pd.DataFrame("color: gray;", index=df.index, columns=df.columns)
                    for col in df.columns:
                        for idx in df.index:
                            if idx == col:
                                style_df.loc[idx, col] = "color: darkgray; font-style: italic;"
                            elif df.loc[idx, col] < alpha_level:
                                style_df.loc[idx, col] = "color: green; font-weight: bold;"
                    return style_df

                formatted_p = df_p_values.style.format("{:.4e}").apply(
                    highlight_p_values, 
                    alpha_level=alpha, 
                    axis=None
                )
                st.dataframe(formatted_p, use_container_width=True)

        except Exception as ex:
            st.error(f"Failed to calculate metric correlations:\n\n{ex}")

