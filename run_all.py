from src.ingest import run_ingest
from src.split import run_split
from src.score_finbert import run_finbert_scores
from src.score_llm import run_llm_scores
from src.features import build_features
from src.event_study import run_event_study
from src.reporting import save_results


def main() -> None:
    print("[1/6] Ingesting datasets...")
    run_ingest()

    print("[2/6] Splitting transcripts...")
    run_split()

    print("[3/6] Scoring with FinBERT...")
    run_finbert_scores()

    print("[4/6] Scoring with LLM...")
    run_llm_scores()

    print("[5/6] Building features...")
    build_features()

    print("[6/6] Running event study and exports...")
    run_event_study()
    save_results()

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
