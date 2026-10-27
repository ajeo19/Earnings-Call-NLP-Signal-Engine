from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_results() -> None:
    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame(
        {
            "metric": ["status", "notes"],
            "value": ["ready", "Starter pipeline includes working demo modules for ingestion, cleaning, scoring, and event study."],
        }
    )

    table_path = output_dir / "tables" / "pipeline_summary.csv"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(table_path, index=False)
    print(f"Saved summary file to {table_path}")
