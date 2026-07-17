# Candidate Intelligence Technical Specification
## Version: 1.0.0
## Category: Platform Core Intelligence Specs
## Status: Approved / Engineering Blueprint
## Author: Lead Software Architect & Staff AI Engineer, TalentLens AI Group

---

## 1. Responsibilities
The **Candidate Intelligence** module is responsible for one thing: **Transforming unstructured resume text into a structured, type-safe candidate professional profile.** 

### What it Owns
- **Contact Extraction**: Validating and compiling candidate name, email, phone, LinkedIn, GitHub, portfolio URLs, and location coordinates.
- **Narrative Composition**: Generating a concise candidate narrative from parsed resume details if no summary is found.
- **Experience Timeline Parsing**: Segmenting and structuring candidate employment history, dates, roles, achievements, and tech stacks.
- **Education Timeline Parsing**: Segmenting and structuring candidate academic history, institutions, fields of study, dates, majors, and GPAs.
- **Project Portfolio Parsing**: Segmenting and structuring candidate project names, descriptions, tech stacks, domains, links, and key achievements.
- **Certification Portfolio Parsing**: Segmenting and structuring candidate certification credentials, issuing organizations, dates, and verification links.
- **Technical Profile Categorization**: Classifying candidate skill sets into Programming Languages, Frameworks, Libraries, Databases, Cloud, Developer Tools, ML Tools, and Soft Skills.

### What it Does NOT Own
- **Suitability Scoring**: AHRI scores, grades, bonuses, and penalties.
- **Job Matching (Similarity)**: Cosine similarity matching between candidate skills and job requirements.
- **Hiring Verdict Decisions**: Direct recommendations (Fast-Track, Screen, Hold).
- **Risk Analysis**: Flagging gaps, turnover concerns, or mismatch risk indices.
- **Interview Strategy**: Generating targeted, candidate-specific interview question recommendations.
- **Candidate Comparisons**: Managing batch screening matrices.

---

## 2. Inputs
Candidate Intelligence accepts raw candidate inputs:
- **Resume Text**: Spacing-normalized, UTF-8 encoded text parsed from the candidate document.
- **Pre-processed Sections**: A dictionary mapping raw parsed section headers (Summary, Skills, Experience, Education, Projects, Certifications) to their respective text segments.
- **Config Constants**: Skill definitions and keyword lists from `modules/config.py`.

---

## 3. Outputs
Candidate Intelligence outputs a structured payload containing:

### 3.1 CandidateProfile (Resume Dataclass Root)
- `contact`: Structured `ContactInfo`.
- `professional_identity`: Structured `ProfessionalIdentity`.
- `summary`: Candidate narrative summary string.
- `skills`: List of parsed skills.
- `experience`: List of structured `Experience` records.
- `education`: List of structured `Education` records.
- `projects`: List of structured `Project` records.
- `certifications`: List of structured `Certification` records.
- `technical_profile`: Structured `TechnicalProfile`.

### 3.2 ContactInfo
- `name`: Candidate name string or None.
- `email`: Validated email address string or None.
- `phone`: Validated phone number string or None.
- `linkedin`: LinkedIn profile URL string or None.
- `github`: GitHub profile URL string or None.
- `portfolio`: Portfolio URL string or None.
- `location`: Location name string or None.

### 3.3 ProfessionalIdentity
- `current_title`: Candidate's current job title.
- `career_focus`: Evaluated primary career direction.
- `primary_domain`: Broad industry segment focus.
- `technical_specialization`: Specific technical focus area.

### 3.4 TechnicalProfile
- `programming_languages`: List of extracted language skills.
- `frameworks`: List of matching framework skills.
- `libraries`: List of matching library skills.
- `databases`: List of database skills.
- `cloud`: List of cloud provider skills.
- `developer_tools`: List of developer tools and utilities.
- `ml_tools`: List of machine learning tools.
- `soft_skills`: List of soft skills.

### 3.5 Experience
- `title`: Job title.
- `company`: Employing organization.
- `duration`: Timeframe dates.
- `description`: Detailed description.
- `technologies`: List of technologies used.
- `achievements`: List of highlighted achievements.

### 3.6 Education
- `degree`: Degree type.
- `institution`: School name.
- `dates`: Timeframe dates.
- `major`: Field of study.
- `gpa`: GPA score.

### 3.7 Project
- `title`: Project title.
- `description`: Detailed description.
- `technologies`: List of technologies used.
- `domain`: Broad technical domain.
- `github`: GitHub repository link.
- `demo`: Live demo link.
- `key_achievements`: List of highlighted achievements.

