import os
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm
from scipy.interpolate import UnivariateSpline

sys.path.append(os.path.dirname(__file__))

from contract_calendar import time_to_expiry


RAW_ROOTS = [
    Path(r"F:\CFFEX.2025"),
    Path(r"F:\CFFEX.2026"),
]

OUT_ROOT = Path(r"D:\Quant_Option_Project\data_parquet\batch_test")

RISK_FREE_RATE = 0.017
MAX_FILES = 3

USECOLS = [
    "iRecvTime",
    "symbol",
    "lastPrice",
    "BP1",
    "AP1",
    "volume",
    "openInterest",
]


def black76_price(F, K, T, r, sigma, option_type):
    if F <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return np.nan

    sqrt_T = np.sqrt(T)
    d1 = (np.log(F / K) + 0.5 * sigma * sigma * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    discount = np.exp(-r * T)

    if option_type == "C":
        return discount * (F * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == "P":
        return discount * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
    return np.nan


def implied_vol_black76(option_price, F, K, T, r, option_type):
    if option_price <= 0 or F <= 0 or K <= 0 or T <= 0:
        return np.nan

    def objective(sigma):
        return black76_price(F, K, T, r, sigma, option_type) - option_price

    try:
        return brentq(objective, 1e-6, 5.0, maxiter=100)
    except ValueError:
        return np.nan


def black76_extended_greeks(F, K, T, r, sigma, option_type):
    if F <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return pd.Series([np.nan] * 7)

    sqrt_T = np.sqrt(T)
    discount = np.exp(-r * T)

    d1 = (np.log(F / K) + 0.5 * sigma * sigma * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    pdf = norm.pdf(d1)

    if option_type == "C":
        delta = discount * norm.cdf(d1)
        theta = (
            -discount * F * pdf * sigma / (2 * sqrt_T)
            + RISK_FREE_RATE * discount * (F * norm.cdf(d1) - K * norm.cdf(d2))
        )
    else:
        delta = -discount * norm.cdf(-d1)
        theta = (
            -discount * F * pdf * sigma / (2 * sqrt_T)
            + RISK_FREE_RATE * discount * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
        )

    gamma = discount * pdf / (F * sigma * sqrt_T)
    vega = discount * F * pdf * sqrt_T
    vanna = -discount * pdf * d2 / sigma
    vomma = vega * d1 * d2 / sigma
    speed = -gamma / F * (1 + d1 / (sigma * sqrt_T))

    return pd.Series([delta, gamma, vega, theta, vanna, vomma, speed])


def build_option_table(raw_path):
    df = pd.read_csv(
        raw_path,
        compression="xz",
        usecols=USECOLS,
    )

    df["symbol"] = df["symbol"].str.strip()

    fut = df[df["symbol"].str.startswith("IF")].copy()
    opt = df[df["symbol"].str.startswith("IO")].copy()

    fut = fut[["iRecvTime", "symbol", "lastPrice"]].rename(
        columns={
            "symbol": "fut_symbol",
            "lastPrice": "future_price",
        }
    )

    parts = opt["symbol"].str.split("-", expand=True)

    opt["expiry_code"] = parts[0].str[2:]
    opt["option_type"] = parts[1]
    opt["strike"] = parts[2].astype(float)
    opt["fut_symbol"] = "IF" + opt["expiry_code"]

    def build_price(row):
        bp = row["BP1"]
        ap = row["AP1"]

        if bp > 0 and ap > 0:
            return (bp + ap) / 2
        elif bp > 0:
            return bp
        elif ap > 0:
            return ap
        return np.nan

    opt["option_price"] = opt.apply(build_price, axis=1)
    opt = opt[opt["option_price"].notna()].copy()

    valid_futs = set(fut["fut_symbol"].unique())
    opt = opt[opt["fut_symbol"].isin(valid_futs)].copy()

    opt = opt.sort_values("iRecvTime")
    fut = fut.sort_values("iRecvTime")

    merged = pd.merge_asof(
        opt,
        fut,
        by="fut_symbol",
        on="iRecvTime",
        direction="nearest",
        tolerance=5_000_000_000,
    )

    result = merged[
        [
            "iRecvTime",
            "symbol",
            "fut_symbol",
            "expiry_code",
            "option_type",
            "strike",
            "option_price",
            "future_price",
            "BP1",
            "AP1",
            "volume",
            "openInterest",
        ]
    ].copy()

    result = result[
        (result["future_price"].notna())
        & (result["future_price"] > 0)
        & (result["option_price"] > 0)
        & (result["strike"] > 0)
    ].copy()

    return result


def add_iv(option_df, trade_date):
    df = option_df.copy()

    df["T"] = df["expiry_code"].apply(
        lambda x: time_to_expiry(trade_date, x)
    )

    df = df[df["T"].notna() & (df["T"] > 0)].copy()

    df["implied_vol"] = df.apply(
        lambda row: implied_vol_black76(
            option_price=row["option_price"],
            F=row["future_price"],
            K=row["strike"],
            T=row["T"],
            r=RISK_FREE_RATE,
            option_type=row["option_type"],
        ),
        axis=1,
    )

    return df


def build_spline_surface(iv_df):
    df = iv_df[iv_df["implied_vol"].notna()].copy()

    results = []

    for (expiry_code, option_type), group in df.groupby(["expiry_code", "option_type"]):
        smile = (
            group.groupby("strike", as_index=False)
            .agg(
                implied_vol=("implied_vol", "median"),
                future_price=("future_price", "median"),
                n_obs=("implied_vol", "count"),
            )
            .sort_values("strike")
        )

        if len(smile) < 4:
            continue

        x = smile["strike"].to_numpy()
        y = smile["implied_vol"].to_numpy()

        spline = UnivariateSpline(x, y, k=3, s=0.0005)
        smile["smoothed_iv"] = spline(x)

        smile["expiry_code"] = expiry_code
        smile["option_type"] = option_type

        results.append(smile)

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)


def add_spline_greeks(iv_df, surface_df):
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
            r=RISK_FREE_RATE,
            sigma=row["smoothed_iv"],
            option_type=row["option_type"],
        ),
        axis=1,
    )

    return df


