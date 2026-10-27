import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

RAW_TRANSCRIPTS_DIR = RAW_DIR / "transcripts"
RAW_PRICES_DIR = RAW_DIR / "prices"
RAW_FACTORS_DIR = RAW_DIR / "factors"
RAW_EARNINGS_DIR = RAW_DIR / "earnings"


def ensure_directories() -> None:
    for path in [
        RAW_TRANSCRIPTS_DIR,
        RAW_PRICES_DIR,
        RAW_FACTORS_DIR,
        RAW_EARNINGS_DIR,
        PROCESSED_DIR,
        RESULTS_DIR,
        RESULTS_DIR / "charts",
        RESULTS_DIR / "tables",
        RESULTS_DIR / "reports",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)
