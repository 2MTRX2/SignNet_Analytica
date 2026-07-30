# network_summary.py
import streamlit as st

from signnet.models.SignedNetwork import SignedNetwork


def network_summary(network: SignedNetwork):
    """Renders an interactive summary layout of the loaded network within the Streamlit UI.

    Utilizes Streamlit's structural grid columns to present key structural metrics 
    of the network—specifically node count, edge count, and directionality—in a 
    clean, modern kpi dashboard format.

    Args:
        network (SignedNetwork): The structured signed network object containing 
            the current node and edge data to analyze.

    Returns:
        None: This component directly renders visual elements to the active 
            Streamlit application context.
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