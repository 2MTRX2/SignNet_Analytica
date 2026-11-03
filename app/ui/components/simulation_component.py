# app/ui/components/simulation_component.py
import pandas as pd
from nicegui import app, ui
from app.ui import style  # Zentralisiertes Design-System importieren
from app.controller.AppState import AppState
from app.controller.SimulationController import SimulationController
from signnet.analysis.simulation.TopologyRegistry import TopologyRegistry

sim_ctrl = SimulationController()

def handle_run_simulation():
    """UI-Handler: Triggert das zeitintensive Simulations-Backend."""
    if 'state' not in app.storage.tab:
        return
    state: AppState = app.storage.tab['state']
    
    try:
        ui.notify("Simulationspipeline gestartet...", type='info')
        sim_ctrl.execute_simulation_pipeline(state)
        ui.notify("Simulation erfolgreich abgeschlossen!", type='positive')
        simulation_results_ui.refresh()
    except Exception as e:
        ui.notify(f"Simulationsfehler: {str(e)}", type='negative', close_button=True, timeout=8000)


def generate_download_bytes(df: pd.DataFrame, state: AppState) -> bytes:
    """Generiert die CSV-Datei inklusive der wissenschaftlichen Metadaten als Header."""
    meta_parts = [
        f"Topo: {state.selected_topology}",
        f"N: {state.sim_global_parameters.get('n')}", # type: ignore
        f"Iter: {state.sim_global_parameters.get('n_iterations')}", # type: ignore
        f"Neg_Ratio: {state.sim_global_parameters.get('neg_ratio')}" # type: ignore
    ]
    for param_name, param_value in state.sim_topology_kwargs.items(): # type: ignore
        meta_parts.append(f"{param_name}: {param_value}")
            
    meta_string = " | ".join(meta_parts)
    csv_string = meta_string + "\n" + df.reset_index().to_csv(index=False)
    return csv_string.encode("utf-8")


