import os
import sys
import shutil
import tempfile
from typing import List, Optional

# Ensure the backend directory is in sys.path regardless of execution working directory
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.matching.pipeline import MatchingPipeline

app = FastAPI(
    title="AI-Based Resume Matching & Ranking Engine",
    description="High-precision candidate resume ranking and qualification analysis engine optimized for CPU inference.",
    version="1.0.0"
)

# Enable CORS for local React/Vite development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = MatchingPipeline()

# In-memory session cache for latest batch evaluation
LATEST_SESSION = {
    "jd_profile": None,
    "rankings": []
}


class JDExtractRequest(BaseModel):
    jd_text: str


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Resume Matcher API",
        "model": "BAAI/bge-small-en-v1.5",
        "version": "1.0.0"
    }


@app.post("/api/v1/jobs/extract")
def extract_job_description(payload: JDExtractRequest):
    """
    Module 1: Extract requirements, skills, experience, and degree from JD text.
    """
    if not payload.jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")
    
    profile = pipeline.parse_job_description(payload.jd_text)
    LATEST_SESSION["jd_profile"] = profile
    return profile


@app.post("/api/v1/resumes/batch-match")
async def batch_match_resumes(
    jd_text: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Modules 2 & 3: Batch upload at least 10 resumes (PDF & DOCX), extract details,
    run requirement MaxSim embedding matching, and generate 0-100 composite rankings.
    """
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")
    if not files:
        raise HTTPException(status_code=400, detail="At least one resume file must be uploaded.")

    temp_dir = tempfile.mkdtemp(prefix="resumes_")
    saved_paths = []

    try:
        for file in files:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in [".pdf", ".docx", ".doc"]:
                continue
            
            temp_path = os.path.join(temp_dir, file.filename)
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)
            saved_paths.append(temp_path)

        if not saved_paths:
            raise HTTPException(status_code=400, detail="No valid PDF or DOCX files provided.")

        # Run pipeline batch ranking
        rankings = pipeline.rank_resumes(saved_paths, jd_text)
        
        # Cache results for candidate-level retrieval
        LATEST_SESSION["jd_profile"] = pipeline.parse_job_description(jd_text)
        LATEST_SESSION["rankings"] = rankings

        return {
            "total_processed": len(rankings),
            "rankings": rankings
        }

    finally:
        # Clean up temporary storage
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.get("/api/v1/rankings")
def get_latest_rankings():
    """
    Module 4: Get ranked candidate dashboard table.
    """
    if not LATEST_SESSION["rankings"]:
        return {"rankings": []}
    return {
        "jd_title": LATEST_SESSION["jd_profile"]["title"] if LATEST_SESSION["jd_profile"] else "Target Role",
        "rankings": LATEST_SESSION["rankings"]
    }


@app.get("/api/v1/candidates/{rank}")
def get_candidate_analysis(rank: int):
    """
    Module 5: Candidate-level analysis drill-down by rank index.
    """
    rankings = LATEST_SESSION.get("rankings", [])
    for c in rankings:
        if c.get("rank") == rank:
            return c
    raise HTTPException(status_code=404, detail="Candidate not found for specified rank.")
