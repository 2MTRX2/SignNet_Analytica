# app/ui/pages/upload_page.py
from nicegui import app, ui
from app.ui import style  # Zentralisiertes Design-System importieren
from app.controller.AppState import AppState, get_session_state
from app.controller.LoadingController import LoadingController
from app.controller.GraphBuilderController import GraphBuilderController
from signnet.io.DatasetRegistry import DatasetRegistry
from signnet.io.LoadingRegistry import REPRESENTATION_REGISTRY, STRATEGY_REGISTRY

# Controller instanziieren
upload_ctrl = LoadingController()
graph_ctrl = GraphBuilderController()


def handle_file_selection(e):
    """
    Schritt 1: Wird gefeuert, sobald eine Datei hochgeladen wird.
    Liest vorab die Spaltennamen aus, falls es eine Edge List ist.
    """
    app_state = get_session_state()
    
    # Datei-Stream zwischenspeichern (wichtig, da wir ihn erst beim Klick final parsen)
    app.storage.tab['pending_file_bytes'] = e.content.read()
    e.content.seek(0)
    
    if app_state.selected_repr_type == "Edge List":
        try:
            # Temporären Loader bauen, um Spaltenköpfe (Header) auszulesen
            temp_rep = REPRESENTATION_REGISTRY["Edge List"]()
            fmt = app_state.selected_file_type.lower()
            
            if fmt not in STRATEGY_REGISTRY:
                raise ValueError(f"Ungültiges Dateiformat: {app_state.selected_file_type}")
                
            temp_loader = STRATEGY_REGISTRY[fmt](temp_rep)
            
            # Nur die rohen Spaltennamen einlesen
            df_raw = temp_loader.read_raw(e.content)
            available_cols = list(df_raw.columns)
            
            # Spalten im State ablegen und Standard-Indizes wählen
            app_state.available_columns = available_cols

            if len(available_cols) >= 3:
                app_state.source_column_name = available_cols[0]
                app_state.target_column_name = available_cols[1]
                app_state.sign_column_name = available_cols[2]
                
            ui.notify("Datei-Struktur erkannt! Bitte ordne jetzt die Spalten zu.", type='info')
            input_fields_container.refresh() # UI-Formular aktualisieren (Dropdowns einblenden)
            
        except Exception as ex:
            ui.notify(f"Datei konnte nicht gelesen werden: {str(ex)}", type='negative')
    else:
        # Bei Adjacency Matrix brauchen wir kein Mapping, also direkt verarbeiten
        process_final_network(e.content)


def process_final_network(file_buffer=None):
    """Schritt 2: Führt das finale Laden des Netzwerks und Generieren der Grafik aus."""
    state = get_session_state()
    
    # Falls der Buffer aus dem Klick-Event kommt, oder aus dem Tab-Speicher geholt wird
    if file_buffer is None:
        import io
        if 'pending_file_bytes' not in app.storage.tab:
            ui.notify("Bitte wähle zuerst eine Datei aus!", type='warning')
            return
        file_buffer = io.BytesIO(app.storage.tab['pending_file_bytes'])

    try:
        # UploadController ausführen
        upload_ctrl.process_upload(file_buffer, state)
        ui.notify("Netzwerk-Architektur erfolgreich berechnet!", type='positive')
        
        # Pyvis-Grafik generieren
        graph_ctrl.generate_visualization(state)
        visualization_container.refresh()
        
    except Exception as error:
        ui.notify(f"Fehler: {str(error)}", type='negative', close_button=True)


def handle_predefined_selection(e):
    """UI-Handler für vordefinierte Datensätze."""
    if not e.value:
        return
    state = get_session_state()
    try:
        upload_ctrl.process_predefined_upload(e.value, state)
        ui.notify(f"Beispiel '{e.value}' geladen!", type='positive')
        
        # Formular zurücksetzen, da Beispieldaten fertig definiert sind
        state.available_columns = None

        input_fields_container.refresh()
        
        graph_ctrl.generate_visualization(state)
        visualization_container.refresh()
    except Exception as error:
        ui.notify(f"Fehler: {str(error)}", type='negative')


