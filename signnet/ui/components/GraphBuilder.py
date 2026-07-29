# GraphBuilder.py
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from signnet.adapters.NetworkXAdapter import NetworkXAdapter
from signnet.models.SignedNetwork import SignedNetwork

def create_graphical_signed_network(network: SignedNetwork):
    """Generates an interactive physics-based visualization of the signed network.
    
    Enriches the existing NetworkX graph structure with visual attributes (colors, styles)
    and renders it dynamically into the Streamlit UI via Pyvis.
    """
    G = NetworkXAdapter.to_networkx(network)
    
    for u, v, data in G.edges(data=True):
        sign = int(data.get('sign', 1))
        
        # Colour metric
        edge_color = "#2ca02c" if sign > 0 else "#d62728"  
        edge_style = True if sign < 0 else False          

        data['color'] = edge_color
        data['dashes'] = edge_style
        data['title'] = f"Relation: {sign}"
        data['weight'] = abs(sign)

    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="#000000")
    
    net.from_nx(G)
    
    net.toggle_physics(True)
    
    try:
        html_content = net.generate_html()
        components.html(html_content, height=520, scrolling=True)
    except Exception as e:
        st.error(f"Could not render network visualization: {e}")
