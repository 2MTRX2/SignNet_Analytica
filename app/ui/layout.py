# layout.py
from contextlib import contextmanager
from typing import Optional
from nicegui import ui

from app.ui.AppStyle import AppStyle

@contextmanager
def shared_layout(title: str = "SignNet Analytica", content_bg: Optional[str] = None):
    """
    A context manager that provides a shared layout for NiceGUI pages.
    """
    bg_class = content_bg if content_bg else AppStyle.MAIN_BG
    ui.query('body').classes(AppStyle.MAIN_BG)

    # create a row that fills the entire viewport height and width  
    with ui.row().classes('w-full h-screen p-4 gap-4 no-wrap items-stretch bg-slate-100'):
        
        # Sidebar
        with ui.column().classes(f'{AppStyle.SIDEBAR_BG} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE} p-6 w-64 h-full shrink-0 {AppStyle.SHADOW_SMOOTH}'):
            
            # Logo & Dashboard Link
            with ui.link(target='/').classes('text-current no-underline hover:opacity-70 transition-opacity w-full'):
                with ui.row().classes('items-center gap-md mb-6 px-2 cursor-pointer no-wrap'):
                    ui.icon('share', size='md').classes(AppStyle.ACCENT_TEXT)
                    with ui.column().classes('gap-none'):
                        ui.label("SignNet").classes(f'text-xl font-bold tracking-tight {AppStyle.TEXT_MAIN} leading-none')
                        ui.label("Analytica").classes(f'text-xs {AppStyle.TEXT_MUTED} font-medium tracking-widest uppercase')
                    ui.icon('share', size='md').classes(f'{AppStyle.ACCENT_TEXT} flip-horizontal')
            
            # Vertical Navigation Buttons
            with ui.column().classes('w-full gap-xs'):
                ui.button('Network Library', on_click=lambda: ui.navigate.to('/library')).props('flat align=left no-caps').classes(f'w-full text-base font-normal {AppStyle.TEXT_NAV} {AppStyle.ROUNDED_MEDIUM} py-2.5 {AppStyle.HOVER_NAV}')
                ui.button('Network Structure', on_click=lambda: ui.navigate.to('/structure')).props('flat align=left no-caps').classes(f'w-full text-base font-normal {AppStyle.TEXT_NAV} {AppStyle.ROUNDED_MEDIUM} py-2.5 {AppStyle.HOVER_NAV}')
                ui.button('Network Dynamics', on_click=lambda: ui.navigate.to('/dynamics')).props('flat align=left no-caps').classes(f'w-full text-base font-normal {AppStyle.TEXT_NAV} {AppStyle.ROUNDED_MEDIUM} py-2.5 {AppStyle.HOVER_NAV}')
                ui.button('Network Lab', on_click=lambda: ui.navigate.to('/lab')).props('flat align=left no-caps').classes(f'w-full text-base font-normal {AppStyle.TEXT_NAV} {AppStyle.ROUNDED_MEDIUM} py-2.5 {AppStyle.HOVER_NAV}')

        # Content Area

        # If the background class is the same as the card background, we can add a border and shadow for better visual separation
        is_white = bg_class == AppStyle.MAIN_BG
        card_effects = f'{AppStyle.BORDER_CLEAN} {AppStyle.SHADOW_SMOOTH}' if is_white else ''
        
        with ui.column().classes(f'p-8 {bg_class} {card_effects} {AppStyle.ROUNDED_LARGE} h-full grow overflow-auto {AppStyle.TEXT_MAIN}'):
            yield
