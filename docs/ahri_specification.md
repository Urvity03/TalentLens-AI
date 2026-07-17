# Adaptive Hiring Readiness Index (AHRI) - Specification Document
## Version: 1.0.0
## Classification: Flagship Core Technology Specification
## Author: Tech Lead & Senior AI Engineer, TalentLens AI Group

---

## 1. Meaning & Definition
The **Adaptive Hiring Readiness Index (AHRI)** is TalentLens AI's flagship scoring methodology. It is an explainable, multi-dimensional score (0.0 to 100.0) that represents a candidate's readiness and suitability for a specific role. 

Unlike legacy keyword-matching algorithms or simple "black-box" vector similarities, AHRI evaluates candidates by combining semantic similarity scores with explicit skill bonuses, gaps penalties, and resume completeness weights. It adjusts dynamically depending on the stringency of the target role requirements.

## 2. Vision
Our vision is to establish AHRI as the global standard for candidate pre-screening suitability. Much like PageRank became the standard for web page relevance, AHRI aims to become the definitive standard for talent mapping. We seek to replace subjective screening practices with a transparent, explainable index that hiring managers and recruiters can rely on with confidence.

---

## 3. Mathematical Scoring Model

The AHRI score is calculated using the following mathematical formula:

$$\text{AHRI} = \text{max}\left(0.0, \text{min}\left(\text{Base Similarity} + \text{Bonus} - \text{Penalty}, 100.0\right)\right)$$

### 3.1 Base Semantic Similarity
The **Base Similarity** score represents the semantic alignment between the candidate's profile and the job description. It is computed as a weighted sum of three cosine similarity values derived from dense sentence embeddings (using `sentence-transformers`):

$$\text{Base Similarity} = w_{\text{summary}} \cdot S_{\text{summary}} + w_{\text{skills}} \cdot S_{\text{skills}} + w_{\text{experience}} \cdot S_{\text{experience}}$$

#### Weights ($w_i$)
- $w_{\text{summary}} = 0.20$ (Executive Summary alignment)
- $w_{\text{skills}} = 0.50$ (Skill profile alignment)
- $w_{\text{experience}} = 0.30$ (Employment experience and descriptions alignment)

$$\sum w_i = 1.00$$

### 3.2 Skill Bonus
To reward candidates who possess the exact skills specified in the job description:

$$\text{Bonus} = \text{min}\left(N_{\text{matched}} \cdot B_{\text{skill}}, B_{\text{max}}\right)$$

- $N_{\text{matched}}$: Number of matching job description skills found in the resume.
- $B_{\text{skill}}$: Skill bonus factor ($1.0$ point per match).
- $B_{\text{max}}$: Maximum cap on skill bonuses ($10.0$ points).

### 3.3 Skill Penalty
To penalize candidates who lack key skills specified in the job description:

$$\text{Penalty} = \text{min}\left(N_{\text{missing}} \cdot P_{\text{skill}}, P_{\text{max}}\right)$$

- $N_{\text{missing}}$: Number of required job description skills missing from the resume.
- $P_{\text{skill}}$: Skill penalty factor ($0.5$ points per missing skill).
- $P_{\text{max}}$: Maximum cap on skill penalties ($10.0$ points).

---

## 4. Grade Boundaries
The final AHRI score is mapped to a letter grade to provide clear recruiter classification:

| AHRI Score Range | Grade | Recruiter Interpretation |
| :--- | :--- | :--- |
| **90.00 – 100.00** | **A+** | **Outstanding Fit**: Exceeds requirements; candidate holds all core skills and extensive matching experience. |
| **80.00 – 89.99** | **A** | **Excellent Fit**: Strong alignment; minor skill gaps that can be quickly bridged with light onboarding. |
| **70.00 – 79.99** | **B** | **High Fit**: Satisfactory alignment; candidate possesses core skills but lacks secondary tools/skills. |
| **60.00 – 69.99** | **C** | **Moderate Fit**: Gaps present; candidate requires substantial upskilling or transition training. |
| **50.00 – 59.99** | **D** | **Marginal Fit**: Weak alignment; significant experience and skill mismatches. |
| **0.00 – 49.99** | **F** | **Unsuitable**: No relevant match. |

