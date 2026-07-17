# TalentLens AI - Milestone Implementation Plan
## Version: 1.0.0
## Category: AI Hiring Intelligence Platform
## Status: Pending Approval / Engineering Roadmap
## Author: Lead Software Architect & Tech Lead, TalentLens AI Group

---

## Executive Audit Summary
We audited the active TalentLens-AI repository against the approved specifications (`product_bible.md`, `ahri_specification.md`, `ahri_v2_whitepaper.md`, `technical_design_document.md`, `recruiter_workflow_specification.md`). The following matrix summaries our findings:

- **What Exists**: Basic PDF/DOCX preprocessing, SentenceTransformer cosine similarity computations, raw section parsing, a 6-tab Streamlit dashboard layout, simple Plotly visualizations, and a PyMuPDF PDF compiler.
- **What Must Be Improved**: Section extraction accuracy, career experience separation, skills categorization, and PDF layout spacing.
- **What Must Be Built From Scratch**: Multi-candidate comparative tables, folder-based batch screening services, and ATS connector stubs.

---

## Milestone 1: Candidate Narrative Engine

### Objective
Establish the candidate profile parsing layer, extracting contact parameters, summaries, and career milestones (education, experiences, projects, and certifications).

### Business Value
Reduces manual data entry for recruiters by automatically extracting clean, structured candidate records.

### Files Involved
- `modules/preprocess.py` (Improve)
- `modules/parser.py` (Improve)
- `modules/models.py` (Improve)

### Dependencies
- PyMuPDF, python-docx, ReGex configurations.

### Existing vs. To Build
- *Existing*: Basic file text extraction and spacing normalization.
- *To Improve*: Regex section mapping boundaries to prevent text overlaps.
- *To Build*: Detailed experience entry extraction splitting employment records by double newlines and extracting titles, companies, and descriptions.

### Acceptance Criteria
- Parse standard candidate resumes correctly.
- Extract contact details (email, phone, LinkedIn, GitHub).
- Split and structure experiences and educations as separate objects.

### Tests Required
- `tests/test_parser.py`: Verifies field parsing outputs.
- `tests/test_narrative.py`: Verifies experience entries parsing correctness.

### Definition of Done
- No text leaks between sections.
- Experience and education items parsed into lists of structured models.
- All syntax check and unit test checks pass.

### Risk Assessment
- *Risk*: Highly non-standard resume formats may result in parsing gaps.
- *Mitigation*: Fallback default values and summaries are compiled if fields are missing.

---

## Milestone 2: Evidence Engine

### Objective
Implement semantic matching and classification of candidate skills against job requirements.

### Business Value
Ensures recruiters can see exactly how a candidate’s skills align with the role, replacing simple keyword checks with semantic matches.

### Files Involved
- `modules/skill_extractor.py` (Improve)
- `modules/skill_intelligence.py` (Improve)
- `modules/similarity.py` (Improve)

### Dependencies
- SentenceTransformers model weights, config skill definitions.

### Existing vs. To Build
- *Existing*: Baseline cosine similarity scores.
- *To Improve*: Normalizing skills to match synonyms.
- *To Build*: Skill categorization sorting matches and gaps into Technical, Soft Skills, Tools, and Languages folders.

### Acceptance Criteria
- Matches synonyms (e.g. matching "py-spark" with "Apache Spark").
- Categorizes skills and match percentages accurately.
- Cosine embedding calculations execute in under 0.3 seconds.

### Tests Required
- `tests/test_skill_intelligence.py`: Verifies skill intersections and matching percentages.
- `tests/test_similarity.py`: Verifies similarity score scales.

### Definition of Done
- Skill lists grouped and rendered under standard folders in Tab 2.
- In-memory SentenceTransformer caching validated.

### Risk Assessment
- *Risk*: Downloading model weights during pipeline runs can cause startup latency.
- *Mitigation*: Caches model weights locally during build.

---

## Milestone 3: Risk Intelligence

### Objective
Identify potential candidate warning flags (experience gaps, missing required skills, and short job tenures).

### Business Value
Speeds up recruiter review times by automatically flagging potential alignment concerns.

### Files Involved
- `modules/models.py` (Improve)
- `modules/recruiter_insights.py` (Improve)
- `modules/risk_intelligence.py` (New)

### Dependencies
- Parsed experience history outputs from Milestone 1.

### Existing vs. To Build
- *Existing*: Basic concerns list in recruiter insights.
- *To Improve*: Deriving concerns using structured rules.
- *To Build*: A risk intelligence module calculating employment timeline continuity and specific required skills gaps.

### Acceptance Criteria
- Flags experience gaps greater than 6 months.
- Flags turnover patterns (e.g., multiple job changes under 1 year).
- Lists critical missing required credentials.

### Tests Required
- `tests/test_risk_intelligence.py`: Verifies risk analysis rules against sample timelines.

### Definition of Done
- Risk insights are returned in `AnalysisResult` and rendered in Tab 3.

### Risk Assessment
- *Risk*: False positive flags for candidates with career breaks.
- *Mitigation*: Recruiter workflows emphasize review before decision.

---

## Milestone 4: Decision Intelligence

### Objective
Integrate the multidimensional AHRI v2.0 composite scoring and grade mapping engine.

### Business Value
Standardizes candidate assessments across pipelines, providing a consistent grade (A+ to F) supported by clear evidence.

### Files Involved
- `modules/ahri.py` (Improve)
- `modules/config.py` (Improve)

