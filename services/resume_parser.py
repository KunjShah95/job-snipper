import re


def _extract_skills_from_text(raw_text):
    """
    Extract skills from resume text intelligently.
    Looks for Skills/Technical Skills sections and extracts items.
    Falls back to comprehensive keyword matching if no section found.
    """
    skills = []
    
    # Try to find Skills section (common headers)
    skills_section_pattern = r"(?i)(skills?|technical\s+skills?|core\s+competenc(?:y|ies)|expertise|proficiencies?)[\s:]*\n(.*?)(?=\n\n|\n[A-Z][A-Z\s]+:|\Z)"
    skills_section_match = re.search(skills_section_pattern, raw_text, re.DOTALL)
    
    if skills_section_match:
        # Extract from skills section
        skills_text = skills_section_match.group(2)
        
        # Split by common delimiters (comma, pipe, bullet, semicolon, newline)
        skill_items = re.split(r'[,|•·\n;]', skills_text)
        
        for item in skill_items:
            # Clean and validate each skill
            skill = item.strip().strip('•·-*→◦■□')
            # Keep items that are 2-50 chars and have some letters
            if skill and 2 <= len(skill) <= 50 and re.search(r'[a-zA-Z]', skill):
                # Remove common noise words
                if not re.match(r'^(and|or|the|with|including|such as|etc)$', skill, re.I):
                    skills.append(skill)
    
    # Return only skills found in dedicated Skills sections
    # This ensures NO hardcoded skills and only actual resume content is shown
    return skills[:100]  # Limit to 100 skills max


def parse_resume_to_json(raw_text):
    """
    Extract structured data from resume text:
    - Name, email, phone, location
    - Skills
    - Education
    - Experience
    Returns a dict and preserves raw_text.
    """
    try:
        # Extract skills from Skills/Technical Skills section intelligently
        skills = _extract_skills_from_text(raw_text)
        
        # Extract education qualifications
        education_pattern = r"(B\.Sc|M\.Sc|B\.Tech|M\.Tech|PhD|MBA|Bachelor|Master|Associate)"
        education = re.findall(education_pattern, raw_text, re.I)
        
        # Extract experience indicators
        experience_pattern = r"(\d+\+?\s?years|internship|project|worked at|experience)"
        experience = re.findall(experience_pattern, raw_text, re.I)

        # Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
        email = email_match.group(0) if email_match else ""

        # Phone (simple patterns)
        phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", raw_text)
        phone = phone_match.group(0) if phone_match else ""

        # Name heuristic
        name = ""
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        for l in lines[:8]:
            m = re.match(r"(?i)name[:\-]\s*(.+)", l)
            if m:
                name = m.group(1).strip()
                break
        if not name and lines:
            for l in lines[:6]:
                if "@" in l or re.search(r"\d", l):
                    continue
                if 1 <= len(l.split()) <= 4:
                    name = l
                    break

        # Location heuristic
        loc = ""
        loc_match = re.search(r"(?i)(location|address)[:\-]\s*(.+)", raw_text)
        if loc_match:
            loc = loc_match.group(2).strip()
        else:
            cs = re.search(r"\b([A-Za-z ]+),\s*([A-Z]{2}|\b[A-Za-z]{2,}\b)\b", raw_text)
            if cs:
                loc = cs.group(0)

        # Deduplicate while preserving order
        def uniq(seq):
            seen = set()
            out = []
            for x in seq:
                k = x.strip().lower()
                if k and k not in seen:
                    seen.add(k)
                    out.append(x.strip())
            return out

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "location": loc,
            "skills": uniq(skills),
            "education": uniq(education),
            "experience": uniq(experience),
            "raw_text": raw_text,
        }
    except Exception as e:
        print(f"Resume parsing failed: {e}")
        return {"skills": [], "education": [], "experience": [], "raw_text": raw_text}


class ResumeParser:
    """Compatibility wrapper providing a class-based API expected by pages.

    Provides parse_resume(raw_text) which returns the same structure as
    parse_resume_to_json.
    """

    def __init__(self):
        pass

    def parse_resume(self, raw_text: str):
        """Parse resume text and return structured JSON-like dict."""
        return parse_resume_to_json(raw_text)
