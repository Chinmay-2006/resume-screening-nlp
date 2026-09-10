from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess_text
from skills import extract_skills


def compute_tfidf_similarity(resume_text, jd_text):
    """
    Compute overall textual similarity (0-100) between resume and JD
    using TF-IDF + cosine similarity.
    """
    resume_clean = " ".join(preprocess_text(resume_text))
    jd_clean = " ".join(preprocess_text(jd_text))

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])

    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)


def skill_gap_report(resume_text, jd_text):
    """
    Compare skills mentioned in the resume vs the JD.
    Returns matched skills, missing skills, and skill match percentage.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    # Skill match percentage = matched / total skills required by JD
    if len(jd_skills) > 0:
        skill_match_pct = round((len(matched) / len(jd_skills)) * 100, 2)
    else:
        skill_match_pct = 0.0

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "jd_skills_total": sorted(jd_skills),
        "skill_match_pct": skill_match_pct
    }


from semantic import compute_semantic_similarity

def compute_final_score(resume_text, jd_text, skill_weight=0.6, content_weight=0.4):
    """
    Final score = Skill Match (60%) + Content Similarity (40%)
    Content Similarity = average of TF-IDF (exact word overlap) and
    Semantic Similarity (meaning-based overlap via spaCy).
    """
    tfidf_score = compute_tfidf_similarity(resume_text, jd_text)
    semantic_score = compute_semantic_similarity(resume_text, jd_text)
    content_score = round((tfidf_score + semantic_score) / 2, 2)

    report = skill_gap_report(resume_text, jd_text)
    jd_skill_count = len(report["jd_skills_total"])

    if jd_skill_count == 0:
        final_score = content_score
        note = "No specific technical skills detected in JD — ranked by overall content similarity (TF-IDF + semantic)."
    else:
        final_score = (report["skill_match_pct"] * skill_weight) + (content_score * content_weight)
        note = None

    final_score = round(final_score, 2)

    return {
        "final_score": final_score,
        "tfidf_score": tfidf_score,
        "semantic_score": semantic_score,
        "content_score": content_score,
        "skill_match_pct": report["skill_match_pct"],
        "matched_skills": report["matched_skills"],
        "missing_skills": report["missing_skills"],
        "note": note
    }


if __name__ == "__main__":
    from extractor import extract_text

    resume_text = extract_text("sample_data/resume1.txt")
    jd_text = extract_text("sample_data/job_description.txt")

    result = compute_final_score(resume_text, jd_text)

    print(f"Final Score: {result['final_score']}%")
    print(f"  - TF-IDF Similarity: {result['tfidf_score']}%")
    print(f"  - Skill Match: {result['skill_match_pct']}%")
    print("Matched Skills:", result['matched_skills'])
    print("Missing Skills:", result['missing_skills'])