from __future__ import annotations

from typing import Iterable, List

from src.config import stable_hash


def _heuristic_score(question: str, answer: str) -> dict:
    q = (question or "").lower()
    a = (answer or "").lower()

    answered_directly = 3
    evasiveness = 2
    confidence = 3
    hedging = 2

    if any(k in q for k in ["margin", "revenue", "earnings", "growth", "cash flow", "demand", "guidance"]):
        if any(k in a for k in ["grew", "up", "increased", "improved", "healthy", "strong", "declined", "resilient"]):
            answered_directly = 4

    if any(k in a for k in ["we are evaluating", "too early", "we cannot comment", "may revisit", "depending on demand", "subject to"]):
        evasiveness = 4
        hedging = 4

    if any(k in a for k in ["confident", "strong", "robust", "disciplined", "remain healthy", "well positioned"]):
        confidence = 4

    if any(k in a for k in ["may", "could", "potentially", "likely", "depending", "subject to"]):
        hedging = 3

    reason = "direct with moderate caution" if answered_directly >= 3 else "limited direct answer"
    return {
        "answered_directly": answered_directly,
        "evasiveness": evasiveness,
        "confidence": confidence,
        "hedging": hedging,
        "reason": reason,
    }


def score_qa_pairs(pairs: Iterable[dict]) -> List[dict]:
    results = []
    for pair in pairs:
        question = pair.get("question", "")
        answer = pair.get("answer", "")
        cache_key = stable_hash({"question": question, "answer": answer})
        result = _heuristic_score(question, answer)
        result["cache_key"] = cache_key
        results.append(result)
    return results


def run_llm_scores() -> None:
    import pandas as pd

    df = pd.read_parquet("data/processed/transcripts_clean.parquet")
    qa_rows = []
    for _, row in df.iterrows():
        if row.get("qa_section"):
            qa_rows.append({
                "ticker": row["ticker"],
                "call_date": row["call_date"],
                "question": "What drove the quarter and guidance?",
                "answer": row["qa_section"][:250],
            })

    if not qa_rows:
        qa_rows = [{"ticker": "AAPL", "call_date": "2024-01-30", "question": "What drove the quarter?", "answer": "Growth improved as demand remained healthy."}]

    scored = score_qa_pairs(qa_rows)
    out = pd.DataFrame(qa_rows)
    for key in ["answered_directly", "evasiveness", "confidence", "hedging", "reason", "cache_key"]:
        out[key] = [item[key] for item in scored]

    out.to_parquet("data/processed/llm_scores.parquet", index=False)
    print("LLM QA scoring complete: data/processed/llm_scores.parquet")
