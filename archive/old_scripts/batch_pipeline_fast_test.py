from pathlib import Path
from datetime import datetime
import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(__file__))

from iv_cache_engine import add_iv_cache
from iv_spline_engine import build_spline_surface
from greeks_spline_engine_batch import add_spline_greeks

RAW_ROOT = Path(r"C:\Users\yyyjz\Desktop\2026intern\CFFEX.2026")

RAW_FILES = sorted(RAW_ROOT.glob("*.csv.xz"))[:2]

OUTPUT_ROOT = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_fast_test"
)

RESAMPLE_SECONDS = 10

USECOLS = [
    "iRecvTime",
    "symbol",
    "lastPrice",
    "BP1",
    "AP1",
    "volume",
    "openInterest",
]


def get_trade_date(file_path):
    name = Path(file_path).name
    date_str = name.replace("CFFEX.IF.", "").replace(".csv.xz", "")
    return datetime.strptime(date_str, "%Y%m%d")


def build_option_price(df):
    both = (df["BP1"] > 0) & (df["AP1"] > 0)
    bid_only = (df["BP1"] > 0) & (df["AP1"] <= 0)
    ask_only = (df["AP1"] > 0) & (df["BP1"] <= 0)

    df["option_price"] = None

    df.loc[both, "option_price"] = (
        df.loc[both, "BP1"] + df.loc[both, "AP1"]
    ) / 2

    df.loc[bid_only, "option_price"] = df.loc[bid_only, "BP1"]
    df.loc[ask_only, "option_price"] = df.loc[ask_only, "AP1"]

    return df


def build_option_table(raw_df):
    fut = raw_df[raw_df["symbol"].str.startswith("IF")].copy()
    opt = raw_df[raw_df["symbol"].str.startswith("IO")].copy()

    fut = fut[["iRecvTime", "symbol", "lastPrice"]].rename(
        columns={
            "symbol": "fut_symbol",
            "lastPrice": "future_price",
        }
    )

    opt = build_option_price(opt)
    opt = opt[opt["option_price"].notna()].copy()

    parts = opt["symbol"].str.split("-", expand=True)

    opt["expiry_code"] = parts[0].str[2:]
    opt["option_type"] = parts[1]
    opt["strike"] = parts[2].astype(float)
    opt["fut_symbol"] = "IF" + opt["expiry_code"]

    valid_futs = set(fut["fut_symbol"].unique())
    opt = opt[opt["fut_symbol"].isin(valid_futs)].copy()

    opt = opt.sort_values("iRecvTime")
    fut = fut.sort_values("iRecvTime")

    merged = pd.merge_asof(
        opt,
        fut,
        by="fut_symbol",
        on="iRecvTime",
        direction="nearest",
        tolerance=5_000_000_000,
    )

    merged = merged[merged["future_price"].notna()].copy()

    return merged


def resample_10s(df):
    df["time_bucket"] = (
        df["iRecvTime"] // (RESAMPLE_SECONDS * 1_000_000_000)
    )

    df = (
        df.sort_values("iRecvTime")
        .groupby(["symbol", "time_bucket"], as_index=False)
        .tail(1)
        .copy()
    )

    return df


def main():
    print("Files to process:", len(RAW_FILES))

    for file_path in RAW_FILES:
        trade_date = get_trade_date(file_path)
        trade_date_str = trade_date.strftime("%Y%m%d")

        print("\n" + "=" * 60)
        print("Processing:", trade_date_str)

        out_dir = OUTPUT_ROOT / f"trade_date={trade_date_str}"
        out_dir.mkdir(parents=True, exist_ok=True)

        print("\nStep 1 Read Raw")

        raw_df = pd.read_csv(
            file_path,
            compression="xz",
            usecols=USECOLS,
        )

        raw_df["symbol"] = raw_df["symbol"].str.strip()

        print("Raw rows:", len(raw_df))

        print("\nStep 2 Build Option Table")

        option_df = build_option_table(raw_df)

        print("Option rows:", len(option_df))

        print("\nStep 3 Resample 10s")

        option_df = resample_10s(option_df)

        print("Resampled rows:", len(option_df))

        option_df.to_parquet(
            out_dir / "option_table.parquet",
            index=False,
        )

        print("\nStep 4 IV Cache")

        iv_df = add_iv_cache(
            option_df,
            trade_date,
        )

        print("IV rows:", len(iv_df))

        iv_df.to_parquet(
            out_dir / "iv_table.parquet",
            index=False,
        )
        print("\nStep 5 Spline Surface")

        surface_df = build_spline_surface(iv_df)

        print("Spline rows:", len(surface_df))

        surface_df.to_parquet(
            out_dir / "iv_spline.parquet",
            index=False,
        )

        print("\nStep 6 Greeks with Spline IV")

        greeks_df = add_spline_greeks(
            iv_df,
            surface_df,
        )

        print("Greeks rows:", len(greeks_df))

        greeks_df.to_parquet(
            out_dir / "greeks_spline.parquet",
            index=False,
        )

        print("\nSaved:")
        print(out_dir)


if __name__ == "__main__":
    main()