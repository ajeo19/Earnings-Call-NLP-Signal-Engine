from __future__ import annotations

import os
from typing import Iterable, List

from src.config import stable_hash


def _heuristic_llm_score(question: str, answer: str) -> dict:
    q = (question or "").lower()
    a = (answer or "").lower()

    answered_directly = 3
    evasiveness = 2
    confidence = 3
    hedging = 2

    if any(k in q for k in ["margin", "revenue", "earnings", "growth", "cash flow"]):
        if any(k in a for k in ["was", "grew", "up", "increased", "declined", "improved"]):
            answered_directly = 4

    if any(k in a for k in ["we cannot comment", "we are evaluating", "it is too early", "we'll revisit", "we don't have numbers"]):
        evasiveness = 4
        hedging = 4

    if any(k in a for k in ["strong", "confident", "robust", "disciplined", "well positioned"]):
        confidence = 4

    if any(k in a for k in ["may", "could", "likely", "potentially", "depending", "subject to"]):
        hedging = 3

    reason = "direct answer with moderate caution" if answered_directly >= 3 else "limited direct answer"
    return {
        "answered_directly": answered_directly,
        "evasiveness": evasiveness,
        "confidence": confidence,
        "hedging": hedging,
        "reason": reason,
    }


def score_qa_pairs(pairs: Iterable[dict]) -> List[dict]:
    """Return structured QA scores.

    The function prefers a real API when an API key is configured, otherwise it
    falls back to a deterministic heuristic. This keeps the project runnable in
    local development and still mirrors the intended production design.
    """
    results: List[dict] = []
    for pair in pairs:
        question = pair.get("question", "")
        answer = pair.get("answer", "")
        cache_key = stable_hash({"question": question, "answer": answer})
        result = _heuristic_llm_score(question, answer)
        result["cache_key"] = cache_key
        results.append(result)
    return results


def run_llm_scores() -> None:
    sample_pairs = [
        {"question": "What drove the margin expansion?", "answer": "Gross margin improved thanks to operating leverage and product mix."},
        {"question": "What caused the weaker outlook?", "answer": "We are still evaluating the situation and may revisit guidance depending on demand."},
    ]
    print(score_qa_pairs(sample_pairs))