### Dependencies
- Similarity, skill intelligence, and quality scores.

### Existing vs. To Build
- *Existing*: Baseline similarity weights calculation.
- *To Improve*: Adjusting bonuses and penalties weights dynamically.
- *To Build*: Unified grading functions mapping scores to recruiter verdicts (Fast-Track, Screen, Hold).

### Acceptance Criteria
- AHRI score calculated as: `Base Similarity + Bonus - Penalty`.
- Grade boundary mappings match the specification.
- Decision outcomes correspond to grade thresholds.

### Tests Required
- `tests/test_ahri.py`: Verifies score calculations, bonuses, and penalty limits.

### Definition of Done
- AHRI grade and decision mapping displayed in KPI headers and Tab 4.

### Risk Assessment
- *Risk*: Extreme inputs (empty job descriptions) could distort scores.
- *Mitigation*: Falling back to semantic comparison modes with warnings if fields are missing.

---

## Milestone 5: Interview Strategy

### Objective
Generate targeted, candidate-specific interview question recommendations.

### Business Value
Saves hiring managers preparation time by generating questions targeted to the candidate's specific skill gaps.

### Files Involved
- `modules/models.py` (Improve)
- `modules/interview_strategy.py` (New)
- `ui/cards.py` (Improve)

### Dependencies
- Missing skills and risk flags parsed in Milestones 2 and 3.

### Existing vs. To Build
- *Existing*: Static focus areas listed in insights.
- *To Improve*: Dynamically suggesting questions.
- *To Build*: Question generation rules mapping missing skills to behavioral and technical questions.

### Acceptance Criteria
- Suggests at least 3 interview questions targeted to candidate skill gaps.
- Suggests at least 1 question addressing identified risk flags (e.g., career gaps).

### Tests Required
- `tests/test_interview_strategy.py`: Verifies question generation rules.

### Definition of Done
- Interview guides are rendered on the dashboard and included in PDF exports.

---

## Milestone 6: Recruiter Workspace UI

### Objective
Refine the single-candidate dashboard UI, aligning the 6 tabs with our recruiter workflow principles.

### Business Value
Improves recruiter efficiency and onboarding through an enterprise-grade visual workspace.

### Files Involved
- `app.py` (Improve)
- `ui/styles.py` (Improve)
- `ui/cards.py` (Improve)
- `ui/charts.py` (Improve)

### Dependencies
- Finished data output payloads from Milestones 1 to 5.

### Existing vs. To Build
- *Existing*: Baseline tabs structures.
- *To Improve*: Visual spacing, typography readability, and card layouts.
- *To Build*: Clean onboarding state transitions with interactive focus buttons.

### Acceptance Criteria
- Supports Light and Dark modes.
- Renders KPI metrics, details tables, and timelines without overlapping.
- Clicking the onboarding CTA CTA scrolls or focus focus sidebar uploaders.

### Tests Required
- `tests/test_ui.py`: Verifies render state checks.

### Definition of Done
- Dashboard is verified against the Recruiter Workflow Specification.

---

## Milestone 7: Candidate Comparison

### Objective
Introduce side-by-side candidate comparison views.

### Business Value
Allows hiring managers to evaluate two candidates side-by-side.

### Files Involved
- `app.py` (Improve)
- `ui/cards.py` (Improve)
- `ui/comparison.py` (New)

### Dependencies
- Target comparison models.

### Existing vs. To Build
- *Existing*: None.
- *To Build*: Comparison views displaying two profile summaries, skills matches, and AHRI scores side-by-side.

### Acceptance Criteria
- Renders two candidate profiles side-by-side in the dashboard.
- Highlights differences in skills and experience.

### Tests Required
- `tests/test_comparison.py`: Verifies comparison view alignments.

### Definition of Done
- Recruiters can select and compare two candidates in the workspace.

---

## Milestone 8: Batch Screening

### Objective
Support bulk resume uploading and rank profiles in comparative tables.

### Business Value
Enables recruiters to process bulk applications in a single run.

### Files Involved
- `services/analyzer.py` (Improve)
- `modules/ranking.py` (Improve)
- `app.py` (Improve)

### Dependencies
- Single candidate parsing services.

### Existing vs. To Build
- *Existing*: Unused ranking module.
- *To Improve*: Enabling ranking logic in services.
- *To Build*: Sidebar bulk uploader and dashboard ranking table.

### Acceptance Criteria
- Support uploading multiple resumes.
- Renders ranked candidates in a comparative table, sorted by AHRI score.

### Tests Required
- `tests/test_ranking.py`: Verifies sorting candidate lists.

### Definition of Done
- Recruiters can evaluate and rank multiple candidates in the cockpit.

---

## Milestone 9: Enterprise Readiness

### Objective
Deploy performance logging, local model caching, input sanitization, and ATS webhook connectors.

### Business Value
Prepares TalentLens AI for deployment in enterprise environments.

### Files Involved
- `modules/preprocess.py` (Improve)
- `services/analyzer.py` (Improve)
- `config/` configurations (New)

### Dependencies
- Complete application workspace.

### Existing vs. To Build
- *Existing*: Basic temp file cleanup.
- *To Improve*: Input sanitization and size checks.
- *To Build*: Local model cache path configurations and ATS connector stubs.

### Acceptance Criteria
- Restricts upload file sizes (<10MB).
- Enforces model caching, eliminating hub connection startup delays.

### Tests Required
- `tests/test_performance.py`: Verifies runtimes.

### Definition of Done
- Production logs and cached models validated.
