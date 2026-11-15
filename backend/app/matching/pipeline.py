import os
import re
from typing import Dict, List, Any, Optional

from app.parsers.pdf_parser import PDFParser
from app.parsers.docx_parser import DocxParser
from app.nlp.skills_matcher import SkillsMatcher
from app.nlp.experience_calc import ExperienceCalculator
from app.nlp.embedding_engine import EmbeddingEngine
from app.matching.scoring import ScoringEngine


class MatchingPipeline:
    """
    End-to-end AI Resume Matching and Ranking Pipeline.
    Orchestrates parsing, entity extraction, chunk MaxSim embedding, and calibrated 4-pillar scoring.
    """

    def __init__(self, taxonomy_path: Optional[str] = None):
        self.pdf_parser = PDFParser()
        self.docx_parser = DocxParser()
        self.skills_matcher = SkillsMatcher(taxonomy_path)
        self.exp_calc = ExperienceCalculator()
        self.embedding_engine = EmbeddingEngine.get_instance()
        self.scoring_engine = ScoringEngine()

    def parse_job_description(self, jd_text: str) -> Dict[str, Any]:
        """
        Extracts structured requirements, skills, experience, and degree from JD text.
        (Module 1 Functional Requirement).
        """
        # Extract skills
        extracted_skills = self.skills_matcher.extract_skills(jd_text)
        all_skills = [s["canonical"] for s in extracted_skills]

        # Extract required years
        exp_match = re.search(r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)', jd_text, re.IGNORECASE)
        required_years = float(exp_match.group(1)) if exp_match else None

        # Split into requirement bullet lines for MaxSim embedding
        lines = [l.strip() for l in jd_text.split('\n') if len(l.strip()) >= 20]
        req_lines = []
        for line in lines:
            cleaned = re.sub(r'^[•\-\*\d+\.]\s*', '', line).strip()
            # Select lines that describe responsibilities, requirements, or qualifications
            if any(kw in cleaned.lower() for kw in ["require", "experience", "proficien", "skill", "responsib", "build", "design", "develop", "maintain", "lead"]):
                req_lines.append(cleaned)

        if not req_lines:
            # Fallback to general lines
            req_lines = [l for l in lines if len(l) >= 30][:8]

        # Degree requirement detection
        degree_match = re.search(r'(bachelor|master|phd|degree|b\.s|m\.s)[^\n\.]*', jd_text, re.IGNORECASE)
        required_degree = degree_match.group(0).strip() if degree_match else None

        return {
            "title": lines[0] if lines else "Target Position",
            "required_years": required_years,
            "skills": all_skills,
            "requirement_lines": req_lines,
            "required_degree": required_degree,
            "raw_text": jd_text
        }

    def process_resume(self, file_path: str, jd_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses a single resume file (PDF or DOCX) and evaluates against the JD.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            parsed = self.pdf_parser.parse(file_path)
        elif ext in [".docx", ".doc"]:
            parsed = self.docx_parser.parse(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        full_text = parsed["full_text"]
        chunks = parsed["chunks"]

        # 1. Skills Extraction & Comparison
        cand_skills_data = self.skills_matcher.extract_skills(full_text)
        cand_skills = [s["canonical"] for s in cand_skills_data]
        skills_comparison = self.skills_matcher.compare_skills(
            required_skills=jd_profile.get("skills", []),
            preferred_skills=[],
            candidate_skills=cand_skills
        )

        # 2. Experience Extraction & Scoring
        # Prioritize the isolated work experience section if detected to avoid picking up dates
        # from educational timelines or dataset metrics in project descriptions (e.g. "matches (2008-2026)")
        exp_text = parsed["sections"].get("experience", "").strip()
        if not exp_text or len(exp_text) < 30:
            exp_text = full_text

        exp_data = self.exp_calc.extract_experience_from_text(
            exp_text,
            jd_keywords=jd_profile.get("skills", [])
        )
        exp_score_data = self.exp_calc.score_experience(
            relevant_years=exp_data["relevant_years"],
            required_years=jd_profile.get("required_years")
        )

        # 3. Requirement-Level MaxSim Semantic Matching
        semantic_result = self.embedding_engine.compute_maxsim(
            jd_requirements=jd_profile.get("requirement_lines", []),
            resume_chunks=chunks
        )

        # 4. Education Scoring
        edu_result = self.scoring_engine.score_education(
            candidate_degree_text=parsed["sections"].get("education", "") or full_text,
            required_degree_text=jd_profile.get("required_degree")
        )

        # 5. Composite Scoring & Rationale Generation
        metrics = {
            "candidate_name": parsed["name"],
            "email": parsed["email"],
            "phone": parsed["phone"],
            "total_years": exp_data["total_years"],
            "relevant_years": exp_data["relevant_years"],
            "required_years": jd_profile.get("required_years"),
            "matched_required": skills_comparison["matched_required"],
            "missing_required": skills_comparison["missing_required"],
            "all_extracted_skills": cand_skills,
            "raw_semantic_similarity": semantic_result["raw_similarity"],
            "requirement_matches": semantic_result["requirement_matches"],
            "degree_matched": edu_result["degree_matched"]
        }

        evaluation = self.scoring_engine.compute_composite_score(
            skills_score=skills_comparison["skills_score"],
            experience_score=exp_score_data["experience_score"],
            semantic_score=semantic_result["semantic_score"],
            education_score=edu_result["education_score"],
            metrics=metrics
        )

        return {
            "filename": os.path.basename(file_path),
            "candidate_name": parsed["name"],
            "email": parsed["email"],
            "phone": parsed["phone"],
            "relevant_experience": exp_data["relevant_years"],
            "total_experience": exp_data["total_years"],
            "overall_score": evaluation.overall_score,
            "breakdown": evaluation.breakdown.model_dump(),
            "matched_skills": skills_comparison["matched_required"],
            "missing_skills": skills_comparison["missing_required"],
            "all_skills": cand_skills,
            "education_level": edu_result["candidate_level"],
            "rationale": evaluation.rationale,
            "requirement_citations": semantic_result["requirement_matches"][:4]  # Top citations
        }

    def rank_resumes(
        self,
        resume_paths: List[str],
        jd_text: str
    ) -> List[Dict[str, Any]]:
        """
        Evaluates a batch of resumes against a JD and returns sorted candidate rankings.
        (Modules 2, 3, 4, 5).
        """
        jd_profile = self.parse_job_description(jd_text)
        results = []

        for path in resume_paths:
            try:
                res = self.process_resume(path, jd_profile)
                results.append(res)
            except Exception as e:
                print(f"Error processing {path}: {e}")

        # Sort descending by overall_score, tie-break by relevant_experience
        results.sort(key=lambda x: (x["overall_score"], x["relevant_experience"]), reverse=True)

        # Assign rank indices
        for i, r in enumerate(results):
            r["rank"] = i + 1

        return results
