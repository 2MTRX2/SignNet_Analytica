# app/ui/pages/centrality_page.py
from nicegui import app, ui

from signnet.analysis.centrality.CentralityRegistry import CentralityRegistry
from app.ui import style  # Zentralisiertes Design-System importieren
from app.controller.AppState import AppState, get_session_state
from app.controller.CentralityController import CentralityController
from app.ui.components.network_summary import render_network_summary
from app.ui.components.correlation_component import render_correlation_analysis_ui 
from app.ui.components.simulation_component import render_simulation_benchmarking_ui

# Instantiierung des Controllers
centrality_ctrl = CentralityController()


def handle_run_analysis():
    state = get_session_state()
    try:
        # 1. Controller rechnet und schreibt Daten in den State
        centrality_ctrl.run_analysis(state)
        ui.notify("Zentralitätsanalyse erfolgreich abgeschlossen!", type='positive')
        
        # 2. DIE SAUBERE LÖSUNG: Wir rufen das Refresh einfach DIREKT im Erfolgsfall auf!
        results_section_ui.refresh()
        
    except Exception as e:
        ui.notify(f"Fehler bei der Berechnung: {str(e)}", type='negative', close_button=True)

@ui.refreshable
def dynamic_parameters_form_ui(app_state: AppState):
    """Generiert reaktiv Eingabefelder für Metriken, die konfigurierbare Parameter besitzen."""
    if not app_state.selected_measure_names:
        return

    has_parameters = any(
        len(CentralityRegistry.get_measure_class(name).PARAMETERS) > 0 
        for name in app_state.selected_measure_names
    )

    if has_parameters:
        ui.markdown("#### Metrik-Parameter konfigurieren").classes(style.SUBSECTION_HEADING + ' mt-4')
        
        with ui.card().classes(style.CARD_MUTED):
            for name in app_state.selected_measure_names:
                measure_class = CentralityRegistry.get_measure_class(name)
                params = measure_class.PARAMETERS  # Erwartet ein Dict oder eine Liste aus der Registry
                
                if params:
                    ui.label(f"Parameter für {name}:").classes('font-semibold text-xs text-blue-600 mb-1')
                    # Sicherstellen, dass das Sub-Dict im State existiert
                    if name not in app_state.runtime_parameters:
                        app_state.runtime_parameters[name] = {} # type: ignore
                        
                    for p_name, p_config in params.items(): # type: ignore
                        # Generiert Eingabefelder basierend auf dem Typ in deiner Registry
                        if p_config.get("type") == "float":
                            ui.number(
                                label=p_config.get("label", p_name),
                                format='%.4f',
                                step=0.01
                            ).bind_value(app_state.runtime_parameters[name], p_name).classes(style.INPUT_HALF_WIDTH + ' mb-2') # type: ignore
                        elif p_config.get("type") == "int":
                            ui.number(
                                label=p_config.get("label", p_name),
                                step=1
                            ).bind_value(app_state.runtime_parameters[name], p_name).classes(style.INPUT_HALF_WIDTH + ' mb-2') # type: ignore


@ui.refreshable
def results_section_ui(app_state: AppState):
    """Rendert die Ergebnistabelle und Folgeanalysen, sobald Daten vorliegen."""
    if app_state.centrality_results is None:
        return

    ui.markdown("### Analyse-Ergebnisse").classes(style.SECTION_HEADING + ' mt-6')
    
    # 1. ERGEBNISTABELLE (AgGrid)
    with ui.card().classes(style.CARD_STANDARD + ' mb-6'):
        df_clean = app_state.centrality_results.reset_index() # type: ignore
        ui.aggrid.from_pandas(df_clean).classes('w-full h-80')

    ui.hr().classes('my-6') # type: ignore

    # 2. SUB-KOMPONENTE: KORRELATIONSANALYSE
    ui.markdown("#### 📊 Korrelations-Analyse").classes('text-xl font-semibold mb-2 text-slate-800')
    ui.label("Führe statistische Vergleiche zwischen den berechneten Metriken durch.").classes('text-slate-500 mb-4 text-sm')
    render_correlation_analysis_ui(app_state)

    ui.hr().classes('my-6') # type: ignore

    # 3. SUB-KOMPONENTE: SIMULATIONS BENCHMARKING
    ui.markdown("#### ⚙️ Simulation & Benchmarking").classes('text-xl font-semibold mb-2 text-slate-800')
    ui.label("Vergleiche dein empirisches Netzwerk mit synthetischen Topologien.").classes('text-slate-500 mb-4 text-sm')
    
    # KORREKTUR: 'state' existierte hier lokal nicht, wurde auf 'app_state' korrigiert!
    render_simulation_benchmarking_ui(app_state)


def on_measure_selection_changed(e):
    """Wird gefeuert, wenn der Nutzer Maße auswählt oder abwählt."""
    app_state = get_session_state()
    app_state.selected_measure_names = e.value
    # Parameter-Formular reaktiv neu zeichnen
    dynamic_parameters_form_ui.refresh()


def centrality_page():
    """Die Hauptseite für die Zentralitätsanalyse im Browser."""
    app_state = get_session_state()

    # Sicherheitsnetz: Wenn im Upload-Bereich kein Netzwerk geladen wurde
    if app_state.current_network is None:
        with ui.card().classes(style.CARD_WARNING):
            ui.icon('warning', size='lg').classes('text-amber-500')
            ui.label("Kein Netzwerk aktiv").classes('text-xl font-bold text-amber-800 my-2')
            ui.label("Bitte lade zuerst im Upload-Bereich eine Netzwerkdatei oder ein vordefiniertes Dataset hoch.").classes('text-slate-600 text-sm')
        return

    # KPI Summary Cards rendern
    render_network_summary(app_state.current_network)
    
    ui.hr().classes('my-4') # type: ignore

    # --- HAUPTLAYOUT ---
    ui.label("Zentralitäts-Analyse").classes(style.PAGE_TITLE)
    ui.label("Berechne strukturelle Metriken für dein geladenes Signed Network.").classes(style.PAGE_SUBTITLE)

    # 1. METRIK-AUSWAHL (Multi-Select)
    measure_options = CentralityRegistry.get_available_names()
    
    with ui.card().classes(style.CARD_STANDARD + ' mb-4'):
        ui.markdown("#### 1. Zentralitätsmaße auswählen").classes('text-slate-700 font-semibold mb-2')
        ui.select(
            options=measure_options,
            multiple=True,
            value=app_state.selected_measure_names,
            on_change=on_measure_selection_changed,
            label="Zentralitätsmetriken"
        ).classes(style.INPUT_MAX_WIDTH)

        # Dynamisches Parameter-Formular platzieren (reaktiv eingebettet)
        dynamic_parameters_form_ui(app_state)

    # 2. RUN-BUTTON & SPINNER
    with ui.row().classes('items-center gap-4 my-4'):
        ui.button(
            "Analyse ausführen", 
            on_click=handle_run_analysis
        ).bind_enabled_from(app_state, 'is_loading', backward=lambda x: not x).classes(style.BTN_PRIMARY)
        
        # Der Spinner taucht automatisch auf, wenn berechnet wird
        ui.spinner(size='lg').bind_visibility_from(app_state, 'is_loading')

    # 3. ERGEBNIS-BEREICH (Wird automatisch aktualisiert und eingeblendet)
    results_section_ui(app_state)
    
