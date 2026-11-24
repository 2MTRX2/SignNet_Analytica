# dashboard.py
from nicegui import ui
from app.ui.layout import shared_layout
from app.ui.AppStyle import AppStyle 

def init_dashboard_page():
    @ui.page('/')  
    async def dashboard_page():
        await ui.context.client.connected() 
        with shared_layout():
        
            # Titel 
            with ui.column().classes('w-full mb-6 gap-xs'):
                ui.label("SignNet Analytica").classes(f'text-3xl {AppStyle.FONT_SANS} {AppStyle.TEXT_MAIN}')
            
            # Grid for pages
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-6 w-full'):
                
                # Network Library
                with ui.card().classes(f'p-6 cursor-pointer {AppStyle.HOVER_CARD} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/library')):
                    with ui.row().classes('items-center gap-4 no-wrap w-full'):
                        ui.icon('local_library', size='lg').classes(f'{AppStyle.ACCENT_TEXT} shrink-0')
                        with ui.column().classes('gap-none flex-1'):
                            ui.label('Network Library').classes(f'text-lg {AppStyle.TEXT_MAIN}')
                            ui.label('Upload and manage network datasets.').classes(f'text-sm {AppStyle.TEXT_MUTED}')

                # Network Structure
                with ui.card().classes(f'p-6 cursor-pointer {AppStyle.HOVER_CARD} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/structure')):
                    with ui.row().classes('items-center gap-4 no-wrap w-full'):
                        ui.icon('hub', size='lg').classes(f'{AppStyle.ACCENT_TEXT} shrink-0')
                        with ui.column().classes('gap-none flex-1'):
                            ui.label('Network Structure').classes(f'text-lg {AppStyle.TEXT_MAIN}')
                            ui.label('Analyze the topological structure and nodes of your networks with centrality measures.').classes(f'text-sm {AppStyle.TEXT_MUTED}')


                # Network Dynamics
                with ui.card().classes(f'p-6 cursor-pointer {AppStyle.HOVER_CARD} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/dynamics')):
                    with ui.row().classes('items-center gap-4 no-wrap w-full'):
                        ui.icon('timeline', size='lg').classes(AppStyle.ACCENT_TEXT)
                        with ui.column().classes('gap-none'):
                            ui.label('Network Dynamics').classes(f'text-lg {AppStyle.TEXT_MAIN}')
                            ui.label('Analyze the stability and efficiency of your networks over time.').classes(f'text-sm {AppStyle.TEXT_MUTED}')

                # Network Lab
                with ui.card().classes(f'p-6 cursor-pointer {AppStyle.HOVER_CARD} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}') \
                        .on('click', lambda: ui.navigate.to('/lab')):
                    with ui.row().classes('items-center gap-4 no-wrap w-full'):
                        ui.icon('science', size='lg').classes(AppStyle.ACCENT_TEXT)
                        with ui.column().classes('gap-none'):
                            ui.label('Network Lab').classes(f'text-lg {AppStyle.TEXT_MAIN}')
                            ui.label('Experiment freely with algorithms and test datasets.').classes(f'text-sm {AppStyle.TEXT_MUTED}')
