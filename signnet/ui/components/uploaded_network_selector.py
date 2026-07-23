# uploaded_network_selector.py

import streamlit as st
from signnet.ui.components.file_upload import file_upload
from signnet.io.NetworkBuilder import load_and_build_network

from signnet.io.data_representation.EdgeListNormaliser import EdgeListNormaliser
from signnet.io.data_loading.CsvStrategy import CsvStrategy
from signnet.io.data_loading.ExcelStrategy import ExcelStrategy
from signnet.io.data_loading.JsonStrategy import JsonStrategy

def uploaded_network_selector() -> getattr:
    """
    Renders the file upload UI, handles validation, column mapping, 
    and returns a fully built SignedNetwork instance once processed.
    """
    config = file_upload()

    if config is None:
        st.info("Please upload a network file above to begin the analysis.")
        return None

    if config.directed:
        st.warning("Directed networks have not been implemented yet. Please untick 'Directed network' to proceed.")
        st.session_state.network_processed = False
        st.stop()

    if config.representation not in ["Edge List", "Adjacency Matrix"]:
        st.error(f"Unsupported network representation: {config.representation}")
        return None
        
    if config.file_type not in ["CSV", "Excel", "JSON"]:
        st.error(f"Unsupported file format: {config.file_type}")
        return None
    
    source_name, target_name, sign_name = 'source', 'target', 'sign'
    proceed_with_loading = True

    if config.representation == "Edge List":
        temp_rep = EdgeListNormaliser()
        fmt = config.file_type.lower()
        
        if fmt == "csv":
            temp_loader = CsvStrategy(temp_rep)
        elif fmt == "excel":
            temp_loader = ExcelStrategy(temp_rep)
        else:
            temp_loader = JsonStrategy(temp_rep)

        df_raw = temp_loader.read_raw(config.file)
        available_cols = list(df_raw.columns)

        st.subheader("Column Mapping")
        st.info("Please assign the file columns to the network roles:")

        default_src_idx = 0 if len(available_cols) > 0 else 0
        default_tgt_idx = 1 if len(available_cols) > 1 else 0
        default_sgn_idx = 2 if len(available_cols) > 2 else 0

        def reset_network_processed():
            st.session_state.network_processed = False
        
        col1, col2, col3 = st.columns(3)
        with col1: 
            source_name = st.selectbox("Source Column:", available_cols, index=default_src_idx, key="src_sel_key", on_change=reset_network_processed)
        with col2: 
            target_name = st.selectbox("Target Column:", available_cols, index=default_tgt_idx, key="tgt_sel_key", on_change=reset_network_processed)
        with col3: 
            sign_name = st.selectbox("Sign/Value Column:", available_cols, index=default_sgn_idx, key="sgn_sel_key", on_change=reset_network_processed)

        if "network_processed" not in st.session_state:
            st.session_state.network_processed = False

        if st.button("Process Network Architecture"):
            st.session_state.network_processed = True

        proceed_with_loading = st.session_state.network_processed
        
        if not proceed_with_loading:
            st.info("Click the button above to calculate the network metrics with the selected columns.")

    if proceed_with_loading:
        try:
            if hasattr(config.file, "seek"):
                config.file.seek(0)

            network = load_and_build_network(
                file_buffer=config.file,
                file_type=config.file_type,
                representation_type=config.representation,
                is_directed=config.directed,
                source_col=source_name, 
                target_col=target_name,
                sign_col=sign_name
            )
            return network
        except Exception as ex:
            st.error(f"Failed to load network:\n\n{ex}")
            return None

    return None
