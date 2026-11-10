"""
-> Build it step by step: first uploading, then predefined datasets 
"""

# library_page.py
from nicegui import ui

from app.ui.layout import shared_layout

def init_library_page():
    @ui.page('/library')
    def library_page():
        with shared_layout():
            ui.label('Netzwerk-Bibliothek')
            # Hier kommt die komplexe Logik für Tabellen, Graphen etc. hin
