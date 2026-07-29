# app.py
import streamlit as st

from signnet.ui.pages.centrality_page import show as show_centrality_page
from signnet.ui.components.predefined_dataset_selector import predefined_dataset_selector
from signnet.ui.components.uploaded_network_selector import uploaded_network_selector
from signnet.ui.components.GraphBuilder import create_graphical_signed_network

def main():
    """Entry point of the Streamlit application."""

    st.set_page_config(
        page_title="Signed Network Analysis",
        page_icon="📊",
        layout="wide",
    )

    st.title("Signed Network Analysis Framework")

    # ==================================================================
    # SECTION 1: DATA CONFIGURATION & LOADING
    # ==================================================================
    st.header("1. Data Input")
    
    # Selection of the input method
    input_method = st.radio(
        "Select Data Source",
        ["Upload File", "Predefined Dataset"],
        horizontal=True
    )

    # Ensure that the application starts with an empty network
    network = None

    # Proceed with the input method of a predefined dataset
    if input_method == "Predefined Dataset":
        network = predefined_dataset_selector()

    # Proceed with the input method of an uploaded file
    elif input_method == "Upload File":
        network = uploaded_network_selector()

    # Ensure that no not-implemented method can be chosen
    else:
        st.error(f"Developer Error: Input method '{input_method}' is not implemented yet.")

    # ==================================================================
    # SECTION 2: CENTRALITY ANALYSIS
    # ==================================================================
    st.divider()
    st.header("2. Centrality Analysis")

    if network is not None:
        create_graphical_signed_network(network)
        show_centrality_page(network)
    else:
        st.info("Waiting for a valid network to be loaded in Section 1...")


if __name__ == "__main__":
    main()
