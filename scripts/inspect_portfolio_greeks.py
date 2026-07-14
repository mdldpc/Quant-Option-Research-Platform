import pandas as pd

df = pd.read_parquet("research/datasets/portfolio_greeks_2026H1.parquet")

print("=" * 80)
print("Shape")
print("=" * 80)
print(df.shape)

print()

print("=" * 80)
print("Columns")
print("=" * 80)
print(df.columns.tolist())

print()

print("=" * 80)
print("Trades")
print("=" * 80)
print(df["trade_id"].value_counts().sort_index())

print()

print("=" * 80)
print("Head")
print("=" * 80)
print(df.head())

print()

print("=" * 80)
print("Net Greeks Summary")
print("=" * 80)
print(
    df[
        [
            "net_delta",
            "net_gamma",
            "net_vega",
            "net_theta",
            "net_vanna",
            "net_vomma",
        ]
    ].describe()
)