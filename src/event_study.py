from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    out = df.sort_values(["ticker", "call_date"]).copy().reset_index(drop=True)
    out["quarter"] = out["call_date"].dt.to_period("Q").astype(str)

    for col in ["finbert_prepared", "finbert_qa", "lm_uncertainty", "llm_evasiveness"]:
        if col not in out.columns:
            out[col] = 0.0

    out["tone_chg"] = out.groupby("ticker")["finbert_prepared"].diff().fillna(0.0)
    out["qa_gap"] = out["finbert_qa"] - out["finbert_prepared"]
    out["hedge_chg"] = out.groupby("ticker")["lm_uncertainty"].diff().fillna(0.0)
    out["evasion"] = out["llm_evasiveness"]

    for c in ["tone_chg", "qa_gap", "hedge_chg", "evasion"]:
        std = out[c].std(ddof=0)
        out[f"{c}_z"] = 0.0 if std == 0 else (out[c] - out[c].mean()) / std

    out["signal"] = 0.25 * out["tone_chg_z"] + 0.25 * out["qa_gap_z"] + 0.25 * out["hedge_chg_z"] + 0.25 * out["evasion_z"]
    return out


def run_feature_build() -> None:
    import pandas as pd

    transcript = pd.read_parquet("data/processed/transcripts_clean.parquet")
    finbert = pd.read_parquet("data/processed/finbert_scores.parquet")
    llm = pd.read_parquet("data/processed/llm_scores.parquet")

    df = transcript.merge(finbert[["ticker", "call_date", "finbert_prepared", "finbert_qa"]], on=["ticker", "call_date"], how="left")
    df["lm_uncertainty"] = 0.1
    df["llm_evasiveness"] = llm["evasiveness"].values[:len(df)] if len(llm) >= len(df) else [0.0 for _ in range(len(df))]

    features = build_features(df)
    features.to_parquet("data/processed/features.parquet", index=False)
    print("Feature engineering complete: data/processed/features.parquet")
