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


def build_demo_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
            "call_date": pd.to_datetime(["2024-01-01", "2024-04-01", "2024-01-01", "2024-04-01"]),
            "transcript": [
                "Prepared remarks. Question and answer session. Management discussed guidance.",
                "Prepared remarks. Question and answer session. Management discussed margins.",
                "Prepared remarks. Question and answer session. Management discussed cloud revenue.",
                "Prepared remarks. Question and answer session. Management discussed AI adoption.",
            ],
            "source": ["demo", "demo", "demo", "demo"],
        }
    )


def run_ingest() -> None:
    """Generate a local demo dataset for a working pipeline.

    Replace this with real transcript, price, factor, and earnings ingestion for
    production use. This version is intentionally deterministic and fast.
    """
    ensure_directories()
    df = build_demo_dataset()
    save_parquet(df, "data/processed/transcripts_raw.parquet")
    print("Demo ingest complete: data/processed/transcripts_raw.parquet")
