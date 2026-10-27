from __future__ import annotations

from typing import Iterable, List

from transformers import pipeline

from src.config import PROJECT_ROOT


def score_sentences(sentences: Iterable[str], batch_size: int = 32) -> list[float]:
    """Score sentence-level sentiment with FinBERT.

    Falls back to a lightweight placeholder when the model is unavailable.
    """
    sent_list = list(sentences)
    if not sent_list:
        return []

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
        # Fallback so the project remains runnable in minimal local environments.
        return [0.0 for _ in sent_list]


def run_finbert_scores() -> None:
    sample_texts = [
        "Revenue increased strongly this quarter.",
        "Margins were weaker but guidance remains stable.",
    ]
    scores = score_sentences(sample_texts)
    print({"sample_scores": scores})
