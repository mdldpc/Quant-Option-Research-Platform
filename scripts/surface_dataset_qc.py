from pathlib import Path
import pandas as pd
import numpy as np

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\surface_dataset_near_2026H1.parquet"
)

OUT_DIR = Path(
    r"D:\Quant_Option_Project\research\exports"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\surface_dataset_qc_report.txt"
)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Reading surface dataset...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:")
    print(df.shape)

    lines = []
    lines.append("====================================")
    lines.append("Near Surface Dataset QC Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {DATA_FILE}")
    lines.append(f"Shape: {df.shape}")
    lines.append("")
    lines.append(f"Trade date range: {df['trade_date'].min()} - {df['trade_date'].max()}")
    lines.append(f"Unique trade dates: {df['trade_date'].nunique()}")
    lines.append(f"Unique time buckets: {df[['trade_date', 'time_bucket']].drop_duplicates().shape[0]}")
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

    print("\nEmpty surface cells:")
    empty_count = (df["row_count"] == 0).sum()
    total_count = len(df)
    empty_ratio = empty_count / total_count
    print("row_count == 0:", empty_count)
    print("empty ratio:", empty_ratio)

    lines.append("Empty surface cells:")
    lines.append(f"row_count == 0: {empty_count}")
    lines.append(f"empty ratio: {empty_ratio:.4%}")
    lines.append("")

    valid = df[df["row_count"] > 0].copy()

    print("\nValid surface shape:")
    print(valid.shape)

    lines.append(f"Valid surface shape: {valid.shape}")
    lines.append("")

    print("\nBucket coverage:")
    bucket_cov = (
        df.groupby("surface_moneyness_bucket", observed=False)
        .agg(
            total_cells=("row_count", "size"),
            valid_cells=("row_count", lambda x: (x > 0).sum()),
            empty_cells=("row_count", lambda x: (x == 0).sum()),
        )
        .reset_index()
    )

    bucket_cov["valid_ratio"] = (
        bucket_cov["valid_cells"] / bucket_cov["total_cells"]
    )

    print(bucket_cov)

    lines.append("Bucket coverage:")
    lines.append(str(bucket_cov))
    lines.append("")

    bucket_cov.to_csv(
        OUT_DIR / "surface_bucket_coverage.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nIV summary by bucket:")
    iv_by_bucket = (
        valid.groupby("surface_moneyness_bucket", observed=False)["smoothed_iv_mean"]
        .describe()
    )
    print(iv_by_bucket)

    lines.append("IV summary by bucket:")
    lines.append(str(iv_by_bucket))
    lines.append("")

    print("\nDaily valid cell summary:")
    daily_valid = (
        valid.groupby("trade_date")
        .size()
        .describe()
    )
    print(daily_valid)

    lines.append("Daily valid cell summary:")
    lines.append(str(daily_valid))
    lines.append("")

    print("\nExtreme IV surface cells:")
    high = valid[valid["smoothed_iv_mean"] > 1.0].copy()
    low = valid[valid["smoothed_iv_mean"] < 0.10].copy()

    print("smoothed_iv_mean > 1.0:", len(high))
    print("smoothed_iv_mean < 0.10:", len(low))

    lines.append("Extreme IV surface cells:")
    lines.append(f"smoothed_iv_mean > 1.0: {len(high)}")
    lines.append(f"smoothed_iv_mean < 0.10: {len(low)}")
    lines.append("")

    if len(high) > 0:
        high_sample = (
            high.sort_values("smoothed_iv_mean", ascending=False)
            .head(200)
        )

        high_out = OUT_DIR / "surface_extreme_high_iv.csv"
        high_sample.to_csv(
            high_out,
            index=False,
            encoding="utf-8-sig",
        )

        lines.append("High IV sample:")
        lines.append(str(high_sample.head(50)))
        lines.append(f"Saved high sample: {high_out}")
        lines.append("")

    if len(low) > 0:
        low_sample = (
            low.sort_values("smoothed_iv_mean", ascending=True)
            .head(200)
        )

        low_out = OUT_DIR / "surface_extreme_low_iv.csv"
        low_sample.to_csv(
            low_out,
            index=False,
            encoding="utf-8-sig",
        )

        lines.append("Low IV sample:")
        lines.append(str(low_sample.head(50)))
        lines.append(f"Saved low sample: {low_out}")
        lines.append("")

    print("\nDaily average surface by bucket...")
    daily_surface = (
        valid.groupby(
            ["trade_date", "surface_moneyness_bucket"],
            observed=False,
        )["smoothed_iv_mean"]
        .mean()
        .reset_index()
        .pivot(
            index="trade_date",
            columns="surface_moneyness_bucket",
            values="smoothed_iv_mean",
        )
        .reset_index()
    )

    daily_surface_out = OUT_DIR / "daily_surface_bucket_iv.csv"
    daily_surface.to_csv(
        daily_surface_out,
        index=False,
        encoding="utf-8-sig",
    )

    lines.append("Daily surface bucket IV saved:")
    lines.append(str(daily_surface_out))
    lines.append("")

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved report:")
    print(REPORT_FILE)
    print("Saved bucket coverage:")
    print(OUT_DIR / "surface_bucket_coverage.csv")
    print("Saved daily surface bucket IV:")
    print(daily_surface_out)


if __name__ == "__main__":
    main()