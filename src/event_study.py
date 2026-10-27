from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def abnormal_returns(stock_ret: pd.Series, factors: pd.DataFrame, est_window: pd.Index, event_window: pd.Index) -> pd.Series:
    """Estimate abnormal returns using a factor model on the estimation window."""
    X = sm.add_constant(factors.loc[est_window])
    y = stock_ret.loc[est_window] - factors.loc[est_window, "RF"]
    beta = sm.OLS(y, X).fit().params
    pred = sm.add_constant(factors.loc[event_window]).dot(beta)
    actual = stock_ret.loc[event_window] - factors.loc[event_window, "RF"]
    return actual - pred


def compute_car(ar: pd.Series) -> float:
    return float(ar.sum())


def run_event_study() -> None:
    dates = pd.date_range("2024-01-01", periods=12, freq="D")
    stock_ret = pd.Series(np.linspace(0.001, 0.03, len(dates)), index=dates)
    factors = pd.DataFrame(
        {
            "RF": np.full(len(dates), 0.0002),
            "Mkt_RF": np.linspace(0.0005, 0.015, len(dates)),
        },
        index=dates,
    )

    est_window = dates[:7]
    event_window = dates[7:]
    ar = abnormal_returns(stock_ret, factors, est_window, event_window)
    print({
        "CAR_1_5": compute_car(ar[:5]),
        "CAR_total": compute_car(ar),
        "days": len(ar),
    })
