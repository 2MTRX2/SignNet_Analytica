# structure_page.py
from nicegui import ui

from app.ui.layout import shared_layout

def init_structure_page():
    @ui.page('/structure')
    def structure_page():
        with shared_layout():
            ui.label('Netzwerk-Struktur')
            # Hier kommt die komplexe Logik für Tabellen, Graphen etc. hin