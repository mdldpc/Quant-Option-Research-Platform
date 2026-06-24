import pandas as pd
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

OPTION_TABLE = (
    r"D:\Quant_Option_Project\data_parquet"
    r"\batch_test\trade_date=20250102\option_table.parquet"
)

RISK_FREE_RATE = 0.017


def black76_price(
    F,
    K,
    T,
    r,
    sigma,
    option_type,
):

    if sigma <= 0:
        return np.nan

    sqrt_T = np.sqrt(T)

    d1 = (
        np.log(F / K)
        + 0.5 * sigma**2 * T
    ) / (sigma * sqrt_T)

    d2 = d1 - sigma * sqrt_T

    discount = np.exp(-r * T)

    if option_type == "C":
        return (
            discount
            * (
                F * norm.cdf(d1)
                - K * norm.cdf(d2)
            )
        )

    else:
        return (
            discount
            * (
                K * norm.cdf(-d2)
                - F * norm.cdf(-d1)
            )
        )


def implied_vol_black76(
    option_price,
    F,
    K,
    T,
    r,
    option_type,
):

    if (
        option_price <= 0
        or F <= 0
        or K <= 0
        or T <= 0
    ):
        return np.nan

    def objective(sigma):

        return (
            black76_price(
                F,
                K,
                T,
                r,
                sigma,
                option_type,
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

    except:
        return np.nan


print("Reading option table...")

df = pd.read_parquet(OPTION_TABLE)

print("\nTotal Rows:")
print(len(df))

# ---------------------------
# TEMP
# 先只测20万行
# ---------------------------

df = df.head(200_000).copy()

print("\nTest Rows:")
print(len(df))

# ---------------------------
# T
# ---------------------------

df["T"] = 0.043835616438356165

# ---------------------------
# Unique Cache Key
# ---------------------------

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

print("\nUnique IV Keys:")
print(len(unique_df))

print("\nCompression Ratio:")
print(
    len(unique_df)
    / len(df)
)

# ---------------------------
# Solve IV Once
# ---------------------------

print("\nCalculating Unique IV...")

unique_df["implied_vol"] = unique_df.apply(
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

print("\nValid IV Ratio:")
print(
    unique_df["implied_vol"]
    .notna()
    .mean()
)

# ---------------------------
# Merge Back
# ---------------------------

print("\nMerging back...")

result = df.merge(
    unique_df,
    on=key_cols,
    how="left",
)

print("\nFinal Rows:")
print(len(result))

print("\nMissing IV:")
print(
    result["implied_vol"]
    .isna()
    .mean()
)

print("\nIV Summary:")
print(
    result["implied_vol"]
    .describe()
)