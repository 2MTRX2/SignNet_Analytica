# centrality_page.py

import streamlit as st

from signnet.analysis.centrality.CentralityAnalysis import CentralityAnalysis

from signnet.ui.components.centrality_selector import centrality_selector
from signnet.ui.components.network_summary import network_summary

from signnet.analysis.centrality.centrality_measures.SignedDegreeCentrality import SignedDegreeCentrality
from signnet.analysis.centrality.centrality_measures.PnCentrality import PnCentrality
from signnet.analysis.centrality.centrality_measures.PiiCentrality import PiiCentrality
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBallester import KbCentralityBallester
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralityBloch import KbCentralityBloch
from signnet.analysis.centrality.centrality_measures.KbCentrality.KbCentralitySadler import KbCentralitySadler

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
        st.subheader("2. Configure Parameters")
        
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
                    max_value=0, 
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
    state_key = f"centrality_res_{id(network)}_{degree_beta}_{pii_beta}_{pii_max_distance}_{sorted(selected_names)}"
    
    if st.button("Run Analysis", type="primary"):
        # Wrap execution in a native spinner for complex network operations
        with st.spinner("Calculating selected metrics..."):
            analysis = CentralityAnalysis(selected_measures)
            # Store calculated DataFrame safely inside the user session
            st.session_state[state_key] = analysis.compute(network)

    # ------------------------------------------------------------------
    # Step 6: Render results table if matching state key exists
    # ------------------------------------------------------------------
    if state_key in st.session_state:
        st.subheader("Results")
        st.dataframe(
            st.session_state[state_key],
            use_container_width=True,
        )
