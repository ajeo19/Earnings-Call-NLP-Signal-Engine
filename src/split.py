from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ensure_directories


def read_parquet(path: str | Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def save_parquet(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def build_demo_transcript_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ticker": ["AAPL", "MSFT", "NVDA", "AMZN"],
            "call_date": pd.to_datetime([
                "2024-01-30",
                "2024-01-31",
                "2024-02-01",
                "2024-02-02",
            ]),
            "transcript": [
                "Prepared remarks. We delivered strong revenue growth and improved operating margin. Question and answer session. Analysts asked about guidance and demand mix. Management noted that sales may improve later in the year depending on demand.",
                "Prepared remarks. The cloud business grew nicely and we remain confident in execution. Question and answer session. Analysts asked about AI demand and customer concentration. Management said the market remains healthy and growth should continue.",
                "Prepared remarks. We saw robust demand and a strong quarter despite supply constraints. Question and answer session. Analysts challenged the guidance and asked about inventory. Management said it is too early to comment on the next quarter and we are evaluating the situation.",
                "Prepared remarks. We remain disciplined and continue to invest for long-run growth. Question and answer session. Analysts asked about retail performance and margin leverage. Management said results were resilient and may improve as costs normalize.",
            ],
            "source": ["demo", "demo", "demo", "demo"],
        }
    )


def build_demo_price_dataset() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    rows = []
    for ticker in ["AAPL", "MSFT", "NVDA", "AMZN"]:
        base = 100 + hash(ticker) % 50
        for i, d in enumerate(dates):
            ret = 0.0008 + ((i % 5) * 0.0006) + ((hash(ticker) % 7) * 0.0002)
            rows.append({
                "ticker": ticker,
                "date": d,
                "adj_close": base * (1 + ret * (i + 1)) * (1 + (0.0005 * (i % 3))),
                "returns": ret,
            })
    return pd.DataFrame(rows)


def build_demo_factor_dataset() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    return pd.DataFrame({
        "date": dates,
        "Mkt_RF": [0.0008 + i * 0.0002 for i in range(len(dates))],
        "SMB": [0.0002 + (i % 7) * 0.0001 for i in range(len(dates))],
        "HML": [0.0001 + (i % 5) * 0.00015 for i in range(len(dates))],
        "RF": [0.00003 for _ in dates],
    })


def build_demo_earnings_dataset() -> pd.DataFrame:
    return pd.DataFrame({
        "ticker": ["AAPL", "MSFT", "NVDA", "AMZN"],
        "quarter": ["2024Q1", "2024Q1", "2024Q1", "2024Q1"],
        "eps": [5.1, 2.9, 1.8, 1.5],
        "sue": [0.3, 0.5, -0.2, 0.4],
    })


def run_ingest() -> None:
    ensure_directories()
    transcript_df = build_demo_transcript_dataset()
    prices_df = build_demo_price_dataset()
    factors_df = build_demo_factor_dataset()
    earnings_df = build_demo_earnings_dataset()

    save_parquet(transcript_df, "data/processed/transcripts_raw.parquet")
    save_parquet(prices_df, "data/processed/prices.parquet")
    save_parquet(factors_df, "data/processed/factors.parquet")
    save_parquet(earnings_df, "data/processed/earnings.parquet")

    print("Ingest complete: demo transcript, prices, factors, and earnings data prepared.")