@ui.refreshable
def input_fields_container(state: AppState):
    """Rendert die dynamische Parser- und Spaltenkonfiguration."""
    ui.markdown("#### ⚙️ Parser-Konfiguration").classes('text-slate-700 font-semibold mb-2')
    
    available_cols = state.available_columns 

    with ui.column().classes('w-full gap-3'):
        with ui.row().classes('w-full gap-4'):
            ui.select(options=['csv', 'excel', 'json'], label='Dateiformat').bind_value(state, 'selected_file_type').classes(style.INPUT_HALF_WIDTH)
            ui.select(options=['Edge List', 'Adjacency Matrix'], label='Repräsentation').bind_value(state, 'selected_repr_type').classes(style.INPUT_HALF_WIDTH)

        ui.checkbox('Gerichtetes Netzwerk (Directed)').bind_value(state, 'is_directed').classes('my-1')

        # DYNAMISCHES SPALTEN-MAPPING (Das Herzstück deines Upload-Selectors!)
        if state.selected_repr_type == 'Edge List':
            ui.separator().classes('my-2')
            if available_cols:
                ui.markdown("##### 🔍 Spaltenzuordnung ausführen").classes('text-xs font-bold text-blue-600')
                ui.label("Ordne die erkannten Spalten den Netzwerkrollen zu:").classes('text-xs text-slate-500 -mt-2')
                with ui.row().classes('w-full gap-4'):
                    ui.select(options=available_cols, label='Source Column').bind_value(state, 'source_column_name').classes('flex-1')
                    ui.select(options=available_cols, label='Target Column').bind_value(state, 'target_column_name').classes('flex-1')
                    ui.select(options=available_cols, label='Sign/Value Column').bind_value(state, 'sign_column_name').classes('flex-1')
                
                # Der "Verarbeiten"-Button wird eingeblendet, sobald die Spalten da sind
                ui.button("Netzwerk-Architektur berechnen", on_click=lambda: process_final_network()).classes(style.BTN_SUCCESS + ' mt-2')
            else:
                # Textfelder als Fallback/Platzhalter, bevor eine Datei gewählt wurde
                ui.markdown("##### Spaltennamen (Vorauswahl)").classes('text-xs font-bold text-slate-400')
                with ui.row().classes('w-full gap-4'):
                    ui.input(label='Source').bind_value(state, 'source_column_name').classes('flex-1').props('disabled')
                    ui.input(label='Target').bind_value(state, 'target_column_name').classes('flex-1').props('disabled')
                    ui.input(label='Sign').bind_value(state, 'sign_column_name').classes('flex-1').props('disabled')


@ui.refreshable
def visualization_container(state: AppState):
    """Rendert die Pyvis-Grafik-Vorschau."""
    if state.current_network is None:
        with ui.card().classes(style.CARD_PLACEHOLDER):
            ui.icon('cloud_upload', size='xl').classes('text-slate-300')
            ui.label("Warte auf gültiges Netzwerk...").classes('text-slate-400 font-medium mt-2')
        return

    ui.markdown("### 🌐 Interaktive Netzwerk-Vorschau").classes(style.SECTION_HEADING + ' mt-4')
    with ui.card().classes('w-full p-2 shadow-sm border border-slate-200 overflow-hidden'):
        if state.network_visualization_html:
            ui.html(state.network_visualization_html).classes('w-full h-[520px]')
        else:
            with ui.row().classes('w-full justify-center items-center h-64'):
                ui.spinner(size='md')


def upload_page():
    """Haupt-Layout der Upload-Seite."""
    state = get_session_state()

    ui.label("1. Data Input & Configuration").classes(style.PAGE_TITLE)
    ui.label("Lade deine Netzwerkdaten hoch oder nutze Beispieldatensätze.").classes(style.PAGE_SUBTITLE)

    with ui.row().classes('w-full gap-6 items-start'):
        with ui.column().classes('w-full md:w-5/12 gap-4'):
            with ui.card().classes(style.CARD_STANDARD):
                ui.markdown("#### 📂 Datenquelle auswählen").classes('text-slate-700 font-semibold mb-2')
                
                with ui.tabs().classes('w-full border-b border-slate-200') as tabs:
                    manual_tab = ui.tab('Datei hochladen')
                    predefined_tab = ui.tab('Beispiel-Datensätze')
                
                with ui.tab_panels(tabs, value=manual_tab).classes('w-full bg-transparent shadow-none p-0 mt-4'):
                    with ui.tab_panel(manual_tab).classes('p-0 gap-4'):
                        input_fields_container(state)
                        
                        ui.markdown("##### Datei auswählen").classes('text-xs font-bold text-slate-500 mt-4')
                        ui.upload(
                            label='Netzwerkdatei auswählen',
                            on_upload=handle_file_selection,
                            auto_upload=True
                        ).classes('w-full border border-slate-200 rounded-lg shadow-none')
                    
                    with ui.tab_panel(predefined_tab).classes('p-0 gap-4'):
                        ui.markdown("##### Muster-Netzwerk wählen").classes('text-xs font-bold text-slate-500')
                        available_datasets = DatasetRegistry.get_available_names()
                        ui.select(options=[''] + available_datasets, label='Verfügbare Test-Netzwerke', on_change=handle_predefined_selection).classes(style.INPUT_MAX_WIDTH)

        with ui.column().classes('flex-1 min-w-[350px]'):
            visualization_container(state)

