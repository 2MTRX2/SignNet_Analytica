# app.py
from nicegui import ui
from app.ui.layout import shared_layout

from app.ui.pages.dashboard_page import init_dashboard_page
from app.ui.pages.library_page import init_library_page  
from app.ui.pages.structure_page import init_structure_page
from app.ui.pages.dynamics_page import init_dynamics_page
from app.ui.pages.lab_page import init_lab_page

# Pages
init_dashboard_page()
init_library_page()
init_structure_page()
init_dynamics_page()
init_lab_page()

# STarting Server
ui.run(title="SignNet Analytica", dark=False)

