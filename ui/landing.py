"""Landing page builder showing centered hero banner, unified upload card, and workflow steps."""

import streamlit as st
from ui.components import upload_card


def render_landing_page() -> tuple:
    """Render the landing view hero block, single upload card, and workflow step cards.

    Returns:
        tuple: (resume_file, jd_file, pasted_jd, analyze_clicked)
    """
    render_hero_banner()
    
    # 1. Unified beautiful upload card container
    with st.container(border=True):
        st.markdown('<div style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px;">Candidate & Job Profile Inputs</div>', unsafe_allow_html=True)
        
        col_resume, col_jd, col_paste = st.columns(3)
        
        with col_resume:
            upload_card("Upload Resume", "landing_resume_uploader", ["pdf", "docx", "txt"])
            resume_file = st.session_state.get("landing_resume_uploader", None)

        with col_jd:
            upload_card("Upload Job Description", "landing_jd_uploader", ["pdf", "txt"])
            jd_file = st.session_state.get("landing_jd_uploader", None)

        with col_paste:
            with st.container(border=True):
                st.markdown(
                    """
                    <div style="margin-bottom: 8px;">
                        <div style="font-size: 13px; font-weight: 700; color: #111827;">Paste Job Description</div>
                        <div style="font-size: 10px; color: #6B7280; margin-top: 2px;">Paste requirements directly</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                pasted_jd = st.text_area(
                    "Paste Job Description text input",
                    placeholder="Enter requirements here...",
                    key="landing_paste_jd",
                    height=95,
                    label_visibility="collapsed"
                )

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # Bottom full width Analyze Candidate button
        analyze_clicked = st.button(
            "Analyzing..." if st.session_state.get("analysis_running") else "Analyze Candidate",
            key="landing_analyze_btn",
            use_container_width=True,
            disabled=st.session_state.get("analysis_running", False)
        )

    # 2. Simple workflow sequence cards row
    render_workflow_steps()

    return resume_file, jd_file, pasted_jd, analyze_clicked


def render_hero_banner() -> None:
    """Render the hero text information block."""
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center; padding: 24px 0;">
                <div style="font-size: 48px; font-weight: 800; color: #111827; letter-spacing: -0.025em; line-height: 1.1;">
                    Understand Every Candidate Beyond Their Resume
                </div>
                <div style="font-size: 15px; color: #6B7280; margin-top: 12px; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.5;">
                    Upload a candidate resume and job description to generate an AI-powered recruiter intelligence report.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_workflow_steps() -> None:
    """Render the workflow flowchart blocks."""
    st.markdown('<div style="font-size: 13px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 32px; text-align: center; margin-bottom: 16px;">Platform Workflow</div>', unsafe_allow_html=True)
    
    col_s1, col_arrow1, col_s2, col_arrow2, col_s3 = st.columns([1, 0.2, 1, 0.2, 1])
    
    with col_s1:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 20px; text-align: center;">
                <div style="background: #EEF2FF; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
                </div>
                <div style="font-size: 15px; font-weight: 700; color: #111827;">1. Upload Documents</div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 6px; line-height: 1.4;">Select resume and JD files</div>
            </div>
            """,
            unsafe_allow_html=True
        )
            
    with col_arrow1:
        st.markdown('<div style="text-align: center; margin-top: 36px; color: #6B7280; font-size: 18px; font-weight: 800;">→</div>', unsafe_allow_html=True)
        
    with col_s2:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 20px; text-align: center;">
                <div style="background: #EEF2FF; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
                </div>
                <div style="font-size: 15px; font-weight: 700; color: #111827;">2. AI Analysis</div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 6px; line-height: 1.4;">Parser matches required skill set</div>
            </div>
            """,
            unsafe_allow_html=True
        )
            
    with col_arrow2:
        st.markdown('<div style="text-align: center; margin-top: 36px; color: #6B7280; font-size: 18px; font-weight: 800;">→</div>', unsafe_allow_html=True)
        
    with col_s3:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 20px; text-align: center;">
                <div style="background: #EEF2FF; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14M22 4L12 14.01l-3-3"/></svg>
                </div>
                <div style="font-size: 15px; font-weight: 700; color: #111827;">3. Recruiter Intelligence</div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 6px; line-height: 1.4;">Review scorecards and match gaps</div>
            </div>
            """,
            unsafe_allow_html=True
        )
