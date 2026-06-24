from pathlib import Path
import pandas as pd

WIDE_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\term_structure_wide.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_iv_summary.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\daily_iv_summary.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\daily_iv_summary_report.txt"
)

IV_COLS = [
    "near_iv",
    "next_iv",
    "third_iv",
    "fourth_iv",
    "next_minus_near_iv",
    "third_minus_near_iv",
    "fourth_minus_near_iv",
]


def main():
    print("Reading term structure wide dataset...")
    df = pd.read_parquet(WIDE_FILE)

    print("Source shape:")
    print(df.shape)

    existing_cols = [
        col for col in IV_COLS
        if col in df.columns
    ]

    print("Columns used:")
    print(existing_cols)

    print("Building daily IV summary...")

    agg_dict = {}

    for col in existing_cols:
        agg_dict[f"{col}_mean"] = (col, "mean")
        agg_dict[f"{col}_median"] = (col, "median")
        agg_dict[f"{col}_std"] = (col, "std")
        agg_dict[f"{col}_min"] = (col, "min")
        agg_dict[f"{col}_max"] = (col, "max")
        agg_dict[f"{col}_count"] = (col, "count")

    daily = (
        df.groupby("trade_date")
        .agg(
            row_count=("time_bucket", "count"),
            **agg_dict,
        )
        .reset_index()
        .sort_values("trade_date")
    )

    print("Daily summary shape:")
    print(daily.shape)

    print("Saving outputs...")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    daily.to_parquet(OUT_FILE, index=False)
    daily.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("====================================")
    lines.append("Daily IV Summary Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {WIDE_FILE}")
    lines.append(f"Output parquet: {OUT_FILE}")
    lines.append(f"Output csv: {OUT_CSV}")
    lines.append("")
    lines.append(f"Source shape: {df.shape}")
    lines.append(f"Daily shape: {daily.shape}")
    lines.append("")
    lines.append(f"Trade date range: {daily['trade_date'].min()} - {daily['trade_date'].max()}")
    lines.append(f"Unique trade dates: {daily['trade_date'].nunique()}")
    lines.append("")
    lines.append("Daily row_count summary:")
    lines.append(str(daily["row_count"].describe()))
    lines.append("")
    lines.append("Near IV summary:")
    if "near_iv_mean" in daily.columns:
        lines.append(str(daily["near_iv_mean"].describe()))
    else:
        lines.append("near_iv_mean not available")
    lines.append("")
    lines.append("Next minus Near IV summary:")
    if "next_minus_near_iv_mean" in daily.columns:
        lines.append(str(daily["next_minus_near_iv_mean"].describe()))
    else:
        lines.append("next_minus_near_iv_mean not available")
    lines.append("")
    lines.append("First 20 rows:")
    lines.append(str(daily.head(20)))

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved parquet:")
    print(OUT_FILE)
    print("Saved csv:")
    print(OUT_CSV)
    print("Saved report:")
    print(REPORT_FILE)

    print("\nPreview:")
    print(daily.head(20))

    print("\nNear IV daily mean summary:")
    if "near_iv_mean" in daily.columns:
        print(daily["near_iv_mean"].describe())

    print("\nNext-Near daily spread mean summary:")
    if "next_minus_near_iv_mean" in daily.columns:
        print(daily["next_minus_near_iv_mean"].describe())


if __name__ == "__main__":
    main()