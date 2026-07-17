"""Main dashboard application orchestration for TalentLens-AI."""

import os
import tempfile
import time
import pandas as pd
import streamlit as st

from services.analyzer import analyze_candidate
from ui.cards import (
    candidate_summary_card,
    empty_state,
    export_panel,
    insights_summary_card,
    loading_state,
    metric_card,
    recommendation_banner,
    roadmap_timeline,
    section_header,
    skills_card,
)
from ui.charts import render_bar_chart, render_gauge, render_pie_chart
from ui.export_pdf import generate_pdf_report
from ui.navbar import render_navbar
from ui.styles import load_css

# --- Page Configurations ---
st.set_page_config(
    page_title="TalentLens AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initializations ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "cta_clicked" not in st.session_state:
    st.session_state.cta_clicked = False

# --- Header/Navbar Render ---
theme = render_navbar()

# --- CSS Design System Injection ---
st.markdown(f"<style>{load_css(theme)}</style>", unsafe_allow_html=True)

# --- Sidebar Controls Render ---
with st.sidebar:
    from ui.sidebar import render_sidebar
    uploaded_resume, jd_text, uploaded_jd, analyze_clicked = render_sidebar()

# --- Trigger Analysis Pipeline Action ---
if analyze_clicked:
    if not uploaded_resume:
        st.error("Please upload a candidate resume to begin.")
    elif not jd_text and not uploaded_jd:
        st.error("Please provide a job description (paste text or upload file).")
    else:
        # Create temporary files to pass to the backend orchestration analyzer
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as t_resume:
            t_resume.write(uploaded_resume.read())
            resume_path = t_resume.name

        jd_path = None
        if jd_text:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as t_jd:
                t_jd.write(jd_text)
                jd_path = t_jd.name
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as t_jd:
                t_jd.write(uploaded_jd.read())
                jd_path = t_jd.name

        try:
            # Render visual loading progress diagnostics logs checklist
            loading_placeholder = st.empty()
            steps = [
                "Parsing Resume",
                "Parsing Job Description",
                "Extracting Skills",
                "Calculating Similarity",
                "Computing AHRI",
                "Generating Recruiter Insights",
                "Building Dashboard",
            ]

            for idx in range(len(steps)):
                with loading_placeholder:
                    loading_state(steps, idx)
                time.sleep(0.35)

            # Invoke backend pipeline orchestration
            result = analyze_candidate(resume_path, jd_path)
            st.session_state.analysis_result = result
            st.session_state.cta_clicked = False  # Reset onboarding click state

            # Completed step rendering
            with loading_placeholder:
                loading_state(steps, len(steps))
            time.sleep(0.2)
            loading_placeholder.empty()

        finally:
            # Securely clean up temporary files
            for path in [resume_path, jd_path]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass
        st.rerun()

# --- Render Platform Cockpit View ---
res = st.session_state.analysis_result

if res is None:
    # Handle smooth focus guidance warning on Empty State CTA click
    if st.session_state.cta_clicked:
        st.info("← Sidebar Active! Please drag and drop your candidate resume in the panel on the left to get started.")

    # Onboarding Empty State Display
    empty_state(
        title="TalentLens AI Workspace",
        description=(
            "Upload candidate resumes and matching job descriptions in the sidebar. "
            "TalentLens AI will parse qualifications, calculate readiness index scores, "
            "outline roadmap development curves, and compile executive recruiter guides."
        ),
        cta="Get Started Now",
        illustration="assignment_ind",
    )
else:
    # 1. Top KPI Row (AHRI, Quality, Match, Potential)
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    with col_kpi1:
        ahri_badge_type = "success" if res.ahri.score >= 70 else "warning"
        metric_card(
            title="AHRI Score",
            value=f"{res.ahri.score:.1f}",
            subtitle="Suitability readiness index",
            badge=f"Grade {res.ahri.grade}",
            badge_type=ahri_badge_type,
            icon="developer_board",
        )

    with col_kpi2:
        quality_badge_type = "success" if res.quality >= 80 else "warning"
        metric_card(
            title="Resume Quality",
            value=f"{res.quality:.1f}%",
            subtitle="Completeness evaluation",
            badge="Complete" if res.quality >= 80 else "Gaps Detected",
            badge_type=quality_badge_type,
            icon="description",
        )

    with col_kpi3:
        skills_badge_type = "success" if res.skill_intelligence.match_percentage >= 70 else "warning"
        metric_card(
            title="Skill Match",
            value=f"{res.skill_intelligence.match_percentage:.1f}%",
            subtitle="Matched target requirements",
            badge="High Match" if res.skill_intelligence.match_percentage >= 70 else "Needs Upskill",
            badge_type=skills_badge_type,
            icon="extension",
        )

    with col_kpi4:
        potential_badge_type = (
            "success"
            if "High" in res.potential.level
            or "Outstanding" in res.potential.level
            or "Excellent" in res.potential.level
            else "warning"
        )
        metric_card(
            title="Potential Level",
            value=f"{res.potential.score:.1f}",
            subtitle="Growth forecast scale",
            badge=res.potential.level,
            badge_type=potential_badge_type,
            icon="trending_up",
        )

    # Vertical space spacing spacer
    st.markdown('<div style="height: var(--space-6);"></div>', unsafe_allow_html=True)

    # 2. Main Dashboard Navigation Tabs
    tab_overview, tab_skills, tab_insights, tab_analytics, tab_roadmap, tab_export = st.tabs([
        "Overview",
        "Skills Intelligence",
        "Recruiter Insights",
        "Analytics",
        "Career Roadmap",
        "Export Report",
    ])

    with tab_overview:
        section_header(
            title="Candidate Profile Summary",
            subtitle="Contact info, similarity metrics, education details, and professional experience",
            action="Profile",
        )
        candidate_summary_card(
            name=res.resume.contact.name,
            email=res.resume.contact.email,
            phone=res.resume.contact.phone,
            linkedin=res.resume.contact.linkedin,
            github=res.resume.contact.github,
            similarity=res.similarity.overall,
            quality=res.quality,
            summary=res.resume.summary,
            education=res.resume.education,
            experience=res.resume.experience,
            projects=res.resume.projects,
            certifications=res.resume.certifications,
        )

    with tab_skills:
        section_header(
            title="Skills Match Matrix",
            subtitle="Detailed extraction categorizing Technical, Tools, Soft Skills, and Languages",
            action="Skills",
        )

        col_skills, col_pie = st.columns([1.2, 1.0])
        with col_skills:
            skills_card(
                matched_skills=res.skill_intelligence.matched,
                missing_skills=res.skill_intelligence.missing,
            )

        with col_pie:
            st.markdown('<div class="tl-chart">', unsafe_allow_html=True)
            fig_donut = render_pie_chart(
                labels=["Matched", "Missing"],
                values=[
                    len(res.skill_intelligence.matched),
                    len(res.skill_intelligence.missing),
                ],
                title="Gaps Distribution Share Ratio",
                theme=theme,
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_insights:
        section_header(
            title="Recruiter Insights",
            subtitle="Strengths highlights, areas of concern, hiring decisions, risk factors, and culture fits",
            action="Insights",
        )

        verdict_status = "success" if res.ahri.score >= 70 else "warning"
        recommendation_banner(
            status=verdict_status,
            message=f"Hiring Verdict Verdict: {res.recruiter.recommendation}",
        )

        col_ins_l, col_ins_r = st.columns(2)
        with col_ins_l:
            insights_summary_card(
                title="Strengths Highlighted",
                items=res.recruiter.strengths,
                status_type="success",
                icon="check_circle",
            )
            insights_summary_card(
                title="Culture Fit Alignment",
                items=res.ahri.strengths[:3],
                status_type="primary",
                icon="psychology",
            )

        with col_ins_r:
            insights_summary_card(
                title="Identified Risk Factors",
                items=res.recruiter.concerns,
                status_type="danger",
                icon="error",
            )
            insights_summary_card(
                title="Interview Focus Areas",
                items=[f"Assess core knowledge of {s}" for s in res.ahri.missing_skills[:3]],
                status_type="warning",
                icon="help",
            )

    with tab_analytics:
        section_header(
            title="Analytics Deep-Dive",
            subtitle="Large index gauges, score comparisons, and visual readiness comparators",
            action="Analytics",
        )

        col_gauge, col_bar = st.columns(2)
        with col_gauge:
            st.markdown('<div class="tl-chart">', unsafe_allow_html=True)
            fig_gauge = render_gauge(
                value=res.ahri.score,
                title="Readiness Index (AHRI)",
                theme=theme,
                grade=res.ahri.grade,
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_bar:
            st.markdown('<div class="tl-chart">', unsafe_allow_html=True)
            fig_bar = render_bar_chart(
                labels=["Growth Potential", "Profile Quality", "AHRI Score"],
                values=[res.potential.score, res.quality, res.ahri.score],
                title="Assessment Comparisons",
                theme=theme,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="tl-card">', unsafe_allow_html=True)
        st.markdown('<div class="tl-card-header"><span class="material-symbols-outlined tl-icon">grid_on</span> Comparison Evaluation Matrix</div>', unsafe_allow_html=True)
        df_scores = pd.DataFrame(
            {
                "Suitability Metric": [
                    "Hiring Readiness (AHRI)",
                    "Resume Profile Quality",
                    "Skill Match Percentage",
                    "Predicted Career Growth Potential",
                ],
                "Diagnostics Score": [
                    f"{res.ahri.score:.1f} / 100.0",
                    f"{res.quality:.1f}%",
                    f"{res.skill_intelligence.match_percentage:.1f}%",
                    f"{res.potential.score:.1f} / 100.0",
                ],
                "Hiring Classification": [
                    f"Grade {res.ahri.grade}",
                    "Qualified" if res.quality >= 80 else "Standard Integrity",
                    "High Match" if res.skill_intelligence.match_percentage >= 70 else "Gaps Identified",
                    res.potential.level,
                ],
            }
        )
        st.dataframe(df_scores, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_roadmap:
        section_header(
            title="Upskilling Growth Pathway",
            subtitle="bridge qualification gaps chronologically connecting Week 1, Month 1, Month 3, and Month 6 timeline cohorts",
            action="Pathway",
        )

        col_time, col_courses = st.columns(2)
        with col_time:
            roadmap_timeline(res.roadmap.steps)

        with col_courses:
            insights_summary_card(
                title="Recommended Courses & Projects",
                items=[f"Complete {s} fundamentals upskilling project" for s in res.skill_intelligence.missing[:3]],
                status_type="primary",
                icon="school",
            )

    with tab_export:
        section_header(
            title="Export Candidate Assessment",
            subtitle="Print-friendly PDF report compiler, preview summaries, and download triggers",
            action="Export",
        )

        col_dl, col_preview = st.columns(2)
        with col_dl:
            export_panel(pdf_bytes_ready=True)

            pdf_bytes = generate_pdf_report(res)
            st.download_button(
                label="Download Report PDF",
                data=pdf_bytes,
                file_name=f"Assessment_Report_{res.resume.contact.name or 'Candidate'}.pdf",
                mime="application/pdf",
                key="pdf_download_button",
            )

        with col_preview:
            st.markdown(
                """
                <div class="tl-card">
                    <div class="tl-card-header"><span class="material-symbols-outlined tl-icon">visibility</span> Export Report Preview Summary</div>
                    <div class="tl-card-body" style="font-size: 14px; line-height: 1.6;">
                        <strong>Document Title:</strong> TalentLens AI - Candidate Evaluation Report<br>
                        <strong>Total Pages:</strong> 2 Pages<br>
                        <strong>Format Type:</strong> Standard PDF Document (MIME: application/pdf)<br><br>
                        <em>Contains Candidate profile biography, contacts, education background, professional experience history, suitability indices (AHRI, Quality, Match Rate, Potential), recruiter strengths and concerns lists, and the personal upskilling roadmap.</em>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
