import numpy as np
import pandas as pd

GREEKS_PATH = r"D:\Quant_Option_Project\data_parquet\greeks_sample.parquet"

GREEK_COLS = [
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():
    df = pd.read_parquet(GREEKS_PATH)

    print("Shape:")
    print(df.shape)

    print("\nMissing values:")
    print(df[GREEK_COLS].isna().sum())

    print("\nInfinite values:")
    print(np.isinf(df[GREEK_COLS]).sum())

    print("\nSummary:")
    print(df[GREEK_COLS].describe())

    print("\nExtreme rows:")
    print(
        df.sort_values("vomma", ascending=False)[
            [
                "symbol",
                "option_type",
                "strike",
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
        ].head(20)
    )


if __name__ == "__main__":
    main()