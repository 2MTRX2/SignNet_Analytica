# style.py
class AppStyle:
    # --- BACKGROUNDS ---
    MAIN_BG = 'bg-slate-50'
    SIDEBAR_BG = 'bg-slate-100/80 backdrop-blur-md'
    CARD_BG = 'bg-white'
    
    # --- INTERACTIONS ---
    ACCENT = 'bg-blue-600'
    ACCENT_TEXT = 'text-blue-600'
    ACCENT_HOVER = 'hover:bg-blue-700'
    NAV_ACTIVE_BG = 'bg-blue-50/80'
    
    # --- EDGE TYPES (SIGNED NETWORKS) ---
    EDGE_POSITIVE = 'bg-emerald-500'
    EDGE_POSITIVE_TEXT = 'text-emerald-500'
    EDGE_NEGATIVE = 'bg-rose-500'
    EDGE_NEGATIVE_TEXT = 'text-rose-500'
    
    # --- TEXT COLORS ---
    TEXT_MAIN = 'text-slate-900'
    TEXT_MUTED = 'text-slate-500'
    TEXT_NAV = 'text-slate-700'
    
    # --- BORDERS & SHADOWS (APPLE CLEAN) ---
    BORDER_CLEAN = 'border border-slate-200/60'
    SHADOW_SMOOTH = 'shadow-sm shadow-slate-100'
    ROUNDED_LARGE = 'rounded-2xl'  
    ROUNDED_MEDIUM = 'rounded-xl'  
    
    # --- TYPOGRAPHY (FONT STACKS) ---
    FONT_SANS = (
        "font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', "
        "'SF Pro Text', 'Helvetica Neue', 'Segoe UI', 'Inter', sans-serif;"
    )
    
    FONT_MONO = (
        "font-family: 'SF Mono', SFMono-Regular, ui-monospace, "
        "'DejaVu Sans Mono', Menlo, Consolas, monospace;"
    )

    SHADOW_SMOOTH = (
        "shadow-["
        "0_1px_2px_rgba(0,0,0,0.03),"
        "0_12px_24px_-4px_rgba(0,0,0,0.04)"
        "]"
    )
    # For modals, popovers, and other overlay components
    SHADOW_MODAL = (
        "shadow-["
        "0_1px_3px_rgba(0,0,0,0.05),"
        "0_20px_40px_-12px_rgba(0,0,0,0.08)"
        "]"
    )

    HOVER_NAV = 'hover:bg-slate-200/60 transition-all duration-150 ease-in-out'
    # Hover accent for e.g. buttons 
    HOVER_ACCENT = 'hover:bg-blue-700 transition-all duration-150 ease-in-out'

    HOVER_TABLE_ROW = 'hover:bg-slate-50 transition-colors duration-100'
    HOVER_CARD_CSS = (
        "transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); "
        "transform-gpu: true; "
        "cursor: pointer;"
    )
    
    # Der Style, der beim Hovern injiziert wird
    HOVER_CARD_EFFECT = (
        "this.style.transform='scale(1.01)'; "
        "this.style.borderColor='#cbd5e1'; "  # entspricht border-slate-300
        "this.style.boxShadow='0 4px 12px rgba(0,0,0,0.02), 0 16px 32px -4px rgba(0,0,0,0.04)';"
    )
    
    # Der Style, der beim Verlassen des Hovers zurückgesetzt wird
    HOVER_CARD_RESET = (
        "this.style.transform='scale(1)'; "
        "this.style.borderColor='#e2e8f0'; "  # entspricht border-slate-200/60
        "this.style.boxShadow='none';"
    )

