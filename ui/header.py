"""Unified page header builder displaying standard page title and description."""

import streamlit as st


def render_header() -> None:
    """Render the standard header with page details on the left, removing duplicate actions."""
    st.markdown('<div style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -0.025em; line-height: 1.1;">Candidate Intelligence Report</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 13px; color: #6B7280; margin-top: 4px; line-height: 1.4; margin-bottom: 24px;">AI-powered resume analysis and recruiter intelligence.</div>', unsafe_allow_html=True)
