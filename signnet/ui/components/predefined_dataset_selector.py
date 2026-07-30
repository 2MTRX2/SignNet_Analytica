# predefined_dataset_selector.py
from typing import Optional
import streamlit as st

from signnet.io.DatasetRegistry import DatasetRegistry
from signnet.io.NetworkBuilder import load_and_build_network 

from signnet.models.SignedNetwork import SignedNetwork


def predefined_dataset_selector() -> Optional[SignedNetwork]:
    """
    Renders the Streamlit UI to select, describe, and load a predefined dataset.

    Fetches available dataset names from the DatasetRegistry, displays metadata (description 
    and format) via captions, and attempts to safely read and build the network 
    from the underlying binary file.

    Returns:
        The initialized signed network instance, or None if an error occurs during file retrieval
        or network building.
    """
    # Set up the various dataset options
    available_datasets = DatasetRegistry.get_available_names()
    selected_dataset_name = st.selectbox("Choose a sample dataset to test:", available_datasets)

    # Display the info about the selected dataset
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
