from pathlib import Path
import pandas as pd
import numpy as np

FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

GREEKS = [
    "implied_vol",
    "smoothed_iv",
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():
    print("Reading dataset...")

    df = pd.read_parquet(FILE)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nTrade Date Range:")
    print(df["trade_date"].min())
    print(df["trade_date"].max())

    print("\nUnique Trade Dates:")
    print(df["trade_date"].nunique())

    print("\nMissing Values:")
    print(df[GREEKS].isna().sum())

    print("\nInfinite Values:")
    for col in GREEKS:
        print(col, np.isinf(df[col]).sum())

    daily = (
        df.groupby("trade_date")
        .size()
        .sort_index()
    )

    print("\nDaily Row Count Summary:")
    print(daily.describe())

    print("\nSmallest Days:")
    print(daily.nsmallest(10))

    print("\nLargest Days:")
    print(daily.nlargest(10))

    print("\nCheck excluded date 20260505:")
    if "20260505" in set(df["trade_date"].astype(str)):
        print("WARNING: 20260505 exists in final dataset.")
    else:
        print("OK: 20260505 is excluded.")

    print("\nGreeks Summary:")
    print(
        df[
            [
                "implied_vol",
                "smoothed_iv",
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

    print("\nTop 10 rows:")
    print(df.head(10))


if __name__ == "__main__":
    main()