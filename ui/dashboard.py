"""Candidate Intelligence dashboard report renderer containing scorecards, timelines, and roadmaps."""

import streamlit as st
import json
from datetime import datetime
from ui.components import section_header, metric_card, info_chip, progress_bar, summary_card


def render_dashboard(res) -> None:
    """Render the full candidate analysis report sections.

    Args:
        res: Consolidated AnalysisResult dataclass object.
    """
    render_candidate_overview(res)
    render_intelligence_scores(res)
    
    # Grid split for Summary and Skills
    col_summary, col_skills = st.columns([1.2, 0.8])
    with col_summary:
        render_executive_summary(res)
    with col_skills:
        render_skills_matrix(res)

    # Grid split for Projects and Timeline
    col_proj, col_time = st.columns(2)
    with col_proj:
        render_projects(res)
    with col_time:
        render_career_timeline(res)

    # Grid split for Recruiter Insights and Hiring Recommendations
    col_recruiter, col_recommendation = st.columns(2)
    with col_recruiter:
        render_recruiter_insights(res)
    with col_recommendation:
        render_hiring_recommendation(res)

    render_career_roadmap(res)
    render_export_section(res)


def render_candidate_overview(res) -> None:
    """Render Candidate Overview section containing basic metadata details."""
    st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
    section_header("1. Candidate Overview")
    
    name = res.resume.contact.name or "Candidate Profile"
    role = res.resume.professional_identity.current_title or res.resume.professional_identity.technical_specialization or "Engineer"
    exp = f"{len(res.resume.experience)} Roles" if res.resume.experience else "Professional"
    loc = res.resume.contact.location or "Not Specified"
    
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"**Name:** {name}")
            st.markdown(f"**Role:** {role}")
        with c2:
            st.markdown(f"**Experience:** {exp}")
            st.markdown(f"**Location:** {loc}")
        with c3:
            if res.resume.contact.email:
                st.markdown(f"**Email:** {res.resume.contact.email}")
            if res.resume.contact.phone:
                st.markdown(f"**Phone:** {res.resume.contact.phone}")
        with c4:
            links = []
            if res.resume.contact.linkedin:
                links.append(f"[LinkedIn]({res.resume.contact.linkedin})")
            if res.resume.contact.github:
                links.append(f"[GitHub]({res.resume.contact.github})")
            if res.resume.contact.portfolio:
                links.append(f"[Portfolio]({res.resume.contact.portfolio})")
            
            st.markdown("**Links:**")
            if links:
                st.markdown(" / ".join(links))
            else:
                st.markdown("None provided")


def render_intelligence_scores(res) -> None:
    """Render Intelligence Scores section mapping computed scores cards."""
    st.markdown('<div id="scores"></div>', unsafe_allow_html=True)
    section_header("2. Intelligence Scores")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("AHRI Score", f"{res.ahri.score:.0f}", f"Grade: {res.ahri.grade}")
    with m2:
        metric_card("Resume Quality", f"{res.quality:.0f}", "Structure Score")
    with m3:
        match_val = res.similarity.overall * 100 if res.similarity.overall <= 1.0 else res.similarity.overall
        metric_card("Skill Match", f"{match_val:.0f}%", "Requirements Match")
    with m4:
        metric_card("Potential Level", res.potential.level, f"Score: {res.potential.score:.0f}")


def render_executive_summary(res) -> None:
    """Render Candidate Summary details container."""
    summary_text = res.resume.summary or "Summary not provided by parser."
    summary_card("3. Executive Summary", summary_text)


def render_skills_matrix(res) -> None:
    """Render Skills Matrix progress bar items."""
    st.markdown('<div id="skills"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 12px;'>4. Skills Match Matrix</div>", unsafe_allow_html=True)
        
        # Display match percentage
        st.markdown(f"**Overall Skill Match:** {res.skill_intelligence.match_percentage:.0f}%")
        
        # Show progress bars for matched skills
        if res.skill_intelligence.matched:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #6B7280; margin-top: 8px; margin-bottom: 4px;'>Matched Skills</div>", unsafe_allow_html=True)
            for skill in res.skill_intelligence.matched[:4]:
                progress_bar(skill, 100.0)
                
        # Show missing skills as warning chips
        if res.skill_intelligence.missing:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #6B7280; margin-top: 12px; margin-bottom: 4px;'>Missing Gaps</div>", unsafe_allow_html=True)
            chips_html = "".join([info_chip(s, "warning") for s in res.skill_intelligence.missing[:6]])
            st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)


