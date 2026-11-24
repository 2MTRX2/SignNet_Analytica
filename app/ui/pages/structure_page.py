# structure_page.py
import io
from nicegui import events, ui

from app.ui.layout import shared_layout
from app.ui.AppStyle import AppStyle
from app.controller.AppState import get_session_state
from app.controller.LoadingController import LoadingController
from signnet.io.LoadingRegistry import REPRESENTATION_REGISTRY, STRATEGY_REGISTRY

def init_structure_page():
    @ui.page('/structure')
    async def structure_page():
        await ui.context.client.connected() 
        with shared_layout():
            await ui.context.client.connected()
            state = get_session_state()
            pending_file: dict[str, bytes | None] = {'bytes': None}
            ui.label('Netzwerk-Struktur')
            # Hier kommt die komplexe Logik für Tabellen, Graphen etc. hin

