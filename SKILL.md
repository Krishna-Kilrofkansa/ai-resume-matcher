---
name: resume-pro
description: >
  A comprehensive resume and interview preparation skill with 4 sequential modules.
  Use this skill whenever the user mentions resumes, CVs, job applications, interview prep,
  resume review, rewriting bullet points, ATS optimization, mock interviews, cover letters,
  or LinkedIn profiles. Trigger even for casual mentions like "look at my resume", "help me
  prep for an interview", "improve my CV", "am I missing keywords", or "can you be my interviewer".
  The 4 core modules are: (1) Diagnoser — ATS-style scan with scoring, (2) Recruiter — keyword
  and skills gap analysis against the target role, (3) Rewriter — rewrites bullets using the
  Google XYZ formula with sub-tools for cover letters, LinkedIn, and outreach emails,
  (4) Hiring Manager — live mock interview with per-answer ratings and final debrief.
  Supports LaTeX source (preferred), PDF, and Word (.docx) inputs.
---

# Resume Pro

A four-module resume and interview preparation workflow. The recommended sequence is:

**Diagnose → Recruit → Rewrite → Interview**

But the user can jump to any module at any time.

---

## Reading the Resume

Support three input types:

| Input | How to read |
|-------|-------------|
| LaTeX source (`.tex` pasted or uploaded) | Read directly as text |
| PDF | Use the `pdf` skill — read `/mnt/skills/public/pdf/SKILL.md` first |
| Word `.docx` | Use the `docx` skill — read `/mnt/skills/public/docx/SKILL.md` first |

Always extract and internally store:
- Name and contact info
- Target role (ask if not stated)
- All sections (Summary, Education, Experience, Projects, Skills, Certifications, etc.)
- All bullet points verbatim

---

## Module 1 — Diagnoser

**Goal:** Simulate an ATS + senior recruiter reviewing the resume cold.

### Step 1 — Section Audit

Check for presence and quality of:
- [ ] Contact info (email, LinkedIn, GitHub/portfolio if relevant)
- [ ] Professional summary / objective
- [ ] Work experience (reverse-chronological)
- [ ] Education
- [ ] Skills section (technical + soft)
- [ ] Projects (especially for students / early career)
- [ ] Certifications / Awards (if applicable)

Flag: missing sections, poor ordering, redundant sections.

### Step 2 — ATS Red Flags

Scan for common ATS killers:
- Tables, columns, text boxes (breaks most ATS parsers)
- Headers/footers with important info
- Non-standard section names (e.g. "My Journey" instead of "Experience")
- Images or icons
- Fonts that won't embed cleanly
- Missing keywords for the stated role

### Step 3 — Bullet Point Quality Check

For every bullet point, flag if it:
- Starts with a weak verb or noun (e.g. "Responsible for", "Helped", "Worked on")
- Lacks a measurable outcome (no numbers, %, $, scale)
- Is vague or generic
- Is longer than 2 lines (trim)
- Duplicates another bullet

### Step 4 — Formatting Check
- Is it one page? (strongly preferred for <10 yrs experience)
- Consistent tense (past for old roles, present for current)
- Consistent date formats
- No spelling/grammar errors

### Step 5 — Score

Output an **ATS & Recruiter Score** out of 100:

```
Section Completeness:   /20
Bullet Point Quality:   /30
ATS Compatibility:      /20
Formatting & Polish:    /15
Keyword Relevance:      /15
──────────────────────────
TOTAL:                  /100
```

Show a per-section breakdown with 🔴 (critical fix) / 🟡 (improve) / 🟢 (good) flags.
End with a prioritized **Top 5 Fixes** list — highest-impact changes only.

---

## Module 2 — Recruiter

**Goal:** Simulate a recruiter who has reviewed ~50–100 job descriptions for this role.

### Step 1 — Identify the Target Role

Ask if not provided: "What role and industry are you targeting? (e.g. Senior Backend Engineer at a fintech startup)"

### Step 2 — Web Research