---

## 5. Input Data Schema
To calculate AHRI, the scoring engine requires the following inputs:
- **Resume Model**:
  - `contact`: Parsed contact fields.
  - `summary`: Candidate summary text block.
  - `skills`: List of parsed skills.
  - `experience`: List of experience entries with descriptions.
  - `education`: List of education entries with descriptions.
- **Job Description Model**:
  - `title`: Target role title.
  - `summary`: Short job overview.
  - `skills`: List of required skills.
  - `experience`: Required experience text.
  - `education`: Required education text.

---

## 6. Output Properties
The AHRI engine outputs a structured payload containing:
- `score`: Rounded floating-point value between 0.00 and 100.00.
- `grade`: String letter grade mapping.
- `strengths`: List of matching required skills.
- `missing_skills`: List of missing required skills.
- `recommendation`: Contextual summary verdict.

---

## 7. Penalty Rules & Edge Cases

### 7.1 Extreme Gaps
If a candidate misses more than 80% of required skills, the base similarity is heavily impacted, and the max penalty ($10.0$ points) is automatically applied, keeping the score below **C** range.

### 7.2 Zero Skills in Job Description
If a job description is uploaded without a "Skills" section:
- $S_{\text{skills}}$ defaults to a similarity value of `100.0`.
- Bonus and Penalty values default to `0.0`.
- The system flags a warning: `"JD lacks structured skills; AHRI calculation downgraded to pure semantic comparison."`

### 7.3 Empty Resume Sections
If a resume lacks a "Summary" or "Experience" section, its respective cosine similarity defaults to `0.0`, resulting in a significantly lower score.

---

## 8. Decision Mapping & Interpretation
Recruiters and hiring managers use AHRI scores to automate pipeline decisions:

- **Score >= 80.0 (Grade A/A+)**: **Fast-Track**. Candidate bypasses manual screening and is routed directly to hiring manager review.
- **Score 70.0 – 79.9 (Grade B)**: **Standard Screen**. Recruiter reviews candidate profile manually, checking education and project history.
- **Score < 70.0 (Grade C/D/F)**: **Auto-Hold / Upskilling Route**. Candidates are placed on hold. A personalized career roadmap is compiled to help them bridge skill gaps.

---

## 9. Explainability Framework
To avoid the "black-box" problem, every AHRI score includes a detailed explanation:
1. **Semantic Fit Breakdown**: Shows the contribution of the executive summary, skills, and experience to the base similarity score.
2. **Skill Influence Ledger**: Displays the exact impact of skill bonuses and missing skill penalties on the score.
3. **Traceability**: All matching scores are mapped directly to source sentences in the candidate's resume.

---

## 10. Bias Considerations
To ensure fair evaluations:
- **Demographic Isolation**: The scoring engine excludes names, emails, phones, LinkedIn profiles, and GitHub links from similarity embeddings.
- **Academic Neutrality**: Education similarity evaluates degrees and fields of study, ignoring specific university names to prevent school-brand bias.
- **Synonym Normalization**: The semantic engine uses dense embeddings to match synonyms (e.g., matching "Python scripting" with "Python coding"), preventing keyword penalties.

---

## 11. Validation & Testing Strategy

### 11.1 Golden Dataset Validation
A curatated "Golden Dataset" of 100 candidate resumes and 10 job descriptions evaluated by senior recruiters is maintained. 
- **Validation Criteria**: The system's AHRI scores must correlate with human recruiter ratings with a Pearson correlation coefficient ($r$) of at least $0.85$.

### 11.2 Regression Testing
Every code change triggers automated regression tests verifying that:
- Standard candidate resumes yield the exact expected AHRI scores.
- Unsuitable profiles do not receive high grades.
- PDF exports match score outputs exactly.
- Extreme inputs (empty files, giant strings) do not cause runtime errors.
