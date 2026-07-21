# app.py
import streamlit as st

# Data Representation
from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_representation.AdjacencyMatrixNormaliser import AdjacencyMatrixNormaliser

# Data Loading Strategies
from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_loading.ExcelStrategy import ExcelStrategy
from signnet.io.data_loading.JsonStrategy import JsonStrategy

# Models & UI
from signnet.models.SignedNetwork import SignedNetwork
from signnet.ui.components.file_upload import file_upload
from signnet.ui.pages.centrality_page import show as show_centrality_page


@st.cache_data(show_spinner="Processing and building signed network...")
def load_and_build_network(
    file_buffer, 
    file_type: str, 
    representation_type: str, 
    is_directed: bool, 
    source_col: str = 'source',  
    target_col: str = 'target',
    sign_col: str = 'sign'
) -> SignedNetwork:
    """
    Selects the appropriate file strategy and normaliser dynamically.
    Caches the resulting SignedNetwork to ensure high performance.
    """
    if representation_type == "Edge List":
        representation = EdgeListNormaliser(source_col=source_col, target_col=target_col, sign_col=sign_col)
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
            
            source_name, target_name, sign_name = 'source', 'target', 'sign'
            proceed_with_loading = True

            if config.representation == "Edge List":
                # Temporären Dummy-Normaliser erstellen, nur um an die Spaltennamen zu kommen
                # Da config.file ein Buffer ist, nutzen wir eine temporäre Strategie für read_raw
                temp_rep = EdgeListNormaliser()
                if config.file_type.lower() == "csv":
                    temp_loader = CsvStrategy(temp_rep)
                elif config.file_type.lower() == "excel":
                    temp_loader = ExcelStrategy(temp_rep)
                else:
                    temp_loader = JsonStrategy(temp_rep)

                # Rohe Spalten auslesen (wird gecached im Loader-Instanz-Objekt)
                df_raw = temp_loader.read_raw(config.file)
                available_cols = list(df_raw.columns)

                st.subheader("Column Mapping")
                st.info("Please assign the file columns to the network roles:")

                default_src_idx = 0 if len(available_cols) > 0 else 0
                default_tgt_idx = 1 if len(available_cols) > 1 else 0
                default_sgn_idx = 2 if len(available_cols) > 2 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1: source_name = st.selectbox("Source Column:", available_cols, index=default_src_idx, key="src_sel")
                with col2: target_name = st.selectbox("Target Column:", available_cols, index=default_tgt_idx, key="tgt_sel")
                with col3: sign_name = st.selectbox("Sign/Value Column:", available_cols, index=default_sgn_idx, key="sgn_sel")

                if not st.button("Process Network Architecture"):
                    proceed_with_loading = False
                    st.info("Click the button above to calculate the network metrics with the selected columns.")

            # Load the network from uploaded file
            if proceed_with_loading:
                try:
                    # Streamlit buffer gets reset
                    if hasattr(config.file, "seek"):
                        config.file.seek(0)

                    network = load_and_build_network(
                        file_buffer=config.file,
                        file_type=config.file_type,
                        representation_type=config.representation,
                        is_directed=config.directed,
                        source_col=source_name,  # Übergabe der sauberen String-Variablen
                        target_col=target_name,
                        sign_col=sign_name
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