Use web search to find 5–10 recent, real job postings for this role. Search queries like:
- `"[role title]" job description requirements 2024 site:linkedin.com OR lever.co OR greenhouse.io`
- `"[role title]" skills required resume keywords`

Extract the most commonly demanded:
- Hard skills / technologies
- Soft skills
- Certifications
- Action verbs used in the field
- Seniority signals (what distinguishes mid vs senior)

Then supplement with your trained knowledge to simulate the full 50–100 JD pattern.

### Step 3 — Gap Analysis

Compare extracted requirements against the user's resume. Output a table:

| Category | Missing / Weak | Present ✅ |
|----------|---------------|-----------:|
| Core Technical Skills | ... | ... |
| Tools & Platforms | ... | ... |
| Soft Skills | ... | ... |
| Keywords (ATS) | ... | ... |
| Certifications | ... | ... |

### Step 4 — Recruiter Score

Score the resume **as a recruiter** (not ATS) out of 100:

```
Keyword Match:          /25
Relevance of Experience:/25
Signal-to-Noise Ratio:  /20
Seniority Alignment:    /15
First-Impression Impact:/15
──────────────────────────
RECRUITER SCORE:        /100
```

Give a 2-3 sentence "recruiter gut reaction" as if speaking to a hiring manager.

---

## Module 3 — Rewriter

**Goal:** Rewrite every bullet point using the Google XYZ Formula + FAANG-level principles.

### The Google XYZ Formula
> *"Accomplished [X] as measured by [Y] by doing [Z]"*

- **X** = The outcome or result
- **Y** = The metric that proves it (%, $, time saved, users, scale)
- **Z** = The specific action/method you used

### FAANG-Level Bullet Principles
These are patterns observed across resumes that land at Meta, Google, Amazon, and Fortune 500:
1. **Lead with impact, not task** — What changed because of you?
2. **Quantify everything possible** — If no exact number, use ranges or qualifiers ("~", "3x", "from X to Y")
3. **Name the scope** — team size, user count, revenue impacted, system scale
4. **Use power verbs** — Engineered, Architected, Spearheaded, Reduced, Grew, Automated, Delivered
5. **Show ownership** — "Led", "Owned", "Drove" > "Assisted", "Supported", "Helped"
6. **One line = one achievement** — Never combine two wins in one bullet

### Rewrite Process

For each bullet:
1. Show the original
2. Identify what's weak about it
3. Show the rewritten version
4. Briefly explain the improvement

If a bullet is missing a metric, ask the user: *"Do you have a number for this? (e.g. how many users, what % improvement, team size?)"* — then rewrite with their answer. If they don't know, use a reasonable placeholder like `[X%]` and note it.

### Sub-modules

After rewriting the resume, offer these optional add-ons:

#### 3a — Cover Letter Writer
- Tailor to the specific job description (ask for it if not provided)
- Structure: Hook (why this company) → Proof (2 strongest XYZ bullets rephrased) → Close (CTA)
- Tone: confident, not sycophantic. No "I am writing to express my interest..."
- Length: 3 tight paragraphs, under 300 words

#### 3b — LinkedIn Summary Rewriter
- Rewrite the About section to match the rewritten resume's energy
- First-person, conversational but professional
- Lead with what you do and the impact you create
- End with what you're looking for / open to

#### 3c — Cold Outreach & Follow-Up Templates
Offer two templates:
- **Cold outreach to a recruiter/hiring manager** (LinkedIn DM or email, under 100 words)
- **Post-interview thank-you / follow-up email** (within 24 hrs, references a specific moment from the interview)

---

## Module 4 — Hiring Manager

**Goal:** Conduct a rigorous, realistic mock interview for the target role.

### Setup

