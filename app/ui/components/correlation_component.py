# app/ui/components/correlation_component.py
import pandas as pd
from typing import cast
from nicegui import app, ui
from app.ui import style  # Zentralisiertes Design-System importieren
from app.controller.AppState import AppState
from app.controller.CorrelationController import CorrelationController
from signnet.analysis.correlations.CorrelationRegistry import CorrelationRegistry

corr_ctrl = CorrelationController()

def highlight_p_values(df: pd.DataFrame, alpha_level: float) -> pd.DataFrame:
    """Generates a conditional styling matrix for a pandas DataFrame based on statistical significance thresholds."""
    style_df = pd.DataFrame("color: gray;", index=df.index, columns=df.columns)
    for col in df.columns:
        for idx in df.index:
            if idx == col:
                style_df.loc[idx, col] = "color: darkgray; font-style: italic;"
            elif cast(float, df.loc[idx, col]) < alpha_level:
                style_df.loc[idx, col] = "color: green; font-weight: bold;"
    return style_df


def handle_correlation_change():
    """Triggert den Controller bei Parameter-Änderungen und aktualisiert die Sektion."""
    if 'state' not in app.storage.tab:
        return
    state: AppState = app.storage.tab['state']
    
    try:
        corr_ctrl.run_correlation_analysis(state)
        correlation_tabs_ui.refresh()
    except Exception as e:
        ui.notify(f"Korrelations-Fehler: {str(e)}", type='negative')


@ui.refreshable
def correlation_tabs_ui(state: AppState):
    """Rendert die reaktiven Ergebnistabs für Koeffizienten und p-Werte."""
    if state.correlation_matrix is None or state.p_value_matrix is None:
        return

    # Tabs erzeugen (moderne Alternative zu st.tabs)
    with ui.tabs().classes('w-full border-b border-slate-200') as tabs:
        tab1 = ui.tab('Correlation Coefficients')
        tab2 = ui.tab('p-Values (Significance)')

    with ui.tab_panels(tabs, value=tab1).classes('w-full bg-transparent p-0 mt-4'):
        # TAB 1: KORRELATIONSKOEFFIZIENTEN
        with ui.tab_panel(tab1).classes('p-0 gap-2'):
            ui.markdown("Values closer to 1.0 or -1.0 indicate strong positive or negative correlations.").classes('text-xs text-slate-500 mb-2')
            # Nutzt das Pandas-eigene CSS-Gradient-Styling und rendert es nativ im Web
            styled_corr = state.correlation_matrix.style.background_gradient(cmap='coolwarm', vmin=-1.0, vmax=1.0)
            ui.html(styled_corr.to_html()).classes('w-full overflow-x-auto border border-slate-200 rounded-xl p-2 bg-white')

        # TAB 2: P-WERTE
        with ui.tab_panel(tab2).classes('p-0 gap-2'):
            alpha_val = state.selected_alpha if state.selected_alpha is not None else 0.05
            ui.markdown(f"Values below {alpha_val} indicate that the correlation is statistically significant.").classes('text-xs text-slate-500 mb-2')
            # Wendet deine custom highlight_p_values Funktion auf das HTML-Rendering an
            styled_p = state.p_value_matrix.style.format("{:.4e}").apply(
                highlight_p_values, alpha_level=alpha_val, axis=None
            )
            ui.html(styled_p.to_html()).classes('w-full overflow-x-auto border border-slate-200 rounded-xl p-2 bg-white')


def render_correlation_analysis_ui(state: AppState) -> None:
    """Orchestrates and renders the interactive correlation analysis interface."""
    # KORREKTUR: Validierung gegen shape-Attribut abgesichert (verhindert IndexError bei unberechneten Datensätzen)
    if state.centrality_results is None or state.centrality_results.shape[1] < 2: # type: ignore
        ui.markdown("Please select and compute at least **two** centrality measures to perform a correlation analysis.").classes(style.CARD_WARNING + ' text-amber-700 text-sm')
        return

    # KORREKTUR: Abgesicherter Zugriff auf Registry-Listen falls diese leer sein sollten
    available_metrics = CorrelationRegistry.get_available_names()
    if state.selected_correlation_metric is None and available_metrics:
        state.selected_correlation_metric = available_metrics[0]
    if state.selected_alpha is None:
        state.selected_alpha = 0.05

    # Initial-Berechnung beim ersten Rendern triggern
    if state.correlation_matrix is None:
        try:
            corr_ctrl.run_correlation_analysis(state)
        except Exception:
            pass

    # Eingabe-Kontrollen nebeneinander platzieren (Nutzt die standardisierten Spaltenbreiten des Themes)
    with ui.row().classes('w-full gap-4 items-center mb-4'):
        ui.select(
            options=available_metrics,
            label='Select Correlation Metric',
            on_change=handle_correlation_change
        ).bind_value(state, 'selected_correlation_metric').classes(style.INPUT_HALF_WIDTH)

        ui.select(
            options={0.05: 'α = 0.05 (95.0% Confidence)', 
                     0.01: 'α = 0.01 (99.0% Confidence)', 
                     0.001: 'α = 0.001 (99.9% Confidence)', 
                     0.10: 'α = 0.10 (90.0% Confidence)'},
            label='Select Significance Level (Alpha)',
            on_change=handle_correlation_change
        ).bind_value(state, 'selected_alpha').classes(style.INPUT_HALF_WIDTH)

    # Die reaktive Tab-Ergebnis-Sektion einbetten
    correlation_tabs_ui(state)
