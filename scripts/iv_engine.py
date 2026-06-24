import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm

sys.path.append(os.path.dirname(__file__))

from contract_calendar import time_to_expiry


OPTION_TABLE = r"D:\Quant_Option_Project\data_parquet\option_table_sample.parquet"
OUT_PATH = r"D:\Quant_Option_Project\data_parquet\iv_sample.parquet"

TRADE_DATE = datetime(2025, 1, 1)
RISK_FREE_RATE = 0.017

SAMPLE_EXPIRY = "2501"
SAMPLE_SIZE = 2000


def black76_price(F, K, T, r, sigma, option_type):
    if F <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return np.nan

    d1 = (np.log(F / K) + 0.5 * sigma * sigma * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    discount = np.exp(-r * T)

    if option_type == "C":
        return discount * (F * norm.cdf(d1) - K * norm.cdf(d2))

    if option_type == "P":
        return discount * (K * norm.cdf(-d2) - F * norm.cdf(-d1))

    return np.nan


def implied_vol_black76(option_price, F, K, T, r, option_type):
    if option_price <= 0 or F <= 0 or K <= 0 or T <= 0:
        return np.nan

    def objective(sigma):
        return black76_price(F, K, T, r, sigma, option_type) - option_price

    try:
        return brentq(
            objective,
            1e-6,
            5.0,
            maxiter=100
        )
    except ValueError:
        return np.nan


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print("Reading option table...")
    df = pd.read_parquet(OPTION_TABLE)

    df["expiry_code"] = df["symbol"].str.extract(r"IO(\d{4})")[0]

    df = df[df["expiry_code"] == SAMPLE_EXPIRY].copy()

    df["T"] = df["expiry_code"].apply(
        lambda x: time_to_expiry(TRADE_DATE, x)
    )

    df = df[
        (df["option_price"] > 0)
        & (df["future_price"] > 0)
        & (df["strike"] > 0)
        & (df["T"] > 0)
    ].copy()

    df = df.head(SAMPLE_SIZE).copy()

    print("Sample rows:", len(df))
    print("Expiry:", SAMPLE_EXPIRY)
    print("T:", df["T"].iloc[0])

    print("Calculating implied volatility...")

    df["implied_vol"] = df.apply(
        lambda row: implied_vol_black76(
            option_price=row["option_price"],
            F=row["future_price"],
            K=row["strike"],
            T=row["T"],
            r=RISK_FREE_RATE,
            option_type=row["option_type"],
        ),
        axis=1
    )

    print("\nIV Summary:")
    print(df["implied_vol"].describe())

    print("\nNaN IV ratio:")
    print(df["implied_vol"].isna().mean())

    print("\nSample:")
    print(df[
        [
            "symbol",
            "option_type",
            "strike",
            "option_price",
            "future_price",
            "T",
            "implied_vol"
        ]
    ].head(30))

    df.to_parquet(OUT_PATH, index=False)

    print("\nSaved to:")
    print(OUT_PATH)


if __name__ == "__main__":
    main()