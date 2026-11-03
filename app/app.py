# app.py
from contextlib import contextmanager
from nicegui import app, ui

from app.ui import style
from app.controller.AppState import get_session_state
from app.ui.pages.upload_page import upload_page
from app.ui.pages.centrality_page import centrality_page


@contextmanager
def base_layout(title: str):
    """Generates the unified, application-wide shell layout including headers and navigation drawers.

    Leverages python context management via yielding to securely inject multi-page view content 
    into a structured, responsive maximum-width layout grid. Enforces design system constraints
    by pulling core aesthetics directly from the centralized style repository.

    Args:
        title (str): Semantic descriptor of the active sub-view for logging and title mutations.
    """
    app_state = get_session_state()
    
    # 1. HEADER (Zentralisiertes Slate-Farbschema)
    with ui.header().classes('bg-slate-800 text-white items-center justify-between px-6 py-3 shadow-md'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('lan', size='md').classes('text-blue-400')
            ui.label('SignNet Analytica').classes('text-xl font-bold tracking-wide')
            ui.badge('v1.0.0', color='blue').classes('text-xs px-2')
        
        # Systemweiter Lade-Indikator, reaktiv gekoppelt an den asynchronen Verarbeitungsstatus
        ui.spinner(size='md', color='white').bind_visibility_from(app_state, 'is_loading')

    # 2. PERSISTENTE SEITENLEISTE (Dunkles Navigation-Drawer Design)
    with ui.left_drawer(fixed=True, value=True).classes('bg-slate-900 text-slate-300 p-4 border-r border-slate-800 w-[260px]'):
        ui.label('NAVIGATION').classes(style.SUBSECTION_HEADING + ' px-3')
        
        # Reaktive Link-Strukturen mit einheitlichen Hover-Aesthetics
        with ui.column().classes('w-full gap-1'):
            ui.link('🌐 Data Input / Upload', '/').classes(
                'w-full px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors text-sm font-medium'
            )
            ui.link('📊 Centrality Analysis', '/centrality').classes(
                'w-full px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors text-sm font-medium'
            )
            
        ui.separator().classes('border-slate-800 my-6')
        
        # Meta-Informationsblock (Entspricht dem alten Streamlit-About-Menü)
        with ui.column().classes('px-3 text-xs text-slate-500 gap-2'):
            ui.label('Chair of Microeconomics').classes('font-semibold text-slate-400')
            ui.label('University of Fribourg')
            with ui.row().classes('gap-2 mt-2'):
                ui.link('GitHub', 'https://github.com/2MTRX2/SignNet_Analytica').classes('text-blue-500 hover:underline')
                ui.link('Bugs', 'https://github.com/2MTRX2/SignNet_Analytica/issues').classes('text-blue-500 hover:underline')

    # 3. ZENTRALER INHALTSBEREICH (Nutzt das standardisierte Max-Width-Layout des Style Guides)
    with ui.column().classes('w-full max-w-7xl mx-auto p-8 gap-4'):
        # Das yield erlaubt es den einzelnen Routen, ihren Content direkt in diesen Column-Block zu injizieren
        yield


# ==================================================================
# DEFINITION DER MULTI-PAGE ROUTEN (Nutzen die Context-Manager-Syntax)
# ==================================================================

@ui.page('/')
def index_route():
    """Route für den Datenimport (Ehemals Sektion 1)."""
    with base_layout("Data Input"):
        upload_page()  # Inhalt wird sauber innerhalb des Max-Width-Rasters gerendert


@ui.page('/centrality')
def centrality_route():
    """Route für die Analyse-Pipelines (Ehemals Sektion 2)."""
    with base_layout("Centrality Analysis"):
        centrality_page()  # Inhalt wird sauber innerhalb des Max-Width-Rasters gerendert


