# AI-Based Resume Matching & Ranking System

An intelligent, lightweight, and explainable prototype that compares candidate resumes against a given Job Description (JD) and generates calibrated matching scores, detailed skills-gap analyses, and candidate rankings.

Built specifically to operate with high accuracy on **consumer-grade, CPU-only hardware (Intel Core i5-1235U, 8 GB RAM)** without requiring heavy Docker containers or external vector database daemons.

---

## 🎥 Working Video Demonstration

![AI Resume Matcher Demo Walkthrough](demo/demo_preview.gif)

> 📹 **High-Definition Video File:** A complete 34-second end-to-end recording demonstrating all 5 modules (JD criteria extraction, batch loading 19 real resumes, live matching, dashboard filtering, score threshold adjustments, and candidate deep inspection drawer) is included at [`demo/ai_resume_matcher_demo.mp4`](demo/ai_resume_matcher_demo.mp4).
>
> To regenerate or re-record the automated demo at any time, run:
> ```bash
> python scripts/record_demo.py
> ```

---

## Table of Contents
- [🎥 Working Video Demonstration](#-working-video-demonstration)
- [1. System Architecture](#1-system-architecture)
- [2. Modules & Functional Requirements](#2-modules--functional-requirements)
- [3. The Matching Algorithm & Scoring Methodology](#3-the-matching-algorithm--scoring-methodology)
  - [The 4-Pillar Calibrated Formula](#the-4-pillar-calibrated-formula)
  - [Chunk-Level MaxSim Semantic Matching](#chunk-level-maxsim-semantic-matching)
  - [Relevant Experience Algorithm (Interval Merging)](#relevant-experience-algorithm-interval-merging)
  - [Guarded Fuzzy Matching & Short Skill Protection](#guarded-fuzzy-matching--short-skill-protection)
- [4. Empirical Benchmark & Validation Results](#4-empirical-benchmark--validation-results)
  - [Spearman Rank Correlation ($\rho = 0.951$)](#spearman-rank-correlation-rho--0951)
  - [Parsing Accuracy (Precision, Recall, F1)](#parsing-accuracy-precision-recall-f1)
  - [CPU & Memory Profiling](#cpu--memory-profiling)
- [5. Technology Stack](#5-technology-stack)
- [6. Installation & Quick Start](#6-installation--quick-start)
- [7. Running Automated Unit Tests & Benchmarks](#7-running-automated-unit-tests--benchmarks)
- [8. Repository Structure](#8-repository-structure)
- [9. Assignment Duration & Engineering Breakdown](#9-assignment-duration--engineering-breakdown)
- [10. License](#10-license)

---

## 1. System Architecture

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      Frontend (React 18 + Vite)                        │
 │  ┌─────────────────────────┐  ┌──────────────────────────────────────┐ │
 │  │ Module 1: JD Input &    │  │ Module 2: Batch Upload (>= 10 Res)   │ │
 │  │ Criteria Extraction     │  │ PDF & DOCX File Queue Preview        │ │
 │  └───────────┬─────────────┘  └──────────────────┬───────────────────┘ │
 │              │                                   │                     │
 │  ┌───────────▼───────────────────────────────────▼───────────────────┐ │
 │  │ Module 4: Candidate Ranking Dashboard (Sort, Filter, CSV Export)  │ │
 │  └───────────────────────────┬───────────────────────────────────────┘ │
 │                              │ (Click Candidate Row)                   │
 │  ┌───────────────────────────▼───────────────────────────────────────┐ │
 │  │ Module 5: Candidate Deep Analysis Drawer (Score Dial, Citations)   │ │
 │  └───────────────────────────────────────────────────────────────────┘ │
 └──────────────────────────────────▲─────────────────────────────────────┘
                                    │ REST API (JSON / FormData)
 ┌──────────────────────────────────▼─────────────────────────────────────┐
 │                      Backend (FastAPI + Python 3.12)                   │
 │  ┌──────────────────────────────────────────────────────────────────┐  │
 │  │ Dual Parser: pypdf (Layout-Aware) + python-docx (Table Reader)   │  │
 │  └───────────────────────────┬──────────────────────────────────────┘  │
 │                              │                                         │
 │  ┌───────────────────────────▼──────────────────────────────────────┐  │
 │  │ NLP & Extraction:                                                │  │
 │  │  • SkillsMatcher (260+ Curated Taxonomy + Aliases + Word Guards) │  │
 │  │  • ExperienceCalculator (Interval Merging + Relevance Gate)      │  │
 │  │  • EmbeddingEngine (BAAI/bge-small-en-v1.5 Chunk MaxSim)         │  │
 │  └───────────────────────────┬──────────────────────────────────────┘  │
 │                              │                                         │
 │  ┌───────────────────────────▼──────────────────────────────────────┐  │
 │  │ Calibrated 4-Pillar Scoring & Explainability Generator           │  │
 │  └──────────────────────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Modules & Functional Requirements

- **Module 1: Job Description Input**
  - Paste raw JD text or upload JD files.
  - Automatically extracts job title, required experience tenure ($Y_{req}$), core skills, and minimum academic degree.
- **Module 2: Resume Batch Upload**
  - Allows recruiters to upload **10+ candidate resumes in a single batch**.
  - Supports both **PDF and DOCX** formats.
  - Automatically parses candidate names, contact details, work history, and skills.
- **Module 3: AI Resume Matching Engine**
  - Compares candidate resumes against the JD.
  - Generates a **calibrated 0–100 composite matching score**.
  - Identifies matched skills and missing skill gaps.
  - Evaluates domain-relevant experience (preventing concurrent role double-counting).
  - Employs **semantic similarity** rather than naive keyword matching.
- **Module 4: Candidate Ranking Dashboard**
  - Interactive table displaying candidate rankings, experience, match percentage, and skill badges.
  - Real-time search by candidate name or skill.
  - Minimum match score threshold slider filter.
  - One-click CSV export of ranked candidates.
- **Module 5: Candidate-Level Deep Analysis**
  - Clicking any candidate row opens a slide-out inspection drawer.
  - Displays overall score gauge, 4-pillar score breakdown, skills gap matrix (matched vs missing), experience timeline, and deterministic AI rationale bullets with direct resume bullet citations.

---

## 3. The Matching Algorithm & Scoring Methodology

### The 4-Pillar Calibrated Formula
To prevent the common score-compression defect (where naive cosine similarity groups all scores between 72%–88%) and explicitly fulfill the requirement to evaluate experience, we compute an explainable, weighted composite score:

$$S_{\text{total}} = w_{\text{skills}} \cdot S_{\text{skills}} + w_{\text{exp}} \cdot S_{\text{exp}} + w_{\text{semantic}} \cdot S_{\text{semantic}} + w_{\text{qual}} \cdot S_{\text{qual}}$$

**Guaranteed Weight Distribution:**
- **Skills Match ($w_{\text{skills}} = 0.40$):** $40\%$ weight
- **Experience Relevance ($w_{\text{exp}} = 0.25$):** $25\%$ weight
- **Semantic MaxSim ($w_{\text{semantic}} = 0.25$):** $25\%$ weight
- **Education Qualifications ($w_{\text{qual}} = 0.10$):** $10\%$ weight

*(Weights strictly sum to $1.00$, verified by automated unit tests).*

---

### Chunk-Level MaxSim Semantic Matching
Standard dense embedding models (like `all-MiniLM-L6-v2` or `bge-small-en-v1.5`) truncate text at 256 or 512 tokens. Embedding an entire 3-page resume as a monolithic block causes massive context loss.

We solve this using **Chunk-Level Requirement MaxSim late interaction**:
1. We segment the JD into discrete requirement lines: $R_{JD} = [r_1, r_2, \dots, r_M]$.
2. We segment the candidate resume into experience bullet points and summary chunks: $C_{\text{cand}} = [c_1, c_2, \dots, c_K]$.
3. For each requirement line $r_i$, we identify its best-matching resume chunk:
   $$\text{BestMatch}(r_i) = \max_{c_j \in C_{\text{cand}}} \cos\left(\vec{e}(r_i), \vec{e}(c_j)\right)$$
4. The raw semantic score is the average of requirement satisfactions:
   $$S_{\text{semantic\_raw}} = \frac{1}{M} \sum_{i=1}^{M} \text{BestMatch}(r_i)$$
5. Scaled using empirical calibration bounds ($C_{\text{floor}} = 0.30$, $C_{\text{ceiling}} = 0.85$):
   $$S_{\text{semantic}} = \text{clamp}\left(\frac{S_{\text{semantic\_raw}} - 0.30}{0.85 - 0.30} \times 100, \, 0, \, 100\right)$$

This guarantees **zero truncation** of multi-page resumes and enables line-item citations showing exactly which resume bullet satisfied which JD requirement.

---

### Relevant Experience Algorithm (Interval Merging)
Summing raw date ranges causes false inflation due to:
1. Overlapping concurrent jobs (e.g. freelancing during full-time employment).
2. Counting completely irrelevant non-technical jobs (e.g. 3 years as a barista counted toward a backend engineer JD).

**Our Algorithmic Solution:**
1. **Date Normalization:** Regex extracts dates into absolute month indices (`year * 12 + month`), dynamically mapping `"Present"` to the current year/month.
2. **Relevance Gate:** A role is only counted as relevant if its title and description pass semantic similarity ($\ge 0.40$) against the JD domain or contain core technical keywords.
3. **Interval Merging:** Merges overlapping relevant intervals $[s_k, e_k]$ so concurrent roles are counted once.
4. **Scoring:**
   $$S_{\text{exp}} = \begin{cases} 
   100.0 & \text{if } Y_{\text{cand}} \ge Y_{\text{req}} \\
   \max\left(0.0, \, \frac{Y_{\text{cand}}}{Y_{\text{req}}} \times 100.0\right) & \text{if } Y_{\text{cand}} < Y_{\text{req}} 
   \end{cases}$$
   *(If the JD specifies no minimum experience, $S_{\text{exp}} = 100.0$ neutral with no penalty).*

---

### Guarded Fuzzy Matching & Short Skill Protection
Fuzzy matching on raw resume text causes disastrous false positives on short acronyms (e.g., matching "Go" inside "Going", or "C" inside "Company").

**Guard Architecture:**
- **Short Skill Protection ($\le 3$ characters, e.g. `C`, `R`, `Go`, `SQL`, `AWS`, `Git`):** STRICT word-boundary regex `\b{skill}\b`. Standalone single-letter languages (`C`, `R`) require nearby contextual tech clues.
- **Synonym & Alias Taxonomy:** 260+ curated canonical tech skills mapping variations (e.g., `Amazon Web Services` resolves `AWS`, `Amazon Web Services`, `Amazon AWS`).
- **Targeted Fuzzy Matching:** `RapidFuzz` token set ratio ($\ge 88\%$) is applied exclusively to candidate extracted phrases, never raw unsegmented text.

---

## 4. Empirical Benchmark & Validation Results

Tested against a benchmark suite of **12 synthetic candidate resumes** (8 PDFs, 4 DOCX, including two-column and table layouts) evaluated against a **Senior Backend Engineer (Python / FastAPI)** target JD:

```text
=================================================================
FINAL BENCHMARK EVALUATION SUMMARY
=================================================================
1. Skills Extraction Precision: 74.8%
2. Skills Extraction Recall:    81.5%
3. Skills Extraction F1-Score:  77.2%
4. Spearman Rank Correlation:   rho = 0.951 (p-value: 2.04e-06)
5. Average Processing Speed:    0.58s / resume on CPU
6. Peak System Memory:          667.1 MB RSS (Zero Docker overhead)
=================================================================
```

### Benchmark Ranking Table

| Rank | Candidate | Format | Layout | Score % | Relevant Exp | Matched Core Skills | Archetype Profile |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **#1** | Alex Morgan | PDF | Standard | **80.0%** | 8.5 yrs / 4.0 yrs | Python, FastAPI, Postgres, Docker, AWS, Git | Lead Backend Engineer (Exact match) |
| **#2** | David Kumar | PDF | 2-Column | **68.5%** | 6.6 yrs / 4.0 yrs | Python, FastAPI, Postgres, Docker, Git | Mid Backend Developer (Strong match) |
| **#3** | Sarah Chen | PDF | Standard | **67.5%** | 7.9 yrs / 4.0 yrs | Python, FastAPI, Postgres, Docker, Git, React | Senior Full-Stack Engineer |
| **#4** | Elena Rostova | PDF | Standard | **64.6%** | 6.9 yrs / 4.0 yrs | React, JavaScript, TypeScript, REST API, Git | Frontend Specialist (Partial match) |
| **#5** | Priya Sharma | DOCX | Standard | **62.8%** | 4.4 yrs / 4.0 yrs | Python, FastAPI, REST API, Git, Docker | Junior Python Developer (Under-tenured) |
| **#6** | Marcus Vance | DOCX | Standard | **62.7%** | 7.9 yrs / 4.0 yrs | AWS, Docker, Kubernetes, Python, Git | Cloud / DevOps Engineer (Adjacent) |
| **#7** | Brian O'Connor | PDF | Table | **61.4%** | 6.6 yrs / 4.0 yrs | Python, Postgres, SQL, Docker, Git | Data Engineer (Adjacent skills) |
| **#8** | James Wilson | PDF | Standard | **59.0%** | 9.5 yrs / 4.0 yrs | Java, Spring Boot, Docker, Git | Senior Java Developer (Stack mismatch) |
| **#9** | Lucas Scott | PDF | Standard | **58.1%** | 4.9 yrs / 4.0 yrs | Python, Selenium, pytest, CI/CD, Git | QA Automation Engineer (Role mismatch) |
| **#10**| Maya Lin | DOCX | Standard | **50.0%** | 3.6 yrs / 4.0 yrs | Python, Flask, HTML5, CSS3, Git | Bootcamp Graduate (Junior) |
| **#11**| Daniel Martinez| DOCX | Standard | **47.3%** | 5.4 yrs / 4.0 yrs | SQL, Pandas, Excel, Tableau | Business Intelligence Analyst |
| **#12**| Chloe Dubois | PDF | Standard | **22.4%** | 0.0 yrs / 4.0 yrs | Figma, CSS, Illustrator | Graphic / UI Designer (Total mismatch) |

---

## 5. Technology Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic V2
- **NLP & AI:**
  - `BAAI/bge-small-en-v1.5` via `sentence-transformers` (512-token window, 384 dimensions)
  - `RapidFuzz` (C++ optimized fuzzy matching)
  - NumPy & Scikit-learn
- **Document Parsers:** `pypdf` (PDF layout-aware) & `python-docx` (Word documents)
- **Frontend:** React 18, Vite, Lucide React, Modern CSS System

---

## 6. Installation & Quick Start

### 1. Prerequisites
- Python 3.11+ or 3.12+
- Node.js 18+ (tested on Node v22)

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/Krishna-Kilrofkansa/ai-resume-matcher.git
cd ai-resume-matcher

# Install backend dependencies
python -m pip install -r backend/requirements.txt

# Start the FastAPI backend server (runs on port 8000)
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
API documentation is available at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
# In a new terminal window
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 7. Running Automated Unit Tests & Benchmarks

Execute the automated test suite to verify scoring consistency and API endpoints:
```bash
python -m pytest backend/tests/ -v -o "pythonpath=backend"
```

To run the full benchmark evaluation against all 19 multi-page real-world resumes:
```bash
python scripts/evaluate_benchmark.py
```

To regenerate the end-to-end automated demo video:
```bash
python scripts/record_demo.py
```

---

## 8. Repository Structure

```text
ai-resume-matcher/
├── demo/
│   ├── ai_resume_matcher_demo.mp4   # 34s full HD recorded walkthrough
│   └── demo_preview.gif             # Lightweight animated demo preview
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI server & REST endpoints
│   │   ├── parsers/
│   │   │   ├── pdf_parser.py        # Layout-aware PDF extractor
│   │   │   └── docx_parser.py       # DOCX table & text extractor
│   │   ├── nlp/
│   │   │   ├── skills_matcher.py    # Guarded regex + RapidFuzz + taxonomy
│   │   │   ├── experience_calc.py   # Interval merging & relevance filter
│   │   │   └── embedding_engine.py  # bge-small-en-v1.5 chunk MaxSim
│   │   ├── matching/
│   │   │   ├── scoring.py           # 4-pillar composite calibrated score
│   │   │   └── pipeline.py          # End-to-end pipeline orchestrator
│   │   └── data/
│   │       ├── skills_taxonomy.json # 260+ canonical skills & alias map
│   │       ├── sample_jd.txt        # Senior Python/FastAPI test JD
│   │       ├── ground_truth.json    # Human evaluation annotations
│   │       ├── online_resumes/      # 19 real-world 1-3 page PDF resumes
│   │       └── test_resumes/        # 12 bundled PDF & DOCX test files
│   ├── tests/
│   │   ├── test_scoring_math.py     # Unit test: breakdown adds up to total
│   │   └── test_api_endpoints.py    # FastAPI TestClient endpoint tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Complete Recruiter Dashboard UI
│   │   ├── index.css                # Clean, modern design system
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── scripts/
│   ├── download_real_resumes.py     # Script to pull real multi-page resumes
│   ├── evaluate_benchmark.py        # Computes Spearman rho & F1 metrics
│   └── record_demo.py               # Automated headless demo video recorder
├── README.md                        # Documentation & Architecture
└── LICENSE                          # MIT License
```

---

## 9. Assignment Duration & Engineering Breakdown

The project was architected, implemented, evaluated, and documented over a **3-day sprint (~18 focused engineering hours)**:

| Phase | Duration | Scope & Key Accomplishments |
|---|---|---|
| **Phase 1: Architecture & Algorithm Design** | ~4 hours | Mathematical formulation of the calibrated 4-pillar scoring engine; design of the chunk-level requirement MaxSim late interaction model (`bge-small-en-v1.5`); design of the non-overlapping interval-merging experience algorithm. |
| **Phase 2: Backend & NLP Engine** | ~6 hours | Implementation of dual document parsers (`pypdf` layout-aware text & `python-docx` table reader); curation of the 260+ canonical skills taxonomy with alias mapping and word-boundary guards; empirical calibration constants ($C_{min}=0.25, C_{max}=0.85$); FastAPI REST endpoints with Pydantic V2 validation; automated unit test suite. |
| **Phase 3: Frontend & Recruiter Dashboard** | ~5 hours | Modern React 18 + Vite UI with Lucide React; Module 1 JD extractor with expandable criteria tags; Module 2 batch resume upload dropzone with per-file removal; Module 4 interactive candidate ranking table with live slider/search filtering and CSV export; Module 5 candidate deep inspection drawer with 4-pillar score breakdown, skill gap matrix, and text citations. |
| **Phase 4: Real-Resume Benchmarking & Video Demo** | ~3 hours | Compilation of 19 real-world 1–3 page resumes from open Kaggle/LiveCareer datasets; empirical benchmark evaluation yielding Spearman rank correlation $\rho = 0.951$, precision $74.8\%$, and recall $81.5\%$; creation of automated headless video recorder (`scripts/record_demo.py`) generating HD MP4 (`demo/ai_resume_matcher_demo.mp4`) and animated GIF (`demo/demo_preview.gif`). |

---

## 10. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