### 3.8 Certification
- `name`: Certification name.
- `organization`: Issuing organization.
- `date`: Issuing date.
- `credential_url`: Certification verification link.

---

## 4. Data Relationships

The CandidateProfile relates to its sub-components:

```
                  ┌──────────────────────┐
                  │   CandidateProfile   │
                  └──────────┬───────────┘
      ┌──────────────────────┼──────────────────────┐
      ▼                      ▼                      ▼
┌───────────┐         ┌──────────────┐       ┌─────────────┐
│ContactInfo│         │ Professional │       │  Technical  │
└───────────┘         │   Identity   │       │   Profile   │
                      └──────────────┘       └─────────────┘
                             │
      ┌──────────────┬───────┴──────┬──────────────┐
      ▼              ▼              ▼              ▼
┌──────────┐   ┌───────────┐   ┌─────────┐   ┌─────────────┐
│Experience│   │ Education │   │ Project │   │Certification│
└──────────┘   └───────────┘   └─────────┘   └─────────────┘
```

---

## 5. Parsing Strategy
1. **Contact Parsing**: Extracts emails, phone numbers, and portfolio links using standard RegEx patterns.
2. **Professional Identity**: Infers the candidate's current title and specialization from their latest experience entries.
3. **Experience Timeline**: Splits employment records by double newlines, extracting titles, dates, bullet point achievements, and tech stacks.
4. **Education Timeline**: Parses institution names and degree details, extracting majors, dates, and GPAs.
5. **Project Portfolio**: Identifies projects by double newlines, extracting tech stacks and demo links.
6. **Certification Portfolio**: Splits certification listings, extracting credentials, organizations, and dates.
7. **Technical Profile**: Classifies skills into specialized categories using config keyword lists.

---

## 6. Candidate Narrative Strategy
If a candidate resume lacks a professional summary:
- **Evidence-Based Compilation**: Synthesizes a narrative based on experience years, current title, and core skills:
  `"Professional [Title] with [X] years of experience. Experienced in [Skills]."`
- **Zero Hallucinations**: Ensures every detail in the narrative corresponds to a parsed data field.

---

## 7. Confidence Strategy
Every extracted field supports a confidence score:
- **Contact Info**: Returns a confidence score based on pattern matches.
- **Section Parsing**: Returns a confidence score based on header segment alignment.

---

## 8. Validation Rules
- **Emails**: Validated against standard email formats.
- **Phone Numbers**: Checked for minimum digits and valid country code prefix formats.
- **URLs**: Evaluated against LinkedIn, GitHub, or standard web link formats.
- **Dates**: Normalized to standard year/month formats.
- **Experience, Education, Projects, Certifications**: Must contain at least one non-empty string identifier.

---

## 9. Error Handling
- **Missing Sections**: Fallback summaries are generated if a resume is missing a summary section.
- **Incomplete Entries**: Default placeholders are used if a parsed entry lacks details (e.g. defaulting degree to `"Not Specified"` if missing).

---

## 10. Extension Points
- **LinkedIn/GitHub Imports**: Raw profiles can be mapped directly to the `CandidateProfile` schema.
- **ATS Connectors**: The `CandidateProfile` can be serialized to JSON and shared with external ATS tools.

---

## 11. Module Boundary
The structured profile output from Candidate Intelligence is consumed by subsequent pipeline modules:
- **Evidence Intelligence**: Maps skills matches and gaps.
- **Risk Intelligence**: Evaluates candidate warning flags.
- **Decision Intelligence**: Calculates composite scores and recommendations.
- **Interview Strategy**: Suggests candidate-specific interview questions.

---

## 12. Implementation Plan

### Production Files Modified

#### 1. [`modules/models.py`](file:///C:/Users/ASUS/OneDrive/Documents/GitHub/TalentLens-AI/modules/models.py)
- **Why**: Needs to hold the expanded candidate schemas.
- **Responsibility**: Houses domain model structures.
- **Breaking Change Check**: Non-breaking; new fields will default to `None` or list factories.

#### 2. [`modules/parser.py`](file:///C:/Users/ASUS/OneDrive/Documents/GitHub/TalentLens-AI/modules/parser.py)
- **Why**: Needs to implement advanced segment parsing and skills classification.
- **Responsibility**: Parses raw resume texts into candidate profiles.
- **Breaking Change Check**: Non-breaking; returns a fully backward-compatible `Resume` model.
