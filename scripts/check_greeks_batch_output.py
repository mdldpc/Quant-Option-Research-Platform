import pandas as pd
import numpy as np

FILE = (
    r"D:\Quant_Option_Project\data_parquet"
    r"\batch_fast_test"
    r"\trade_date=20260102"
    r"\greeks_spline.parquet"
)

df = pd.read_parquet(FILE)

print("Shape:")
print(df.shape)

greek_cols = [
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]

print("\nMissing Values:")
print(df[greek_cols].isna().sum())

print("\nInfinite Values:")
print(
    np.isinf(df[greek_cols])
    .sum()
)

print("\nSummary:")
print(
    df[greek_cols]
    .describe()
)

print("\nLargest Abs Delta:")
print(
    df.loc[
        df["delta"].abs().nlargest(10).index,
        [
            "symbol",
            "delta",
            "gamma",
            "vega",
            "theta",
        ],
    ]
)

print("\nLargest Vega:")
print(
    df.loc[
        df["vega"].nlargest(10).index,
        [
            "symbol",
            "delta",
            "gamma",
            "vega",
            "theta",
        ],
    ]
)

print("\nLargest Gamma:")
print(
    df.loc[
        df["gamma"].nlargest(10).index,
        [
            "symbol",
            "delta",
            "gamma",
            "vega",
            "theta",
        ],
    ]
)