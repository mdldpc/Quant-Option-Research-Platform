import pandas as pd

RAW_FILE = r"F:\CFFEX.2025\CFFEX.IF.20250102.csv.xz"

USECOLS = [
    "symbol",
    "lastPrice",
    "BP1",
    "AP1",
]

print("Reading file...")

df = pd.read_csv(
    RAW_FILE,
    compression="xz",
    usecols=USECOLS,
)

df["symbol"] = df["symbol"].str.strip()

opt = df[df["symbol"].str.startswith("IO")].copy()

print("\nTotal option rows:")
print(len(opt))

def build_price(row):
    bp = row["BP1"]
    ap = row["AP1"]

    if bp > 0 and ap > 0:
        return (bp + ap) / 2
    elif bp > 0:
        return bp
    elif ap > 0:
        return ap
    return None

opt["option_price"] = opt.apply(build_price, axis=1)

opt = opt[opt["option_price"].notna()]

unique_keys = opt[
    [
        "symbol",
        "option_price",
    ]
].drop_duplicates()

print("\nUnique symbol+price:")
print(len(unique_keys))

print("\nCompression ratio:")
print(len(unique_keys) / len(opt))