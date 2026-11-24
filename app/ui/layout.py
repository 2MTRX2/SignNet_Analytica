# layout.py
from contextlib import contextmanager
from typing import Optional
from nicegui import ui

from app.ui.AppStyle import AppStyle
from app.controller.AppState import get_session_state

# ==================================================================
# NAVIGATION SELECTED NETWORK STATS
# ==================================================================
def _render_sidebar_stats():
    """Reaktive Statistik-Box am unteren Rand der Sidebar für state.selected."""
    state = get_session_state()

    # If no network is selected
    with ui.column().classes(
        f'w-full mt-auto p-4 {AppStyle.MAIN_BG} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_MEDIUM} gap-1'
    ).bind_visibility_from(state, 'selected', backward=lambda b: b is None or b.stats is None):
        ui.label('No Active Network').classes(f'text-xs {AppStyle.TEXT_MUTED}')
        ui.label('Select a network in the library.').classes(f'text-xs {AppStyle.TEXT_MUTED}')

    # If a network is selected
    with ui.column().classes(
        f'w-full mt-auto p-4 {AppStyle.MAIN_BG} {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_MEDIUM} gap-1.5'
    ).bind_visibility_from(state, 'selected', backward=lambda b: b is not None and b.stats is not None):
        
        # Filename
        ui.label().classes(f'text-sm w-full truncate {AppStyle.TEXT_MAIN}').bind_text_from(
            state, 'selected', backward=lambda b: b.stats.filename if (b and b.stats) else ''
        )
        ui.separator().classes('my-1')

        # Key-Value Rows
        def stat_line(label: str, extractor):
            with ui.row().classes('w-full justify-between items-center no-wrap'):
                ui.label(label).classes(f'text-xs {AppStyle.TEXT_MUTED}')
                ui.label().classes(f'text-xs font-medium {AppStyle.TEXT_MAIN}').style(AppStyle.FONT_SANS).bind_text_from(
                    state, 'selected', backward=lambda b: str(extractor(b.stats)) if (b and b.stats) else '-'
                )

        stat_line('Nodes', lambda s: s.num_nodes)
        stat_line('Edges', lambda s: s.num_edges)
        stat_line('Directed', lambda s: 'Yes' if s.is_directed else 'No')
        stat_line('Components', lambda s: s.num_components)
        stat_line('Isolated', lambda s: s.num_isolated_nodes)

        # Ratio Bars
        def ratio_line(title: str, extractor, hex_color: str, text_class: str):
            with ui.column().classes('w-full gap-0.5 mt-1'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label(title).classes(f'text-xs {AppStyle.TEXT_MUTED}')
                    ui.label().classes(f'text-xs {text_class}').style(AppStyle.FONT_SANS).bind_text_from(
                        state, 'selected', backward=lambda b: f'{extractor(b.stats):.1f}%' if (b and b.stats) else '0.0%'
                    )
                ui.linear_progress(show_value=False).props('rounded track-color="grey-3"').classes(
                    'h-1.5 rounded-full'
                ).style(f'--q-primary: {hex_color}').bind_value_from(
                    state, 'selected', backward=lambda b: (extractor(b.stats) / 100.0) if (b and b.stats) else 0.0
                )

        ratio_line('Neg. Edges', lambda s: s.negative_edge_ratio, AppStyle.EDGE_NEGATIVE_HEX, AppStyle.EDGE_NEGATIVE_TEXT)
        ratio_line('Bal. Triads', lambda s: s.balanced_triad_ratio, AppStyle.EDGE_POSITIVE_HEX, AppStyle.EDGE_POSITIVE_TEXT)
        ratio_line('Density', lambda s: s.density, AppStyle.EDGE_POSITIVE_HEX, AppStyle.EDGE_POSITIVE_TEXT)

# ==================================================================
# NAVIGATION
# ==================================================================
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

            # Render the Stats of the Selected Network
            _render_sidebar_stats()

        # Content Area
        # If the background class is the same as the card background, we can add a border and shadow for better visual separation
        is_white = bg_class == AppStyle.MAIN_BG
        card_effects = f'{AppStyle.BORDER_CLEAN} {AppStyle.SHADOW_SMOOTH}' if is_white else ''
        
        with ui.column().classes(f'p-8 {bg_class} {card_effects} {AppStyle.ROUNDED_LARGE} h-full grow overflow-auto {AppStyle.TEXT_MAIN}'):
            yield
