from pathlib import Path
import pandas as pd
import numpy as np

WIDE_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\term_structure_wide.parquet"
)

OUT_DIR = Path(
    r"D:\Quant_Option_Project\research\exports"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\term_structure_qc_report.txt"
)

SPREAD_COLS = [
    "next_minus_near_iv",
    "third_minus_near_iv",
    "fourth_minus_near_iv",
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Reading term structure wide dataset...")
    df = pd.read_parquet(WIDE_FILE)

    print("Shape:")
    print(df.shape)

    lines = []

    lines.append("====================================")
    lines.append("Term Structure QC Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {WIDE_FILE}")
    lines.append(f"Shape: {df.shape}")
    lines.append("")

    lines.append("Trade date range:")
    lines.append(f"{df['trade_date'].min()} - {df['trade_date'].max()}")
    lines.append("")
    lines.append(f"Unique trade dates: {df['trade_date'].nunique()}")
    lines.append("")

    lines.append("Missing values:")
    lines.append(str(df.isna().sum()))
    lines.append("")

    lines.append("Infinite values:")
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            lines.append(f"{col}: {np.isinf(df[col]).sum()}")
    lines.append("")

    print("\nSpread Summary:")
    spread_summary = df[SPREAD_COLS].describe()
    print(spread_summary)
    lines.append("Spread summary:")
    lines.append(str(spread_summary))
    lines.append("")

    print("\nExtreme Negative Spreads:")
    for col in SPREAD_COLS:
        if col not in df.columns:
            continue

        extreme = df[df[col] < -0.05].copy()

        print("\n", col)
        print("Count < -0.05:", len(extreme))

        lines.append(f"Extreme negative {col} < -0.05")
        lines.append(f"Count: {len(extreme)}")

        if len(extreme) > 0:
            cols_to_show = [
                "trade_date",
                "time_bucket",
                "near_expiry",
                "near_T",
                "near_iv",
                "next_expiry",
                "next_T",
                "next_iv",
                "third_expiry",
                "third_T",
                "third_iv",
                col,
            ]

            cols_to_show = [
                c for c in cols_to_show
                if c in extreme.columns
            ]

            sample = (
                extreme[cols_to_show]
                .sort_values(col)
                .head(50)
            )

            print(sample)

            out_file = OUT_DIR / f"extreme_negative_{col}.csv"
            sample.to_csv(
                out_file,
                index=False,
                encoding="utf-8-sig",
            )

            lines.append(str(sample))
            lines.append(f"Saved sample: {out_file}")

        lines.append("")

    print("\nExtreme Positive Spreads:")
    for col in SPREAD_COLS:
        if col not in df.columns:
            continue

        extreme = df[df[col] > 0.10].copy()

        print("\n", col)
        print("Count > 0.10:", len(extreme))

        lines.append(f"Extreme positive {col} > 0.10")
        lines.append(f"Count: {len(extreme)}")

        if len(extreme) > 0:
            cols_to_show = [
                "trade_date",
                "time_bucket",
                "near_expiry",
                "near_T",
                "near_iv",
                "next_expiry",
                "next_T",
                "next_iv",
                "third_expiry",
                "third_T",
                "third_iv",
                col,
            ]

            cols_to_show = [
                c for c in cols_to_show
                if c in extreme.columns
            ]

            sample = (
                extreme[cols_to_show]
                .sort_values(col, ascending=False)
                .head(50)
            )

            print(sample)

            out_file = OUT_DIR / f"extreme_positive_{col}.csv"
            sample.to_csv(
                out_file,
                index=False,
                encoding="utf-8-sig",
            )

            lines.append(str(sample))
            lines.append(f"Saved sample: {out_file}")

        lines.append("")

    print("\nDaily Spread Summary:")
    daily = (
        df.groupby("trade_date")[SPREAD_COLS]
        .agg(["mean", "median", "std", "min", "max", "count"])
    )

    print(daily.head(20))

    daily_out = OUT_DIR / "daily_term_spread_summary.csv"
    daily.to_csv(
        daily_out,
        encoding="utf-8-sig",
    )

    lines.append("Daily spread summary saved:")
    lines.append(str(daily_out))
    lines.append("")

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved report:")
    print(REPORT_FILE)
    print("Saved daily summary:")
    print(daily_out)


if __name__ == "__main__":
    main()