from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def abnormal_returns(stock_ret: pd.Series, factors: pd.DataFrame, est_window: pd.Index, event_window: pd.Index) -> pd.Series:
    X = sm.add_constant(factors.loc[est_window])
    y = stock_ret.loc[est_window] - factors.loc[est_window, "RF"]
    beta = sm.OLS(y, X).fit().params
    pred = sm.add_constant(factors.loc[event_window]).dot(beta)
    actual = stock_ret.loc[event_window] - factors.loc[event_window, "RF"]
    return actual - pred


def compute_car(ar: pd.Series) -> float:
    return float(ar.sum())


def run_event_study() -> None:
    prices = pd.read_parquet("data/processed/prices.parquet")
    factors = pd.read_parquet("data/processed/factors.parquet")
    features = pd.read_parquet("data/processed/features.parquet")

    if prices.empty or factors.empty or features.empty:
        print("No event-study data available; skipping run_event_study.")
        return

    dates = pd.to_datetime(factors["date"])
    factor_df = factors.set_index("date").sort_index()
    prices = prices.sort_values(["ticker", "date"]).set_index("date")

    results = []
    for ticker in prices["ticker"].unique():
        ticker_ret = prices.loc[prices["ticker"] == ticker, "returns"].copy()
        ticker_ret.index = pd.to_datetime(ticker_ret.index)
        est_window = ticker_ret.index[:15]
        event_window = ticker_ret.index[15:25]
        if len(est_window) < 2 or len(event_window) == 0:
            continue
        event_factors = factor_df.loc[event_window]
        ar = abnormal_returns(ticker_ret, event_factors, est_window, event_window)
        results.append({
            "ticker": ticker,
            "CAR_10": compute_car(ar[:10]),
            "CAR_all": compute_car(ar),
            "n_days": len(ar),
        })

    out = pd.DataFrame(results)
    out.to_parquet("data/processed/event_study.parquet", index=False)
    print(f"Event study complete: {len(out)} ticker results saved to data/processed/event_study.parquet")
