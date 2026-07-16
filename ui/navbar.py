"""Navbar component for TalentLens-AI."""

import streamlit as st


def render_navbar() -> str:
    """Render the main header/navbar of the platform.

    Displays logo/title, description, and theme selection toggle.

    Returns:
        The selected theme string ("light" or "dark").
    """
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            '<h1 style="margin: 0; font-size: 2.25rem; font-weight: 700;">🔍 TalentLens-AI</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="margin: 0.25rem 0 1.5rem 0; font-style: italic; opacity: 0.8;">'
            "AI-powered Resume Intelligence Platform</p>",
            unsafe_allow_html=True,
        )

    with col2:
        is_dark = st.toggle("Dark Mode 🌙", value=True)
        theme = "dark" if is_dark else "light"

    return theme
