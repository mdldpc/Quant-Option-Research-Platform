import pandas as pd

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

df = pd.read_csv(
    path,
    compression="xz",
    usecols=["symbol"],
    nrows=100000
)

df["symbol"] = df["symbol"].str.strip()

symbols = sorted(df["symbol"].unique())

for s in symbols[:50]:
    if s.startswith("IO"):
        parts = s.split("-")
        base = parts[0]
        opt_type = parts[1]
        strike = parts[2]
        fut_symbol = "IF" + base[2:]

        print(s, "=>", fut_symbol, opt_type, strike)
    elif s.startswith("IF"):
        print(s, "=> FUTURE")