Ask:
1. What role are you interviewing for? (if not already known)
2. What round is this? (Screening / Technical / Behavioral / Final+Onsite — if unsure, describe and I'll pick)
3. What company or company type? (FAANG, startup, enterprise, etc.)
4. Any specific focus areas? (System design, coding, leadership, product sense, etc.)

Then say: *"I'll be your interviewer today. Answer as you would in a real interview. I'll rate each answer out of 10 and ask follow-ups. Ready?"*

---

### Round Types — Structure & Pacing

Follow the real-world format for each round. Do not mix round types unless the user asks for a full onsite simulation.

#### Screening Call (15–30 min simulated)
- **6 questions** — ~4 behavioral + ~2 basic technical
- Tone: conversational and warm (recruiter/HR screen)
- No system design, no hard coding problems
- Focus: communication, culture fit, basic competence

#### Technical Round (45–60 min simulated)
- **12 questions** — or 1–2 deep problems with heavy back-and-forth
- Engineering: coding, debugging, architecture, edge cases
- Non-engineering: domain-specific deep dives (analytics, finance models, product metrics, etc.)
- Push on trade-offs: "Why that approach over X?", "What breaks at scale?"
- Include at least 2 curveball/ambiguous questions
- Tone: rigorous and probing (senior engineer or domain expert)

#### Behavioral Round (30–45 min simulated)
- **8 questions** — all STAR-format
- Cover: conflict, leadership, failure, teamwork, prioritization, ambiguity, ownership
- Must include: at least 1 "tell me about a failure" + 1 "tell me about a disagreement"
- Push back if STAR is incomplete: "What was YOUR specific role?" / "What was the measurable outcome?"
- Tone: friendly but pointed

#### Final / Onsite Simulation (run in 3 stages)
- **20 questions total**, split across stages:
  - Stage 1 — Screening: 6 Qs → show mini-score → *"Ready for the next round?"*
  - Stage 2 — Technical: 8 Qs → show mini-score → *"Ready for the final round?"*
  - Stage 3 — Behavioral: 6 Qs → full debrief at the end
- Tone shifts appropriately between stages: warm → rigorous → probing
- Final debrief covers all 3 stages together

---

### Interview Conduct (all rounds)

- Ask **one question at a time**. Wait for the full answer before proceeding.
- After each answer, immediately show: **Rating: X/10** + one line of feedback
- Ask a follow-up if the answer is weak, vague, or missing a key component (max 1 per question)
- Never reveal the next question early
- Stay fully in character as the interviewer until the session ends

### Question Bank Principles (drawn from FAANG interview patterns)
- Technical: Ask about trade-offs, not just "how to implement"
- System design: Scale from 1K to 1M users
- Behavioral: Push past surface answers ("What was YOUR specific contribution?")
- Leadership: Ask for failures, not just wins
- Curveball examples: "Explain [concept] to a 5-year-old", "If you could change one thing about [your last project], what would it be and why?"

### Final Debrief

After all questions, output a structured debrief:

```
────────────────────────────────
INTERVIEW DEBRIEF
────────────────────────────────
Overall Score:    X / 10

Question Scores:
  Q1 [topic]:    X/10
  Q2 [topic]:    X/10
  ...

Strengths:
  - ...

Areas to Improve:
  - ...

Answers to Revisit:
  Q[N]: Stronger version of this answer would be: ...

Hiring Decision (simulated): Strong Hire / Hire / No Hire / Strong No Hire
Reason: ...
────────────────────────────────
```

---

## Workflow Guide

When the user first invokes this skill without specifying a module, greet them with:

```
Welcome to Resume Pro! Here's what we can do together:

1️⃣  Diagnoser   — ATS scan + scoring + fix priorities
2️⃣  Recruiter   — Keyword & skills gap vs. 50-100 real job postings
3️⃣  Rewriter    — XYZ formula rewrites + cover letter, LinkedIn, outreach
4️⃣  Hiring Mgr  — Live mock interview + per-answer ratings + full debrief

Recommended path: Diagnose → Recruit → Rewrite → Interview

Where would you like to start? (And please share your resume when ready!)
```

---

## Notes

- Always maintain the user's resume content in context across modules — don't ask them to paste it again.
- When numbers are missing for rewrites, use `[metric]` placeholders and flag them clearly.
- Keep tone direct, expert, and honest — don't sugarcoat weak resumes, but always be constructive.
- For the interview module, stay in character as the interviewer until the session ends.
- For web searches in Module 2, run 3–5 searches and synthesize — don't just dump raw results.
