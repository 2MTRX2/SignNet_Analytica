# main.py
from app.app import *  # Importiert alle Routen und Layouts aus der main.py
from nicegui import ui

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="SignNet Analytica",
        favicon="🌐",
        storage_secret="signnet_secure_token_2026",
        port=8080
    )