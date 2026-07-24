# predefined_dataset_selector.py

import streamlit as st
from signnet.io.DatasetRegistry import DatasetRegistry
from signnet.io.NetworkBuilder import load_and_build_network 

from signnet.models.SignedNetwork import SignedNetwork

def predefined_dataset_selector() -> SignedNetwork | None:
    """
    Renders the UI to select and load a predefined dataset.
        
    Returns:
        SignedNetwork or None: The loaded network instance or None if loading failed.
    """
    available_datasets = DatasetRegistry.get_available_names()
    selected_dataset_name = st.selectbox("Choose a sample dataset to test:", available_datasets)
    
    dataset_info = DatasetRegistry.get_info(selected_dataset_name)
    st.caption(f"**Description:** {dataset_info.description}")
    st.caption(f"**Format:** {dataset_info.representation_type} ({dataset_info.file_type})")

    try:
        file_path = DatasetRegistry.get_file_path(selected_dataset_name)

        # Read the file with a context manager so that the resources are freed up after usage.
        # rb to read binary data
        with open(file_path, "rb") as file_buffer:
            network = load_and_build_network(
                file_buffer=file_buffer,
                file_type=dataset_info.file_type,
                representation_type=dataset_info.representation_type,
                is_directed=False, 
                source_col='source', 
                target_col='target',
                sign_col='sign'
            )
            return network
    except Exception as ex:
        st.error(f"Failed to load predefined network:\n\n{ex}")
        return None
