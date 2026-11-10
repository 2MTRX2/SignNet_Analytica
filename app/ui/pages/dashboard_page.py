# dashboard.py
from nicegui import ui
from app.ui.layout import shared_layout
from app.ui.AppStyle import AppStyle  # Import für dein Design-System

def init_dashboard_page():
    @ui.page('/')  # Registriert die absolute Startseite
    def dashboard_page():
        with shared_layout():
        
            # Titel 
            with ui.column().classes('w-full mb-6 gap-xs'):
                ui.label("SignNet Analytica").classes(f'text-3xl {AppStyle.FONT_SANS} {AppStyle.TEXT_MAIN}')
            
            # Grid for pages
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-6 w-full'):
                
                # Network Library
                with ui.card().classes(f'p-6 cursor-pointer {AppStyle.CARD_BG} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE} {AppStyle.HOVER_NAV}') \
                        .on('click', lambda: ui.navigate.to('/library')):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('local_library', size='lg').classes(AppStyle.ACCENT_TEXT)
                        with ui.column().classes('gap-none'):
                            ui.label('Network Library').classes(f'text-lg font-bold {AppStyle.TEXT_MAIN}')
                            ui.label('Upload and manage network datasets.').classes(f'text-sm {AppStyle.TEXT_MUTED}')

                # Network Structure
                with ui.card().classes(f'p-6 cursor-pointer hover:scale-[1.02] hover:shadow-md transition-all duration-200 {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/structure')):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('hub', size='lg').classes(AppStyle.ACCENT_TEXT)
                        with ui.column().classes('gap-none'):
                            ui.label('Network Structure').classes(f'text-lg font-bold {AppStyle.TEXT_MAIN}')
                            ui.label('Analyze the topological structure and nodes of your networks with centrality measures.').classes(f'text-sm {AppStyle.TEXT_MUTED}')

                # Network Dynamics
                with ui.card().classes(f'p-6 cursor-pointer hover:scale-[1.02] hover:shadow-md transition-all duration-200 {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/dynamics')):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('timeline', size='lg').classes(AppStyle.ACCENT_TEXT)
                        with ui.column().classes('gap-none'):
                            ui.label('Network Dynamics').classes(f'text-lg font-bold {AppStyle.TEXT_MAIN}')
                            ui.label('Analyze the stability and efficiency of your networks over time.').classes(f'text-sm {AppStyle.TEXT_MUTED}')

                # Network Lab
                with ui.card().classes(f'p-6 cursor-pointer hover:scale-[1.02] hover:shadow-md transition-all duration-200 {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/lab')):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('science', size='lg').classes(AppStyle.ACCENT_TEXT)
                        with ui.column().classes('gap-none'):
                            ui.label('Network Lab').classes(f'text-lg font-bold {AppStyle.TEXT_MAIN}')
                            ui.label('Experiment freely with algorithms and test datasets.').classes(f'text-sm {AppStyle.TEXT_MUTED}')
