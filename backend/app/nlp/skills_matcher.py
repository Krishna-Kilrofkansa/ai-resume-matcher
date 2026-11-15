import os
import json
import re
from typing import Dict, List, Set, Tuple, Any, Optional
from rapidfuzz import fuzz


class SkillsMatcher:
    """
    High-precision skills extractor and normalizer.
    Combines:
      1. Word-boundary regex guards for short skills (e.g. C, R, Go, SQL, AWS, Git).
      2. Alias & synonym resolution to canonical skill names.
      3. RapidFuzz token matching for long phrases (>= 88% threshold).
    """

    def __init__(self, taxonomy_path: Optional[str] = None):
        if taxonomy_path is None:
            taxonomy_path = os.path.join(
                os.path.dirname(__file__), "..", "data", "skills_taxonomy.json"
            )

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.skills_data = data.get("skills", [])
        self.canonical_map: Dict[str, Dict[str, Any]] = {}
        self.alias_to_canonical: Dict[str, str] = {}
        self.short_skills_patterns: List[Tuple[str, str, re.Pattern]] = []
        self.long_phrases: List[Tuple[str, str]] = []

        self._build_indexes()

    def _build_indexes(self):
        for item in self.skills_data:
            canonical = item["canonical"]
            self.canonical_map[canonical] = item
            is_short = item.get("is_short", False)

            for alias in item.get("aliases", [canonical]):
                normalized_alias = alias.strip().lower()
                self.alias_to_canonical[normalized_alias] = canonical

                # Compile strict regex boundary for short skills (< 4 chars or flagged as is_short)
                if is_short or len(alias) <= 3:
                    # Single letter languages (C, R) require extra context or standalone boundary
                    if alias.upper() in ["C", "R"]:
                        pattern = re.compile(
                            rf'(?<![a-zA-Z0-9_#+])\b{re.escape(alias)}\b(?![a-zA-Z0-9_#+])'
                        )
                    else:
                        pattern = re.compile(rf'\b{re.escape(alias)}\b', re.IGNORECASE)
                    self.short_skills_patterns.append((alias, canonical, pattern))
                else:
                    self.long_phrases.append((alias, canonical))

    def extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts all canonical skills present in the text with metadata.
        Returns a deduplicated list of matched canonical skills.
        """
        if not text:
            return []

        found_canonicals: Dict[str, Dict[str, Any]] = {}
        text_lower = text.lower()

        # Step 1: Strict word-boundary regex for short skills
        for alias, canonical, pattern in self.short_skills_patterns:
            if canonical in found_canonicals:
                continue

            # Context check for single-letter languages (C, R) to prevent false positives
            if alias.upper() in ["C", "R"]:
                # Look for 'C' or 'R' near programming/tech keywords or in a skills section
                matches = pattern.finditer(text)
                for m in matches:
                    start, end = max(0, m.start() - 30), min(len(text), m.end() + 30)
                    surrounding = text[start:end].lower()
                    if any(kw in surrounding for kw in ["programming", "developer", "language", "code", "c++", "python", "skills", "algorithms", "r&d", "statistical"]):
                        found_canonicals[canonical] = {
                            "canonical": canonical,
                            "matched_alias": alias,
                            "category": self.canonical_map[canonical]["category"],
                            "match_type": "strict_regex"
                        }
                        break
            else:
                if pattern.search(text):
                    found_canonicals[canonical] = {
                        "canonical": canonical,
                        "matched_alias": alias,
                        "category": self.canonical_map[canonical]["category"],
                        "match_type": "strict_regex"
                    }

        # Step 2: Exact substring match for long phrases and aliases
        for alias, canonical in self.long_phrases:
            if canonical in found_canonicals:
                continue

            alias_lower = alias.lower()
            # Whole word boundary search for multi-letter terms
            pattern = rf'\b{re.escape(alias_lower)}\b'
            if re.search(pattern, text_lower):
                found_canonicals[canonical] = {
                    "canonical": canonical,
                    "matched_alias": alias,
                    "category": self.canonical_map[canonical]["category"],
                    "match_type": "exact_alias"
                }

        # Step 3: RapidFuzz fallback on candidate noun-chunks / lines (threshold >= 88)
        # We search line by line or phrase by phrase, never across whole document
        lines = [l.strip() for l in text.split('\n') if len(l.strip()) >= 3]
        for line in lines:
            line_lower = line.lower()
            for alias, canonical in self.long_phrases:
                if canonical in found_canonicals:
                    continue
                alias_lower = alias.lower()
                # Skip fuzzing short phrases
                if len(alias_lower) < 5:
                    continue

                score = fuzz.token_set_ratio(alias_lower, line_lower)
                if score >= 88:
                    found_canonicals[canonical] = {
                        "canonical": canonical,
                        "matched_alias": alias,
                        "category": self.canonical_map[canonical]["category"],
                        "match_type": "fuzzy"
                    }

        return list(found_canonicals.values())

    def compare_skills(
        self,
        required_skills: List[str],
        preferred_skills: List[str],
        candidate_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Compares candidate extracted skills against JD requirements.
        Calculates exact skills score and partitions matched vs missing.
        """
        # Normalize JD skills to canonical names if possible
        norm_req = [self.normalize_skill_name(s) for s in required_skills]
        norm_pref = [self.normalize_skill_name(s) for s in preferred_skills]
        norm_cand = set(self.normalize_skill_name(s) for s in candidate_skills)

        matched_req = [s for s in norm_req if s in norm_cand]
        missing_req = [s for s in norm_req if s not in norm_cand]

        matched_pref = [s for s in norm_pref if s in norm_cand]
        missing_pref = [s for s in norm_pref if s not in norm_cand]

        # Calculate mathematically sound skills score
        if norm_req and norm_pref:
            req_coverage = len(matched_req) / len(norm_req)
            pref_coverage = len(matched_pref) / len(norm_pref)
            skills_score = round((0.80 * req_coverage + 0.20 * pref_coverage) * 100.0, 1)
        elif norm_req:
            req_coverage = len(matched_req) / len(norm_req)
            skills_score = round(req_coverage * 100.0, 1)
        else:
            skills_score = 100.0

        return {
            "skills_score": skills_score,
            "matched_required": matched_req,
            "missing_required": missing_req,
            "matched_preferred": matched_pref,
            "missing_preferred": missing_pref,
            "total_matched": matched_req + matched_pref,
            "coverage_pct": round(len(matched_req) / max(1, len(norm_req)) * 100.0, 1)
        }

    def normalize_skill_name(self, skill: str) -> str:
        """Returns the canonical name for a given skill or alias."""
        clean = skill.strip().lower()
        return self.alias_to_canonical.get(clean, skill.strip())
