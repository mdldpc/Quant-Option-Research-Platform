import os
import numpy as np
import pandas as pd
from scipy.stats import norm

IV_PATH = r"D:\Quant_Option_Project\data_parquet\iv_sample.parquet"
OUT_PATH = r"D:\Quant_Option_Project\data_parquet\greeks_sample.parquet"

RISK_FREE_RATE = 0.017


def black76_extended_greeks(F, K, T, r, sigma, option_type):
    if F <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return {
            "delta": np.nan,
            "gamma": np.nan,
            "vega": np.nan,
            "theta": np.nan,
            "vanna": np.nan,
            "vomma": np.nan,
            "speed": np.nan,
        }

    sqrt_T = np.sqrt(T)
    discount = np.exp(-r * T)

    d1 = (np.log(F / K) + 0.5 * sigma * sigma * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T

    pdf_d1 = norm.pdf(d1)

    if option_type == "C":
        delta = discount * norm.cdf(d1)
        theta = (
            -discount * F * pdf_d1 * sigma / (2 * sqrt_T)
            + r * discount * (F * norm.cdf(d1) - K * norm.cdf(d2))
        )

    elif option_type == "P":
        delta = -discount * norm.cdf(-d1)
        theta = (
            -discount * F * pdf_d1 * sigma / (2 * sqrt_T)
            + r * discount * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
        )

    else:
        delta = np.nan
        theta = np.nan

    gamma = discount * pdf_d1 / (F * sigma * sqrt_T)
    vega = discount * F * pdf_d1 * sqrt_T

    vanna = -discount * pdf_d1 * d2 / sigma
    vomma = vega * d1 * d2 / sigma

    speed = -gamma / F * (
        1 + d1 / (sigma * sqrt_T)
    )

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "vanna": vanna,
        "vomma": vomma,
        "speed": speed,
    }


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print("Reading IV sample...")
    df = pd.read_parquet(IV_PATH)

    df = df[df["implied_vol"].notna()].copy()

    print("Rows with valid IV:", len(df))

    greeks = df.apply(
        lambda row: black76_extended_greeks(
            F=row["future_price"],
            K=row["strike"],
            T=row["T"],
            r=RISK_FREE_RATE,
            sigma=row["implied_vol"],
            option_type=row["option_type"],
        ),
        axis=1,
        result_type="expand",
    )

    result = pd.concat([df, greeks], axis=1)

    greek_cols = [
        "delta",
        "gamma",
        "vega",
        "theta",
        "vanna",
        "vomma",
        "speed",
    ]

    print("\nGreek Summary:")
    print(result[greek_cols].describe())

    print("\nSample:")
    print(
        result[
            [
                "symbol",
                "option_type",
                "strike",
                "option_price",
                "future_price",
                "implied_vol",
                "delta",
                "gamma",
                "vega",
                "theta",
                "vanna",
                "vomma",
                "speed",
            ]
        ].head(30)
    )

    result.to_parquet(OUT_PATH, index=False)

    print("\nSaved to:")
    print(OUT_PATH)


if __name__ == "__main__":
    main()