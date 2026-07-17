"""Reusable card components for TalentLens-AI."""

import streamlit as st


def _card(html_content: str, card_class: str = "tl-card") -> None:
    """Internal helper to render generic HTML content inside a custom styled container.

    Args:
        html_content: The HTML content to wrap inside the container.
        card_class: The CSS class selector name for styling.
    """
    st.markdown(f'<div class="{card_class}">{html_content}</div>', unsafe_allow_html=True)


def _render_icon(icon: str, extra_class: str = "tl-icon") -> str:
    """Internal helper to generate a standard Material Symbols Outlined HTML icon element.

    Args:
        icon: The name of the icon symbol.
        extra_class: Optional additional CSS class configuration name.

    Returns:
        The HTML span element string.
    """
    if not icon:
        return ""
    return f'<span class="material-symbols-outlined {extra_class}">{icon}</span>'


def _categorize_skills(skills: list[str]) -> dict[str, list[str]]:
    """Internal helper to classify a list of skills into common recruiting folders.

    Args:
        skills: List of extracted skill name strings.

    Returns:
        A dictionary mapping category name folders to skill lists.
    """
    categories = {
        "Technical": [],
        "Tools": [],
        "Soft Skills": [],
        "Languages": [],
    }

    langs_set = {
        "python",
        "javascript",
        "java",
        "c++",
        "c#",
        "ruby",
        "go",
        "rust",
        "sql",
        "html",
        "css",
        "typescript",
        "swift",
        "kotlin",
        "english",
        "spanish",
        "french",
        "german",
        "mandarin",
    }
    tools_set = {
        "docker",
        "aws",
        "kubernetes",
        "k8s",
        "git",
        "github",
        "gitlab",
        "terraform",
        "ansible",
        "jenkins",
        "jira",
        "confluence",
        "figma",
        "slack",
        "vscode",
        "linux",
    }
    soft_set = {
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "agile",
        "scrum",
        "collaboration",
        "management",
        "mentoring",
        "critical thinking",
    }

    for skill in skills:
        s_lower = skill.lower().strip()
        if s_lower in langs_set:
            categories["Languages"].append(skill)
        elif s_lower in tools_set:
            categories["Tools"].append(skill)
        elif s_lower in soft_set:
            categories["Soft Skills"].append(skill)
        else:
            categories["Technical"].append(skill)

    return categories


def section_header(
    title: str,
    subtitle: str | None = None,
    action: str | None = None,
) -> None:
    """Render a reusable page section header with optional subtitle and action badge labels.

    Args:
        title: Main heading string.
        subtitle: Secondary descriptive text.
        action: Interactive badge label string.
    """
    badge_html = f'<span class="tl-badge tl-badge-primary">{action}</span>' if action else ""
    sub_html = f'<div class="tl-section-subtitle">{subtitle}</div>' if subtitle else ""

    html = f"""
    <div class="tl-section-header">
        <div class="tl-flex">
            <span class="tl-section">{title}</span>
            {badge_html}
        </div>
        {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def stat_row(label: str, value: str) -> None:
    """Render a formatted candidate stat key-value data row.

    Args:
        label: Description label.
        value: Info value string.
    """
    html = f"""
    <div class="tl-info-row">
        <span style="color: var(--muted);">{label}:</span>
        <strong style="color: var(--text);">{value}</strong>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def metric_card(
    title: str,
    value: str,
    subtitle: str,
    badge: str = "",
    badge_type: str = "primary",
    icon: str = "",
) -> None:
    """Render a MetricCard component for displaying key score variables.

    Args:
        title: The label text of the metric.
        value: The main display number or value.
        subtitle: Helper subtitle context description.
        badge: Optional status text to overlay in a badge.
        badge_type: Color style configuration of the badge ('primary', 'success', 'warning', 'danger').
        icon: Material Symbol Outlined icon name string.
    """
    icon_html = _render_icon(icon)
    badge_html = f'<span class="tl-badge tl-badge-{badge_type}">{badge}</span>' if badge else ""

    content = f"""
    <div class="tl-flex-between">
        <span style="font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em;">{title}</span>
        {icon_html}
    </div>
    <div style="font-size: 32px; font-weight: 700; color: var(--text); margin: 8px 0;">{value}</div>
    <div class="tl-flex-between">
        <span style="font-size: 12px; color: var(--muted);">{subtitle}</span>
        {badge_html}
    </div>
    """
    _card(content, card_class="tl-metric")


