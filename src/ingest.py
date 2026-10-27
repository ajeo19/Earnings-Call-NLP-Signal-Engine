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


def run_ingest() -> None:
    """Placeholder data ingestion pipeline.

    Replace this with actual transcript, price, factor, and earnings downloads.
    """
    ensure_directories()

    # Example empty dataset placeholders to ensure the project runs cleanly.
    df = pd.DataFrame({
        "ticker": [],
        "call_date": [],
        "transcript": [],
        "source": [],
    })

    save_parquet(df, "data/processed/transcripts_raw.parquet")
    print("Ingest pipeline ready; add your actual download logic here.")
