"""SaaS Dashboard Metric Cards component for TalentLens-AI."""

import streamlit as st


def metric_dashboard_card(
    title: str,
    value: str,
    subtitle: str,
    badge: str = "",
) -> None:
    """Render a premium SaaS dashboard metric card.

    Displays a title, large centered value, subtitle, and an optional badge
    in the top-right corner inside a card container.

    Args:
        title: The title description.
        value: The main metric value (centered).
        subtitle: The footer note or indicator.
        badge: Optional badge string shown in the top-right corner.
    """
    badge_html = ""
    if badge:
        badge_html = f"""
        <div style="position: absolute; top: 1rem; right: 1.2rem; font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 9999px; background: rgba(128, 128, 128, 0.12); opacity: 0.9;">
            {badge}
        </div>
        """

    html = f"""
    <div class="premium-card" style="position: relative; display: flex; flex-direction: column; justify-content: space-between;">
        {badge_html}
        <div style="font-size: 0.8rem; opacity: 0.7; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; text-align: left;">
            {title}
        </div>
        <div style="font-size: 3rem; font-weight: 800; text-align: center; margin: 1rem 0; line-height: 1;">
            {value}
        </div>
        <div style="font-size: 0.85rem; opacity: 0.65; text-align: center; font-weight: 500;">
            {subtitle}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
