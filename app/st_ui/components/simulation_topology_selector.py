# simulation_topology_selector.py

import streamlit as st


def simulation_topology_selector(available_topologies: list[str]) -> str:
    """
    Displays a radio element containing all available centrality measure names
    and returns the name chosen by the user.

    Args:
        available_topologies (list[str]): A list of strings representing the names 
                                        of all supported network topologies.

    Returns:
        str: A string containing only the selected topology name.
    """
    # Render the native Streamlit multiselect dropdown component
    selected_topology = st.radio(
        label="Select one topology",
        options=available_topologies,
        horizontal=True,
        help="You can select one topology. Parameters will appear dynamically if required."
    )

    return selected_topology
