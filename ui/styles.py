"""Premium stylesheet and CSS variable declarations for TalentLens-AI."""

from ui.theme import DARK_THEME, LIGHT_THEME


def load_css(theme_name: str = "dark") -> str:
    """Generate a custom CSS string to style the Streamlit interface.

    Loads the selected theme values, injects CSS variables, sets up the typography
    scale, and defines reusable custom component styles.

    Args:
        theme_name: Name of the theme to load ("light" or "dark").

    Returns:
        A stylesheet string containing all CSS classes and variables.
    """
    t = DARK_THEME if theme_name == "dark" else LIGHT_THEME

    return f"""
    /* --- Google Font & Material Icons --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0');

    /* --- Keyframes --- */
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    /* --- Theme Variables & Tokens --- */
    :root {{
        /* Colors */
        --background: {t["background"]};
        --surface: {t["surface"]};
        --card: {t["card"]};
        --border: {t["border"]};
        --primary: {t["primary"]};
        --accent: {t["accent"]};
        --success: {t["success"]};
        --warning: {t["warning"]};
        --danger: {t["danger"]};
        --text: {t["text"]};
        --muted: {t["muted"]};

        /* Radii */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-full: 9999px;
    }}

    /* --- Base Styling --- */
    html, body {{
        font-family: 'Inter', sans-serif;
    }}

    /* --- Reusable Layout Utilities --- */
    .tl-flex {{
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}

    .tl-flex-between {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 8px !important;
    }}

    .tl-flex-center {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }}

    .tl-grid-2 {{
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 12px !important;
    }}

    .tl-stack {{
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
    }}

    .tl-info-row {{
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        font-size: 14px !important;
    }}

    .tl-divider {{
        border-bottom: 1px solid var(--border) !important;
        margin-top: 16px !important;
        margin-bottom: 16px !important;
        width: 100% !important;
    }}

    /* --- Reusable Custom Classes --- */

    /* AppHeader Class */
    .tl-navbar {{
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 16px 24px !important;
        margin-bottom: 24px !important;
    }}

    .tl-navbar-brand {{
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }}

    .tl-navbar-logo {{
        background-color: var(--primary) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: var(--radius-md) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 14px !important;
        flex-shrink: 0 !important;
    }}

    .tl-navbar-title-stack {{
        display: flex !important;
        flex-direction: column !important;
        gap: 2px !important;
        text-align: left !important;
    }}

    .tl-navbar-title {{
        font-size: 16px !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        line-height: 1.2 !important;
    }}

    .tl-navbar-subtitle {{
        font-size: 12px !important;
        color: var(--muted) !important;
    }}

    .tl-navbar-actions {{
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
        gap: 16px !important;
        height: 100% !important;
        width: 100% !important;
    }}

    .tl-avatar {{
        width: 28px !important;
        height: 28px !important;
        border-radius: var(--radius-full) !important;
        background-color: rgba(99, 102, 241, 0.1) !important;
        color: var(--primary) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        font-weight: 700 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
        font-size: 12px !important;
    }}

    .tl-theme-toggle {{
        display: inline-flex !important;
        align-items: center !important;
    }}

    .tl-navbar-divider {{
        border-bottom: 1px solid var(--border) !important;
        margin-top: 8px !important;
        margin-bottom: 24px !important;
        width: 100% !important;
    }}

    /* SidebarPanel Container */
    .tl-sidebar {{
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
    }}

    /* Card Components */
    .tl-card {{
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 24px !important;
        margin-bottom: 16px !important;
    }}

    .tl-card-header {{
        font-size: 16px !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        border-bottom: 1px solid var(--border) !important;
        padding-bottom: 8px !important;
        margin-bottom: 12px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}

    .tl-card-body {{
        font-size: 14px !important;
        color: var(--text) !important;
        line-height: 1.6 !important;
    }}

    .tl-card-footer {{
        margin-top: 12px !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* Recommendation & Status Banner */
    .tl-banner {{
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 16px 24px !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        margin-bottom: 24px !important;
    }}

    .tl-banner-primary {{
        border-left: 4px solid var(--primary) !important;
        background-color: rgba(99, 102, 241, 0.05) !important;
        color: var(--text) !important;
    }}

    .tl-banner-success {{
        border-left: 4px solid var(--success) !important;
        background-color: rgba(16, 185, 129, 0.05) !important;
        color: var(--text) !important;
    }}

    .tl-banner-warning {{
        border-left: 4px solid var(--warning) !important;
        background-color: rgba(245, 158, 11, 0.05) !important;
        color: var(--text) !important;
    }}

    .tl-banner-danger {{
        border-left: 4px solid var(--danger) !important;
        background-color: rgba(239, 68, 68, 0.05) !important;
        color: var(--text) !important;
    }}

    /* UploadCard Wrapper */
    .tl-upload {{
        background-color: var(--card) !important;
        border: 1px dashed var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 16px !important;
        margin-bottom: 16px !important;
        text-align: center !important;
    }}

    /* Analyze Button Custom Wrapper */
    .tl-button {{
        width: 100% !important;
    }}

    .tl-button button {{
        border-radius: var(--radius-lg) !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        background-color: var(--primary) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--primary) !important;
        height: 48px !important;
        width: 100% !important;
    }}

    .tl-button button:hover {{
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
        color: #FFFFFF !important;
    }}

    /* Section Headers */
    .tl-section {{
        font-size: 24px !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        margin-bottom: 0px !important;
    }}

    .tl-section-header {{
        margin-bottom: 24px !important;
        text-align: left !important;
    }}

    .tl-section-subtitle {{
        font-size: 14px !important;
        color: var(--muted) !important;
        margin-top: 4px !important;
    }}

    /* Metric KPI Cards */
    .tl-metric {{
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 16px 24px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        min-height: 120px !important;
        height: 100% !important;
    }}

    /* Chart Container Wrapper */
    .tl-chart {{
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 24px !important;
        margin-bottom: 16px !important;
    }}

    /* Icons and Spinners */
    .tl-icon {{
        font-size: 20px !important;
        color: var(--muted) !important;
        flex-shrink: 0 !important;
    }}

    .tl-spin {{
        font-size: 20px !important;
        color: var(--primary) !important;
        animation: spin 2s linear infinite !important;
        flex-shrink: 0 !important;
    }}

    /* Reusable Badges styling */
    .tl-badge {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 4px 12px !important;
        border-radius: var(--radius-full) !important;
        margin: 4px !important;
        border: 1px solid transparent !important;
    }}

    .tl-badge-primary {{
        background-color: rgba(99, 102, 241, 0.1) !important;
        color: var(--primary) !important;
        border-color: rgba(99, 102, 241, 0.2) !important;
    }}

    .tl-badge-success {{
        background-color: rgba(16, 185, 129, 0.1) !important;
        color: var(--success) !important;
        border-color: rgba(16, 185, 129, 0.2) !important;
    }}

    .tl-badge-warning {{
        background-color: rgba(245, 158, 11, 0.1) !important;
        color: var(--warning) !important;
        border-color: rgba(245, 158, 11, 0.2) !important;
    }}

    .tl-badge-danger {{
        background-color: rgba(239, 68, 68, 0.1) !important;
        color: var(--danger) !important;
        border-color: rgba(239, 68, 68, 0.2) !important;
    }}

    /* Empty Onboarding State */
    .tl-empty-state {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        padding: 48px 24px !important;
        max-width: 480px !important;
        margin: 0 auto !important;
    }}

    /* --- Reusable Timeline (Flexbox & Normal Flow, No Absolute Positioning) --- */
    .timeline-row {{
        display: flex !important;
        flex-direction: row !important;
        gap: 16px !important;
        margin-bottom: 0px !important;
    }}

    .timeline-left {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        flex-shrink: 0 !important;
    }}

    .timeline-dot {{
        width: 10px !important;
        height: 10px !important;
        border-radius: var(--radius-full) !important;
        background-color: var(--primary) !important;
        border: 2px solid var(--background) !important;
        flex-shrink: 0 !important;
    }}

    .timeline-line {{
        width: 2px !important;
        flex-grow: 1 !important;
        background-color: var(--border) !important;
        min-height: 24px !important;
    }}

    .timeline-content {{
        padding-bottom: 24px !important;
        flex-grow: 1 !important;
    }}

    /* Loading Diagnostics Steps */
    .tl-step-completed {{
        color: var(--success) !important;
    }}

    .tl-step-active {{
        color: var(--primary) !important;
        font-weight: 600 !important;
    }}

    .tl-step-pending {{
        color: var(--muted) !important;
    }}

    /* Loading container override */
    .tl-loading-state {{
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 24px !important;
        max-width: 480px !important;
        margin: 48px auto !important;
    }}
    """
