import pytest
from app.matching.scoring import ScoringEngine, ScoreBreakdown


def test_scoring_weights_sum_to_one():
    engine = ScoringEngine()
    total_w = sum(engine.weights.values())
    assert abs(total_w - 1.0) < 1e-4, f"Weights must sum to 1.0, got {total_w}"


def test_composite_score_mathematical_consistency():
    """
    Asserts that overall_score ALWAYS equals the weighted sum of its pillars.
    Guarantees no discrepancy like the one identified in Fix 1.
    """
    engine = ScoringEngine()
    test_cases = [
        # (skills, exp, semantic, edu)
        (90.0, 100.0, 78.0, 100.0),
        (71.4, 80.0, 65.0, 100.0),
        (100.0, 100.0, 100.0, 100.0),
        (0.0, 0.0, 0.0, 0.0),
        (45.5, 60.0, 52.3, 75.0),
        (85.0, 25.0, 90.0, 50.0)
    ]

    for s_skills, s_exp, s_sem, s_edu in test_cases:
        expected_raw = 0.40 * s_skills + 0.25 * s_exp + 0.25 * s_sem + 0.10 * s_edu
        expected_score = round(max(0.0, min(100.0, expected_raw)), 1)

        result = engine.compute_composite_score(
            skills_score=s_skills,
            experience_score=s_exp,
            semantic_score=s_sem,
            education_score=s_edu,
            metrics={"matched_required": ["Python"], "missing_required": []}
        )

        assert result.overall_score == pytest.approx(expected_score, abs=0.01), (
            f"Math mismatch: expected {expected_score}, got {result.overall_score} "
            f"for inputs ({s_skills}, {s_exp}, {s_sem}, {s_edu})"
        )


def test_skills_coverage_calculation():
    from app.nlp.skills_matcher import SkillsMatcher
    matcher = SkillsMatcher()

    # If 5 of 7 required skills matched with 0 preferred
    res = matcher.compare_skills(
        required_skills=["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API", "Git"],
        preferred_skills=[],
        candidate_skills=["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"]
    )

    # 5/7 = 71.4%
    assert res["skills_score"] == 71.4
    assert len(res["matched_required"]) == 5
    assert len(res["missing_required"]) == 2
