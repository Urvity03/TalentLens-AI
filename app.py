"""Main application entrypoint for the TalentLens AI Recruiter Intelligence Platform."""

import os
import tempfile
import traceback
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
    if "analysis_running" not in st.session_state:
        st.session_state.analysis_running = False
    if "analysis_progress" not in st.session_state:
        st.session_state.analysis_progress = 0
    if "analysis_step" not in st.session_state:
        st.session_state.analysis_step = ""
    if "analysis_steps_log" not in st.session_state:
        st.session_state.analysis_steps_log = []
    if "analysis_error" not in st.session_state:
        st.session_state.analysis_error = None

    # Cached file storage values
    if "uploaded_resume_name" not in st.session_state:
        st.session_state.uploaded_resume_name = None
    if "uploaded_resume_bytes" not in st.session_state:
        st.session_state.uploaded_resume_bytes = None
    if "uploaded_jd_name" not in st.session_state:
        st.session_state.uploaded_jd_name = None
    if "uploaded_jd_bytes" not in st.session_state:
        st.session_state.uploaded_jd_bytes = None


def render_skeletons(placeholder) -> None:
    """Display pulsing skeleton loading state cards inside a placeholder container."""
    placeholder.markdown(
        """
        <div style="margin-top: 32px; padding: 24px; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 18px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);">
            <div style="font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 16px;">Candidate Overview</div>
            <div class="skeleton" style="height: 16px; width: 60%; margin-bottom: 8px;"></div>
            <div class="skeleton" style="height: 16px; width: 40%; margin-bottom: 8px;"></div>
            <div class="skeleton" style="height: 16px; width: 80%; margin-bottom: 24px;"></div>
            
            <div style="font-size: 15px; font-weight: 700; color: #111827; margin-top: 24px; margin-bottom: 16px;">Intelligence Metrics</div>
            <div style="display: flex; gap: 16px;">
                <div class="skeleton" style="flex: 1; height: 80px; border-radius: 8px;"></div>
                <div class="skeleton" style="flex: 1; height: 80px; border-radius: 8px;"></div>
                <div class="skeleton" style="flex: 1; height: 80px; border-radius: 8px;"></div>
            </div>
            
            <div style="font-size: 15px; font-weight: 700; color: #111827; margin-top: 24px; margin-bottom: 16px;">Skills Matrix</div>
            <div class="skeleton" style="height: 12px; width: 100%; margin-bottom: 8px;"></div>
            <div class="skeleton" style="height: 12px; width: 90%; margin-bottom: 8px;"></div>
            <div class="skeleton" style="height: 12px; width: 95%;"></div>
        </div>
        
        <style>
            .skeleton {
                background: linear-gradient(90deg, #E2E8F0 25%, #F1F5F9 50%, #E2E8F0 75%);
                background-size: 200% 100%;
                animation: loading 1.5s infinite;
                border-radius: 4px;
            }
            @keyframes loading {
                0% { background-position: 200% 0; }
                100% { background-position: -200% 0; }
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def run_pipeline_analysis() -> None:
    """Execute the backend candidate evaluation pipeline with live state feedback reporting."""
    # Write temp resume file
    resume_suffix = os.path.splitext(st.session_state.uploaded_resume_name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=resume_suffix) as temp_resume:
        temp_resume.write(st.session_state.uploaded_resume_bytes)
        resume_path = temp_resume.name

    # Write temp JD file
    jd_suffix = os.path.splitext(st.session_state.uploaded_jd_name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=jd_suffix) as temp_jd:
        temp_jd.write(st.session_state.uploaded_jd_bytes)
        jd_path = temp_jd.name

    # Setup rendering placeholders
    progress_bar = st.progress(0)
    status_text = st.empty()
    steps_log = st.empty()
    skeleton_placeholder = st.empty()
    
    # Render initial skeletons inside placeholder
    render_skeletons(skeleton_placeholder)

    def progress_callback(step_name: str, percentage: int):
        st.session_state.analysis_progress = percentage
        st.session_state.analysis_step = step_name
        if step_name not in st.session_state.analysis_steps_log:
            st.session_state.analysis_steps_log.append(step_name)

        # Update progress bar value
        progress_bar.progress(percentage / 100.0)

        # Update status text
        status_text.markdown(f"**Current Step:** {step_name} ({percentage}%)")

        # Update log summary
        log_html = "<div style='font-size: 13px; color: #6B7280; line-height: 1.6; margin-top: 12px;'>"
        for step in st.session_state.analysis_steps_log:
            if step == "Complete":
                log_html += f"<div style='color: #16A34A; font-weight: bold;'>✓ {step}</div>"
            elif step == step_name:
                log_html += f"<div style='color: #4F46E5; font-weight: bold;'>➜ {step}</div>"
            else:
                log_html += f"<div style='color: #16A34A;'>✓ {step}</div>"
        log_html += "</div>"
        steps_log.markdown(log_html, unsafe_allow_html=True)

    try:
        # Run real backend analysis
        result = analyze_candidate(resume_path, jd_path, progress_callback=progress_callback)
        st.session_state.analysis_result = result
        st.session_state.analysis_running = False
        st.session_state.analysis_error = None
        
        # Explicitly empty all placeholders before rendering dashboard
        progress_bar.empty()
        status_text.empty()
        steps_log.empty()
        skeleton_placeholder.empty()
        
        st.rerun()
    except Exception as e:
        # Log error traceback in details
        print("Analysis Exception Traceback:")
        traceback.print_exc()
        
        # Empty all placeholders on error too
        progress_bar.empty()
        status_text.empty()
        steps_log.empty()
        skeleton_placeholder.empty()
        
        st.session_state.analysis_error = str(e)
        st.session_state.analysis_running = False
        st.rerun()
    finally:
        # Clean up temp files
        for path in (resume_path, jd_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


def render_error_card() -> None:
    """Render a professional recruitment platform error feedback screen."""
    st.markdown(
        """
        <div style="background: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 12px; padding: 24px; margin-top: 24px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="background: #EF4444; color: #FFFFFF; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">!</div>
                <div style="font-size: 16px; font-weight: 700; color: #991B1B;">Analysis Failed</div>
            </div>
            <div style="font-size: 14px; color: #7F1D1D; line-height: 1.5; margin-bottom: 16px;">
                Unable to process the uploaded files. Please verify the resume and job description requirements and try again.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Retry Evaluation", key="retry_analysis_btn"):
        st.session_state.analysis_error = None
        st.session_state.analysis_result = None
        st.session_state.analysis_running = False
        st.rerun()


def main() -> None:
    """Render sidebar, header, and coordinate between landing page and dashboard views."""
    init_app()

    # Render sidebar
    with st.sidebar:
        render_sidebar()

    # Render header (title and subtitle only)
    render_header()

    # Check for error state first
    if st.session_state.analysis_error is not None:
        render_error_card()
        return

    # Load session state variables
    res = st.session_state.analysis_result

    if st.session_state.analysis_running:
        # Render Loading Screen
        st.markdown(
            """
            <div style="margin-bottom: 24px;">
                <div style="font-size: 24px; font-weight: 800; color: #111827;">TalentLens AI</div>
                <div style="font-size: 15px; color: #6B7280; margin-top: 4px;">Analyzing Candidate Profile...</div>
                <div style="font-size: 13px; color: #9CA3AF; margin-top: 2px; margin-bottom: 16px;">Please wait while TalentLens AI evaluates the candidate.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        run_pipeline_analysis()

    elif res is None:
        # Render Landing Page with single upload cards row
        land_resume, land_jd, land_paste, land_analyze = render_landing_page()
        
        if land_analyze:
            if not land_resume:
                st.error("Please upload a candidate resume to begin.")
            elif not land_jd and not land_paste:
                st.error("Please provide a job description (upload a file or paste requirements).")
            else:
                # Persist files data to state across execution cycles
                st.session_state.uploaded_resume_name = land_resume.name
                land_resume.seek(0)
                st.session_state.uploaded_resume_bytes = land_resume.read()
                
                if land_jd:
                    st.session_state.uploaded_jd_name = land_jd.name
                    land_jd.seek(0)
                    st.session_state.uploaded_jd_bytes = land_jd.read()
                else:
                    st.session_state.uploaded_jd_name = "jd.txt"
                    st.session_state.uploaded_jd_bytes = land_paste.encode("utf-8")
                
                st.session_state.analysis_running = True
                st.session_state.analysis_steps_log = []
                st.rerun()
    else:
        # Render Dashboard Report View
        render_dashboard(res)


if __name__ == "__main__":
    main()
