# TalentLens AI - Recruiter Workflow Specification
## Version: 1.0.0
## Category: AI Hiring Intelligence Platform
## Status: Approved / User Experience Blueprint
## Author: Lead Product Designer & VP of Product, TalentLens AI Group

---

## 1. Recruiter Goals
The primary goal of a recruiter using TalentLens AI is to **make fast, accurate, and explainable screening decisions.** Recruiters are trying to answer several key questions:
- Does this candidate possess the required technical skills for the role?
- Does their professional experience demonstrate the depth and impact needed?
- What are the potential risks or qualifications gaps associated with this profile?
- Should I move this candidate to the next round of interviews?
- What specific topics or gaps should the hiring manager focus on during the interview?

---

## 2. User Journey
The recruiter's journey flows through a structured, multi-stage process:

```
[Application Opens] ──► [Onboarding Empty State]
                              │
                              ▼
                        [Upload Files] ── (Resume PDF/DOCX & JD Text/File)
                              │
                              ▼
                        [Pipeline Run] ── (Ticking progress checkpoints logs)
                              │
                              ▼
                        [Review Space] ── (Metrics KPIs & 6 interactive tabs)
                              │
                              ▼
                        [Action Export] ─ (One-click candidate assessment PDF)
```

1. **Application Opens**: Recruiter lands on a clean workspace displaying a focused empty state.
2. **Upload Files**: Recruiter uploads the candidate resume and configures the target job requirements.
3. **Pipeline Run**: Ticking progress checklist logs keep the recruiter informed during the analysis run.
4. **Review Space**: Renders core suitability KPIs and the 6-tab dashboard workspace.
5. **Action Export**: Recruiter generates and downloads the Candidate Evaluation Report PDF.

---

## 3. Recruiter Decision Flow
To prevent cognitive overload, the interface guides the recruiter through a natural decision-making path:

```
[Profile Context] ────────► (Who is this candidate? Contacts, summary, education)
        │
        ▼
[Capability Assessment] ──► (Can they do the job? Skills matrix match)
        │
        ▼
[Risk Identification] ────► (What are the risks? Strengths/Concerns ledger)
        │
        ▼
[Hiring Verdict] ─────────► (Should I interview? AHRI grading and indicators)
        │
        ▼
[Interview Copilot] ──────► (What should I ask? Targeted focus questions)
        │
        ▼
[Assessment Export] ──────► (Export candidate report PDF)
```

---

## 4. Information Hierarchy
Information is structured by importance to allow quick scanning:
- **Primary Information (Top Screen)**: Overall suitability score (AHRI), resume quality metric, skill match percentage, and recommendation verdict.
- **Secondary Information (Tabs)**: Candidate contact details, categorized skill match matrices, and strengths/concerns lists.
- **Supporting Information (Detailed Cards)**: Professional experience histories, education backgrounds, and chronological upskilling roadmaps.

---

## 5. Dashboard Sections
The workspace layout is divided into dedicated tabs:
- **Overview**: Displays contact links, experience records, education details, and parsed projects.
- **Skills Intelligence**: Displays matched and missing skills grouped into technical categories.
- **Recruiter Insights**: Displays strengths, concerns, recommendation verdicts, and culture fit indicators.
- **Analytics**: Compiles gauges, bar charts, and suitability comparison dataframes.
- **Career Roadmap**: Displays chronological upskilling timelines (Weeks/Months) and recommended courses.
- **Export Report**: Displays report details and triggers report PDF downloads.

---

## 6. Screen-by-Screen Breakdown
- **Landing Onboarding Page**: Prompt recruiters to configure files in the sidebar, providing an active "Get Started" guidance button.
- **Diagnostics Processing Stage**: Displays a progress checklist during runs to maintain user engagement.
- **Platform Cockpit Workspace**: An interactive 6-tab panel displaying candidate credentials, insights, and export triggers.

---

## 7. Recruiter Questions
At every stage, the interface addresses specific recruiter questions:
- *On Overview*: Who is this candidate and what is their background?
- *On Skills Matrix*: Do they hold the required technical qualifications?
- *On Recruiter Insights*: What are their key strengths and potential risk gaps?
- *On Analytics*: How do their credentials compare against our target hiring standards?
- *On Career Roadmap*: How can they bridge identified skill gaps?
- *On Export*: How can I share this candidate profile evaluation with my hiring manager?

---

## 8. Empty States
Before files are configured, the empty state displays:
- A clean, centered workspace title and platform description.
- A functional "Get Started" CTA button. Clicking the button displays a guidance warning: `"← Sidebar Active! Please drag and drop your candidate resume in the panel on the left to get started."`

---

## 9. Loading Experience
During evaluations, the progress loader displays an active checklist showing completed, processing, and pending steps. This keeps recruiters engaged and manages expectations during the model run.

---

## 10. Error Experience
Errors are communicated clearly using color-coded status elements:
- *Missing Job Description*: Displays `"Please provide a job description (paste text or upload file)."`
- *Invalid/Corrupted Files*: Displays `"No readable text extracted. Please verify that your PDF/DOCX file is not corrupted."`
- *Parser Failures*: Gracefully handles missing resume sections using automated summary generation fallbacks.

---

## 11. Explainability Experience
Every AI suitability grade is supported by clear evidence:
- **No Unexplained Penalties**: Any score reduction corresponds to a visible entry in the missing skills list or concerns ledger.
- **Source Traceability**: Matching metrics map directly to parsed text segments.
- **Confidence Disclosures**: Highlights the completeness rating of the candidate's profile.

---

## 12. Export Experience
The exported PDF report is a structured, two-page document:
- **Page 1 (Intake & Verdict)**: Displays candidate contact details, readiness metrics, and recruiter strengths and concerns.
- **Page 2 (Detail & Roadmaps)**: Displays experience history, education background, and the candidate upskilling roadmap.

---

## 13. Future Workflow
- **Batch Evaluation Workspace**: Supports uploading multiple resumes, ranking profiles in comparative scoring tables.
- **ATS webhook integrations**: Pushes candidate suitability recommendations directly to third-party tools like Ashby and Greenhouse.
- **Sourcing connector cards**: Connects profiles to LinkedIn and GitHub for credential validation.

---

## 14. UX Principles
Every design decision follows several core principles:
- **Clarity Over Decoration**: We prioritize clean text and scannable metrics over distracting visual widgets.
- **Explain Before Scoring**: We justify every score with visible evidence (matched skills, strengths).
- **Evidence Before Recommendation**: Recruiter recommendations must list the matching credentials that justify the decision.
- **Trust Before Automation**: The platform supports recruiter decisions rather than replacing them.
