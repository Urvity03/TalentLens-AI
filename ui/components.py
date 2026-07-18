"""Reusable native Streamlit components for the TalentLens AI interface."""

import streamlit as st


def section_header(title: str, description: str = "") -> None:
    """Render a standard header with a divider.

    Args:
        title: The section title.
        description: Supporting detail subtext.
    """
    st.markdown(f"### {title}")
    if description:
        st.markdown(f"<div style='color: #6B7280; font-size: 13px; margin-top: -8px; margin-bottom: 12px;'>{description}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 8px 0 16px 0; border: 0; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)


def metric_card(label: str, value: str, subtext: str = "") -> None:
    """Render a single white rounded container metric card.

    Args:
        label: The metric label descriptor.
        value: Score value.
        subtext: Evaluation level detail.
    """
    with st.container(border=True):
        st.markdown(f"<div style='font-size: 10px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em;'>{label}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 26px; font-weight: 800; color: #4F46E5; margin-top: 4px;'>{value}</div>", unsafe_allow_html=True)
        if subtext:
            st.markdown(f"<div style='font-size: 11px; font-weight: 600; color: #6B7280; margin-top: 2px;'>{subtext}</div>", unsafe_allow_html=True)


def upload_card(label: str, key: str, file_type: list[str]) -> None:
    """Render an onboarding upload box container.

    Args:
        label: Card header label descriptor.
        key: Streamlit uploader state key.
        file_type: Allowed files extension formats.
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 8px;">
            <div style="font-size: 13px; font-weight: 700; color: #111827;">{label}</div>
            <div style="font-size: 10px; color: #6B7280; margin-top: 2px;">Supports: {", ".join(file_type).upper()}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.file_uploader(
        label,
        type=file_type,
        key=key,
        label_visibility="collapsed"
    )


def info_chip(text: str, type_variant: str = "primary") -> str:
    """Generate the HTML code block for a single colored text badge.

    Args:
        text: Badge label.
        type_variant: Color theme selector (primary, success, warning).

    Returns:
        HTML string.
    """
    bg_color = "rgba(79, 70, 229, 0.06)"
    border_color = "rgba(79, 70, 229, 0.1)"
    text_color = "#4F46E5"

    if type_variant == "success":
        bg_color = "rgba(22, 163, 74, 0.06)"
        border_color = "rgba(22, 163, 74, 0.1)"
        text_color = "#16A34A"
    elif type_variant == "warning":
        bg_color = "rgba(217, 119, 6, 0.06)"
        border_color = "rgba(217, 119, 6, 0.1)"
        text_color = "#D97706"

    return f'<span style="background:{bg_color}; border:1px solid {border_color}; border-radius:6px; padding:2px 8px; font-size:10px; font-weight:600; color:{text_color}; margin-right:6px; display:inline-block; margin-bottom:4px;">{text}</span>'


def progress_bar(label: str, percentage: float) -> None:
    """Render a skill matching metrics progress bar with alignment.

    Args:
        label: Skill label.
        percentage: Match score progress value.
    """
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #111827; margin-bottom: 2px;">
            <span>{label}</span>
            <span>{percentage:.0f}%</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.progress(min(max(percentage / 100.0, 0.0), 1.0))


def summary_card(title: str, text: str) -> None:
    """Render a text card content block.

    Args:
        title: Header label descriptor.
        text: Content block details.
    """
    with st.container(border=True):
        st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 8px;'>{title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 12px; line-height: 1.6; color: #111827;'>{text}</div>", unsafe_allow_html=True)
