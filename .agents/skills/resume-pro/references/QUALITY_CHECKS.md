# Quality Gates — Detailed Rules & Examples

This document contains the full rule set, edge cases, and examples for each of the 5 Quality Gates that run before every Resume Pro module.

---

## Gate 1 — Repetition Detection

### What to Scan

| Type | Example (Bad) | Fix |
|------|--------------|-----|
| Exact duplicate | "Developed REST APIs" appears in Role A and Role B | Keep in the most impactful role; rephrase the other |
| Semantic duplicate | "Built CI/CD pipelines" + "Set up continuous integration" | Merge into one bullet with combined impact |
| Verb repetition | 5 bullets starting with "Developed" | Rotate verbs: Engineered, Architected, Built, Designed, Implemented |
| Phrase echoing | "Responsible for managing…" × 3 | Replace with action verbs: Led, Directed, Oversaw |
| Redundant skill listing | "Python" in Skills AND "Proficient in Python" in summary | Keep in Skills section only; let bullets demonstrate proficiency |

### Severity Levels

- 🔴 **Critical**: Exact duplicate bullets (shows carelessness)
- 🟡 **Warning**: Semantic duplicates or 3+ verb repetitions
- 🟢 **Info**: Minor phrase echoing (2 instances)

### Edge Cases

- **Promotion within same company**: It's okay to reference the same project if the scope changed — but the bullets must show progression (e.g. "Contributed to" → "Led")
- **Skills in context**: Mentioning a skill in a bullet ("Built microservices in Go") is NOT a duplicate of listing "Go" in the Skills section — that's expected and good

---

## Gate 2 — Date Consistency

### Accepted Formats (pick ONE and use everywhere)

| Format | Example |
|--------|---------|
| `Mon YYYY` | Jan 2023 – Present |
| `Month YYYY` | January 2023 – Present |
| `MM/YYYY` | 01/2023 – Present |
| `YYYY` (education only) | 2019 – 2023 |

### Rules

1. **All dates must use the same format** — mixing "Jan 2023" and "01/2023" is a 🟡 warning
2. **Reverse chronological order is mandatory** for Work Experience
3. **Gaps > 3 months** get flagged with a prompt: "Consider adding context (freelance, education, travel)"
4. **Overlapping dates** get flagged unless the resume explicitly labels one as "Part-time" or "Freelance"
5. **Future end dates** are only acceptable as "Present" or "Current"
6. **Very short roles (< 3 months)** get flagged: "Consider listing as a project or contract instead"

### Common Mistakes

```
❌  "2023 Jan - 2024 Feb"        → ✅  "Jan 2023 – Feb 2024"
❌  "Jan 2023 - present"         → ✅  "Jan 2023 – Present"
❌  Mixed: "Jan 2023" + "2023-03"→ ✅  Pick one format
❌  "2024 - 2023" (reversed)     → ✅  "2023 – 2024"
```

### Timeline Table Format

```
Role / Entry              | Start      | End        | Duration | Issues
Senior Eng, Company A     | Jan 2023   | Present    | 1y 6m   | ✅
Backend Eng, Company B    | Mar 2021   | Dec 2022   | 1y 9m   | ✅
Intern, Company C         | Jun 2020   | Aug 2020   | 3m      | 🟡 Short
[GAP]                     | Sep 2020   | Feb 2021   | 6m      | 🔴 Unexplained
```

---

## Gate 3 — Length & Depth Analysis

### Page Length Guidelines

| Experience Level | Ideal Length | Maximum |
|-----------------|-------------|---------|
| Student / Entry (0–2 yrs) | 1 page | 1 page |
| Mid-level (3–7 yrs) | 1 page | 1.5 pages |
| Senior (8–15 yrs) | 1–2 pages | 2 pages |
| Executive (15+ yrs) | 2 pages | 3 pages |

### Section Balance Targets

```
Experience:    50–65% of total space
Skills:        10–15%
Education:     10–15%
Summary:        5–10%
Projects:       5–15% (higher for students)
Awards/Certs:   0–5%
```

### Bullet Count Rules

| Situation | Ideal Bullets | Flag |
|-----------|:------------:|------|
| Current role | 4–6 | 🟡 if < 3 or > 8 |
| Previous role (< 2 years) | 3–4 | 🟡 if < 2 or > 6 |
| Previous role (2+ years) | 4–6 | 🟡 if < 3 or > 8 |
| Internship | 2–3 | 🟡 if > 4 |
| Very old role (5+ yrs ago) | 2–3 | 🟡 if > 4 |

### Depth Signals

