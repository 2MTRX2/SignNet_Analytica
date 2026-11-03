# file_upload.py
from dataclasses import dataclass
from typing import Optional
import streamlit as st

from signnet.io.LoadingRegistry import STRATEGY_REGISTRY
from signnet.io.LoadingRegistry import EXTENSION_TO_FORMAT
from signnet.io.LoadingRegistry import get_available_file_types
from signnet.io.LoadingRegistry import get_available_representations


@dataclass
class FileUploadConfig:
    """
    Stores the validated user configuration for a network file upload.

    Acts as a data transfer object (DTO) that encapsulating the uploaded file 
    binary alongside its user-selected and system-detected metadata required 
    for subsequent processing.

    Attributes:
        file (Optional[object]): The raw Streamlit UploadedFile object containing 
            the binary data, or None if no file is present.
        file_type (str): The validated uppercase format name (e.g., 'CSV', 'EXCEL', 'JSON') 
            selected by the user.
        representation (str): The structural format of the network data (e.g., 'Edge List').
        directed (bool): Flag indicating whether the underlying network edges 
            are directed.
    """
    file: Optional[object]
    file_type: str
    representation: str
    directed: bool

def file_upload() -> Optional[FileUploadConfig]:
    """
    Renders the file upload UI component with automatic format detection and strict validation.

    Injects interactive Streamlit components into the view to handle network file selection. 
    It dynamically restricts allowed extensions based on active strategies, automatically 
    pre-selects the file format dropdown by parsing the uploaded file extension, and manages 
    the state for structural network representation.

    Args:
        None

    Returns:
        Optional[FileUploadConfig]: A fully populated configuration object if a valid 
            file is uploaded and a specific format is explicitly chosen; otherwise None.
    """
    # select all available extensions if the corresponding strategy exists e.g. csv, json...
    allowed_extensions = [ext for ext, fmt in EXTENSION_TO_FORMAT.items() if fmt.lower() in STRATEGY_REGISTRY]

    # input box
    uploaded_file = st.file_uploader(
        "Choose a network file (Drag & Drop or click Browse)",
        type=allowed_extensions,
        accept_multiple_files=False
    )

    if uploaded_file is None:
        return None

    # extract extension of the file
    detected_ext = uploaded_file.name.split(".")[-1].lower()

    # extract all the available file formats to display them in the selection box e.g. CSV, JSON, EXCEL...
    available_formats = get_available_file_types()
    file_type_options = ["Select format..."] + available_formats

    # transform the detected extension to a format e.g. xls -> EXCEL
    target_format = EXTENSION_TO_FORMAT.get(detected_ext)

    # set the default index according to the detected format in the selection box
    default_index = (
        file_type_options.index(target_format) 
        if target_format in file_type_options 
        else 0
    )

    # selection box for the file format
    file_type = st.selectbox(
        "File format",
        options=file_type_options,
        index=default_index
    )

    # continue only if a format is chosen
    if file_type == "Select format...":
        st.warning("Please specify the correct file format for this network.")
        return None

    # get the representation options e.g. edge list, adjacency matrix...
    representation_options = get_available_representations()
    current_cached_type = st.session_state.get("representation_type_key", representation_options[0])
    default_rep_index = (
        representation_options.index(current_cached_type) 
        if current_cached_type in representation_options 
        else 0
    )

    # radio element for the network representation with default index
    representation = st.radio(
        "Select Network Representation: ",
        options=representation_options,
        index=default_rep_index,          
        key="representation_type_key" 
    )

    # checkbox for directed networks
    directed = st.checkbox(
        "Directed network",
        value=False,
    )

    return FileUploadConfig(
        file=uploaded_file,
        file_type=file_type,
        representation=representation,
        directed=directed,
    )
