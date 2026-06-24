import os
import numpy as np
import pandas as pd
from scipy.stats import norm

IV_SURFACE_PATH = r"D:\Quant_Option_Project\data_parquet\iv_spline_sample.parquet"
OPTION_PATH = r"D:\Quant_Option_Project\data_parquet\iv_sample.parquet"

OUT_PATH = r"D:\Quant_Option_Project\data_parquet\greeks_spline_sample.parquet"

RISK_FREE_RATE = 0.017


def black76_extended_greeks(F, K, T, r, sigma, option_type):

    if (
        F <= 0
        or K <= 0
        or T <= 0
        or sigma <= 0
    ):
        return pd.Series(
            [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
            ]
        )

    sqrt_T = np.sqrt(T)

    d1 = (
        np.log(F / K)
        + 0.5 * sigma * sigma * T
    ) / (sigma * sqrt_T)

    d2 = d1 - sigma * sqrt_T

    pdf = norm.pdf(d1)

    discount = np.exp(-r * T)

    if option_type == "C":

        delta = discount * norm.cdf(d1)

        theta = (
            -discount
            * F
            * pdf
            * sigma
            / (2 * sqrt_T)
            + r
            * discount
            * (
                F * norm.cdf(d1)
                - K * norm.cdf(d2)
            )
        )

    else:

        delta = -discount * norm.cdf(-d1)

        theta = (
            -discount
            * F
            * pdf
            * sigma
            / (2 * sqrt_T)
            + r
            * discount
            * (
                K * norm.cdf(-d2)
                - F * norm.cdf(-d1)
            )
        )

    gamma = (
        discount
        * pdf
        / (F * sigma * sqrt_T)
    )

    vega = (
        discount
        * F
        * pdf
        * sqrt_T
    )

    vanna = (
        -discount
        * pdf
        * d2
        / sigma
    )

    vomma = (
        vega
        * d1
        * d2
        / sigma
    )

    speed = (
        -gamma
        / F
        * (
            1
            + d1 / (sigma * sqrt_T)
        )
    )

    return pd.Series(
        [
            delta,
            gamma,
            vega,
            theta,
            vanna,
            vomma,
            speed,
        ]
    )


def main():

    os.makedirs(
        os.path.dirname(OUT_PATH),
        exist_ok=True,
    )

    print("Reading data...")

    option_df = pd.read_parquet(OPTION_PATH)
    surface_df = pd.read_parquet(IV_SURFACE_PATH)

    option_df["expiry_code"] = (
        option_df["symbol"]
        .str.extract(r"IO(\d{4})")[0]
    )

    option_df = option_df.merge(
        surface_df[
            [
                "expiry_code",
                "option_type",
                "strike",
                "smoothed_iv",
            ]
        ],
        on=[
            "expiry_code",
            "option_type",
            "strike",
        ],
        how="left",
    )

    print(
        "Rows with spline IV:",
        option_df["smoothed_iv"]
        .notna()
        .sum(),
    )

    df = option_df[
        option_df["smoothed_iv"]
        .notna()
    ].copy()

    greeks = df.apply(
        lambda row: black76_extended_greeks(
            row["future_price"],
            row["strike"],
            row["T"],
            RISK_FREE_RATE,
            row["smoothed_iv"],
            row["option_type"],
        ),
        axis=1,
    )

    greeks.columns = [
        "delta",
        "gamma",
        "vega",
        "theta",
        "vanna",
        "vomma",
        "speed",
    ]

    result = pd.concat(
        [df, greeks],
        axis=1,
    )

    print("\nGreek Summary:")
    print(
        result[
            [
                "delta",
                "gamma",
                "vega",
                "theta",
                "vanna",
                "vomma",
                "speed",
            ]
        ].describe()
    )

    print("\nSample:")
    print(
        result[
            [
                "symbol",
                "option_type",
                "strike",
                "future_price",
                "smoothed_iv",
                "delta",
                "gamma",
                "vega",
                "theta",
            ]
        ].head(20)
    )

    result.to_parquet(
        OUT_PATH,
        index=False,
    )

    print("\nSaved to:")
    print(OUT_PATH)


if __name__ == "__main__":
    main()