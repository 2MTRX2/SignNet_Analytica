# centrality_page.py

import streamlit as st
import pandas as pd

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis

from signnet.ui.components.centrality_selector import centrality_selector
from signnet.ui.components.network_summary import network_summary

from signnet.analysis.centrality.centrality_measures.SignedDegreeCentrality import SignedDegreeCentrality
from signnet.analysis.centrality.centrality_measures.PnCentrality import PnCentrality
from signnet.analysis.centrality.centrality_measures.PiiCentrality import PiiCentrality
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBallester import KbCentralityBallester
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBloch import KbCentralityBloch
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralitySadler import KbCentralitySadler
from signnet.analysis.correlations.CorrelationAnalysis import CorrelationAnalysis
from signnet.analysis.correlations.correlation_measures.SpearmanStrategy import SpearmanStrategy
from signnet.analysis.correlations.correlation_measures.PearsonStrategy import PearsonStrategy
from signnet.analysis.correlations.correlation_measures.KendallStrategy import KendallStrategy

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
    st.subheader("Select Centrality Measures")

    # Define all available algorithm options for the selection UI
    measure_options = [
        "Signed Degree",
        "PN Centrality",
        "PII Centrality",
        "KB Centrality (Ballester)",
        "KB Centrality (Bloch)",
        "KB Centrality (Sadler)"
    ]

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
    degree_beta = 1.0
    pii_beta = -0.25
    pii_max_distance = 3

    # Only render the parameter configuration block if a configurable measure is active
    if "Signed Degree" in selected_names or "PII Centrality" in selected_names:
        st.subheader("Configure Parameters")
        
        # Split layout into columns for clean visual alignment side-by-side
        col1, col2 = st.columns(2)

        # Contextual input for Signed Degree parameter
        with col1:
            if "Signed Degree" in selected_names:
                st.markdown("**Signed Degree Options**")
                degree_beta = st.number_input(
                    "Beta (Degree)", 
                    value=1.0, 
                    step=0.1
                )

        # Contextual sliders for PII Centrality parameters
        with col2:
            if "PII Centrality" in selected_names:
                st.markdown("**PII Centrality Options**")
                pii_beta = st.slider(
                    "Beta (PII)", 
                    min_value=-1.0, 
                    max_value=0.0, 
                    value=-0.25, 
                    step=0.05
                )
                pii_max_distance = st.slider(
                    "Max Distance (PII)", 
                    min_value=0, 
                    max_value=10, 
                    value=3
                )
        st.divider()
    
    # ------------------------------------------------------------------
    # Step 4: Map selected names to configured class instances
    # ------------------------------------------------------------------
    selected_measures = {}

    if "Signed Degree" in selected_names:
        selected_measures["Signed Degree"] = SignedDegreeCentrality(beta=degree_beta)
        
    if "PN Centrality" in selected_names:
        selected_measures["PN Centrality"] = PnCentrality()
        
    if "PII Centrality" in selected_names:
        selected_measures["PII Centrality"] = PiiCentrality(beta=pii_beta, max_distance=pii_max_distance)
        
    if "KB Centrality (Ballester)" in selected_names:
        selected_measures["KB Centrality (Ballester)"] = KbCentralityBallester()
        
    if "KB Centrality (Bloch)" in selected_names:
        selected_measures["KB Centrality (Bloch)"] = KbCentralityBloch()
        
    if "KB Centrality (Sadler)" in selected_names:
        selected_measures["KB Centrality (Sadler)"] = KbCentralitySadler()

    # ------------------------------------------------------------------
    # Step 5: Execute analysis and manage session state persistence
    # ------------------------------------------------------------------
    st.subheader("Run Analysis")

    # Generate a unique hash key containing network instance id and all variable settings.
    # This automatically clears old results from the screen if parameters or metrics change.
    expected_state_key = f"params_{degree_beta}_{pii_beta}_{pii_max_distance}_{sorted(selected_names)}"
    
    if st.button("Run Analysis", type="primary"):
        # Wrap execution in a native spinner for complex network operations
        with st.spinner("Calculating selected metrics..."):
            analysis = CentralityAnalysis(measures=list(selected_measures.values()))

            st.session_state["active_centrality_results"] = analysis.compute(network)
 
            st.session_state["current_param_hash"] = expected_state_key

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
                ["Spearman Rank Correlation (Recommended)", "Pearson Linear Correlation", "Kendall Tau Correlation"]
            )

        with ctrl_col2:
            alpha = st.selectbox(
                "Select Significance Level (Alpha):",
                [0.05, 0.01, 0.001, 0.10],
                index=0,  # Standardmäßig auf 0.05 gesetzt
                format_func=lambda x: f"α = {x} ({(1-x)*100:.1f}% Confidence)"
            )
        
        if ui_choice == "Spearman Rank Correlation (Recommended)":
            corr_strategy = SpearmanStrategy()
        elif ui_choice == "Pearson Linear Correlation":
            corr_strategy = PearsonStrategy()
        else:
            corr_strategy = KendallStrategy()

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

