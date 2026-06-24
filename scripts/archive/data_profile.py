import pandas as pd

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

df = pd.read_csv(
    path,
    compression="xz",
    nrows=100000
)

print("=" * 50)
print("Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nUnique Symbols")
print(df["symbol"].nunique())

print("\nFirst 20 Symbols")
print(df["symbol"].unique()[:20])

print("\nTime Range")
print(df["updateTime"].min())
print(df["updateTime"].max())