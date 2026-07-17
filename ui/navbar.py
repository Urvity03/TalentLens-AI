"""Navbar component for TalentLens-AI."""

import streamlit as st


def _render_icon(icon: str) -> str:
    """Generate a standard Material Symbols Outlined HTML icon element.

    Args:
        icon: The name of the icon symbol.

    Returns:
        The HTML span element string.
    """
    if not icon:
        return ""
    return f'<span class="material-symbols-outlined tl-icon">{icon}</span>'


def render_navbar() -> str:
    """Render the AppHeader component of the TalentLens-AI platform.

    Displays the monogram logo, platform titles, theme toggle controls, and
    user account settings action elements inline using native Streamlit columns.

    Returns:
        The active theme mode ("light" or "dark").
    """
    # Outer structural container block
    st.markdown('<div class="tl-navbar">', unsafe_allow_html=True)

    col_brand, col_toggle, col_actions = st.columns([5, 1.5, 1.5])

    with col_brand:
        st.markdown(
            """
            <div class="tl-navbar-brand">
                <div class="tl-navbar-logo">TL</div>
                <div class="tl-navbar-title-stack">
                    <span class="tl-navbar-title">TalentLens AI</span>
                    <span class="tl-navbar-subtitle">AI Recruiting Intelligence Platform</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_toggle:
        is_dark = st.toggle("Dark Mode", value=True, key="theme_toggle")
        theme = "dark" if is_dark else "light"

    with col_actions:
        settings_icon = _render_icon("settings")
        st.markdown(
            f"""
            <div class="tl-navbar-actions">
                {settings_icon}
                <div class="tl-avatar">UT</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom border separator line (participates naturally in vertical layout)
    st.markdown('<div class="tl-navbar-divider"></div>', unsafe_allow_html=True)

    return theme
