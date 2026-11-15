# Google XYZ Formula — Deep Dive

The XYZ formula is Google's internal framework for writing resume bullet points. It ensures every bullet communicates **impact, evidence, and method**.

---

## The Formula

> **"Accomplished [X] as measured by [Y] by doing [Z]"**

| Component | What it is | Why it matters |
|-----------|-----------|---------------|
| **X** — Accomplishment | The outcome or result you achieved | Shows what changed because of you |
| **Y** — Metric | The number that proves it (%, $, users, time) | Makes the claim credible and concrete |
| **Z** — Method | The specific action or approach you used | Shows HOW you did it (your skills in action) |

---

## Examples by Experience Level

### Entry Level / Intern

**Before (weak):**
```
- Helped the team with testing and bug fixes
```

**After (XYZ):**
```
- Reduced regression bug rate by 35% (X+Y) by building an automated test suite
  covering 200+ edge cases using Jest and Cypress (Z)
```

---

### Mid-Level (3-7 years)

**Before (weak):**
```
- Worked on improving the search functionality
```

**After (XYZ):**
```
- Improved search relevance by 28% and reduced P95 latency from 800ms to 200ms (X+Y)
  by redesigning the Elasticsearch indexing pipeline with custom analyzers and
  query-time boosting (Z)
```

---

### Senior Level (8+ years)

**Before (weak):**
```
- Led a team to migrate the platform to microservices
```

**After (XYZ):**
```
- Led 8-engineer team to decompose monolith into 12 microservices, reducing
  deployment time from 4 hours to 15 minutes and achieving 99.97% uptime (X+Y)
  by designing event-driven architecture with Kafka, implementing circuit breakers,
  and establishing SLO-driven monitoring (Z)
```

---

### Non-Engineering Roles

**Product Manager:**
```
- Grew monthly active users by 140% (from 50K to 120K) in 6 months (X+Y)
  by launching a referral program with tiered rewards and A/B testing
  3 onboarding flows to optimize activation (Z)
```

**Data Analyst:**
```
- Identified $2.3M in annual cost savings across 3 business units (X+Y)
  by building an automated spend analysis dashboard in Looker with
  anomaly detection on vendor invoices (Z)
```

**Marketing:**
```
- Increased qualified lead generation by 65% quarter-over-quarter (X+Y)
  by redesigning the content funnel with SEO-optimized landing pages
  and implementing lead scoring with HubSpot workflows (Z)
```

---

## Power Verbs by Category

### Building & Creating
Architected, Built, Created, Designed, Developed, Engineered, Implemented, Launched

### Leading & Driving
Championed, Directed, Drove, Founded, Led, Managed, Orchestrated, Spearheaded

### Improving & Optimizing
Accelerated, Enhanced, Improved, Optimized, Reduced, Refined, Revamped, Streamlined

### Analyzing & Solving
Analyzed, Debugged, Diagnosed, Identified, Investigated, Resolved, Troubleshot, Uncovered

### Growing & Scaling
Expanded, Generated, Grew, Increased, Multiplied, Scaled, Strengthened, Tripled

### Automating & Innovating
Automated, Modernized, Pioneered, Prototyped, Revolutionized, Standardized, Transformed

---

## Common Mistakes

### ❌ Missing the Metric (Y)

```
Bad:  "Improved system performance by optimizing database queries"
Good: "Improved system performance by 3x, reducing API response time
       from 1.2s to 400ms, by optimizing 15 critical database queries
       with composite indexes and query plan analysis"
```

### ❌ Missing the Method (Z)

```
Bad:  "Reduced customer churn by 20%"
Good: "Reduced customer churn by 20% ($500K ARR saved) by building a
       predictive model using XGBoost on usage patterns and triggering
       automated re-engagement campaigns for at-risk accounts"
```

### ❌ Leading with the Task, Not the Impact (X)

```
Bad:  "Responsible for maintaining the CI/CD pipeline"
Good: "Cut deployment failures by 60% and reduced release cycle from
       2 weeks to daily by redesigning the CI/CD pipeline with
       GitHub Actions, Docker multi-stage builds, and canary deployments"
```

### ❌ Combining Multiple Achievements

```
Bad:  "Built the payment system, mentored 3 junior devs, and reduced
       infrastructure costs"
Good: Split into 3 separate bullets, each with its own XYZ.
```

---

## When You Don't Have Exact Numbers

Use these strategies to still quantify:

| Strategy | Example |
|----------|---------|
| **Ranges** | "Reduced load time by 30–40%" |
| **Multipliers** | "Improved throughput by ~3x" |
| **Before → After** | "From 5-minute deploys to under 30 seconds" |
| **Scale indicators** | "For a platform serving 500K+ monthly users" |
| **Team/scope** | "Across a team of 12 engineers" |
| **Frequency** | "Processing 10K+ transactions daily" |
| **Placeholder** | "Reduced costs by [X]% — ask user for exact figure" |

> **Rule**: An approximate number is always better than no number. "~30%" beats "significantly improved".

---

## XYZ Checklist

For every bullet you write, verify:

- [ ] Starts with a strong action verb (not "Responsible for", "Helped", "Worked on")
- [ ] Contains at least one quantified metric
- [ ] Specifies the method or technology used
- [ ] Fits on 1–2 lines maximum
- [ ] Describes a single achievement (not a compound sentence)
- [ ] Would make sense to someone outside your company
- [ ] Shows YOUR contribution, not your team's
