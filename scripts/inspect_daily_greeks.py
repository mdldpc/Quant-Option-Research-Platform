import pandas as pd

df = pd.read_parquet("research/summaries/daily_greeks_summary.parquet")

print("=" * 80)
print("Columns")
print("=" * 80)
print(df.columns.tolist())

print()

print("=" * 80)
print("Shape")
print("=" * 80)
print(df.shape)

print()

print("=" * 80)
print("Head")
print("=" * 80)
print(df.head())

print()

print("=" * 80)
print("Data Types")
print("=" * 80)
print(df.dtypes)