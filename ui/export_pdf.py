"""PDF report generation service using PyMuPDF (fitz)."""

import fitz


def generate_pdf_report(res: any) -> bytes:
    """Generate a clean, professional candidate evaluation PDF report.

    Args:
        res: The AnalysisResult dataclass object containing pipeline findings.

    Returns:
        Bytes representing the compiled PDF document.
    """
    doc = fitz.open()

    # --- Page 1: Profile & Scores ---
    page1 = doc.new_page()

    # Title & Subtitle Header
    page1.insert_text(
        (54, 54),
        "TalentLens AI - Candidate Evaluation Report",
        fontsize=16,
        fontname="helv-bold",
        color=(0.043, 0.09, 0.141),
    )
    page1.insert_text(
        (54, 72),
        "TalentLens AI Recruiting Intelligence Platform",
        fontsize=9,
        fontname="helv",
        color=(0.42, 0.45, 0.5),
    )

    y = 110

    # Section 1: Candidate Bio & Contact Info
    page1.insert_text((54, y), "Candidate Profile Summary", fontsize=11, fontname="helv-bold", color=(0.19, 0.25, 0.35))
    y += 18
    page1.insert_text((54, y), f"Name: {res.resume.contact.name or 'Not Specified'}", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"Email: {res.resume.contact.email or 'Not Specified'}", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"Phone: {res.resume.contact.phone or 'Not Specified'}", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"LinkedIn: {res.resume.contact.linkedin or 'Not Specified'}", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"GitHub: {res.resume.contact.github or 'Not Specified'}", fontsize=9, fontname="helv")

    y += 25

    # Section 2: Metrics Summary
    page1.insert_text((54, y), "Evaluation Index Summary", fontsize=11, fontname="helv-bold", color=(0.19, 0.25, 0.35))
    y += 18
    page1.insert_text((54, y), f"Hiring Readiness (AHRI): {res.ahri.score:.1f} / 100.0 (Grade {res.ahri.grade})", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"Resume Completeness Quality: {res.quality:.1f} / 100.0", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"Skills Match Rate: {res.skill_intelligence.match_percentage:.1f}%", fontsize=9, fontname="helv")
    y += 13
    page1.insert_text((54, y), f"Career Potential Predictor: {res.potential.score:.1f} (Level: {res.potential.level})", fontsize=9, fontname="helv")

    y += 25

    # Section 3: Recruiter Insights
    page1.insert_text((54, y), "Recruiter Insights & Decision Guide", fontsize=11, fontname="helv-bold", color=(0.19, 0.25, 0.35))
    y += 18
    page1.insert_text((54, y), f"Recommendation: {res.recruiter.recommendation}", fontsize=9, fontname="helv-bold")

    y += 20
    page1.insert_text((54, y), "Key Strengths Highlighted:", fontsize=8, fontname="helv-bold", color=(0.42, 0.45, 0.5))
    for s in res.recruiter.strengths[:3]:
        y += 13
        page1.insert_text((64, y), f"- {s}", fontsize=9, fontname="helv")

    y += 20
    page1.insert_text((54, y), "Identified Concerns / Risk Gaps:", fontsize=8, fontname="helv-bold", color=(0.42, 0.45, 0.5))
    for c in res.recruiter.concerns[:3]:
        y += 13
        page1.insert_text((64, y), f"- {c}", fontsize=9, fontname="helv")

    # --- Page 2: Experience, Education, and Roadmap ---
    page2 = doc.new_page()

    page2.insert_text(
        (54, 54),
        "TalentLens AI - Candidate Experience & Roadmap",
        fontsize=16,
        fontname="helv-bold",
        color=(0.043, 0.09, 0.141),
    )

    y2 = 100

    # Professional Experience list in PDF
    page2.insert_text((54, y2), "Professional Experience History", fontsize=11, fontname="helv-bold", color=(0.19, 0.25, 0.35))
    y2 += 18
    if not res.resume.experience:
        page2.insert_text((54, y2), "No experience history records detected.", fontsize=9, fontname="helv")
        y2 += 13
    else:
        for exp in res.resume.experience[:3]:
            title = exp.title or "Position"
            company = exp.company or "Company"
            page2.insert_text((54, y2), f"{title} at {company}", fontsize=9, fontname="helv-bold")
            y2 += 13
            desc = exp.description or ""
            # Wrap lines simply if description is long
            desc_lines = [desc[i:i+85] for i in range(0, min(len(desc), 170), 85)]
            for d_l in desc_lines:
                page2.insert_text((64, y2), d_l, fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
                y2 += 11
            y2 += 5

    y2 += 15

    # Education Background list in PDF
    page2.insert_text((54, y2), "Education History", fontsize=11, fontname="helv-bold", color=(0.19, 0.25, 0.35))
    y2 += 18
    if not res.resume.education:
        page2.insert_text((54, y2), "No education history records detected.", fontsize=9, fontname="helv")
        y2 += 13
    else:
        for edu in res.resume.education[:2]:
            degree = edu.degree or "Degree"
            inst = edu.institution or "Institution"
            page2.insert_text((54, y2), f"{degree} - {inst}", fontsize=9, fontname="helv-bold")
            y2 += 13
            desc = edu.description or ""
            page2.insert_text((64, y2), desc[:85], fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
            y2 += 13

    y2 += 15

    # Skills Development Roadmap
    page2.insert_text((54, y2), "Personalized Career Upskilling Pathway", fontsize=11, fontname="helv-bold", color=(0.19, 0.25, 0.35))
    y2 += 18

    if not res.roadmap.steps:
        page2.insert_text((54, y2), "All required skills matched. No learning roadmap required.", fontsize=9, fontname="helv")
    else:
        for idx, step in enumerate(res.roadmap.steps[:4]):
            page2.insert_text((54, y2), f"Phase {idx + 1}: {step[:80]}", fontsize=9, fontname="helv")
            y2 += 15

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes
