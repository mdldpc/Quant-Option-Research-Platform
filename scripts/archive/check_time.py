import pandas as pd

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

df = pd.read_csv(
    path,
    compression="xz",
    usecols=["iRecvTime", "updateTime", "mTime", "symbol"],
    nrows=2000
)

df["symbol"] = df["symbol"].str.strip()

print("=== IF SAMPLE ===")
print(
    df[df["symbol"].str.startswith("IF")]
    .head(20)
)

print("\n=== IO SAMPLE ===")
print(
    df[df["symbol"].str.startswith("IO")]
    .head(20)
)