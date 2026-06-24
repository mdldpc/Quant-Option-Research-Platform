from pathlib import Path
import pandas as pd
import numpy as np

SOURCE_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\atm_iv_dataset_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\atm_term_structure_2026H1.parquet"
)

OUT_DAILY_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_atm_term_structure_2026H1.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\atm_term_structure_preview.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\atm_term_structure_summary.txt"
)


def main():
    print("Reading ATM IV dataset...")
    df = pd.read_parquet(SOURCE_FILE)

    print("Source shape:")
    print(df.shape)

    keep_cols = [
        "trade_date",
        "time_bucket",
        "expiry_code",
        "T",
        "atm_strike",
        "future_price",
        "atm_iv",
        "call_iv",
        "put_iv",
        "has_call",
        "has_put",
        "has_both",
    ]

    df = df[keep_cols].copy()

    print("Filtering valid ATM IV rows...")
    df = df[
        df["atm_iv"].notna()
        & np.isfinite(df["atm_iv"])
        & df["T"].notna()
        & np.isfinite(df["T"])
    ].copy()

    print("Valid shape:")
    print(df.shape)

    print("Assigning term rank by T...")
    df = df.sort_values(
        ["trade_date", "time_bucket", "T", "expiry_code"]
    )

    df["term_rank"] = (
        df.groupby(["trade_date", "time_bucket"])
        .cumcount()
        + 1
    )

    df["days_to_expiry"] = df["T"] * 365

    print("ATM term structure shape:")
    print(df.shape)

    print("Building daily ATM term structure summary...")

    daily = (
        df.groupby(["trade_date", "term_rank"])
        .agg(
            atm_iv_mean=("atm_iv", "mean"),
            atm_iv_median=("atm_iv", "median"),
            atm_iv_std=("atm_iv", "std"),
            T_mean=("T", "mean"),
            days_to_expiry_mean=("days_to_expiry", "mean"),
            row_count=("atm_iv", "count"),
            expiry_count=("expiry_code", "nunique"),
        )
        .reset_index()
        .sort_values(["trade_date", "term_rank"])
    )

    print("Daily summary shape:")
    print(daily.shape)

    print("\nTerm rank counts:")
    print(df["term_rank"].value_counts().sort_index())

    print("\nDaily term rank counts:")
    print(daily["term_rank"].value_counts().sort_index())

    print("\nATM IV by term rank:")
    print(df.groupby("term_rank")["atm_iv"].describe())

    print("Saving outputs...")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_DAILY_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(OUT_FILE, index=False)
    daily.to_parquet(OUT_DAILY_FILE, index=False)

    df.head(100_000).to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("====================================")
    lines.append("ATM Term Structure Summary")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
    lines.append(f"Output file: {OUT_FILE}")
    lines.append(f"Daily output file: {OUT_DAILY_FILE}")
    lines.append("")
    lines.append(f"Final shape: {df.shape}")
    lines.append(f"Daily shape: {daily.shape}")
    lines.append("")
    lines.append(f"Trade dates: {df['trade_date'].nunique()}")
    lines.append(f"Time buckets: {df[['trade_date', 'time_bucket']].drop_duplicates().shape[0]}")
    lines.append(f"Unique expiries: {df['expiry_code'].nunique()}")
    lines.append("")
    lines.append("Term rank counts:")
    lines.append(str(df["term_rank"].value_counts().sort_index()))
    lines.append("")
    lines.append("ATM IV by term rank:")
    lines.append(str(df.groupby("term_rank")["atm_iv"].describe()))
    lines.append("")
    lines.append("Days to expiry by term rank:")
    lines.append(str(df.groupby("term_rank")["days_to_expiry"].describe()))

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved ATM term structure:")
    print(OUT_FILE)
    print("Saved daily summary:")
    print(OUT_DAILY_FILE)
    print("Saved preview:")
    print(OUT_CSV)
    print("Saved report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()