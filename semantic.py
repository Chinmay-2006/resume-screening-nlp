import spacy

_nlp = None

def _load_model():
    """Load the spaCy model once and reuse it (loading is slow, so we cache it)."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_md")
    return _nlp


def compute_semantic_similarity(resume_text, jd_text):
    """
    Compute similarity based on word MEANING (via spaCy word vectors),
    not just exact word overlap. Captures cases like "backend developer"
    vs "server-side engineer" being conceptually related.
    Returns a percentage (0-100).
    """
    nlp = _load_model()
    doc1 = nlp(resume_text[:100000])  # truncate extreme edge cases (spaCy has a length limit)
    doc2 = nlp(jd_text[:100000])
    score = doc1.similarity(doc2)
    return round(score * 100, 2)