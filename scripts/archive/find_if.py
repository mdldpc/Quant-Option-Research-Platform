import pandas as pd

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

df = pd.read_csv(
    path,
    compression="xz",
    usecols=["symbol"],
    nrows=1_000_000
)

df["symbol"] = df["symbol"].str.strip()

if_symbols = sorted([s for s in df["symbol"].unique() if s.startswith("IF")])
io_symbols = sorted([s for s in df["symbol"].unique() if s.startswith("IO")])

print("IF symbols count:", len(if_symbols))
print(if_symbols[:50])

print("\nIO symbols count:", len(io_symbols))
print(io_symbols[:20])