# GraphBuilder.py
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from signnet.adapters.NetworkXAdapter import NetworkXAdapter
from signnet.models.SignedNetwork import SignedNetwork


def create_graphical_signed_network(network: SignedNetwork):
    """Generates and renders an interactive, physics-based HTML visualization of the signed network.

    Converts the domain SignedNetwork object into a NetworkX graph structure using an 
    adapter pattern. It then maps structural edge attributes to visual aesthetics—using green 
    solid lines for positive relations and red dashed lines for negative relations—before 
    injecting the compiled Pyvis physics simulation natively into the Streamlit layout.

    Args:
        network (SignedNetwork): The fully initialized network containing the nodes 
            and signed edges to visually represent.

    Returns:
        None: This function handles side effects by rendering an interactive HTML 
            component directly into the active Streamlit view.
    """
    # Convert the network into a networkx structre with an appropriate adapter
    G = NetworkXAdapter.to_networkx(network)

    # Looping over each node and defining the edge colour and edge style for each node
    for u, v, data in G.edges(data=True):
        sign = int(data.get('sign', 1))
        
        # Colour metric
        edge_color = "#2ca02c" if sign > 0 else "#d62728"  
        edge_style = True if sign < 0 else False          

        data['color'] = edge_color
        data['dashes'] = edge_style
        data['title'] = f"Relation: {sign}"
        data['weight'] = abs(sign)

    # Instantiate a Pyvis network
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="#000000")

    # Using the networkx as an input for the Pyvis network
    net.from_nx(G)
    
    net.toggle_physics(True)
    
    try:
        # Compile the network into a HTML and JS
        html_content = net.generate_html()
        # Streamlit function to embed the compiled network
        components.html(html_content, height=520, scrolling=True)
    except Exception as e:
        st.error(f"Could not render network visualization: {e}")