def recommendation_banner(status: str, message: str) -> None:
    """Render a highlighted recommendation card bar outlining the decision output.

    Args:
        status: The severity level ('success', 'warning', 'danger', 'primary').
        message: Recommender verdict text.
    """
    icon_name = "gavel"
    if status == "success":
        icon_name = "check_circle"
    elif status == "warning":
        icon_name = "warning"
    elif status == "danger":
        icon_name = "error"

    icon_html = _render_icon(icon_name)
    banner_class = f"tl-banner tl-banner-{status}"

    content = f"""
    {icon_html}
    <div style="font-size: 16px; font-weight: 600;">{message}</div>
    """
    _card(content, card_class=banner_class)


def candidate_summary_card(
    name: str,
    email: str,
    phone: str,
    linkedin: str,
    github: str,
    similarity: float,
    quality: float,
    summary: str,
    education: list[any],
    experience: list[any],
    projects: list[any],
    certifications: list[any],
) -> None:
    """Render candidate profile credentials, contact info, employment, projects, and certifications.

    Args:
        name: Name of the candidate.
        email: Email contact info.
        phone: Phone number contact info.
        linkedin: LinkedIn profile URL.
        github: GitHub profile URL.
        similarity: Overall similarity match index.
        quality: Resume completeness score.
        summary: Executive summary biography paragraph.
        education: List of parsed education history objects.
        experience: List of parsed employment history objects.
        projects: List of parsed projects.
        certifications: List of parsed certifications.
    """
    st.markdown('<div class="tl-card">', unsafe_allow_html=True)

    header_icon = _render_icon("person")
    st.markdown(
        f'<div class="tl-card-header">{header_icon} Candidate Profile Summary</div>',
        unsafe_allow_html=True,
    )

    # 1. Contact Details Grid
    col_l, col_r = st.columns(2)
    with col_l:
        stat_row("Name", name or "Not Specified")
        stat_row("Email", email or "Not Specified")
        stat_row("Phone", phone or "Not Specified")
    with col_r:
        stat_row("LinkedIn", linkedin or "Not Specified")
        stat_row("GitHub", github or "Not Specified")
        stat_row("Semantic Fit", f"{similarity:.1f}%")

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 2. Summary
    st.markdown(
        '<div style="font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Executive Summary</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="tl-card-body" style="margin-bottom: 16px;">{summary or "No summary segment detected."}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 3. Experience & Education split columns
    col_exp, col_edu = st.columns(2)
    with col_exp:
        st.markdown(
            '<div style="font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Experience History</div>',
            unsafe_allow_html=True,
        )
        exp_rows = []
        for exp in experience:
            title = exp.title or "Position"
            company = exp.company or "Company"
            desc = exp.description or ""
            exp_rows.append(
                f'<div style="margin-bottom: 12px;">'
                f'<div style="font-weight: 600; color: var(--text);">{title} at {company}</div>'
                f'<div class="tl-card-body" style="font-size: 13px; color: var(--muted); margin-top: 2px;">{desc}</div>'
                f'</div>'
            )
        st.markdown(
            "".join(exp_rows)
            or '<div style="color: var(--muted); font-size: 14px;">No experience history details.</div>',
            unsafe_allow_html=True,
        )

    with col_edu:
        st.markdown(
            '<div style="font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Education Background</div>',
            unsafe_allow_html=True,
        )
        edu_rows = []
        for edu in education:
            degree = edu.degree or "Degree"
            inst = edu.institution or "Institution"
            desc = edu.description or ""
            edu_rows.append(
                f'<div style="margin-bottom: 12px;">'
                f'<div style="font-weight: 600; color: var(--text);">{degree} - {inst}</div>'
                f'<div class="tl-card-body" style="font-size: 13px; color: var(--muted); margin-top: 2px;">{desc}</div>'
                f'</div>'
            )
        st.markdown(
            "".join(edu_rows)
            or '<div style="color: var(--muted); font-size: 14px;">No education history details.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="tl-divider"></div>', unsafe_allow_html=True)

    # 4. Projects & Certifications split columns
    col_proj, col_cert = st.columns(2)
    with col_proj:
        st.markdown(
            '<div style="font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Projects</div>',
            unsafe_allow_html=True,
        )
        proj_rows = []
        for proj in projects:
            title = proj.title or "Project"
            desc = proj.description or ""
            proj_rows.append(
                f'<div style="margin-bottom: 12px;">'
                f'<div style="font-weight: 600; color: var(--text);">{title}</div>'
                f'<div class="tl-card-body" style="font-size: 13px; color: var(--muted); margin-top: 2px;">{desc}</div>'
                f'</div>'
            )
        st.markdown(
            "".join(proj_rows)
            or '<div style="color: var(--muted); font-size: 14px;">No projects detected.</div>',
            unsafe_allow_html=True,
        )

    with col_cert:
        st.markdown(
            '<div style="font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Certifications</div>',
            unsafe_allow_html=True,
        )
        cert_badges = "".join(f'<span class="tl-badge tl-badge-primary" style="margin-bottom: 4px; display: inline-block;">{c.name}</span> ' for c in certifications)
        st.markdown(
            f'<div>{cert_badges}</div>'
            if cert_badges
            else '<div style="color: var(--muted); font-size: 14px;">No certifications detected.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def skills_card(matched_skills: list[str], missing_skills: list[str]) -> None:
    """Render skills matched and missing details grouped by technical folders.

    Args:
        matched_skills: List of matching skill names.
        missing_skills: List of missing skill names.
    """
    matched_cats = _categorize_skills(matched_skills)
    missing_cats = _categorize_skills(missing_skills)

    categories_html = []
    for cat in ["Technical", "Soft Skills", "Tools", "Languages"]:
        cat_matched = matched_cats[cat]
        cat_missing = missing_cats[cat]

        if not cat_matched and not cat_missing:
            continue

        matched_badges = "".join(f'<span class="tl-badge tl-badge-success">{s}</span>' for s in cat_matched)
        missing_badges = "".join(f'<span class="tl-badge tl-badge-danger">{s}</span>' for s in cat_missing)

        badges_block = []
        if cat_matched:
            badges_block.append(f'<div><span style="font-size: 11px; color: var(--success); font-weight: 600; text-transform: uppercase;">Matched:</span> {matched_badges}</div>')
        if cat_missing:
            badges_block.append(f'<div style="margin-top: 4px;"><span style="font-size: 11px; color: var(--danger); font-weight: 600; text-transform: uppercase;">Missing:</span> {missing_badges}</div>')

        categories_html.append(
            f'<div style="margin-bottom: 16px; text-align: left;">'
            f'<div style="font-size: 13px; font-weight: 600; color: var(--text); border-bottom: 1px solid var(--border); padding-bottom: 4px; margin-bottom: 8px;">{cat} Skills</div>'
            f'{"".join(badges_block)}'
            f'</div>'
        )

    header_icon = _render_icon("extension")
    content = f"""
    <div class="tl-card-header">{header_icon} Skills Match Matrix</div>
    <div class="tl-stack" style="gap: 8px !important;">
        {"".join(categories_html) or '<div style="color: var(--muted); font-size: 14px;">No skills extracted.</div>'}
    </div>
    """
    _card(content, card_class="tl-card")


def insights_summary_card(
    title: str,
    items: list[str],
    status_type: str = "primary",
    icon: str = "",
) -> None:
    """Render reusable diagnostic insight category points inside bordered wrappers.

    Args:
        title: Insights panel heading.
        items: List of textual insight feedback points.
        status_type: Visual theme config mapping ('success', 'warning', 'danger', 'primary').
        icon: Standard icon indicator name.
    """
    icon_html = _render_icon(icon)
    items_html = "".join(
        f'<div class="tl-info-row" style="margin-bottom: 6px;">'
        f'<span class="material-symbols-outlined tl-icon" style="font-size: 16px; color: var(--muted);">arrow_right</span>'
        f'<span>{item}</span></div>' for item in items
    ) or '<div style="color: var(--muted); font-size: 14px;">No highlights detected.</div>'

    content = f"""
    <div class="tl-card-header">{icon_html} {title}</div>
    <div class="tl-stack" style="gap: 8px !important;">
        {items_html}
    </div>
    """
    _card(content, card_class=f"tl-card tl-banner-{status_type}")


def roadmap_timeline(steps: list[str]) -> None:
    """Render the learning pathway steps using custom flex-aligned timeline modules.

    Args:
        steps: Recommended roadmap steps to bridge qualifications.
    """
    if not steps:
        header_icon = _render_icon("celebration", extra_class="tl-icon")
        content = f"""
        <div class="tl-flex" style="color: var(--success); font-size: 14px;">
            {header_icon}
            <span>All required skills are present. No roadmap required.</span>
        </div>
        """
        _card(content, card_class="tl-card")
        return

    milestones = ["Week 1", "Month 1", "Month 3", "Month 6"]
    rows_html = []
    for idx, step in enumerate(steps):
        milestone = milestones[idx] if idx < len(milestones) else f"Phase {idx + 1}"
        is_last = idx == len(steps) - 1
        line_html = "" if is_last else '<div class="timeline-line"></div>'

        row = f"""
        <div class="timeline-row">
            <div class="timeline-left">
                <div class="timeline-dot"></div>
                {line_html}
            </div>
            <div class="timeline-content">
                <div style="font-size: 14px; font-weight: 700; color: var(--primary);">{milestone}</div>
                <div class="tl-card-body" style="margin-top: 4px;">{step}</div>
            </div>
        </div>
        """
        rows_html.append(row)

    header_icon = _render_icon("route")
    content = f"""
    <div class="tl-card-header">{header_icon} Career Roadmap Timeline</div>
    <div style="margin-top: 16px;">
        {"".join(rows_html)}
    </div>
    """
    _card(content, card_class="tl-card")


def export_panel(pdf_bytes_ready: bool) -> None:
    """Render export options card explaining evaluation exports.

    Args:
        pdf_bytes_ready: Boolean mapping if PDF files compilation finished.
    """
    status_color = "var(--success)" if pdf_bytes_ready else "var(--warning)"
    status_text = "Analysis report compiled and ready." if pdf_bytes_ready else "Pending candidate evaluation inputs."

    header_icon = _render_icon("download")
    content = f"""
    <div class="tl-card-header">{header_icon} Export Assessment</div>
    <div class="tl-card-body">
        Download the structured candidate review mapping as a formatted PDF for recruitment pipeline sharing.
    </div>
    <div style="font-size: 12px; font-weight: 600; color: {status_color}; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 12px;">
        Status: {status_text}
    </div>
    """
    _card(content, card_class="tl-card")


def empty_state(
    title: str,
    description: str,
    cta: str,
    illustration: str,
) -> None:
    """Render onboarding vector empty state landing page panel with sidebar focus CTA.

    Args:
        title: Main onboarding message.
        description: Informational descriptive context.
        cta: Button action text.
        illustration: Material symbol icon name representation.
    """
    header_icon = _render_icon(illustration, extra_class="")

    st.markdown('<div class="tl-empty-state">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 48px; color: var(--primary); margin-bottom: 16px;">{header_icon}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 24px; font-weight: 700; color: var(--text); margin-bottom: 8px;">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tl-card-body" style="margin-bottom: 24px; text-align: center;">{description}</div>', unsafe_allow_html=True)

    # Streamlit button wrapping state triggers
    st.markdown('<div class="tl-button" style="max-width: 240px; margin: 0 auto;">', unsafe_allow_html=True)

    def on_cta_click():
        st.session_state.cta_clicked = True

    st.button(cta, key="empty_state_cta", on_click=on_cta_click)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def loading_state(steps: list[str], current_step: int) -> None:
    """Render dynamically updating progress logs checklist indicators.

    Args:
        steps: List of all evaluation task steps.
        current_step: Index of the currently executing step (0-indexed).
    """
    steps_html = []
    for idx, step in enumerate(steps):
        if idx < current_step:
            icon_html = _render_icon("check_circle", extra_class="tl-icon")
            step_class = "tl-step-completed"
        elif idx == current_step:
            icon_html = _render_icon("sync", extra_class="tl-spin")
            step_class = "tl-step-active"
        else:
            icon_html = _render_icon("radio_button_unchecked", extra_class="tl-icon")
            step_class = "tl-step-pending"

        steps_html.append(
            f'<div class="tl-flex {step_class}">'
            f'{icon_html}'
            f'<span>{step}</span></div>'
        )

    content = f"""
    <div class="tl-card-header">Running Candidate Diagnostics</div>
    <div class="tl-stack">
        {"".join(steps_html)}
    </div>
    """
    _card(content, card_class="tl-loading-state")
