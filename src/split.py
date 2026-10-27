import re
from typing import List

QA_PATTERNS = [
    r"question[- ]and[- ]answer",
    r"questions? (and|&) answers?",
    r"Q&A session",
    r"prepared remarks",
]

BOILERPLATE_PATTERNS = [
    r"operator.*?",
    r"safe harbor.*?",
    r"forward-looking statements.*?",
]


def clean_transcript(text: str) -> str:
    cleaned = text or ""
    for pat in BOILERPLATE_PATTERNS:
        cleaned = re.sub(pat, " ", cleaned, flags=re.I | re.S)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def split_transcript(text: str) -> tuple[str, str]:
    """Split transcript into prepared remarks and Q&A, with a conservative fallback."""
    cleaned = clean_transcript(text)
    if not cleaned:
        return "", ""

    for pat in QA_PATTERNS:
        match = re.search(pat, cleaned, flags=re.I)
        if match:
            prepared = cleaned[: match.start()].strip()
            qa = cleaned[match.end() :].strip()
            if prepared and qa:
                return prepared, qa

    # If no explicit Q&A marker is found, treat the whole transcript as prepared remarks.
    return cleaned, ""


def parse_speakers(text: str) -> List[str]:
    speakers = []
    for line in (text or "").splitlines():
        if "--" in line and ":" in line:
            speaker = line.split("--", 1)[0].strip()
            if speaker:
                speakers.append(speaker)
    return speakers


def run_split() -> None:
    sample = "Prepared remarks. We are pleased with growth. Question and answer session. Analyst asked about margins."
    prepared, qa = split_transcript(sample)
    print({
        "prepared": prepared,
        "qa": qa,
        "speakers": parse_speakers(sample),
    })
