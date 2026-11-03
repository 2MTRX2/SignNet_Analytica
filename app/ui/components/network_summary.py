# app/ui/components/network_summary.py
from nicegui import ui
from app.ui import style  # Zentralisiertes Design-System importieren
from signnet.models.SignedNetwork import SignedNetwork

def render_network_summary(network: SignedNetwork) -> None:
    """Renders a clean, modern KPI dashboard card row of the active network metrics.

    Displays key structural properties—specifically node count, edge count, and 
    directionality—using responsive layout columns for enhanced web aesthetics.

    Args:
        network (SignedNetwork): The active signed network domain model containing 
            the vertices and edges to summarize.
    """
    ui.markdown("### 📊 Network Summary").classes(style.SECTION_HEADING + ' mb-2')
    
    # Grid-Layout: Flex-Row mit automatischem Zeilenumbruch und flexiblem Stretching
    with ui.row().classes('w-full gap-4 items-stretch mb-4'):
        
        # Karte 1: Knoten (Nodes) - Nutzt den standardisierten gedeckelten Hintergrund des Style Guides
        with ui.card().classes(style.CARD_MUTED + ' flex-1 min-w-[150px] items-center p-4'):
            ui.label('Nodes').classes(style.SUBSECTION_HEADING)
            ui.label(str(network.number_of_nodes)).classes('text-3xl font-extrabold text-slate-800 mt-1 font-mono')
            
        # Karte 2: Kanten (Edges)
        with ui.card().classes(style.CARD_MUTED + ' flex-1 min-w-[150px] items-center p-4'):
            ui.label('Edges').classes(style.SUBSECTION_HEADING)
            ui.label(str(network.number_of_edges)).classes('text-3xl font-extrabold text-slate-800 mt-1 font-mono')
            
        # Karte 3: Ausrichtung (Directed)
        with ui.card().classes(style.CARD_MUTED + ' flex-1 min-w-[150px] items-center p-4'):
            ui.label('Directed').classes(style.SUBSECTION_HEADING)
            status_text = "Yes" if network.directed else "No"
            color_class = "text-blue-600" if network.directed else "text-slate-600"
            ui.label(status_text).classes(f'text-3xl font-extrabold mt-1 {color_class}')
