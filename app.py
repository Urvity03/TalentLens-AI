"""Main application entrypoint for the TalentLens AI Recruiter Intelligence Platform."""

import os
import tempfile
import streamlit as st

from services.analyzer import analyze_candidate
from ui.styles import load_css
from ui.sidebar import render_sidebar
from ui.header import render_header
from ui.landing import render_landing_page
from ui.dashboard import render_dashboard


def init_app() -> None:
    """Initialize page configurations and CSS styles overrides."""
    st.set_page_config(
        page_title="TalentLens AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

    # Initialize state variables
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None


def process_analysis(resume_file, jd_file, pasted_jd) -> None:
    """Validate inputs, write temporary files, and execute the analysis engine.

    Args:
        resume_file: Uploaded resume file object.
        jd_file: Uploaded job description file object.
        pasted_jd: Plaintext job description input.
    """
    if not resume_file:
        st.error("Please upload a candidate resume to begin.")
        return

    if not jd_file and not pasted_jd:
        st.error("Please provide a job description (upload a file or paste requirements).")
        return

    # Reset file cursor before reading to prevent empty bytes read bug
    resume_file.seek(0)

    # Write resume temp file
    suffix = os.path.splitext(resume_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_resume:
        temp_resume.write(resume_file.read())
        resume_path = temp_resume.name

    # Write JD temp file
    temp_jd_path = None
    if jd_file:
        jd_file.seek(0)  # Reset cursor before read
        suffix_jd = os.path.splitext(jd_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix_jd) as temp_jd:
            temp_jd.write(jd_file.read())
            temp_jd_path = temp_jd.name
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_jd:
            temp_jd.write(pasted_jd)
            temp_jd_path = temp_jd.name

    try:
        with st.spinner("Analyzing candidate profile and requirements..."):
            result = analyze_candidate(resume_path, temp_jd_path)
            st.session_state.analysis_result = result
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
    finally:
        # Securely delete temp files
        for path in (resume_path, temp_jd_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


def main() -> None:
    """Render sidebar, header, and coordinate between landing page and dashboard views."""
    init_app()

    # Render sidebar
    with st.sidebar:
        render_sidebar()

    # Render header (title and subtitle only)
    render_header()

    # Load session state variables
    res = st.session_state.analysis_result

    if res is None:
        # Render Landing Page with single upload cards row
        land_resume, land_jd, land_paste, land_analyze = render_landing_page()
        
        if land_analyze:
            process_analysis(land_resume, land_jd, land_paste)
            st.rerun()
    else:
        # Render Dashboard Report View
        render_dashboard(res)


if __name__ == "__main__":
    main()
