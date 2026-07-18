"""Enterprise recruitment platform vertical navigation sidebar template."""

import streamlit as st


def render_sidebar() -> None:
    """Render the sidebar with brand info, navigation list, and platform details."""
    # 1. Branding Header
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="background: #4F46E5; color: #FFFFFF; width: 32px; height: 32px; border-radius: 6px; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 14px;">TL</div>
                <div style="font-size: 15px; font-weight: 800; color: #111827; letter-spacing: -0.02em;">TalentLens AI</div>
            </div>
            <div style="font-size: 10px; color: #6B7280; margin-top: 6px; line-height: 1.3;">Candidate Intelligence Beyond Keywords</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Add New Analysis Button if a report is active to allow resetting the view
    if st.session_state.get("analysis_result") is not None:
        if st.button("New Analysis", key="sidebar_new_analysis", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.analysis_running = False
            st.session_state.analysis_progress = 0
            st.session_state.analysis_step = ""
            st.session_state.analysis_steps_log = []
            st.session_state.analysis_error = None
            st.session_state.uploaded_resume_name = None
            st.session_state.uploaded_resume_bytes = None
            st.session_state.uploaded_jd_name = None
            st.session_state.uploaded_jd_bytes = None
            st.rerun()

    st.markdown("<hr style='margin: 12px 0; border: 0; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

    # 3. Main Navigation list mapping exact anchors
    nav_items = [
        ("Overview", "#overview"),
        ("Candidate Profile", "#profile"),
        ("Intelligence Scores", "#scores"),
        ("Executive Summary", "#summary"),
        ("Skills Match Matrix", "#skills"),
        ("Top Projects", "#projects"),
        ("Career Timeline", "#timeline"),
        ("Recruiter Insights", "#insights"),
        ("Hiring Recommendation", "#recommendation"),
        ("Career Roadmap", "#roadmap"),
        ("Export Reports", "#export")
    ]

    for label, anchor in nav_items:
        st.markdown(
            f'<a href="{anchor}" style="display:block; text-decoration:none; padding:8px 12px; font-size:12px; font-weight:600; color:#111827; border-radius:6px; margin-bottom:4px; transition:background 0.15s;" onmouseover="this.style.background=\'#F6F8FC\';" onmouseout="this.style.background=\'transparent\';">{label}</a>',
            unsafe_allow_html=True
        )

    st.markdown("<hr style='margin: 16px 0; border: 0; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

    # 4. Footer indicator details
    st.markdown(
        """
        <div style="font-size: 11px; color: #6B7280; padding-left: 12px;">
            Version 1.0
        </div>
        """,
        unsafe_allow_html=True
    )
