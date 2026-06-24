import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm

sys.path.append(os.path.dirname(__file__))

from contract_calendar import time_to_expiry

RISK_FREE_RATE = 0.017


def black76_price(F, K, T, r, sigma, option_type):
    if F <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return np.nan

    sqrt_T = np.sqrt(T)

    d1 = (
        np.log(F / K)
        + 0.5 * sigma * sigma * T
    ) / (sigma * sqrt_T)

    d2 = d1 - sigma * sqrt_T

    discount = np.exp(-r * T)

    if option_type == "C":
        return discount * (
            F * norm.cdf(d1)
            - K * norm.cdf(d2)
        )

    if option_type == "P":
        return discount * (
            K * norm.cdf(-d2)
            - F * norm.cdf(-d1)
        )

    return np.nan


def implied_vol_black76(option_price, F, K, T, r, option_type):
    if option_price <= 0 or F <= 0 or K <= 0 or T <= 0:
        return np.nan

    def objective(sigma):
        return (
            black76_price(
                F=F,
                K=K,
                T=T,
                r=r,
                sigma=sigma,
                option_type=option_type,
            )
            - option_price
        )

    try:
        return brentq(
            objective,
            1e-6,
            5.0,
            maxiter=100,
        )
    except ValueError:
        return np.nan


def add_iv_cache(df, trade_date, r=RISK_FREE_RATE):
    """
    Input:
        df: 10s-resampled option table
        trade_date: datetime

    Output:
        df + T + implied_vol
    """

    df = df.copy()

    df["T"] = df["expiry_code"].apply(
        lambda x: time_to_expiry(
            trade_date,
            x,
        )
    )

    df = df[
        df["T"].notna()
        & (df["T"] > 0)
        & (df["option_price"] > 0)
        & (df["future_price"] > 0)
        & (df["strike"] > 0)
    ].copy()
    if len(df) == 0:
        print("No valid rows after T / price filtering.")
        df["implied_vol"] = np.nan
        return df

    key_cols = [
        "option_type",
        "strike",
        "option_price",
        "future_price",
        "T",
    ]

    unique_df = (
        df[key_cols]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    print("Unique IV keys:", len(unique_df))
    print("Original rows:", len(df))
    print("Compression ratio:", len(unique_df) / len(df))

    unique_df["implied_vol"] = unique_df.apply(
        lambda row: implied_vol_black76(
            option_price=row["option_price"],
            F=row["future_price"],
            K=row["strike"],
            T=row["T"],
            r=r,
            option_type=row["option_type"],
        ),
        axis=1,
    )

    result = df.merge(
        unique_df,
        on=key_cols,
        how="left",
    )

    print(
        "Valid IV ratio:",
        result["implied_vol"].notna().mean()
    )

    return result