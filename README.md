# Earnings Call NLP Signal Engine

A research pipeline for turning raw earnings-call transcripts into tradeable signals and testing them with disciplined, out-of-sample evaluation.

## Project goal

The goal is to build a pipeline that:

- ingests transcript, price, factor, and earnings data
- cleans and parses transcript sections
- scores management tone with dictionary, transformer, and LLM-based methods
- engineers features that are known only at call time
- conducts honest event studies and controls for confounds
- reports results with proper out-of-sample discipline

## Repository structure

```text
Earnings-Call-NLP-Signal-Engine/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── run_all.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── ingest.py
│   ├── split.py
│   ├── score_finbert.py
│   ├── score_llm.py
│   ├── features.py
│   ├── event_study.py
│   └── reporting.py
├── results/
│   ├── charts/
│   ├── tables/
│   └── reports/
├── tests/
│   └── test_split.py
└── .github/
    └── workflows/
        └── ci.yml
```

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment template:

```bash
cp .env.example .env
```

4. Fill in any required API keys or configuration values in `.env`.

## Quick start

Run the full pipeline:

```bash
python run_all.py
```

## Data dictionary

| Table / artifact | Description |
| --- | --- |
| `data/raw/transcripts/*` | Raw transcript files or scraped transcripts |
| `data/raw/prices/*` | Daily adjusted prices from Yahoo Finance or alternative providers |
| `data/raw/factors/*` | Fama-French and momentum factors |
| `data/raw/earnings/*` | EPS / earnings data used for SUE controls |
| `data/processed/transcripts_clean.parquet` | Cleaned transcript data with sections split |
| `data/processed/features.parquet` | Engineered signal features and controls |
| `data/processed/event_study.parquet` | Event-study dataset with CAR windows |
| `results/charts/*` | Plots and visualizations |
| `results/tables/*` | Regression and summary tables |
| `results/reports/*` | Memo-ready output and summary documents |

## Method overview

This project follows the workflow described in the research plan:

- transcript ingestion and join keys on `ticker` and `date`
- splitting prepared remarks, Q&A, and speaker labels
- dictionary scoring using Loughran-McDonald lexicons
- sentence-level FinBERT scoring
- LLM scoring of Q&A pairs using structured JSON output
- feature engineering with look-ahead controls
- Fama-French event study and CAR estimation
- robustness and out-of-sample checks

## Important limitations

- survivorship bias from free price data
- LLM contamination risk from training data overlap
- transcript parsing failures
- look-ahead data leakage risk if event timing is wrong
- potential overfitting from multiple testing and window selection

## Reproducibility

This project is intended to be reproducible with deterministic file outputs and logged experiment choices. Keep a record of:

- data sources
- versions of packages used
- filtering decisions
- dataset date ranges
- parameter settings
- model choices
- out-of-sample splits

## Notes

This repository is a starter scaffold for the research workflow. The code modules contain placeholders and reference the key logic required for a production-quality pipeline.

---

See `src/` modules for extension points and `run_all.py` for the orchestration entry point.
