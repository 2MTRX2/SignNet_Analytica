# app.py
import streamlit as st

# Data Representation
from io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser

# Data Loading Strategies
from io.data_loading.CsvStrategy import CsvStrategy
from io.data_loading.ExcelStrategy import ExcelStrategy
from io.data_loading.JsonStrategy import JsonStrategy

# Models & UI
from models.SignedNetwork import SignedNetwork
from ui.components.file_upload import file_upload
from ui.pages.centrality_page import show as show_centrality_page


@st.cache_data(show_spinner="Processing and building signed network...")
def load_and_build_network(
    file_buffer, 
    file_type: str, 
    representation_type: str, 
    is_directed: bool
) -> SignedNetwork:
    """
    Selects the appropriate file strategy and normaliser dynamically.
    Caches the resulting SignedNetwork to ensure high performance.
    """
    if representation_type == "Edge List":
        representation = EdgeListNormaliser()
    elif representation_type == "Adjacency Matrix":
        representation = AdjacencyMatrixNormaliser()
    else:
        raise ValueError(f"Unsupported network representation: {representation_type}")

    fmt = file_type.lower()
    if fmt == "csv":
        loader = CsvStrategy(representation)
    elif fmt == "excel":
        loader = ExcelStrategy(representation)
    elif fmt == "json":
        loader = JsonStrategy(representation)
    else:
        raise ValueError(f"Unsupported file format configuration: {file_type}")

    network_data = loader.load(file_buffer)
    return SignedNetwork(edges=network_data.edges, nodes=network_data.nodes, directed=is_directed)

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
    
    # Vorbereitung für die Zukunft: Auswahl der Input-Methode
    input_method = st.radio(
        "Select Data Source",
        ["Upload File", "Predefined Dataset (Not implemented yet)"],
        horizontal=True
    )

    network = None

    if input_method == "Upload File":
        config = file_upload()

        if config is not None:
            # Validations
            if config.representation not in ["Edge List", "Adjacency Matrix"]:
                st.error(f"Unsupported network representation: {config.representation}")
                return
            if config.file_type not in ["CSV", "Excel", "JSON"]:
                st.error(f"Unsupported file format: {config.file_type}")
                return

            # Load the network from uploaded file
            try:
                network = load_and_build_network(
                    file_buffer=config.file,
                    file_type=config.file_type,
                    representation_type=config.representation,
                    is_directed=config.directed
                )
            except Exception as ex:
                st.error(f"Failed to load network:\n\n{ex}")
                return
        else:
            st.info("Please upload a network file above to begin the analysis.")

    elif input_method == "Predefined Dataset (Not implemented yet)":
        st.warning("Predefined datasets are currently under development. Please use the 'Upload File' option.")
        # `load_predefined_network()` aufrufen
        network = None

    # ==================================================================
    # SECTION 2: CENTRALITY ANALYSIS
    # ==================================================================
    st.divider()
    st.header("2. Centrality Analysis")

    if network is not None:
        show_centrality_page(network)
    else:
        st.info("Waiting for a valid network to be loaded in Section 1...")


if __name__ == "__main__":
    main()
