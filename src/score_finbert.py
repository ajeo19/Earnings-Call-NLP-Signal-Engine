from __future__ import annotations

from typing import Iterable, List

try:
    from transformers import pipeline
except Exception:  # pragma: no cover
    pipeline = None


def score_sentences(sentences: Iterable[str], batch_size: int = 32) -> list[float]:
    """Sentence-level FinBERT scoring with a safe fallback for local execution."""
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


def run_finbert_scores() -> None:
    sample_texts = [
        "Revenue increased strongly this quarter.",
        "Margins were weaker while guidance remained cautious.",
    ]
    print({"sample_scores": score_sentences(sample_texts)})
