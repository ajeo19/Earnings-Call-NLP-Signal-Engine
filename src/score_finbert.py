from __future__ import annotations

import re
from typing import Iterable, List

from src.ingest import read_parquet

QA_PATTERNS = [
    r"question[- ]and[- ]answer",
    r"questions? (and|&) answers?",
    r"Q&A session",
]

BOILERPLATE_PATTERNS = [
    r"operator.*?",
    r"safe harbor.*?",
    r"forward-looking statements.*?",
    r"conference call.*?",
]


def clean_transcript(text: str) -> str:
    cleaned = text or ""
    for pat in BOILERPLATE_PATTERNS:
        cleaned = re.sub(pat, " ", cleaned, flags=re.I | re.S)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def split_transcript(text: str) -> tuple[str, str]:
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

    return cleaned, ""


def parse_speakers(text: str) -> List[str]:
    speakers = []
    for line in (text or "").splitlines():
        if "--" in line and ":" in line:
            speaker = line.split("--", 1)[0].strip()
            if speaker:
                speakers.append(speaker)
    return speakers


def split_transcript_df(df) -> pd.DataFrame:
    import pandas as pd

    out = df.copy()
    out["prepared_remarks"] = out["transcript"].apply(lambda x: split_transcript(x)[0])
    out["qa_section"] = out["transcript"].apply(lambda x: split_transcript(x)[1])
    out["speaker_labels"] = out["transcript"].apply(parse_speakers)
    out["transcript_length"] = out["transcript"].str.len()
    out["qa_present"] = out["qa_section"].str.len() > 0
    return out


def run_split() -> None:
    df = read_parquet("data/processed/transcripts_raw.parquet")
    cleaned = split_transcript_df(df)
    cleaned.to_parquet("data/processed/transcripts_clean.parquet", index=False)
    print(f"Transcript split complete: {len(cleaned)} rows saved to data/processed/transcripts_clean.parquet")
