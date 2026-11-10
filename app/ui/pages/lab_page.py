# lab_page.py
from nicegui import ui

from app.ui.layout import shared_layout
from app.ui.AppStyle import AppStyle  

def init_lab_page():
    @ui.page('/lab')
    def lab_page():
        with shared_layout():
            with ui.column().classes('w-full mb-6 gap-xs'):
                ui.label("Stay Tuned...").classes(f'text-l {AppStyle.FONT_SANS} {AppStyle.TEXT_MAIN}')
