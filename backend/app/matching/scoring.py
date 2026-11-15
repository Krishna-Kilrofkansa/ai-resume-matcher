import re
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


DEGREE_LEVELS = {
    "phd": 4, "doctorate": 4, "ph.d": 4,
    "master": 3, "m.s": 3, "ms": 3, "m.tech": 3, "msc": 3, "mba": 3,
    "bachelor": 2, "b.s": 2, "bs": 2, "b.tech": 2, "bsc": 2, "b.e": 2, "bba": 2,
    "diploma": 1, "associate": 1, "certificate": 1, "bootcamp": 1
}


class ScoreBreakdown(BaseModel):
    skills_score: float = Field(..., ge=0, le=100)
    experience_score: float = Field(..., ge=0, le=100)
    semantic_score: float = Field(..., ge=0, le=100)
    education_score: float = Field(..., ge=0, le=100)
    weights: Dict[str, float]


class CandidateEvaluation(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    breakdown: ScoreBreakdown
    metrics: Dict[str, Any]
    rationale: List[str]


class ScoringEngine:
    """
    4-Pillar Calibrated Composite Scoring Engine.
    Ensures mathematical consistency: S_total = sum(w_i * S_i).
    """

    DEFAULT_WEIGHTS = {
        "skills": 0.40,
        "experience": 0.25,
        "semantic": 0.25,
        "education": 0.10
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS
        # Validate weights sum to 1.0
        total_w = sum(self.weights.values())
        if abs(total_w - 1.0) > 1e-4:
            raise ValueError(f"Weights must sum to 1.0, got {total_w}")

    def score_education(
        self,
        candidate_degree_text: str,
        required_degree_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ordinal evaluation of educational qualifications.
        Scale: None (0) < Diploma/Cert (1) < Bachelor (2) < Master (3) < PhD (4).
        """
        cand_level = self._extract_degree_level(candidate_degree_text)

        if not required_degree_text or not required_degree_text.strip():
            return {
                "education_score": 100.0,
                "candidate_level": cand_level,
                "required_level": 0,
                "degree_matched": True,
                "rationale": "No specific minimum degree required by JD (100% awarded)."
            }

        req_level = self._extract_degree_level(required_degree_text)

        if cand_level >= req_level:
            score = 100.0
            degree_matched = True
            rationale = "Candidate meets or exceeds required educational level."
        elif cand_level == req_level - 1:
            score = 75.0
            degree_matched = False
            rationale = "Candidate is 1 academic tier below preferred requirement (e.g. Bachelor's vs Master's)."
        else:
            score = 50.0
            degree_matched = False
            rationale = "Candidate qualifications do not fulfill preferred technical degree requirements."

        return {
            "education_score": score,
            "candidate_level": cand_level,
            "required_level": req_level,
            "degree_matched": degree_matched,
            "rationale": rationale
        }

    def _extract_degree_level(self, text: str) -> int:
        if not text:
            return 0
        text_lower = text.lower()
        max_level = 0
        for kw, lvl in DEGREE_LEVELS.items():
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                if lvl > max_level:
                    max_level = lvl
        return max_level

    def compute_composite_score(
        self,
        skills_score: float,
        experience_score: float,
        semantic_score: float,
        education_score: float,
        metrics: Dict[str, Any]
    ) -> CandidateEvaluation:
        """
        Computes mathematically guaranteed composite score and generates explainability rationale.
        """
        w_skills = self.weights["skills"]
        w_exp = self.weights["experience"]
        w_sem = self.weights["semantic"]
        w_edu = self.weights["education"]

        # Exact linear combination
        raw_total = (
            w_skills * skills_score +
            w_exp * experience_score +
            w_sem * semantic_score +
            w_edu * education_score
        )
        overall_score = round(max(0.0, min(100.0, raw_total)), 1)

        breakdown = ScoreBreakdown(
            skills_score=round(skills_score, 1),
            experience_score=round(experience_score, 1),
            semantic_score=round(semantic_score, 1),
            education_score=round(education_score, 1),
            weights=self.weights
        )

        rationale = self._generate_rationale(
            overall_score,
            breakdown,
            metrics
        )

        return CandidateEvaluation(
            overall_score=overall_score,
            breakdown=breakdown,
            metrics=metrics,
            rationale=rationale
        )

    def _generate_rationale(
        self,
        overall_score: float,
        breakdown: ScoreBreakdown,
        metrics: Dict[str, Any]
    ) -> List[str]:
        """Generates clear, deterministic explanatory bullets for Module 5."""
        bullets = []

        # 1. Overall assessment
        if overall_score >= 85:
            bullets.append(f"Strong overall match ({overall_score}%) with comprehensive coverage of core role responsibilities.")
        elif overall_score >= 70:
            bullets.append(f"Solid match ({overall_score}%) with high potential; minor skill or experience gaps identified.")
        elif overall_score >= 50:
            bullets.append(f"Moderate match ({overall_score}%); partially qualified with notable differences in core technical stack.")
        else:
            bullets.append(f"Low match ({overall_score}%); background does not align with primary job requirements.")

        # 2. Skills rationale
        matched_req = metrics.get("matched_required", [])
        missing_req = metrics.get("missing_required", [])
        total_req_count = len(matched_req) + len(missing_req)
        if total_req_count > 0:
            pct = int(len(matched_req) / total_req_count * 100)
            bullets.append(
                f"Skills: Matched {len(matched_req)} of {total_req_count} required skills ({pct}% coverage). "
                f"Key matches: {', '.join(matched_req[:4]) if matched_req else 'None'}."
            )
        if missing_req:
            bullets.append(f"Skill Gaps: Missing core requirements: {', '.join(missing_req[:4])}.")

        # 3. Experience rationale
        cand_exp = metrics.get("relevant_years", 0.0)
        req_exp = metrics.get("required_years")
        if req_exp is not None:
            if cand_exp >= req_exp:
                bullets.append(f"Experience: Exceeds target tenure ({cand_exp} yrs evaluated vs {req_exp} yrs required).")
            else:
                bullets.append(f"Experience: Below target tenure ({cand_exp} yrs evaluated vs {req_exp} yrs required).")
        else:
            bullets.append(f"Experience: Candidate has {cand_exp} years of evaluated relevant experience.")

        # 4. Semantic alignment
        sem_sim = metrics.get("raw_semantic_similarity", 0.0)
        bullets.append(f"Semantic Alignment: {breakdown.semantic_score}% calibrated alignment based on direct resume bullet citations.")

        return bullets
