# style.py
"""
Centralized design system and style guide definitions for SignNet Analytica.

Defines unified Tailwind CSS layout utility strings and semantic color mapping classes 
to enforce visual consistency across all reactive user interface views and components.
"""

# ==================================================================
# SEMANTIC SURFACE AND CARD STYLES
# ==================================================================
# Standandard-Container für Eingabemasken und Datenblöcke
CARD_STANDARD = 'w-full p-5 bg-white border border-slate-200 rounded-xl shadow-sm'
# Leicht abgesetzter Hintergrund für Parameter-Bereiche
CARD_MUTED = 'w-full p-4 bg-slate-50 border border-slate-200 rounded-xl shadow-none'
# Warn- und Hinweiskarten
CARD_WARNING = 'w-full p-6 text-center bg-amber-50 border border-amber-200 rounded-xl shadow-sm'
# Leere Platzhalter-Karten (z.B. vor dem Upload)
CARD_PLACEHOLDER = 'w-full p-8 text-center bg-slate-50 border border-dashed border-slate-300 rounded-xl shadow-none justify-center items-center h-64'

# ==================================================================
# TYPOGRAPHY STYLES
# ==================================================================
PAGE_TITLE = 'text-3xl font-bold text-slate-800 tracking-tight mb-1'
PAGE_SUBTITLE = 'text-sm text-slate-500 mb-6'

SECTION_HEADING = 'text-xl font-bold text-slate-800 mt-4 mb-2'
SUBSECTION_HEADING = 'text-xs font-bold text-slate-400 uppercase tracking-wider mb-2'

# ==================================================================
# ACTION AND COMPONENT STYLES
# ==================================================================
# Primärer Action-Button (z.B. Analyse starten)
BTN_PRIMARY = 'bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg shadow-sm transition-colors'
# Sekundärer Button (z.B. Simulation starten)
BTN_SECONDARY = 'bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold px-4 py-2 rounded-lg transition-colors'
# Erfolgs- oder Berechnungsbutton
BTN_SUCCESS = 'bg-green-600 hover:bg-green-700 text-white font-bold w-full py-2.5 rounded-lg shadow-sm transition-colors'

# Standardbreiten für Selektoren und Eingabefelder
INPUT_MAX_WIDTH = 'w-full cast-w-xl'
INPUT_HALF_WIDTH = 'flex-1 max-w-xs'
