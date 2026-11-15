import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9, "sept": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}

DATE_RANGE_REGEX = re.compile(
    r'(?P<start_month>[A-Za-z]+|\d{1,2})?\s*(?P<start_year>\d{4})\s*[-–—to]+\s*'
    r'(?P<end>(?:Present|Current|Now|Till Date|today|ongoing)|\d{1,2}/\d{4}|[A-Za-z]+\s*\d{4}|\d{4})',
    re.IGNORECASE
)


class ExperienceCalculator:
    """
    Calculates total and relevant candidate experience.
    Features:
      1. Interval merging (merges concurrent jobs to prevent double-counting).
      2. 'Present' handling (calculates dynamically from current year & month).
      3. Role relevance gating against the target JD domain.
      4. Calibrated experience scoring.
    """

    def __init__(self, current_date: Optional[datetime] = None):
        self.now = current_date or datetime.now()
        self.current_month_index = self.now.year * 12 + self.now.month

    def parse_date_to_month_index(self, text: str) -> Optional[int]:
        """Convert a date string (e.g. 'Jan 2021', '06/2019', '2018', 'Present') to an absolute month index."""
        text = text.strip()
        if not text:
            return None

        if re.search(r'(?i)\b(present|current|now|till date|today|ongoing)\b', text):
            return self.current_month_index

        # Pattern: Month Name + Year (e.g. Jan 2021)
        m_match = re.search(r'([A-Za-z]+)\s*(\d{4})', text)
        if m_match:
            month_name = m_match.group(1).lower()
            year = int(m_match.group(2))
            month = MONTH_MAP.get(month_name, 6)  # Default mid-year if unmapped
            return year * 12 + month

        # Pattern: MM/YYYY or MM-YYYY
        slash_match = re.search(r'(\d{1,2})[/-](\d{4})', text)
        if slash_match:
            month = int(slash_match.group(1))
            year = int(slash_match.group(2))
            month = max(1, min(12, month))
            return year * 12 + month

        # Pattern: Solo 4-digit Year (e.g. 2018)
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
        if year_match:
            year = int(year_match.group(1))
            return year * 12 + 6  # Mid-year approximation for year-only ranges

        return None

    def merge_intervals(self, intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Standard interval merging algorithm.
        Prevents double-counting overlapping/concurrent work dates.
        """
        if not intervals:
            return []

        # Filter invalid ranges (start > end) and sort by start
        valid = [(s, e) for s, e in intervals if s <= e]
        if not valid:
            return []

        valid.sort(key=lambda x: x[0])
        merged = [valid[0]]

        for current in valid[1:]:
            prev_start, prev_end = merged[-1]
            if current[0] <= prev_end:
                # Overlap detected: extend previous interval
                merged[-1] = (prev_start, max(prev_end, current[1]))
            else:
                merged.append(current)

        return merged

    def calculate_months_from_intervals(self, intervals: List[Tuple[int, int]]) -> int:
        """Sums the duration of merged intervals in months."""
        merged = self.merge_intervals(intervals)
        total_months = sum((end - start + 1) for start, end in merged)
        return total_months

    def extract_experience_from_text(
        self,
        text: str,
        jd_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extracts date intervals from resume text and partitions into total vs relevant experience.
        """
        all_intervals: List[Tuple[int, int]] = []
        relevant_intervals: List[Tuple[int, int]] = []
        extracted_roles: List[Dict[str, Any]] = []

        lines = text.split('\n')
        for i, line in enumerate(lines):
            match = DATE_RANGE_REGEX.search(line)
            if match:
                start_str = f"{match.group('start_month') or ''} {match.group('start_year')}".strip()
                end_str = match.group('end').strip()

                start_idx = self.parse_date_to_month_index(start_str)
                end_idx = self.parse_date_to_month_index(end_str)

                if start_idx and end_idx and start_idx <= end_idx:
                    # Protect against absurd dates (e.g. before 1970 or far future)
                    min_idx = 1970 * 12
                    max_idx = (self.now.year + 1) * 12
                    if min_idx <= start_idx <= max_idx and start_idx <= end_idx <= max_idx:
                        interval = (start_idx, end_idx)
                        all_intervals.append(interval)

                        # Context relevance check: inspect current line and surrounding 3 lines
                        surrounding = "\n".join(lines[max(0, i-2):min(len(lines), i+4)]).lower()
                        is_relevant = self._is_role_relevant(surrounding, jd_keywords)
                        if is_relevant:
                            relevant_intervals.append(interval)

                        extracted_roles.append({
                            "raw_line": line.strip(),
                            "start": start_str,
                            "end": end_str,
                            "is_relevant": is_relevant
                        })

        # Calculate decimal years
        total_months = self.calculate_months_from_intervals(all_intervals)
        relevant_months = self.calculate_months_from_intervals(relevant_intervals)

        total_years = round(total_months / 12.0, 1)
        relevant_years = round(relevant_months / 12.0, 1)

        # Cap relevant at total if edge case occurs
        relevant_years = min(total_years, relevant_years)

        return {
            "total_years": total_years,
            "relevant_years": relevant_years,
            "intervals_count": len(all_intervals),
            "merged_intervals": self.merge_intervals(relevant_intervals),
            "extracted_roles": extracted_roles
        }

    def _is_role_relevant(self, context_text: str, jd_keywords: Optional[List[str]]) -> bool:
        """
        Determines whether a role is in the relevant domain.
        Checks for software engineering titles and target tech keywords.
        """
        generic_relevant_terms = [
            "engineer", "developer", "architect", "programmer", "software",
            "backend", "full stack", "fullstack", "frontend", "devops",
            "data engineer", "systems", "cloud", "api", "database"
        ]

        # Check generic domain alignment
        if any(term in context_text for term in generic_relevant_terms):
            return True

        # Check JD specific skills/keywords if provided
        if jd_keywords:
            lowered_jd = [k.lower() for k in jd_keywords]
            if any(k in context_text for k in lowered_jd):
                return True

        return False

    def score_experience(
        self,
        relevant_years: float,
        required_years: Optional[float]
    ) -> Dict[str, Any]:
        """
        Computes calibrated experience score.
        If required_years is not specified, returns 100.0 (neutral) with no penalty.
        """
        if required_years is None or required_years <= 0:
            return {
                "experience_score": 100.0,
                "status": "unspecified",
                "delta": 0.0,
                "rationale": f"Candidate has {relevant_years} years of evaluated experience (no strict minimum specified)."
            }

        delta = round(relevant_years - required_years, 1)

        if relevant_years >= required_years:
            score = 100.0
            rationale = f"Meets and exceeds required experience: {relevant_years} years vs {required_years} years required (+{delta} yrs)."
        else:
            # Linear proportion with zero floor
            score = round(max(0.0, (relevant_years / required_years) * 100.0), 1)
            rationale = f"Below required tenure: {relevant_years} years evaluated vs {required_years} years required ({delta} yrs gap)."

        return {
            "experience_score": score,
            "required_years": required_years,
            "candidate_years": relevant_years,
            "delta": delta,
            "rationale": rationale
        }
