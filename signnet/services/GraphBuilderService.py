# GraphBuilderService.py
from pyvis.network import Network
from signnet.adapters.NetworkXAdapter import NetworkXAdapter
from signnet.models.SignedNetwork import SignedNetwork

from app.ui.AppStyle import AppStyle

class GraphBuilderService:
    """
    Executes graph-to-visual transformations and handles interactive HTML network generation.
    """

    def __init__(self):
        pass

    def build_network_html(self, network: SignedNetwork) -> str:
        """Transforms a canonical signed network into an interactive physics-based HTML visualization.

        Args:
            network (SignedNetwork): The fully initialized signed network domain model containing 
                the vertices and edges to visually represent.

        Returns:
            str: A compiled, standalone HTML and JavaScript string representing the physics-based graph view.
        """
        # Convert into NetworkX structure
        G = NetworkXAdapter.to_networkx(network)

        # Node label converting to strings
        for node in G.nodes():
            G.nodes[node]['label'] = str(node)

        # Edge colour and sign definition
        for u, v, data in G.edges(data=True):
            sign = int(data.get('sign', 1))
            
            # Green: Positive; Red: Negative
            edge_color = f"{AppStyle.EDGE_POSITIVE_HEX}" if sign > 0 else f"{AppStyle.EDGE_NEGATIVE_HEX}" 
            # Dashed: Negative
            edge_style = True if sign < 0 else False          

            data['color'] = edge_color
            data['dashes'] = edge_style
            data['title'] = f"Relation: {sign}"
            data['weight'] = abs(sign)

        # Pyvis network Instantiation
        net = Network(height="100%", width="100%", bgcolor="#ffffff", font_color="#000000") # type: ignore

        # NetworkX Graph into Pyvis
        net.from_nx(G)
        net.toggle_physics(True)
        
        # HTML content
        html_content = net.generate_html()

        responsive_css = """
        <style>
            html, body {
                height: 100% !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
            }
            .card, .card-body, #mynetwork {
                height: 100% !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
            }
        </style>
        """
        html_content = html_content.replace("</head>", f"{responsive_css}</head>")
        return html_content
