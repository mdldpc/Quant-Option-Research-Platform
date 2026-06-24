import os
import pandas as pd

RAW_PATH = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"
OUT_PATH = r"D:\Quant_Option_Project\data_parquet\option_table_sample.parquet"

USECOLS = [
    "iRecvTime",
    "symbol",
    "lastPrice",
    "BP1",
    "AP1",
    "volume",
    "openInterest",
]

NROWS = 1_000_000


def build_option_price(row):
    bp = row["BP1"]
    ap = row["AP1"]

    if bp > 0 and ap > 0:
        return (bp + ap) / 2

    elif bp > 0:
        return bp

    elif ap > 0:
        return ap

    return None


def main():

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print("Reading raw file...")

    df = pd.read_csv(
        RAW_PATH,
        compression="xz",
        usecols=USECOLS,
        nrows=NROWS,
    )

    df["symbol"] = df["symbol"].str.strip()

    print("Splitting IF and IO...")

    fut = df[df["symbol"].str.startswith("IF")].copy()
    opt = df[df["symbol"].str.startswith("IO")].copy()

    print("Futures rows:", len(fut))
    print("Options rows:", len(opt))

    fut = fut[
        [
            "iRecvTime",
            "symbol",
            "lastPrice"
        ]
    ].rename(
        columns={
            "symbol": "fut_symbol",
            "lastPrice": "future_price"
        }
    )

    # --------------------------------------------------
    # Parse Option Symbol
    # --------------------------------------------------

    parts = opt["symbol"].str.split("-", expand=True)

    opt["expiry_code"] = parts[0].str[2:]
    opt["option_type"] = parts[1]
    opt["strike"] = parts[2].astype(float)

    opt["fut_symbol"] = "IF" + opt["expiry_code"]

    # --------------------------------------------------
    # Build Option Price
    # --------------------------------------------------

    opt["option_price"] = opt.apply(
        build_option_price,
        axis=1
    )

    opt = opt[
        opt["option_price"].notna()
    ].copy()

    # --------------------------------------------------
    # Keep only futures we actually have
    # --------------------------------------------------

    valid_futs = set(
        fut["fut_symbol"].unique()
    )

    opt = opt[
        opt["fut_symbol"].isin(valid_futs)
    ].copy()

    # --------------------------------------------------
    # Time Alignment
    # --------------------------------------------------

    opt = opt.sort_values("iRecvTime")
    fut = fut.sort_values("iRecvTime")

    print("Merging option with nearest future price...")

    merged = pd.merge_asof(
        opt,
        fut,
        by="fut_symbol",
        on="iRecvTime",
        direction="nearest",
        tolerance=5_000_000_000
    )

    # --------------------------------------------------
    # Final Table
    # --------------------------------------------------

    result = merged[
        [
            "iRecvTime",
            "symbol",
            "fut_symbol",
            "option_type",
            "strike",
            "option_price",
            "future_price",
            "BP1",
            "AP1",
            "volume",
            "openInterest"
        ]
    ].copy()

    result = result[
        result["future_price"].notna()
    ].copy()

    result = result[
        result["future_price"] > 0
    ].copy()

    print()
    print("Final rows:", len(result))

    print()
    print(result.head(20))

    result.to_parquet(
        OUT_PATH,
        index=False
    )

    print()
    print("Saved to:")
    print(OUT_PATH)


if __name__ == "__main__":
    main()