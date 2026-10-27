import re
from typing import Tuple

QA_PATTERNS = [
    r"question[- ]and[- ]answer",
    r"questions? (and|&) answers?",
    r"Q&A session",
]


def split_transcript(text: str) -> tuple[str, str]:
    """Split a transcript into prepared remarks and Q&A.

    Returns:
        (prepared_remarks, q_and_a)
    """
    cleaned = (text or "").strip()
    if not cleaned:
        return "", ""

    for pat in QA_PATTERNS:
        match = re.search(pat, cleaned, flags=re.I)
        if match:
            return cleaned[: match.start()], cleaned[match.end() :]
    return cleaned, ""


def parse_speakers(text: str) -> list[str]:
    """Very lightweight speaker extraction used for transcript audits.

    This should be replaced with a more robust parser in production.
    """
    speakers = []
    for line in (text or "").splitlines():
        if "--" in line and ":" in line:
            speaker = line.split("--", 1)[0].strip()
            if speaker:
                speakers.append(speaker)
    return speakers


def run_split() -> None:
    """Placeholder for transcript processing.

    In production, iterate over transcript rows, detect Q&A boundaries, parse
    speakers, and write clean outputs to Parquet.
    """
    sample = "Management prepared remarks. Q&A session with analysts."
    prepared, qa = split_transcript(sample)
    print({"prepared": prepared[:80], "qa": qa[:80], "speakers": parse_speakers(sample)})