def extract_trade_date(raw_path):
    # filename example: CFFEX.IF.20250101.csv.xz
    date_str = raw_path.name.split(".")[2]
    return datetime.strptime(date_str, "%Y%m%d")


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    files = []
    for root in RAW_ROOTS:
        files.extend(sorted(root.glob("*.csv.xz")))

    files = sorted(files)[:MAX_FILES]

    print("Files to process:", len(files))

    for raw_path in files:
        trade_date = extract_trade_date(raw_path)
        trade_date_str = trade_date.strftime("%Y%m%d")

        print("\n" + "=" * 60)
        print("Processing:", raw_path.name)
        print("Trade date:", trade_date_str)

        out_dir = OUT_ROOT / f"trade_date={trade_date_str}"
        out_dir.mkdir(parents=True, exist_ok=True)

        try:
            option_table = build_option_table(raw_path)
            print("Option table rows:", len(option_table))
            option_table.to_parquet(out_dir / "option_table.parquet", index=False)

            iv_table = add_iv(option_table, trade_date)
            print("IV table rows:", len(iv_table))
            print("Valid IV ratio:", iv_table["implied_vol"].notna().mean())
            iv_table.to_parquet(out_dir / "iv_table.parquet", index=False)

            surface = build_spline_surface(iv_table)
            print("Spline surface rows:", len(surface))
            surface.to_parquet(out_dir / "iv_spline.parquet", index=False)

            greeks = add_spline_greeks(iv_table, surface)
            print("Greeks rows:", len(greeks))
            greeks.to_parquet(out_dir / "greeks_spline.parquet", index=False)

            print("Saved to:", out_dir)

        except Exception as e:
            print("FAILED:", raw_path.name)
            print("ERROR:", repr(e))


if __name__ == "__main__":
    main()