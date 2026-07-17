"""Sidebar navigation panel component for TalentLens-AI."""

import streamlit as st


def render_sidebar() -> tuple[any, str, any, bool]:
    """Render the SidebarPanel component housing analysis files upload controls.

    Displays inputs for candidate resumes, textareas for pasting job descriptions,
    secondary file uploaders for job descriptions, and the analysis action button.

    Returns:
        A tuple containing:
            - uploaded_resume: Streamlit uploaded file object or None.
            - jd_text: Pasted job description text string.
            - uploaded_jd: Streamlit uploaded job description file object or None.
            - analyze_clicked: Boolean indicating if the action button was clicked.
    """
    # Wrap sidebar items in our custom sidebar class
    st.markdown('<div class="tl-sidebar">', unsafe_allow_html=True)

    # 1. Sidebar Header Title and Description
    st.markdown(
        """
        <div class="tl-navbar-title-stack">
            <span class="tl-navbar-title">Candidate Analysis</span>
            <span class="tl-navbar-subtitle">Configure files for diagnostics evaluation</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 2. Candidate Resume Section
    st.markdown(
        '<div style="font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Candidate Resume</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tl-upload">', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF, DOCX)",
        type=["pdf", "docx"],
        key="resume_uploader",
        help="Upload candidate resume in PDF or DOCX format",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 3. Job Description Section (Primary Text Area, Secondary File Uploader)
    st.markdown(
        '<div style="font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Target Job Description</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="tl-textarea-container">', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste Job Description (Primary)",
        placeholder="Paste target job requirements and duties here...",
        key="jd_textarea",
        height=180,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align: center; font-size: 11px; color: var(--muted); font-weight: 600; margin: 8px 0; text-transform: uppercase;">— OR —</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tl-upload">', unsafe_allow_html=True)
    uploaded_jd = st.file_uploader(
        "Upload JD File (Secondary)",
        type=["pdf", "txt"],
        key="jd_uploader",
        help="Alternatively upload job description as PDF or TXT",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 4. Action Button
    st.markdown('<div class="tl-button">', unsafe_allow_html=True)
    analyze_clicked = st.button("Analyze Candidate", key="analyze_button")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 5. Recent Analyses Section (Placeholder Card)
    st.markdown(
        '<div style="font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Recent Analysis History</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="tl-card" style="padding: 12px !important; margin-bottom: 0px !important;">
            <div style="font-size: 12px; color: var(--muted); text-align: center;">No recent analyses yet.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    return uploaded_resume, jd_text, uploaded_jd, analyze_clicked
