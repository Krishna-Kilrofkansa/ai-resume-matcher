import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model"] == "BAAI/bge-small-en-v1.5"


def test_job_description_extract():
    jd_sample = """Title: Senior Python Engineer
Experience Required: 4+ years
Requirements:
- Strong skills in Python and FastAPI
- Hands-on experience with PostgreSQL and Docker
- Knowledge of Amazon Web Services (AWS)
"""
    response = client.post("/api/v1/jobs/extract", json={"jd_text": jd_sample})
    assert response.status_code == 200
    data = response.json()
    assert data["required_years"] == 4.0
    assert "Python" in data["skills"]
    assert "FastAPI" in data["skills"]
    assert "PostgreSQL" in data["skills"]


def test_batch_match_and_rankings():
    # Use 3 sample test files for fast endpoint validation
    test_dir = os.path.join(os.path.dirname(__file__), "..", "app", "data", "test_resumes")
    files_to_test = ["Alex_Morgan_Resume.pdf", "Sarah_Chen_Resume.pdf", "Marcus_Vance_Resume.docx"]

    jd_sample = """Title: Senior Python Engineer
Experience Required: 4+ years
Requirements:
- Strong skills in Python and FastAPI
- Hands-on experience with PostgreSQL and Docker
- Knowledge of Amazon Web Services (AWS)
"""
    files_payload = []
    opened_files = []
    for fn in files_to_test:
        path = os.path.join(test_dir, fn)
        f = open(path, "rb")
        opened_files.append(f)
        mime = "application/pdf" if fn.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        files_payload.append(("files", (fn, f, mime)))

    try:
        response = client.post(
            "/api/v1/resumes/batch-match",
            data={"jd_text": jd_sample},
            files=files_payload
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_processed"] == 3
        rankings = data["rankings"]
        assert len(rankings) == 3
        assert rankings[0]["rank"] == 1
        assert rankings[0]["overall_score"] >= rankings[1]["overall_score"]

        # Test candidate drill-down (Module 5)
        resp_cand = client.get("/api/v1/candidates/1")
        assert resp_cand.status_code == 200
        cand_data = resp_cand.json()
        assert cand_data["rank"] == 1
        assert "breakdown" in cand_data
        assert "rationale" in cand_data
        assert len(cand_data["rationale"]) > 0

    finally:
        for f in opened_files:
            f.close()
