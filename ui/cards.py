"""Reusable UI cards for TalentLens-AI."""

import streamlit as st


def metric_card(title: str, value: str, subtitle: str = "") -> None:
    """Render a styled metric card using the premium-card class.

    Args:
        title: Title of the metric.
        value: Major value to show.
        subtitle: Optional footer note/subtitle.
    """
    sub_html = f'<div style="font-size: 0.8rem; opacity: 0.6;">{subtitle}</div>' if subtitle else ""
    html = f"""
    <div class="premium-card">
        <div style="font-size: 0.85rem; opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">{title}</div>
        <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem;">{value}</div>
        {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def info_card(title: str, content: str) -> None:
    """Render a styled info card using the premium-card class.

    Args:
        title: Title/header of the card.
        content: Paragraph content to display.
    """
    html = f"""
    <div class="premium-card">
        <h4 style="margin: 0 0 0.5rem 0; font-weight: 600; border-bottom: 1px solid rgba(128, 128, 128, 0.2); padding-bottom: 0.25rem;">{title}</h4>
        <p style="margin: 0; font-size: 0.95rem; opacity: 0.9; line-height: 1.5;">{content}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
