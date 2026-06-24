import pandas as pd
from pathlib import Path

FILE = Path(
    r"C:\Users\yyyjz\Desktop\2026intern\CFFEX.2026"
    r"\CFFEX.IF.20260207.csv.xz"
)

USECOLS = [
    "iRecvTime",
    "symbol",
    "updateTime",
    "mTime",
    "lastPrice",
    "BP1",
    "AP1",
    "volume",
    "openInterest",
]

print("File exists:", FILE.exists())
print("File size MB:", FILE.stat().st_size / 1024 / 1024)

df = pd.read_csv(
    FILE,
    compression="xz",
    usecols=USECOLS,
)

df["symbol"] = df["symbol"].str.strip()

print("\nRows:")
print(len(df))

print("\nTime range:")
print(df["updateTime"].min(), df["updateTime"].max())

print("\nUnique symbols:")
print(df["symbol"].nunique())

print("\nSymbol prefix counts:")
print(df["symbol"].str[:2].value_counts())

print("\nFirst 30 rows:")
print(df.head(30))

print("\nLast 30 rows:")
print(df.tail(30))

print("\nVolume summary:")
print(df["volume"].describe())

print("\nRows with volume > 0:")
print((df["volume"] > 0).sum())

print("\nTop symbols:")
print(df["symbol"].value_counts().head(30))