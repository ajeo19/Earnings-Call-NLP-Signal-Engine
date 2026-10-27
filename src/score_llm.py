from __future__ import annotations

from typing import Iterable, List

try:
    from transformers import pipeline
except Exception:  # pragma: no cover
    pipeline = None


def score_sentences(sentences: Iterable[str], batch_size: int = 32) -> list[float]:
    sent_list = list(sentences)
    if not sent_list:
        return []

    if pipeline is None:
        return [0.0 for _ in sent_list]

    try:
        classifier = pipeline(
            "text-classification",
            model="ProsusAI/finbert",
            top_k=None,
            truncation=True,
            max_length=512,
            device=-1,
        )
        outputs = classifier(sent_list, batch_size=batch_size)
        scores: List[float] = []
        for result in outputs:
            positive = next(item for item in result if item["label"] == "positive")
            negative = next(item for item in result if item["label"] == "negative")
            scores.append(float(positive["score"]) - float(negative["score"]))
        return scores
    except Exception:
        return [0.0 for _ in sent_list]


def sentence_score_section(section_text: str) -> float:
    if not section_text:
        return 0.0
    sentences = [s.strip() for s in section_text.split(".") if s.strip()]
    scores = score_sentences(sentences)
    return float(sum(scores) / len(scores)) if scores else 0.0


def run_finbert_scores() -> None:
    import pandas as pd

    df = pd.read_parquet("data/processed/transcripts_clean.parquet")
    df["finbert_prepared"] = df["prepared_remarks"].apply(sentence_score_section)
    df["finbert_qa"] = df["qa_section"].apply(sentence_score_section)
    df.to_parquet("data/processed/finbert_scores.parquet", index=False)
    print("FinBERT scoring complete: data/processed/finbert_scores.parquet")
