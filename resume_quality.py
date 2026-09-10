import textstat

REQUIRED_SECTIONS = {
    "Education": ["education", "b.e.", "b.tech", "bachelor", "degree", "university", "college"],
    "Skills": ["skills", "technical skills", "technologies"],
    "Experience/Projects": ["experience", "project", "internship", "work"],
    "Contact Info": ["@", "linkedin", "github"]
}


def check_completeness(text):
    """Checks whether standard resume sections are present."""
    text_lower = text.lower()
    results = {}
    for section, keywords in REQUIRED_SECTIONS.items():
        results[section] = any(keyword in text_lower for keyword in keywords)

    found_count = sum(results.values())
    completeness_pct = round((found_count / len(REQUIRED_SECTIONS)) * 100, 2)

    return {"sections": results, "completeness_pct": completeness_pct}


def check_readability(text):
    """Flesch Reading Ease score — higher score = easier to read."""
    score = textstat.flesch_reading_ease(text)

    if score >= 60:
        level = "Easy to read"
    elif score >= 30:
        level = "Moderately difficult"
    else:
        level = "Difficult to read"

    return {"score": round(score, 2), "level": level}