def render_projects(res) -> None:
    """Render Top Projects section mapping descriptions and frameworks."""
    st.markdown('<div id="projects"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 8px;'>5. Top Projects</div>", unsafe_allow_html=True)
        if not res.resume.projects:
            st.markdown("<div style='color: #6B7280; font-size: 12px;'>No project details parsed.</div>", unsafe_allow_html=True)
            return

        for p in res.resume.projects[:3]:
            p_title = getattr(p, "title", "Project") or "Project Name"
            p_desc = getattr(p, "description", "") or ""
            p_tech = getattr(p, "technologies", [])
            
            st.markdown(f"<div style='font-size: 11px; font-weight: 700; color: #111827; margin-top: 8px;'>• {p_title}</div>", unsafe_allow_html=True)
            if p_desc:
                st.markdown(f"<div style='font-size: 10px; color: #6B7280; padding-left: 8px; line-height: 1.3;'>{p_desc}</div>", unsafe_allow_html=True)
            if p_tech:
                chips = "".join([info_chip(t) for t in p_tech[:4]])
                st.markdown(f"<div style='padding-left: 8px; margin-top: 4px;'>{chips}</div>", unsafe_allow_html=True)


def render_career_timeline(res) -> None:
    """Render vertical Experience career milestones list."""
    st.markdown('<div id="timeline"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 8px;'>6. Career Timeline</div>", unsafe_allow_html=True)
        if not res.resume.experience:
            st.markdown("<div style='color: #6B7280; font-size: 12px;'>No experience milestones parsed.</div>", unsafe_allow_html=True)
            return

        st.markdown("<div style='position: relative; padding-left: 12px; border-left: 1.5px solid #E5E7EB; margin-left: 4px; display: flex; flex-direction: column; gap: 12px;'>", unsafe_allow_html=True)
        for e in res.resume.experience[:3]:
            title = getattr(e, "title", "Role") or "Role Detail"
            company = getattr(e, "company", "Company") or "Company"
            duration = getattr(e, "duration", "") or "Timeline"
            st.markdown(
                f"""
                <div style="position: relative;">
                    <div style="position: absolute; left: -17px; top: 3px; width: 7px; height: 7px; border-radius: 50%; background: #4F46E5;"></div>
                    <div style="font-size: 11px; font-weight: 700; color: #111827; line-height: 1.2;">{title}</div>
                    <div style="font-size: 9px; color: #6B7280; margin-top: 1px;">{company} · {duration}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_recruiter_insights(res) -> None:
    """Render Recruiter Insights section showing strengths and concerns."""
    st.markdown('<div id="insights"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 8px;'>7. Recruiter Insights</div>", unsafe_allow_html=True)
        
        col_s, col_c = st.columns(2)
        with col_s:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #16A34A; margin-bottom: 4px;'>Key Strengths</div>", unsafe_allow_html=True)
            for s in res.recruiter.strengths[:4]:
                st.markdown(f"<div style='font-size: 10px; color: #111827;'>✓ {s}</div>", unsafe_allow_html=True)
        with col_c:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #D97706; margin-bottom: 4px;'>Areas of Concern</div>", unsafe_allow_html=True)
            if res.recruiter.concerns:
                for c in res.recruiter.concerns[:4]:
                    st.markdown(f"<div style='font-size: 10px; color: #111827;'>! {c}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size: 10px; color: #6B7280;'>No concerns identified</div>", unsafe_allow_html=True)


def render_hiring_recommendation(res) -> None:
    """Render Hiring Recommendation details card."""
    st.markdown('<div id="recommendation"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 8px;'>8. Hiring Recommendation</div>", unsafe_allow_html=True)
        
        st.markdown(f"**Status:** {res.recruiter.recommendation}")
        st.markdown(f"**Confidence Level:** {res.ahri.grade}")
        
        if res.ahri.strengths:
            st.markdown("<div style='font-size: 10px; font-weight: 700; color: #6B7280; margin-top: 6px;'>Evidence Indicators</div>", unsafe_allow_html=True)
            chips = "".join([info_chip(s, "success") for s in res.ahri.strengths[:4]])
            st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)


def render_career_roadmap(res) -> None:
    """Render personalized career roadmap pathways."""
    st.markdown('<div id="roadmap"></div>', unsafe_allow_html=True)
    section_header("9. Career Roadmap")
    
    with st.container(border=True):
        st.markdown("<div style='font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 8px;'>Upskilling Pathway Recommendations</div>", unsafe_allow_html=True)
        for idx, step in enumerate(res.roadmap.steps[:5]):
            st.markdown(f"<div style='font-size: 11px; color: #111827; margin-bottom: 6px;'><b>Step {idx+1}:</b> {step}</div>", unsafe_allow_html=True)


def render_export_section(res) -> None:
    """Render document export download buttons."""
    st.markdown('<div id="export"></div>', unsafe_allow_html=True)
    section_header("10. Export Reports")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.download_button(
            "Export Report as JSON",
            data=json.dumps(
                {
                    "candidate_name": res.resume.contact.name,
                    "scores": {
                        "ahri": res.ahri.score,
                        "quality": res.quality,
                        "overall_match": res.similarity.overall
                    }
                },
                indent=2
            ),
            file_name="candidate_report.json",
            mime="application/json",
            use_container_width=True
        )
        
    with c2:
        markdown_content = f"# Candidate Evaluation: {res.resume.contact.name or 'Candidate'}\n\nAHRI: {res.ahri.score:.0f}\nGrade: {res.ahri.grade}\n\nSummary: {res.resume.summary}"
        st.download_button(
            "Export Report as Markdown",
            data=markdown_content,
            file_name="candidate_report.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    with c3:
        st.download_button(
            "Export Report as PDF SUMMARY",
            data=f"PDF SUMMARY DATA - AHRI Score: {res.ahri.score:.0f}",
            file_name="candidate_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
