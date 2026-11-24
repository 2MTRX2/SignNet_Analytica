# lab_page.py
import io
from nicegui import events, ui

from app.ui.layout import shared_layout
from app.ui.AppStyle import AppStyle
from app.controller.AppState import get_session_state
from app.controller.LoadingController import LoadingController
from signnet.io.LoadingRegistry import REPRESENTATION_REGISTRY, STRATEGY_REGISTRY

def init_lab_page():
    @ui.page('/lab')
    async def lab_page():
        await ui.context.client.connected() 
        with shared_layout():
            await ui.context.client.connected()
            state = get_session_state()
            pending_file: dict[str, bytes | None] = {'bytes': None}
            with ui.column().classes('w-full mb-6 gap-xs'):
                ui.label("Stay Tuned...").classes(f'text-l {AppStyle.FONT_SANS} {AppStyle.TEXT_MAIN}')

