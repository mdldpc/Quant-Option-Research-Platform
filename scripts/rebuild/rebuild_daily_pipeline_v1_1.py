from pathlib import Path
from datetime import datetime
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath("."))

from scripts.rebuild.rebuild_common import (
    iter_cleaned_sessions,
    print_rebuild_header,
    print_progress,
)

from config.trading_calendar import is_abnormal_trading_date

from scripts.iv_cache_engine import add_iv_cache
from scripts.iv_spline_engine import build_spline_surface
from scripts.greeks_spline_engine_batch import add_spline_greeks


OUTPUT_ROOT = Path("data_parquet/batch_2026_v1_1_daily")

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


def extract_trade_date(file_path: Path) -> int:
    return int(file_path.name.split(".")[2])


def trade_date_to_datetime(trade_date: int) -> datetime:
    return datetime.strptime(str(trade_date), "%Y%m%d")


def build_option_price(df: pd.DataFrame) -> pd.DataFrame:
    both = (df["BP1"] > 0) & (df["AP1"] > 0)
    bid_only = (df["BP1"] > 0) & (df["AP1"] <= 0)
    ask_only = (df["AP1"] > 0) & (df["BP1"] <= 0)

    df = df.copy()
    df["option_price"] = None

    df.loc[both, "option_price"] = (
        df.loc[both, "BP1"] + df.loc[both, "AP1"]
    ) / 2

    df.loc[bid_only, "option_price"] = df.loc[bid_only, "BP1"]
    df.loc[ask_only, "option_price"] = df.loc[ask_only, "AP1"]

    return df


def build_option_table(raw_df: pd.DataFrame) -> pd.DataFrame:
    raw_df = raw_df.copy()
    raw_df["symbol"] = raw_df["symbol"].str.strip()

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


def resample_10s(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["time_bucket"] = (
        df["iRecvTime"]
        // (RESAMPLE_SECONDS * 1_000_000_000)
    )

    df = (
        df.sort_values("iRecvTime")
        .groupby(["symbol", "time_bucket"], as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    return df


def process_one_file(file_path: Path) -> None:
    trade_date = extract_trade_date(file_path)

    if is_abnormal_trading_date(trade_date):
        print(f"SKIP {trade_date}: abnormal trading date")
        return

    trade_date_dt = trade_date_to_datetime(trade_date)

    out_dir = OUTPUT_ROOT / f"trade_date={trade_date}"
    out_dir.mkdir(parents=True, exist_ok=True)

    option_table_path = out_dir / "option_table_v1_1.parquet"
    iv_table_path = out_dir / "iv_table_v1_1.parquet"
    iv_spline_path = out_dir / "iv_spline_v1_1.parquet"
    greeks_path = out_dir / "greeks_v1_1.parquet"
    success_flag = out_dir / "SUCCESS.flag"

    if success_flag.exists() and greeks_path.exists():
        print(f"SKIP {trade_date}: already completed")
        return

    print("\n" + "-" * 72)
    print(f"Processing {trade_date}")
    print("-" * 72)

    if option_table_path.exists():
        print("Stage 1: Loading existing option table...")
        option_df = pd.read_parquet(option_table_path)
        print("Option rows:", len(option_df))
    else:
        print("Stage 1: Reading cleaned session...")
        raw_df = pd.read_parquet(file_path, columns=USECOLS)
        print("Cleaned rows:", len(raw_df))

        print("Stage 1: Building option table...")
        option_df = build_option_table(raw_df)
        print("Option rows:", len(option_df))

        print("Stage 1: Resampling (10s)...")
        option_df = resample_10s(option_df)
        print("Resampled rows:", len(option_df))

        option_df.to_parquet(option_table_path, index=False)
        print("Saved option table:")
        print(option_table_path)

    if iv_table_path.exists():
        print("Stage 2: Loading existing IV table...")
        iv_df = pd.read_parquet(iv_table_path)
        print("IV rows:", len(iv_df))
    else:
        print("Stage 2: Calculating IV...")
        iv_df = add_iv_cache(
            option_df,
            trade_date_dt,
        )
        print("IV rows:", len(iv_df))
        print("IV NaN ratio:", iv_df["implied_vol"].isna().mean())

        iv_df.to_parquet(iv_table_path, index=False)
        print("Saved IV table:")
        print(iv_table_path)

    if iv_spline_path.exists():
        print("Stage 2: Loading existing IV spline...")
        surface_df = pd.read_parquet(iv_spline_path)
        print("Spline rows:", len(surface_df))
    else:
        print("Stage 2: Building spline surface...")
        surface_df = build_spline_surface(iv_df)
        print("Spline rows:", len(surface_df))

        surface_df.to_parquet(iv_spline_path, index=False)
        print("Saved IV spline:")
        print(iv_spline_path)

    print("Stage 3: Calculating Greeks...")
    greeks_df = add_spline_greeks(
        iv_df,
        surface_df,
    )

    print("Greeks rows:", len(greeks_df))

    greeks_df.to_parquet(greeks_path, index=False)
    success_flag.touch()

    print("Saved Greeks:")
    print(greeks_path)

    print("DONE:", trade_date)


def main():
    print_rebuild_header("Rebuild Daily Pipeline v1.1 — Stage 3")

    files = list(iter_cleaned_sessions())
    print(f"Cleaned session files: {len(files)}")

    total = len(files)

    for i, file_path in enumerate(files, start=1):
        print_progress(i, total, every=10)

        try:
            process_one_file(file_path)

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            print("Rerun this command later; completed dates will be skipped.")
            raise

        except Exception as e:
            print("FAILED:", file_path.name)
            print("ERROR:", repr(e))
            continue

    print("\nDaily rebuild completed.")


if __name__ == "__main__":
    main()