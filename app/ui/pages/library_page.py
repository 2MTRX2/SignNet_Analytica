# library_page.py
import io
from nicegui import events, ui

from app.ui.layout import shared_layout
from app.ui.AppStyle import AppStyle
from app.controller.AppState import AppState
from app.controller.AppState import get_session_state
from app.controller.LoadingController import LoadingController
from app. controller.GraphBuilderController import GraphBuilderController
from signnet.io.LoadingRegistry import REPRESENTATION_REGISTRY, STRATEGY_REGISTRY

upload_ctrl = LoadingController()
graph_ctrl = GraphBuilderController()

def init_library_page():
    @ui.page('/library')
    async def library_page():
        # Wait for the server connection
        await ui.context.client.connected()
        # Once the connection is established, get the current state
        state = get_session_state()
        # Create a dictionary to ensure non-locality
        pending_file: dict = {'bytes': None, 'name': None}

        with shared_layout():
            mapping_fields_container = ui.column().classes('w-full')


            def render_ratio_bar(title: str, ratio_percent: float, fill_class: str, text_class: str):
                # Wert sicher zwischen 0 und 100 halten
                pct = max(0.0, min(100.0, ratio_percent))
                    
                with ui.column().classes('w-full gap-1 mt-2'):
                    # Kopfzeile mit Titel links und Prozentwert rechts
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label(title).classes(f'text-base {AppStyle.TEXT_MAIN}')
                        ui.label(f'{pct:.1f}%').classes(f'text-base {text_class}')
        
                    # Bar-Hintergrund + farbiger Balken
                    with ui.element('div').classes('w-full h-2.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden'):
                        ui.element('div').classes(f'h-full {fill_class} rounded-full transition-all duration-300').style(f'width: {pct}%')

            def render_mapping_fields():
                # Delete all the existing ui elements in the container
                mapping_fields_container.clear()
                with mapping_fields_container:
                    cols = state.available_columns
                    with ui.row().classes('w-full gap-3'):
                        if cols:
                            # if the columns could be read, use selection boxes
                            ui.select(options=cols, label='Source').bind_value(state, 'source_column_name').classes('flex-1')
                            ui.select(options=cols, label='Target').bind_value(state, 'target_column_name').classes('flex-1')
                            ui.select(options=cols, label='Sign').bind_value(state, 'sign_column_name').classes('flex-1')
                        else:
                            # if the columns couldn't be read, use text boxes
                            ui.input(label='Source').bind_value(state, 'source_column_name').classes('flex-1')
                            ui.input(label='Target').bind_value(state, 'target_column_name').classes('flex-1')
                            ui.input(label='Sign').bind_value(state, 'sign_column_name').classes('flex-1')

            def render_selection_dialog():
                selection_content.clear()
                graph_ctrl.generate_visualization(bundle=state.loaded, app_state=state)

                with selection_content:
                    # HTML Visualisation of Network
                    with ui.column().classes(f'flex-1 h-full {AppStyle.ROUNDED_LARGE} overflow-hidden'):
                        if state.loaded and state.loaded.visualization_html:
                            iframe = ui.element('iframe').classes('w-full h-full border-0')
                            iframe._props['srcdoc'] = state.loaded.visualization_html
                        else:
                            ui.label('No visualization available.').classes('p-4 text-gray-500')

                    # Network Properties
                    with ui.column().classes(f'w-1/4 h-full p-6 {AppStyle.MAIN_BG} {AppStyle.ROUNDED_LARGE} gap-1 overflow-y-auto'):
                        if state.loaded and state.loaded.stats:
                            stats = state.loaded.stats
                            ui.label(f'Number of Nodes: {stats.num_nodes}').classes(f'text-base {AppStyle.TEXT_MAIN}')
                            ui.label(f'Number of Edges: {stats.num_edges}').classes(f'text-base {AppStyle.TEXT_MAIN}')
                            ui.label(f"Directed: {'Yes' if state.is_directed else 'No'}").classes(f'text-base {AppStyle.TEXT_MAIN}')
                            ui.label(f'Number of Components: {stats.num_components}').classes(f'text-base {AppStyle.TEXT_MAIN}')
                            ui.label(f'Number of Isolated Nodes: {stats.num_isolated_nodes}').classes(f'text-base {AppStyle.TEXT_MAIN}')
                            # neg_edge_pct = net.negative_edge_ratio * 100  
                            render_ratio_bar(
                                title='Negative Edges Ratio',
                                ratio_percent=stats.negative_edge_ratio,
                                fill_class=AppStyle.EDGE_NEGATIVE,
                                text_class=AppStyle.EDGE_NEGATIVE_TEXT
                            )
                            # balanced_triad_pct = net.balanced_triad_ratio * 100
                            render_ratio_bar(
                                title='Balanced Triad Ratio',
                                ratio_percent=stats.balanced_triad_ratio,
                                fill_class=AppStyle.EDGE_POSITIVE,
                                text_class=AppStyle.EDGE_POSITIVE_TEXT
                            )

                            render_ratio_bar(
                                title='Density',
                                ratio_percent=stats.density,
                                fill_class=AppStyle.EDGE_POSITIVE,
                                text_class=AppStyle.EDGE_POSITIVE_TEXT
                            )


            # --- 2. UPLOAD HANDLER ---
            async def handle_upload(event: events.UploadEventArguments):
                raw_bytes = await event.file.read()
                pending_file['bytes'] = raw_bytes
                pending_file['name'] = event.file.name 
                file_buffer = io.BytesIO(raw_bytes)

                # Select file type automatically in dropdown
                ext = event.file.name.split('.')[-1].lower()
                if ext in ['csv', 'xlsx', 'json']:
                    state.selected_file_type = 'excel' if ext == 'xlsx' else ext

                # Spaltenköpfe IMMER vorab auslesen
                try:
                    temp_rep = REPRESENTATION_REGISTRY['Edge List']()
                    fmt = state.selected_file_type.lower()
                    temp_loader = STRATEGY_REGISTRY[fmt](temp_rep)

                    df_raw = temp_loader.read_raw(file_buffer)
                    available_cols = list(df_raw.columns)
                    state.available_columns = available_cols

                    if len(available_cols) >= 3:
                        state.source_column_name = available_cols[0]
                        state.target_column_name = available_cols[1]
                        state.sign_column_name = available_cols[2]

                    render_mapping_fields()

                    # Nur rendern & melden, wenn Edge List gewählt ist
                    if state.selected_repr_type == 'Edge List':
                        ui.notify(f'File "{event.file.name}" received! Please verify columns.', type='info')
                    else:
                        ui.notify(f'File "{event.file.name}" successfully received!', type='positive')

                except Exception as e:
                    ui.notify(f'Could not read columns: {e}', type='negative')


            # --- 3. FINALER IMPORT BEIM KLICK AUF "CHOOSE NETWORK" ---
            def process_and_close():
                if state.is_directed: 
                    ui.notify('The current implementation does not support directed networks.', type='warning')
                    return
                if pending_file['bytes'] is None:
                    ui.notify('Please upload a file first!', type='warning')
                    return

                try:
                    file_buffer = io.BytesIO(pending_file['bytes'])
                    upload_ctrl.process_upload(file_buffer, state, pending_file["name"])
                    ui.notify('Network successfully loaded!', type='positive')
                    upload_dialog.close()
                    render_selection_dialog()  # <-- Erst Inhalt + Graph erzeugen
                    selection_dialog.open()    # <-- Dann Fenster öffnen
                except Exception as e:
                    ui.notify(f'Error loading network: {e}', type='negative')

            def handle_select_network():
                if not state.loaded:
                    return
                
                upload_ctrl.commit_loaded_network(state)
                selection_dialog.close()
                
                if state.selected and state.selected.stats:
                    ui.notify(f'Selected "{state.selected.stats.filename}" as active network.', type='positive')


            # --- 4. POP-UP FENSTER (DIALOG) ---
            with ui.dialog() as upload_dialog, ui.card().classes(f'w-full max-w-2xl p-6 {AppStyle.ROUNDED_LARGE}'):
                # Kopfzeile
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Upload Networks').classes(f'text-xl {AppStyle.TEXT_MAIN} {AppStyle.FONT_SANS}')
                    ui.button(icon='close', on_click=upload_dialog.close).props(f'flat round dense {AppStyle.HOVER_NAV}')

                # Drag & Drop Upload-Feld
                ui.upload(
                    label='Drag and drop or choose your network',
                    on_upload=handle_upload,
                    auto_upload=True,
                    max_files=1
                ).props('flat bordered accept=.csv,.xlsx,.json').classes(f'w-full {AppStyle.BORDER_CLEAN} {AppStyle.ROUNDED_LARGE}')

                # Konfigurations-Bereich
                with ui.column().classes('w-full gap-4 mt-4'):
                    # Select Bar für File Types
                    ui.select(
                        options=['csv', 'excel', 'json'],
                        label='File Type'
                    ).bind_value(state, 'selected_file_type').classes('w-full')

                    # Radio für Edge List vs. Adjacency Matrix
                    with ui.column().classes('gap-1'):
                        ui.label('Representation').classes(f'text-xs {AppStyle.TEXT_MUTED} {AppStyle.FONT_SANS}')
                        ui.radio(
                            options=['Edge List', 'Adjacency Matrix']
                        ).bind_value(state, 'selected_repr_type').props('inline')

                    # Checkbox für Directed
                    ui.checkbox('Directed Network').bind_value(state, 'is_directed')

                    # Column Mapping (wird automatisch nur bei "Edge List" eingeblendet)
                    with ui.column().classes('w-full gap-2').bind_visibility_from(
                        state, 'selected_repr_type', value='Edge List'
                    ):
                        ui.separator()
                        ui.label('Column Mapping').classes(f'text-xs {AppStyle.ACCENT_TEXT} {AppStyle.FONT_SANS}')
                        
                        # Initiales Befüllen der Mapping-Felder
                        mapping_fields_container = ui.column().classes('w-full')
                        render_mapping_fields()

                # Fusszeile mit Buttons
                with ui.row().classes('w-full justify-end gap-2 mt-6'):
                    ui.button('Cancel', on_click=upload_dialog.close).props('flat').props('flat no-caps').classes(f'{AppStyle.ROUNDED_MEDIUM}')
                    ui.button('Process Network', on_click=process_and_close).props('no-caps').classes(f'{AppStyle.ACCENT_TEXT} {AppStyle.ROUNDED_MEDIUM} text-white')


            # --- 5. ZWEITES POP-UP FENSTER (SELECTION) ---
            with ui.dialog() as selection_dialog, ui.card().classes(
                f'w-[90vw] max-w-none h-[85vh] p-6 flex flex-col justify-between {AppStyle.ROUNDED_LARGE} {AppStyle.MAIN_BG}'
            ):
                # Header
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label().classes(f'text-xl {AppStyle.TEXT_MAIN}').bind_text_from(state, 'loaded', 
                                                                                       backward=lambda bundle: bundle.stats.filename
                                                                                        if (bundle and bundle.stats) else 'Network Preview')
                    ui.button(icon='close', on_click=selection_dialog.close).props(f'flat round dense {AppStyle.HOVER_NAV}')

                # Empty Container
                selection_content = ui.row().classes('w-full flex-1 gap-6 overflow-hidden')

                # Footer
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancel', on_click=selection_dialog.close).props('flat no-caps').classes(f'{AppStyle.ROUNDED_MEDIUM}')
                    ui.button('Select Network', on_click=handle_select_network).props('no-caps').classes(f'{AppStyle.ACCENT_TEXT} {AppStyle.ROUNDED_MEDIUM} text-white')



            # --- 6. UPLOAD-KARTE AUF DER LIBRARY-SEITE ---
            with ui.card().props('flat').classes(
                f'p-6 cursor-pointer {AppStyle.HOVER_CARD} '
                f'border-2 border-dashed border-gray-300 {AppStyle.ROUNDED_LARGE} items-center justify-center'
            ).on('click', upload_dialog.open):
                with ui.column().classes('items-center justify-center gap-2 py-4'):
                    ui.icon('add', size='xl').classes(AppStyle.ACCENT_TEXT)
                    ui.label('Upload Networks').classes(f'text-lg {AppStyle.TEXT_MAIN} {AppStyle.FONT_SANS}')
                    ui.label('Import a new network dataset').classes(f'text-sm {AppStyle.TEXT_MUTED} {AppStyle.FONT_SANS}')