import pandas as pd

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

usecols = [
    "iRecvTime",
    "symbol",
    "lastPrice",
    "BP1",
    "AP1",
    "volume",
    "openInterest",
]

df = pd.read_csv(
    path,
    compression="xz",
    usecols=usecols,
    nrows=500000
)

df["symbol"] = df["symbol"].str.strip()

# 期货
fut = df[df["symbol"].str.startswith("IF")].copy()
fut = fut[["iRecvTime", "symbol", "lastPrice"]]
fut = fut.rename(columns={
    "symbol": "fut_symbol",
    "lastPrice": "future_price"
})

# 期权
opt = df[df["symbol"].str.startswith("IO")].copy()
opt["option_mid"] = (opt["BP1"] + opt["AP1"]) / 2

parts = opt["symbol"].str.split("-", expand=True)
opt["expiry_code"] = parts[0].str[2:]
opt["option_type"] = parts[1]
opt["strike"] = parts[2].astype(float)
opt["fut_symbol"] = "IF" + opt["expiry_code"]

# 用最近时间向后匹配对应期货价格
opt = opt.sort_values("iRecvTime")
fut = fut.sort_values("iRecvTime")

merged = pd.merge_asof(
    opt,
    fut,
    by="fut_symbol",
    on="iRecvTime",
    direction="backward"
)

print(merged[[
    "iRecvTime",
    "symbol",
    "fut_symbol",
    "option_type",
    "strike",
    "option_mid",
    "future_price"
]].head(30))

print("\nMissing future price:")
print(merged["future_price"].isna().mean())