from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Construct basic, look-ahead-safe features from call-level data.

    The design mirrors the research plan: compare current vs prior quarter tone,
    Q&A relative to prepared remarks, and hedge/evasion intensity.
    """
    if df.empty:
        return df.copy()

    out = df.sort_values(["ticker", "call_date"]).copy().reset_index(drop=True)
    out["quarter"] = out["call_date"].dt.to_period("Q").astype(str)

    if "finbert_prepared" in out.columns:
        out["tone_chg"] = out.groupby("ticker")["finbert_prepared"].diff()
    else:
        out["tone_chg"] = 0.0

    if "finbert_qa" in out.columns and "finbert_prepared" in out.columns:
        out["qa_gap"] = out["finbert_qa"] - out["finbert_prepared"]
    else:
        out["qa_gap"] = 0.0

    if "lm_uncertainty" in out.columns:
        out["hedge_chg"] = out.groupby("ticker")["lm_uncertainty"].diff()
    else:
        out["hedge_chg"] = 0.0

    if "llm_evasiveness" in out.columns:
        out["evasion"] = out["llm_evasiveness"]
    else:
        out["evasion"] = 0.0

    for col in ["tone_chg", "qa_gap", "hedge_chg", "evasion"]:
        if out[col].std(ddof=0) == 0:
            out[f"{col}_z"] = 0.0
        else:
            out[f"{col}_z"] = (out[col] - out[col].mean()) / out[col].std(ddof=0)

    return out


def run_feature_demo() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
            "call_date": pd.to_datetime(["2024-01-01", "2024-04-01", "2024-01-01", "2024-04-01"]),
            "finbert_prepared": [0.2, -0.1, 0.3, 0.1],
            "finbert_qa": [0.1, -0.2, 0.5, 0.2],
            "lm_uncertainty": [0.12, 0.10, 0.08, 0.09],
            "llm_evasiveness": [2, 4, 3, 5],
        }
    )
    result = build_features(df)
    print(result[["ticker", "call_date", "tone_chg", "qa_gap", "hedge_chg", "evasion", "qa_gap_z"]])
    return result
