"""
scorer.py
---------
Optional expansion: Keyword Match Scorer.
Compares the resume text against the job description and calculates
a keyword match percentage score, along with matched and missing keywords.
"""

# Common English filler words to ignore during keyword comparison
STOPWORDS = {
    "and", "the", "to", "a", "of", "in", "for", "with", "on", "is", "are",
    "at", "by", "an", "be", "this", "that", "it", "as", "or", "we", "you",
    "our", "your", "will", "have", "has", "from", "which", "their", "they",
    "was", "were", "but", "not", "can", "all", "also", "if", "into", "more",
    "than", "any", "about", "would", "who", "how", "its", "us", "do",
}


def _clean_words(text: str) -> set:
    """
    Tokenise a block of text into a set of cleaned, lowercase words,
    removing stopwords, punctuation, and very short tokens.

    Args:
        text: Raw input text.

    Returns:
        A set of meaningful lowercase word strings.
    """
    # Remove common punctuation and split
    for char in ".,;:!?()[]{}\"'\n\t/-":
        text = text.replace(char, " ")

    words = {
        word.lower()
        for word in text.split()
        if len(word) > 2 and word.lower() not in STOPWORDS
    }
    return words


def keyword_match_score(resume_text: str, job_description: str) -> dict:
    """
    Calculate the keyword match score between a resume and a job description.

    Args:
        resume_text:     Plain text of the resume.
        job_description: Plain text of the job description.

    Returns:
        A dictionary with:
            - "score"   (float): Match percentage, 0–100.
            - "matched" (list):  Keywords found in both resume and job description.
            - "missing" (list):  Important job keywords NOT found in the resume.
            - "total"   (int):   Total number of unique job keywords evaluated.
    """
    resume_words = _clean_words(resume_text)
    job_words = _clean_words(job_description)

    if not job_words:
        return {"score": 0.0, "matched": [], "missing": [], "total": 0}

    matched = sorted(resume_words & job_words)
    missing = sorted(job_words - resume_words)
    score = round(len(matched) / len(job_words) * 100, 1)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total": len(job_words),
    }