**Too shallow** (🟡):
```
- Worked on backend systems
- Used Python and SQL
- Collaborated with team
```
*Fix: Add scope, metrics, and specific technologies*

**Too deep** (🟡):
```
- Architected and implemented a distributed event-driven microservices
  platform using Apache Kafka for real-time data streaming, PostgreSQL
  with read replicas for data persistence, Redis Cluster for caching
  with TTL-based eviction policies, and Kubernetes with Helm charts for
  container orchestration across 3 availability zones, reducing...
```
*Fix: Split into 2 focused bullets or cut the technology list*

**Just right** (🟢):
```
- Architected event-driven microservices platform (Kafka, PostgreSQL, Redis)
  serving 2M daily events with 99.95% uptime across 3 availability zones
```

---

## Gate 4 — Spelling & Consistency Check

### Technology Name Spelling (Common Mistakes)

| Wrong | Correct |
|-------|---------|
| Javascript, java script | JavaScript |
| Typescript | TypeScript |
| Github, GITHUB | GitHub |
| Mongodb | MongoDB |
| Postgresql, postgre | PostgreSQL |
| NodeJs, node.js | Node.js |
| React.js, react | React (or React.js — pick one) |
| MySql, MYSQL | MySQL |
| Aws, aws | AWS |
| Api, api | API |
| Ci/cd, CI/CD, CICD | CI/CD |
| Graphql | GraphQL |
| Kubernetes, K8 | Kubernetes (k8s as abbreviation) |
| Docker, docker | Docker |
| Tensorflow | TensorFlow |
| Pytorch | PyTorch |

### Consistency Rules

1. **Tense**:
   - Current role → present tense ("Lead", "Drive", "Build")
   - Previous roles → past tense ("Led", "Drove", "Built")
   - NEVER mix within the same role

2. **Punctuation at end of bullets**:
   - Pick one: all bullets end with a period, or none do
   - Mixed periods = 🟡 flag

3. **Capitalization of titles**:
   - Job titles: Title Case ("Senior Software Engineer") — consistent throughout
   - Company names: As officially styled ("McDonald's" not "Mcdonalds")

4. **Number formatting**:
   - Use numerals for metrics: "Reduced latency by 40%" not "forty percent"
   - Use numerals for team sizes: "team of 5" not "team of five"
   - Exception: "one" at the start of a sentence

5. **Abbreviation rules**:
   - First use: spell out with abbreviation in parentheses: "Machine Learning (ML)"
   - Subsequent uses: abbreviation only: "ML"
   - Exception: universally known abbreviations (API, AWS, SQL) don't need expansion

### Spell Check Approach

1. Run standard dictionary check
2. Cross-reference technology names against the table above
3. Verify company names against known entities
4. Flag any word that appears only once and looks like a typo (e.g. "managment", "developped")

---

## Gate 5 — Summary Evaluation

### Anatomy of a Strong Summary

```
[Who you are] + [Years of experience] + [Core expertise] + [Standout achievement] + [What you're looking for]
```

**Example (🟢 Strong):**
```
Senior Backend Engineer with 6+ years of experience building high-throughput
distributed systems at scale. Architected event-driven platforms processing
2M+ daily transactions at 99.95% uptime. Seeking a Staff Engineer role at
a mission-driven company where I can lead platform-level technical decisions.
```

**Example (🔴 Weak):**
```
Hardworking and motivated software engineer looking for new opportunities.
I have experience with many technologies and enjoy solving problems.
```

### Scoring Rubric (out of 10)

| Score | Criteria |
|:-----:|----------|
| 9–10 | Specific, quantified, role-targeted, compelling opening line |
| 7–8 | Good content but missing one element (metric, target role, or specificity) |
| 5–6 | Generic but structurally sound; needs tailoring |
| 3–4 | Vague, uses filler phrases, no metrics |
| 1–2 | Missing, one line, or actively harmful (clichés, desperate tone) |

### Red Flag Phrases (auto-flag)

These phrases should be rewritten or removed:

- "I am writing to express my interest…"
- "Hardworking and motivated"
- "Team player with excellent communication skills"
- "Looking for a challenging opportunity"
- "Passionate about technology" (without specifics)
- "Detail-oriented professional"
- "Results-driven individual"
- "Seeking to leverage my skills"

### Required Elements Checklist

- [ ] States years of experience (number, not vague)
- [ ] Names core technical domain or expertise area
- [ ] Includes at least one quantified achievement
- [ ] Mentions target role or career direction
- [ ] Is 2–4 lines (not too short, not too long)
- [ ] Uses confident, specific language
- [ ] Contains 3–5 ATS-relevant keywords
