import hashlib
import json
from typing import Iterable, List

from src.config import stable_hash


def score_qa_pairs(pairs: Iterable[dict]) -> List[dict]:
    """Placeholder LLM scoring routine using structured JSON output.

    In production, call a model with a fixed prompt, set temperature to zero,
    and cache responses keyed by a hash of the question and answer.
    """
    results: List[dict] = []
    for pair in pairs:
        q = pair.get("question", "")
        a = pair.get("answer", "")
        payload = {"question": q, "answer": a}
        cache_key = stable_hash(payload)

        result = {
            "cache_key": cache_key,
            "answered_directly": 3,
            "evasiveness": 2,
            "confidence": 3,
            "hedging": 2,
            "reason": "placeholder output",
        }
        results.append(result)
    return results


def run_llm_scores() -> None:
    sample_pairs = [
        {"question": "What was the sales growth rate?", "answer": "Sales growth was solid and we saw significant improvement."},
        {"question": "What caused gross margin pressure?", "answer": "We had a temporary logistics issue and we are focused on improving efficiency."},
    ]
    print(score_qa_pairs(sample_pairs))
