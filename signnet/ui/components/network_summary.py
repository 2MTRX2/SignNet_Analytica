# network_summary.py

import streamlit as st

from signnet.models.SignedNetwork import SignedNetwork


def network_summary(network: SignedNetwork):
    """
    Displays a summary of the currently loaded network.
    """

    st.subheader("Network Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Nodes",
        network.number_of_nodes,
    )

    col2.metric(
        "Edges",
        network.number_of_edges,
    )

    col3.metric(
        "Directed",
        "Yes" if network.directed else "No",
    )