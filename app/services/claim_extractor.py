
import re


SENSATIONAL_TERMS = {
    "shocking",
    "unbelievable",
    "secret",
    "exposed",
    "miracle",
    "everyone",
    "never",
    "always",
    "guaranteed",
    "breaking",
    "cover-up",
    "wake up",
    "they don't want you to know",
}


def extract_claims(text: str, limit: int = 8) -> list[str]:
    """Extract candidate sentences for further fact-checking."""
    if not text or not text.strip():
        return []

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    claims = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 15:
            continue

        if sentence not in claims:
            claims.append(sentence)

        if len(claims) >= limit:
            break

    return claims


def detect_red_flags(text: str) -> list[str]:
    """Detect language patterns that deserve closer review."""
    if not text or not text.strip():
        return []

    normalized = text.lower()
    flags = []

    matched_terms = [
        term
        for term in SENSATIONAL_TERMS
        if term in normalized
    ]

    if matched_terms:
        flags.append(
            "Potentially sensational wording detected: "
            + ", ".join(sorted(matched_terms))
            + ". Review the context before drawing conclusions."
        )

    if re.search(r"\b\d+(?:\.\d+)?%", text):
        flags.append(
            "A percentage appears in the content. Check the original "
            "dataset, sample size, date, and calculation."
        )

    if re.search(
        r"\b(study|research|scientists|experts)\b",
        normalized,
    ):
        flags.append(
            "The text refers to research or experts. Look for the original "
            "study or a named, qualified source."
        )

    if not re.search(r"https?://|www\.", text, re.IGNORECASE):
        flags.append(
            "No web link was detected in the submitted text. "
            "Check whether the original source is available."
        )

    return flags
