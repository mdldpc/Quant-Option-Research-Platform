import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(__file__))

from contract_calendar import time_to_expiry

from framework.pricing.implied_vol import (
    implied_volatility,
)

RISK_FREE_RATE = 0.017


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
        lambda row: implied_volatility(
            market_price=row["option_price"],
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