from pathlib import Path
import pandas as pd
import numpy as np

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_greeks_summary.parquet"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\daily_greeks_summary_qc_report.txt"
)

OUT_DIR = Path(
    r"D:\Quant_Option_Project\research\exports"
)

GREEKS = [
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Reading daily Greeks summary...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:")
    print(df.shape)

    lines = []
    lines.append("====================================")
    lines.append("Daily Greeks Summary QC Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {DATA_FILE}")
    lines.append(f"Shape: {df.shape}")
    lines.append("")
    lines.append(f"Trade dates: {df['trade_date'].nunique()}")
    lines.append(f"Moneyness buckets: {df['moneyness_bucket'].nunique()}")
    lines.append("")

    print("\nMissing values:")
    missing = df.isna().sum()
    print(missing)
    lines.append("Missing values:")
    lines.append(str(missing))
    lines.append("")

    print("\nInfinite values:")
    inf_lines = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            n_inf = np.isinf(df[col]).sum()
            inf_lines.append(f"{col}: {n_inf}")
            print(col, n_inf)

    lines.append("Infinite values:")
    lines.extend(inf_lines)
    lines.append("")

    print("\nBucket counts:")
    bucket_counts = df["moneyness_bucket"].value_counts().sort_index()
    print(bucket_counts)
    lines.append("Bucket counts:")
    lines.append(str(bucket_counts))
    lines.append("")

    print("\nRow count by bucket:")
    row_by_bucket = (
        df.groupby("moneyness_bucket", observed=False)["row_count"]
        .describe()
    )
    print(row_by_bucket)
    lines.append("Row count by bucket:")
    lines.append(str(row_by_bucket))
    lines.append("")

    for greek in GREEKS:
        mean_col = f"{greek}_mean"

        print(f"\n{greek.upper()} mean by bucket:")
        by_bucket = (
            df.groupby("moneyness_bucket", observed=False)[mean_col]
            .describe()
        )
        print(by_bucket)

        lines.append(f"{greek.upper()} mean by bucket:")
        lines.append(str(by_bucket))
        lines.append("")

    print("\nExtreme days by Greek:")

    extreme_rows = []

    for greek in GREEKS:
        mean_col = f"{greek}_mean"

        top_high = df.sort_values(mean_col, ascending=False).head(10).copy()
        top_high["greek"] = greek
        top_high["direction"] = "high"

        top_low = df.sort_values(mean_col, ascending=True).head(10).copy()
        top_low["greek"] = greek
        top_low["direction"] = "low"

        extreme_rows.append(top_high)
        extreme_rows.append(top_low)

        print(f"\nTop high {greek}:")
        print(
            top_high[
                [
                    "trade_date",
                    "moneyness_bucket",
                    mean_col,
                    "iv_mean",
                    "row_count",
                ]
            ]
        )

        print(f"\nTop low {greek}:")
        print(
            top_low[
                [
                    "trade_date",
                    "moneyness_bucket",
                    mean_col,
                    "iv_mean",
                    "row_count",
                ]
            ]
        )

        lines.append(f"Top high {greek}:")
        lines.append(
            str(
                top_high[
                    [
                        "trade_date",
                        "moneyness_bucket",
                        mean_col,
                        "iv_mean",
                        "row_count",
                    ]
                ]
            )
        )
        lines.append("")

        lines.append(f"Top low {greek}:")
        lines.append(
            str(
                top_low[
                    [
                        "trade_date",
                        "moneyness_bucket",
                        mean_col,
                        "iv_mean",
                        "row_count",
                    ]
                ]
            )
        )
        lines.append("")

    extremes = pd.concat(extreme_rows, ignore_index=True)

    extreme_out = OUT_DIR / "daily_greeks_extreme_days.csv"
    extremes.to_csv(
        extreme_out,
        index=False,
        encoding="utf-8-sig",
    )

    lines.append("Extreme days saved:")
    lines.append(str(extreme_out))
    lines.append("")

    print("\nCorrelation among Greek means:")
    greek_mean_cols = [f"{g}_mean" for g in GREEKS]
    corr = df[greek_mean_cols + ["iv_mean"]].corr()

    print(corr)
    lines.append("Correlation among Greek means:")
    lines.append(str(corr))
    lines.append("")

    corr_out = OUT_DIR / "daily_greeks_correlation.csv"
    corr.to_csv(
        corr_out,
        encoding="utf-8-sig",
    )

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved report:")
    print(REPORT_FILE)
    print("Saved extreme days:")
    print(extreme_out)
    print("Saved correlation:")
    print(corr_out)


if __name__ == "__main__":
    main()