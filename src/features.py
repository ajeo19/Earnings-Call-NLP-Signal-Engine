import pandas as pd


def build_features() -> pd.DataFrame:
    """Build a lightweight feature dataset with look-ahead-safe naming.

    In production, replace this with the actual feature engineering logic from
    the research plan: tone changes, qa-gap, hedge changes, and z-scored signals.
    """
    df = pd.DataFrame({
        "ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
        "call_date": pd.to_datetime(["2024-01-01", "2024-04-01", "2024-01-01", "2024-04-01"]),
        "finbert_prepared": [0.2, -0.1, 0.3, 0.1],
        "finbert_qa": [0.1, -0.2, 0.5, 0.2],
        "lm_uncertainty": [0.12, 0.10, 0.08, 0.09],
        "llm_evasiveness": [2, 4, 3, 5],
    })

    df = df.sort_values(["ticker", "call_date"]).reset_index(drop=True)
    df["tone_chg"] = df.groupby("ticker")["finbert_prepared"].diff()
    df["qa_gap"] = df["finbert_qa"] - df["finbert_prepared"]
    df["hedge_chg"] = df.groupby("ticker")["lm_uncertainty"].diff()

    for col in ["tone_chg", "qa_gap", "hedge_chg", "llm_evasiveness"]:
        df[f"{col}_z"] = (df[col] - df[col].mean()) / df[col].std(ddof=0)

    return df
