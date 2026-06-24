import pandas as pd

FILE = (
    r"D:\Quant_Option_Project\data_parquet\batch_2026"
    r"\trade_date=20260102"
    r"\greeks_spline.parquet"
)

df = pd.read_parquet(FILE)

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nHead:")
print(df.head(20))

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