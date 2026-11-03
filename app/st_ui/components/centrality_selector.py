# centrality_selector.py

import streamlit as st


def centrality_selector(available_measures: list[str]) -> list[str]:
    """
    Displays a multiselect component containing all available centrality measure names
    and returns the names chosen by the user.

    Args:
        available_measures (list[str]): A list of strings representing the names 
                                        of all supported centrality algorithms.

    Returns:
        list[str]: A list of strings containing only the selected centrality measure names.
    """
    # Render the native Streamlit multiselect dropdown component
    selected_names = st.multiselect(
        label="Select one or more centrality measures",
        options=available_measures,
        help="You can select multiple metrics. Parameters will appear dynamically if required."
    )

    return selected_names
