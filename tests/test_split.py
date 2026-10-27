from src.event_study import run_event_study
from src.features import run_feature_build
from src.ingest import run_ingest
from src.reporting import save_results
from src.score_finbert import run_finbert_scores
from src.score_llm import run_llm_scores
from src.split import run_split


def main() -> None:
    print("[1/7] Ingesting demo datasets...")
    run_ingest()

    print("[2/7] Splitting transcripts...")
    run_split()

    print("[3/7] Scoring prepared remarks and Q&A with FinBERT...")
    run_finbert_scores()

    print("[4/7] Scoring Q&A with LLM-style rubric...")
    run_llm_scores()

    print("[5/7] Building signal features...")
    run_feature_build()

    print("[6/7] Running event study...")
    run_event_study()

    print("[7/7] Exporting pipeline summary...")
    save_results()

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
