"""Candidate Intelligence dashboard report renderer containing scorecards, timelines, and roadmaps."""

import streamlit as st
import json
from datetime import datetime
from ui.components import section_header, metric_card, info_chip, progress_bar


def render_dashboard(res) -> None:
    """Render the full candidate analysis report sections.

    Args:
        res: Consolidated AnalysisResult dataclass object.
    """
    # Page-top Overview anchor
    st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
    
    # 1. Candidate Profile
    render_candidate_overview(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 2. Intelligence Scores
    render_intelligence_scores(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 3. Executive Summary
    render_executive_summary(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 4. Skills Match Matrix
    render_skills_matrix(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 5. Top Projects
    render_projects(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 6. Career Timeline
    render_career_timeline(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 7. Recruiter Insights
    render_recruiter_insights(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 8. Hiring Recommendation
    render_hiring_recommendation(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 9. Career Roadmap
    render_career_roadmap(res)
    st.markdown('<div style="height: 48px;"></div>', unsafe_allow_html=True)
    
    # 10. Export Reports
    render_export_section(res)


def render_candidate_overview(res) -> None:
    """Render Candidate Profile section containing basic metadata details."""
    st.markdown('<div id="profile"></div>', unsafe_allow_html=True)
    section_header("1. Candidate Profile", "Basic contact info, role specialization, and web references.")
    
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
    section_header("2. Intelligence Scores", "Calculated index metrics derived from semantic similarity and resume content structure.")
    
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
    """Render Executive Summary details container."""
    st.markdown('<div id="summary"></div>', unsafe_allow_html=True)
    section_header("3. Executive Summary", "A high-level synthesis of candidate core strengths and matching context.")
    summary_text = res.resume.summary or "Summary not provided by parser."
    with st.container(border=True):
        st.markdown(f"<div style='font-size: 15px; line-height: 1.6; color: #111827;'>{summary_text}</div>", unsafe_allow_html=True)


def render_skills_matrix(res) -> None:
    """Render Skills Match Matrix details container."""
    st.markdown('<div id="skills"></div>', unsafe_allow_html=True)
    section_header("4. Skills Match Matrix", "Matched skills and critical requirements gaps analysis.")
    
    with st.container(border=True):
        # Display match percentage
        st.markdown(f"**Overall Skill Match:** {res.skill_intelligence.match_percentage:.0f}%")
        
        # Show progress bars for matched skills
        if res.skill_intelligence.matched:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 12px; margin-bottom: 8px;'>Matched Skills</div>", unsafe_allow_html=True)
            for skill in res.skill_intelligence.matched[:4]:
                progress_bar(skill, 100.0)
                
        # Show missing skills as warning chips
        if res.skill_intelligence.missing:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 16px; margin-bottom: 8px;'>Missing Gaps</div>", unsafe_allow_html=True)
            chips_html = "".join([info_chip(s, "warning") for s in res.skill_intelligence.missing[:6]])
            st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)


def render_projects(res) -> None:
    """Render Top Projects section mapping descriptions and frameworks."""
    st.markdown('<div id="projects"></div>', unsafe_allow_html=True)
    section_header("5. Top Projects", "Candidate execution highlights extracted from academic or professional project experiences.")
    
    with st.container(border=True):
        if not res.resume.projects:
            st.markdown("<div style='color: #6B7280; font-size: 14px;'>No project details parsed.</div>", unsafe_allow_html=True)
            return

        for p in res.resume.projects[:3]:
            p_title = getattr(p, "title", "Project") or "Project Name"
            p_desc = getattr(p, "description", "") or ""
            p_tech = getattr(p, "technologies", [])
            
            st.markdown(f"<div style='font-size: 15px; font-weight: 700; color: #111827; margin-top: 12px;'>• {p_title}</div>", unsafe_allow_html=True)
            if p_desc:
                st.markdown(f"<div style='font-size: 14px; color: #6B7280; padding-left: 8px; line-height: 1.4; margin-top: 4px;'>{p_desc}</div>", unsafe_allow_html=True)
            if p_tech:
                chips = "".join([info_chip(t) for t in p_tech[:4]])
                st.markdown(f"<div style='padding-left: 8px; margin-top: 6px;'>{chips}</div>", unsafe_allow_html=True)


def render_career_timeline(res) -> None:
    """Render Career Timeline milestones list."""
    st.markdown('<div id="timeline"></div>', unsafe_allow_html=True)
    section_header("6. Career Timeline", "Chronological sequence of candidate job experiences and internships.")
    
    with st.container(border=True):
        if not res.resume.experience:
            st.markdown("<div style='color: #6B7280; font-size: 14px;'>No experience milestones parsed.</div>", unsafe_allow_html=True)
            return

        st.markdown("<div style='position: relative; padding-left: 16px; border-left: 2px solid #E5E7EB; margin-left: 8px; display: flex; flex-direction: column; gap: 16px;'>", unsafe_allow_html=True)
        for e in res.resume.experience[:3]:
            title = getattr(e, "title", "Role") or "Role Detail"
            company = getattr(e, "company", "Company") or "Company"
            duration = getattr(e, "duration", "") or "Timeline"
            st.markdown(
                f"""
                <div style="position: relative;">
                    <div style="position: absolute; left: -22px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #4F46E5;"></div>
                    <div style="font-size: 15px; font-weight: 700; color: #111827; line-height: 1.3;">{title}</div>
                    <div style="font-size: 13px; color: #6B7280; margin-top: 2px;">{company} · {duration}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_recruiter_insights(res) -> None:
    """Render Recruiter Insights section showing strengths and concerns."""
    st.markdown('<div id="insights"></div>', unsafe_allow_html=True)
    section_header("7. Recruiter Insights", "Recruiter feedback points highlighting strengths and potential concerns.")
    
    with st.container(border=True):
        col_s, col_c = st.columns(2)
        with col_s:
            st.markdown("<div style='font-size: 13px; font-weight: 700; color: #16A34A; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Key Strengths</div>", unsafe_allow_html=True)
            for s in res.recruiter.strengths[:4]:
                st.markdown(f"<div style='font-size: 14px; color: #111827; margin-bottom: 4px;'>✓ {s}</div>", unsafe_allow_html=True)
        with col_c:
            st.markdown("<div style='font-size: 13px; font-weight: 700; color: #D97706; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Areas of Concern</div>", unsafe_allow_html=True)
            if res.recruiter.concerns:
                for c in res.recruiter.concerns[:4]:
                    st.markdown(f"<div style='font-size: 14px; color: #111827; margin-bottom: 4px;'>! {c}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size: 14px; color: #6B7280;'>No concerns identified</div>", unsafe_allow_html=True)


def render_hiring_recommendation(res) -> None:
    """Render Hiring Recommendation details card."""
    st.markdown('<div id="recommendation"></div>', unsafe_allow_html=True)
    section_header("8. Hiring Recommendation", "Decision logic support grade and confidence level recommendations.")
    
    with st.container(border=True):
        st.markdown(f"**Status:** {res.recruiter.recommendation}")
        st.markdown(f"**Confidence Level:** {res.ahri.grade}")
        
        if res.ahri.strengths:
            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 12px; margin-bottom: 6px;'>Evidence Indicators</div>", unsafe_allow_html=True)
            chips = "".join([info_chip(s, "success") for s in res.ahri.strengths[:4]])
            st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)


def render_career_roadmap(res) -> None:
    """Render personalized career roadmap pathways."""
    st.markdown('<div id="roadmap"></div>', unsafe_allow_html=True)
    section_header("9. Career Roadmap", "AI-recommended professional pathway roadmap matching candidate skill gaps.")
    
    with st.container(border=True):
        for idx, step in enumerate(res.roadmap.steps[:5]):
            st.markdown(f"<div style='font-size: 14px; color: #111827; margin-bottom: 8px;'><b>Step {idx+1}:</b> {step}</div>", unsafe_allow_html=True)


def render_export_section(res) -> None:
    """Render document export download buttons."""
    st.markdown('<div id="export"></div>', unsafe_allow_html=True)
    section_header("10. Export Reports", "Export the complete recruiter intelligence evaluation report into markdown, text or pdf summary.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Export to PDF",
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
            "Export Recruiter Markdown",
            data=markdown_content,
            file_name="candidate_report.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    with c3:
        st.download_button(
            "Export Recruiter Summary",
            data=f"PDF SUMMARY DATA - AHRI Score: {res.ahri.score:.0f}",
            file_name="candidate_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
