# file_upload.py
from dataclasses import dataclass
from typing import Optional
import streamlit as st

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
    uploaded_file = st.file_uploader(
        "Choose a network file (Drag & Drop or click Browse)",
        type=["csv", "xlsx", "xls", "json"],
    )

    if uploaded_file is None:
        return None

    detected_ext = uploaded_file.name.split(".")[-1].lower()
    
    default_index = 0 
    
    if detected_ext == "csv":
        default_index = 1  # CSV
    elif detected_ext in ["xlsx", "xls"]:
        default_index = 2  # Excel
    elif detected_ext == "json":
        default_index = 3  # JSON

    file_type = st.selectbox(
        "File format",
        [
            "Select format...",  # Index 0
            "CSV",               # Index 1
            "Excel",             # Index 2
            "JSON"               # Index 3
        ],
        index=default_index
    )

    if file_type == "Select format...":
        st.warning("Please specify the correct file format for this network.")
        return None

    representation = st.radio(
        "Network representation",
        [
            "Edge List",
            "Adjacency Matrix",
        ],
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

