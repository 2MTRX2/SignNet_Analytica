# app.py
import streamlit as st

from signnet.ui.pages.centrality_page import show as show_centrality_page
from signnet.ui.components.predefined_dataset_selector import predefined_dataset_selector
from signnet.ui.components.uploaded_network_selector import uploaded_network_selector
from signnet.ui.components.GraphBuilder import create_graphical_signed_network


def main():
    """Entry point of the Streamlit application."""

    st.set_page_config(
        page_title="SignNet Analytica (Beta)",
        page_icon="🌐",
        layout="wide",
    )

    st.title("SignNet Analytica :blue[Beta]")
    st.caption("Version 0.1.0-beta – Major UI restructuring and new features coming soon.")

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
        # Ensures the rendering, the selection, and the loading of a predefined dataset
        network = predefined_dataset_selector()

    # Proceed with the input method of an uploaded file
    elif input_method == "Upload File":
        # Ensures the rendering and the loading of an uploaded dataset
        network = uploaded_network_selector()

    # Ensure that no not-implemented method can be chosen
    else:
        st.error(f"Developer Error: Input method '{input_method}' is not implemented yet.")

    # ==================================================================
    # SECTION 2: CENTRALITY ANALYSIS
    # ==================================================================
    st.divider()
    st.header("2. Centrality Analysis")

    # As soon as a network connection is established, the analysis begins
    if network is not None:
        # Creates a graphical representation of the network and integrates it into the application
        create_graphical_signed_network(network)
        # Performs a static analysis of the network: centrality, correlations, p-value
        show_centrality_page(network)
    else:
        st.info("Waiting for a valid network to be loaded in Section 1...")


if __name__ == "__main__":
    main()
