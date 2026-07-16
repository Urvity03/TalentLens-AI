"""Sidebar component for TalentLens-AI."""

import streamlit as st


def render_sidebar() -> tuple[st.runtime.uploaded_file_manager.UploadedFile | None, st.runtime.uploaded_file_manager.UploadedFile | None, bool]:
    """Render the sidebar for document uploading and initiating analysis.

    Returns:
        A tuple containing (resume_file, job_description_file, analyze_clicked).
    """
    with st.sidebar:
        st.markdown(
            '<h2 style="margin-top: 0; font-size: 1.5rem; font-weight: 600;">📥 Input Center</h2>',
            unsafe_allow_html=True,
        )

        # Upload Resume
        resume_file = st.file_uploader(
            "Upload Resume (PDF / DOCX)",
            type=["pdf", "docx"],
            key="resume_uploader",
        )

        # Upload Job Description
        job_description_file = st.file_uploader(
            "Upload Job Description (TXT / PDF)",
            type=["txt", "pdf"],
            key="jd_uploader",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Analyze Resume Button
        analyze_clicked = st.button(
            "⚡ Analyze Candidate",
            use_container_width=True,
            key="analyze_button",
        )

    return resume_file, job_description_file, analyze_clicked
