from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_results() -> None:
    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)

    event = pd.read_parquet("data/processed/event_study.parquet") if Path("data/processed/event_study.parquet").exists() else pd.DataFrame({"ticker": [], "CAR_10": []})
    summary = pd.DataFrame({
        "metric": ["tickers", "avg_car_10", "status"],
        "value": [len(event), float(event["CAR_10"].mean()) if not event.empty else 0.0, "demo pipeline complete"],
    })

    table_path = output_dir / "tables" / "pipeline_summary.csv"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(table_path, index=False)

    event.to_csv(output_dir / "tables" / "event_study_results.csv", index=False)
    print(f"Results saved to {table_path} and {output_dir / 'tables' / 'event_study_results.csv'}")
