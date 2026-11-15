import re
from typing import Dict, List, Any, Optional
import docx

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
LINKEDIN_REGEX = re.compile(r'linkedin\.com/in/[a-zA-Z0-9_-]+', re.IGNORECASE)
GITHUB_REGEX = re.compile(r'github\.com/[a-zA-Z0-9_-]+', re.IGNORECASE)

KNOWN_SECTION_HEADERS = {
    "summary": ["summary", "professional summary", "profile", "about me", "objective"],
    "experience": ["experience", "work experience", "employment history", "professional experience", "work history"],
    "skills": ["skills", "technical skills", "core competencies", "skills & expertise", "technologies", "proficiencies"],
    "education": ["education", "academic background", "qualifications", "academics"],
    "projects": ["projects", "personal projects", "key projects", "notable projects"]
}


class DocxParser:
    """
    Parser for Microsoft Word (.docx) candidate resumes.
    Extracts paragraphs, table cells, contact metadata, sections, and chunked bullets.
    """

    def __init__(self):
        pass

    def parse(self, file_path_or_stream) -> Dict[str, Any]:
        """Parse a .docx document from a file path or file-like stream."""
        doc = docx.Document(file_path_or_stream)
        raw_lines: List[str] = []

        # Extract text from standard paragraphs
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                raw_lines.append(text)

        # Extract text from tables (handles multi-column & tabular resumes)
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    # De-duplicate adjacent identical cells caused by merged table columns
                    deduped_cells = []
                    for c in row_cells:
                        if not deduped_cells or c != deduped_cells[-1]:
                            deduped_cells.append(c)
                    raw_lines.append(" | ".join(deduped_cells))

        full_text = "\n".join(raw_lines)
        cleaned_text = self._clean_text(full_text)

        name = self._extract_name(cleaned_text)
        email = self._extract_first_match(EMAIL_REGEX, cleaned_text)
        phone = self._extract_first_match(PHONE_REGEX, cleaned_text)
        linkedin = self._extract_first_match(LINKEDIN_REGEX, cleaned_text)
        github = self._extract_first_match(GITHUB_REGEX, cleaned_text)

        sections = self._split_sections(cleaned_text)
        chunks = self._chunk_text(cleaned_text, sections)

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "full_text": cleaned_text,
            "sections": sections,
            "chunks": chunks,
            "num_pages": 1  # DOCX files do not have explicit page breaks without layout rendering
        }

    def _clean_text(self, text: str) -> str:
        text = text.replace('\xa0', ' ').replace('\r\n', '\n').replace('\r', '\n')
        lines = [line.strip() for line in text.split('\n')]
        cleaned_lines = [re.sub(r'[ \t]+', ' ', l) for l in lines]
        return '\n'.join([l for l in cleaned_lines if l])

    def _extract_name(self, text: str) -> str:
        """
        Extract candidate name from the top header lines of the resume.
        Handles apostrophes (e.g. O'Connor), hyphens (e.g. Smith-Jones), and skips false positives.
        """
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        stop_words = {"and", "or", "in", "with", "the", "at", "for", "to", "by", "from", "category", "details"}
        for line in lines[:8]:
            if EMAIL_REGEX.search(line) or PHONE_REGEX.search(line):
                continue
            if '@' in line or 'http' in line.lower() or 'resume' in line.lower() or 'curriculum' in line.lower():
                continue
            if line.endswith('.') or line.endswith(',') or line.endswith(':'):
                continue

            words = line.split()
            if words and words[0].lower() in stop_words:
                continue

            clean_tokens = [w.replace('.', '').replace("'", "").replace('-', '') for w in words]
            if 1 <= len(words) <= 4 and all(t.isalpha() for t in clean_tokens if t):
                lower_line = line.lower()
                if not any(header in lower_line for sublist in KNOWN_SECTION_HEADERS.values() for header in sublist):
                    return line
        return "Candidate"

    def _extract_first_match(self, regex: re.Pattern, text: str) -> Optional[str]:
        match = regex.search(text)
        return match.group(0) if match else None

    def _split_sections(self, text: str) -> Dict[str, str]:
        lines = text.split('\n')
        sections: Dict[str, List[str]] = {
            "summary": [],
            "experience": [],
            "skills": [],
            "education": [],
            "projects": [],
            "other": []
        }

        current_sec = "summary"
        for line in lines:
            normalized = line.strip().lower().rstrip(':')
            detected_sec = None
            for sec_key, header_variants in KNOWN_SECTION_HEADERS.items():
                if normalized in header_variants:
                    detected_sec = sec_key
                    break

            if detected_sec:
                current_sec = detected_sec
            else:
                sections[current_sec].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items() if v}

    def _chunk_text(self, full_text: str, sections: Dict[str, str]) -> List[str]:
        chunks: List[str] = []
        target_sections = ["experience", "projects", "summary"]
        for sec in target_sections:
            content = sections.get(sec, "")
            if not content:
                continue

            raw_bullets = re.split(r'\n(?=[•\-\*\d+\.]|\s{2,})|\n\n+', content)
            for bullet in raw_bullets:
                cleaned = re.sub(r'^[•\-\*\d+\.]\s*', '', bullet).strip()
                if len(cleaned) >= 25:
                    chunks.append(cleaned)

        if len(chunks) < 3:
            paragraphs = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) >= 30]
            chunks.extend(paragraphs)

        return chunks