@ui.refreshable
def simulation_results_ui(state: AppState):
    """Rendert die reaktiven Dashboard-Ergebnisse (Tabs, Tabellen und ECharts)."""
    if state.sim_extremes_results is None or state.sim_gini_results is None:
        return

    # Dateinamen für Downloads berechnen
    topo_sanitized = str(state.selected_topology).lower().replace(' ', '_')

    with ui.tabs().classes('w-full border-b border-slate-200') as tabs:
        tab1 = ui.tab('📊 Extreme Values Benchmark')
        tab2 = ui.tab('⚖️ Gini-Coefficient')

    with ui.tab_panels(tabs, value=tab1).classes('w-full bg-transparent p-0 mt-4'):
        
        # ------------------------------------------------------------------
        # TAB 1: EXTREMWERTE-BENCHMARK
        # ------------------------------------------------------------------
        with ui.tab_panel(tab1).classes('p-0 gap-4'):
            ui.markdown("Average benchmark values across all iterations (maxima, minima, and general mean).").classes('text-xs text-slate-500 mb-2')
            
            # Simulations-Tabelle
            df_ext_clean = state.sim_extremes_results.reset_index()
            ui.aggrid.from_pandas(df_ext_clean).classes('w-full h-52')
            
            # 1. KORREKTUR: Download für Extremwerte (Ehemals Zeile 69)
            ext_bytes = generate_download_bytes(state.sim_extremes_results, state)

            # Ein normaler Button, der beim Klicken (on_click) den Download auslöst
            ui.button(
                "Download Extreme Values (CSV)", 
                on_click=lambda: ui.download(src=ext_bytes, filename=f"sim_extremes_{topo_sanitized}.csv")
            ).classes(style.BTN_SECONDARY + ' mt-2 text-xs')


            # Empirische Baseline (Echtes Eingangsnetzwerk)
            if state.sim_empirical_summary is not None:
                ui.markdown("### Empirical Network Metrics Summary").classes(style.SECTION_HEADING + ' mt-6 mb-1')
                ui.markdown("Aggregated baseline values (maximum, minimum, and mean) computed directly on your real input network.").classes('text-xs text-slate-500 mb-2')
                df_emp_clean = state.sim_empirical_summary.reset_index()
                ui.aggrid.from_pandas(df_emp_clean).classes('w-full h-52')

        # ------------------------------------------------------------------
        # TAB 2: GINI-KOEFFIZIENTEN (STRUKTURELLE UNGLEICHHEIT)
        # ------------------------------------------------------------------
        with ui.tab_panel(tab2).classes('p-0 gap-4'):
            ui.markdown("Average Gini-Coefficient per metric. Higher values indicate higher structural inequality.").classes('text-xs text-slate-500 mb-2')
            
            # Simulations-Tabelle Gini
            df_gini_clean = state.sim_gini_results.reset_index()
            ui.aggrid.from_pandas(df_gini_clean).classes('w-full h-52')
            
            # Download-Button für Gini
            # 2. KORREKTUR: Download-Button für Gini-Koeffizienten weiter unten
            # 2. KORREKTUR: Download für Gini-Koeffizienten weiter unten
            gini_bytes = generate_download_bytes(state.sim_gini_results, state)

            # Klick-Event löst den Download-Befehl aus
            ui.button(
                "Download Gini Coefficients (CSV)", 
                on_click=lambda: ui.download(src=gini_bytes, filename=f"sim_gini_{topo_sanitized}.csv")
            ).classes(style.BTN_SECONDARY + ' mt-2 text-xs mb-4')


            # --- ECHARTS BALKENDIAGRAMM (SIMULATION) ---
            chart_df = state.sim_gini_results.reset_index()
            options = {
                'title': { 'text': 'Simulated Mean Gini Coefficients' },
                'tooltip': {},
                'xAxis': { 'type': 'category', 'data': chart_df['metric_name'].tolist() },
                'yAxis': { 'type': 'value' },
                'series': [{ 'type': 'bar', 'data': chart_df['mean_gini_coefficient'].tolist(), 'itemStyle': { 'color': '#3b82f6' } }]
            }
            ui.echart(options=options).classes('w-full h-64 mt-4')

            # Empirische Baseline Gini (Echtes Eingangsnetzwerk)
            if state.sim_empirical_gini is not None:
                ui.markdown("### Empirical Network Metrics Summary").classes(style.SECTION_HEADING + ' mt-8 mb-1')
                ui.markdown("Aggregated Gini-Coefficients computed directly on your real input network.").classes('text-xs text-slate-500 mb-2')
                
                df_emp_gini_clean = state.sim_empirical_gini.reset_index()
                ui.aggrid.from_pandas(df_emp_gini_clean).classes('w-full h-52')

                # --- ECHARTS BALKENDIAGRAMM (EMPIRISCH) ---
                emp_chart_df = state.sim_empirical_gini.reset_index()
                emp_options = {
                    'title': { 'text': 'Empirical Gini Coefficients' },
                    'tooltip': {},
                    'xAxis': { 'type': 'category', 'data': emp_chart_df['metric_name'].tolist() },
                    'yAxis': { 'type': 'value' },
                    'series': [{ 'type': 'bar', 'data': emp_chart_df['gini_coefficient'].tolist(), 'itemStyle': { 'color': '#10b981' } }]
                }
                ui.echart(options=emp_options).classes('w-full h-64 mt-4')


def render_simulation_benchmarking_ui(state: AppState) -> None:
    """Orchestriert das Simulations-Setup-Layout auf dem Dashboard."""
    available_topologies = TopologyRegistry.get_available_topologies()
    
    if not state.selected_topology and available_topologies:
        state.selected_topology = available_topologies # type: ignore

    with ui.card().classes(style.CARD_STANDARD + ' mt-4'):
        ui.markdown("#### Configure Simulation Constraints").classes('text-slate-700 font-semibold mb-2')
        
        with ui.row().classes('items-center gap-4 my-2'):
            ui.button(
                "Run Simulation Pipeline", 
                on_click=handle_run_simulation
            ).bind_enabled_from(state, 'is_loading', backward=lambda x: not x).classes(style.BTN_PRIMARY)
            
            ui.spinner(size='lg').bind_visibility_from(state, 'is_loading')

        ui.separator().classes('my-4')
        
        # Bindet die reaktive Auswertungs-Sektion ein
        simulation_results_ui(state)
