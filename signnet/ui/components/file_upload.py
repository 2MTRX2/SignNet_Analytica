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
    """Stores the user's file upload configuration."""
    file: Optional[object]
    file_type: str
    representation: str
    directed: bool

def file_upload() -> Optional[FileUploadConfig]:
    """
    Renders the file upload component with automatic format detection
    and strict extension validation.

    Returns:
        FileUploadConfig if a file has been selected and validated,
        otherwise None.
    """
    allowed_extensions = list(STRATEGY_REGISTRY.keys())
    if "excel" in allowed_extensions:
        allowed_extensions.remove("excel")
        allowed_extensions.extend(["xlsx", "xls"])

    # input box
    uploaded_file = st.file_uploader(
        "Choose a network file (Drag & Drop or click Browse)",
        type=allowed_extensions,
        accept_multiple_files=False
    )

    if uploaded_file is None:
        return None

    detected_ext = uploaded_file.name.split(".")[-1].lower()

    available_formats = get_available_file_types()
    file_type_options = ["Select format..."] + available_formats
    
    target_format = EXTENSION_TO_FORMAT.get(detected_ext)
    
    default_index = (
        file_type_options.index(target_format) 
        if target_format in file_type_options 
        else 0
    )

    file_type = st.selectbox(
        "File format",
        options=file_type_options,
        index=default_index
    )

    if file_type == "Select format...":
        st.warning("Please specify the correct file format for this network.")
        return None
    
    representation_options = get_available_representations()
    current_cached_type = st.session_state.get("representation_type_key", representation_options[0])
    default_rep_index = (
        representation_options.index(current_cached_type) 
        if current_cached_type in representation_options 
        else 0
    )

    representation = st.radio(
        "Select Network Representation: ",
        options=representation_options,
        index=default_rep_index,          
        key="representation_type_key" 
    )

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
