import pandas as pd

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

df = pd.read_csv(
    path,
    compression="xz",
    usecols=["symbol", "lastPrice"],
    nrows=500000
)

df["symbol"] = df["symbol"].str.strip()

fut = df[df["symbol"].str.startswith("IF")]

print("Rows:")
print(len(fut))

print("\nUnique IF:")
print(fut["symbol"].unique())

print("\nSample:")
print(fut.head(20))