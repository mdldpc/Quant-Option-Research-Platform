from pathlib import Path
import pandas as pd

SOURCE_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\atm_iv_dataset_2026H1.parquet"
)

OUT_LONG = Path(
    r"D:\Quant_Option_Project\research\datasets\term_structure_long.parquet"
)

OUT_WIDE = Path(
    r"D:\Quant_Option_Project\research\datasets\term_structure_wide.parquet"
)

PREVIEW_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\term_structure_preview.csv"
)

SUMMARY_TXT = Path(
    r"D:\Quant_Option_Project\research\reports\term_structure_summary.txt"
)


RANK_LABELS = {
    1: "near",
    2: "next",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
}


def main():
    print("Reading ATM IV dataset...")
    df = pd.read_parquet(SOURCE_FILE)

    print("Source shape:")
    print(df.shape)

    required_cols = [
        "trade_date",
        "time_bucket",
        "expiry_code",
        "atm_strike",
        "future_price",
        "abs_moneyness",
        "T",
        "atm_iv",
        "call_iv",
        "put_iv",
        "call_put_iv_spread",
        "has_call",
        "has_put",
        "has_both",
        "call_symbol",
        "put_symbol",
        "call_delta",
        "put_delta",
        "call_gamma",
        "put_gamma",
        "call_vega",
        "put_vega",
        "call_theta",
        "put_theta",
        "call_vanna",
        "put_vanna",
        "call_vomma",
        "put_vomma",
        "call_speed",
        "put_speed",
    ]

    df = df[required_cols].copy()

    print("Sorting by trade_date, time_bucket, T...")
    df = df.sort_values(
        ["trade_date", "time_bucket", "T", "expiry_code"]
    )

    print("Assigning term_rank...")
    df["term_rank"] = (
        df.groupby(["trade_date", "time_bucket"])
        .cumcount()
        + 1
    )

    df["term_label"] = df["term_rank"].map(RANK_LABELS)

    long_cols = [
        "trade_date",
        "time_bucket",
        "term_rank",
        "term_label",
        "expiry_code",
        "T",
        "atm_strike",
        "future_price",
        "abs_moneyness",
        "atm_iv",
        "call_iv",
        "put_iv",
        "call_put_iv_spread",
        "has_call",
        "has_put",
        "has_both",
        "call_symbol",
        "put_symbol",
        "call_delta",
        "put_delta",
        "call_gamma",
        "put_gamma",
        "call_vega",
        "put_vega",
        "call_theta",
        "put_theta",
        "call_vanna",
        "put_vanna",
        "call_vomma",
        "put_vomma",
        "call_speed",
        "put_speed",
    ]

    long_df = df[long_cols].copy()

    print("Long dataset shape:")
    print(long_df.shape)

    print("Building wide dataset...")

    base = (
        long_df[["trade_date", "time_bucket"]]
        .drop_duplicates()
        .sort_values(["trade_date", "time_bucket"])
        .reset_index(drop=True)
    )

    wide_df = base.copy()

    for rank, label in RANK_LABELS.items():
        temp = long_df[long_df["term_rank"] == rank].copy()

        temp = temp[
            [
                "trade_date",
                "time_bucket",
                "expiry_code",
                "T",
                "atm_iv",
                "atm_strike",
                "future_price",
            ]
        ].rename(
            columns={
                "expiry_code": f"{label}_expiry",
                "T": f"{label}_T",
                "atm_iv": f"{label}_iv",
                "atm_strike": f"{label}_strike",
                "future_price": f"{label}_future",
            }
        )

        wide_df = wide_df.merge(
            temp,
            on=["trade_date", "time_bucket"],
            how="left",
        )

    print("Calculating IV spreads...")

    if "near_iv" in wide_df.columns and "next_iv" in wide_df.columns:
        wide_df["next_minus_near_iv"] = (
            wide_df["next_iv"] - wide_df["near_iv"]
        )

    if "near_iv" in wide_df.columns and "third_iv" in wide_df.columns:
        wide_df["third_minus_near_iv"] = (
            wide_df["third_iv"] - wide_df["near_iv"]
        )

    if "near_iv" in wide_df.columns and "fourth_iv" in wide_df.columns:
        wide_df["fourth_minus_near_iv"] = (
            wide_df["fourth_iv"] - wide_df["near_iv"]
        )

    if "near_iv" in wide_df.columns and "sixth_iv" in wide_df.columns:
        wide_df["sixth_minus_near_iv"] = (
            wide_df["sixth_iv"] - wide_df["near_iv"]
        )

    print("Wide dataset shape:")
    print(wide_df.shape)

    print("Saving datasets...")
    OUT_LONG.parent.mkdir(parents=True, exist_ok=True)
    OUT_WIDE.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_CSV.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_TXT.parent.mkdir(parents=True, exist_ok=True)

    long_df.to_parquet(OUT_LONG, index=False)
    wide_df.to_parquet(OUT_WIDE, index=False)

    wide_df.head(100_000).to_csv(
        PREVIEW_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    print("Building summary report...")

    total_buckets = wide_df[["trade_date", "time_bucket"]].drop_duplicates().shape[0]

    lines = []
    lines.append("====================================")
    lines.append("Term Structure Dataset Summary")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
    lines.append(f"Long output: {OUT_LONG}")
    lines.append(f"Wide output: {OUT_WIDE}")
    lines.append("")
    lines.append(f"Long shape: {long_df.shape}")
    lines.append(f"Wide shape: {wide_df.shape}")
    lines.append("")
    lines.append(f"Trade dates: {long_df['trade_date'].nunique()}")
    lines.append(f"Unique time buckets: {total_buckets}")
    lines.append(f"Unique expiries: {long_df['expiry_code'].nunique()}")
    lines.append("")
    lines.append("Term rank counts:")
    lines.append(str(long_df["term_rank"].value_counts().sort_index()))
    lines.append("")
    lines.append("Term label counts:")
    lines.append(str(long_df["term_label"].value_counts(dropna=False)))
    lines.append("")
    lines.append("ATM IV summary by rank:")
    lines.append(str(long_df.groupby("term_rank")["atm_iv"].describe()))
    lines.append("")
    lines.append("Wide missing values:")
    lines.append(str(wide_df.isna().sum()))
    lines.append("")
    lines.append("IV spread summary:")
    spread_cols = [
        col for col in wide_df.columns
        if col.endswith("_minus_near_iv")
    ]
    if spread_cols:
        lines.append(str(wide_df[spread_cols].describe()))
    else:
        lines.append("No spread columns generated.")

    SUMMARY_TXT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved long:")
    print(OUT_LONG)
    print("Saved wide:")
    print(OUT_WIDE)
    print("Saved preview:")
    print(PREVIEW_CSV)
    print("Saved summary:")
    print(SUMMARY_TXT)

    print("\nQuick QC:")
    print("Long shape:", long_df.shape)
    print("Wide shape:", wide_df.shape)
    print("Trade dates:", long_df["trade_date"].nunique())
    print("Unique expiries:", long_df["expiry_code"].nunique())
    print("\nTerm rank counts:")
    print(long_df["term_rank"].value_counts().sort_index())
    print("\nSpread summary:")
    if spread_cols:
        print(wide_df[spread_cols].describe())


if __name__ == "__main__":
    main()