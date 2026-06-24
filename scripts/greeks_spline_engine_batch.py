import numpy as np
import pandas as pd
from scipy.stats import norm

RISK_FREE_RATE = 0.017


def black76_extended_greeks(F, K, T, r, sigma, option_type):
    if F <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return pd.Series([np.nan] * 7)

    sqrt_T = np.sqrt(T)
    discount = np.exp(-r * T)

    d1 = (
        np.log(F / K)
        + 0.5 * sigma * sigma * T
    ) / (sigma * sqrt_T)

    d2 = d1 - sigma * sqrt_T
    pdf = norm.pdf(d1)

    if option_type == "C":
        delta = discount * norm.cdf(d1)
        theta = (
            -discount * F * pdf * sigma / (2 * sqrt_T)
            + r * discount * (F * norm.cdf(d1) - K * norm.cdf(d2))
        )
    else:
        delta = -discount * norm.cdf(-d1)
        theta = (
            -discount * F * pdf * sigma / (2 * sqrt_T)
            + r * discount * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
        )

    gamma = discount * pdf / (F * sigma * sqrt_T)
    vega = discount * F * pdf * sqrt_T
    vanna = -discount * pdf * d2 / sigma
    vomma = vega * d1 * d2 / sigma
    speed = -gamma / F * (1 + d1 / (sigma * sqrt_T))

    return pd.Series(
        [delta, gamma, vega, theta, vanna, vomma, speed]
    )


def add_spline_greeks(iv_df, surface_df, r=RISK_FREE_RATE):
    df = iv_df.merge(
        surface_df[
            [
                "expiry_code",
                "option_type",
                "strike",
                "smoothed_iv",
            ]
        ],
        on=["expiry_code", "option_type", "strike"],
        how="left",
    )

    df = df[df["smoothed_iv"].notna()].copy()

    greek_cols = [
        "delta",
        "gamma",
        "vega",
        "theta",
        "vanna",
        "vomma",
        "speed",
    ]

    df[greek_cols] = df.apply(
        lambda row: black76_extended_greeks(
            F=row["future_price"],
            K=row["strike"],
            T=row["T"],
            r=r,
            sigma=row["smoothed_iv"],
            option_type=row["option_type"],
        ),
        axis=1,
    )

    return df