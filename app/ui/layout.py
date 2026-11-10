# layout.py
from nicegui import ui

def shared_layout(title: str = "SignNet Analytica"):
    """
    """
    # 1. Die Navigationsleiste (Header)
    with ui.header(elevated=True).classes('q-pa-md items-center justify-between'):
        with ui.row().classes('items-center gap-md'):
            ui.icon('share', size='sm')
            ui.label(title).classes('text-h6 font-bold')
        
        # Navigation Buttons
        with ui.row().classes('gap-sm'):
            ui.button('Network Library', on_click=lambda: ui.navigate.to('/library')).props('flat color=white')
            ui.button('Network Structure', on_click=lambda: ui.navigate.to('/structure')).props('flat color=white')
            ui.button('Network Dynamics', on_click=lambda: ui.navigate.to('/dynamics')).props('flat color=white')
            ui.button('Network Lab', on_click=lambda: ui.navigate.to('/lab')).props('flat color=white')
