from pathlib import Path
import pandas as pd
import numpy as np

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\smile_dataset_near_2026H1.parquet"
)

OUT_DIR = Path(
    r"D:\Quant_Option_Project\research\exports"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\smile_dataset_qc_report.txt"
)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Reading Near Smile dataset...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:")
    print(df.shape)

    lines = []
    lines.append("====================================")
    lines.append("Near Smile Dataset QC Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {DATA_FILE}")
    lines.append(f"Shape: {df.shape}")
    lines.append("")
    lines.append(f"Trade date range: {df['trade_date'].min()} - {df['trade_date'].max()}")
    lines.append(f"Unique trade dates: {df['trade_date'].nunique()}")
    lines.append(f"Unique expiry codes: {df['expiry_code'].nunique()}")
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

    print("\nOption type counts:")
    opt_counts = df["option_type"].value_counts()
    print(opt_counts)
    lines.append("Option type counts:")
    lines.append(str(opt_counts))
    lines.append("")

    print("\nMoneyness bucket counts:")
    bucket_counts = (
        df["moneyness_bucket"]
        .value_counts(dropna=False)
        .sort_index()
    )
    print(bucket_counts)
    lines.append("Moneyness bucket counts:")
    lines.append(str(bucket_counts))
    lines.append("")

    print("\nIV summary by moneyness bucket:")
    bucket_iv = (
        df.groupby("moneyness_bucket", observed=False)["smoothed_iv"]
        .describe()
    )
    print(bucket_iv)
    lines.append("IV summary by moneyness bucket:")
    lines.append(str(bucket_iv))
    lines.append("")

    print("\nIV summary by option type:")
    type_iv = (
        df.groupby("option_type")["smoothed_iv"]
        .describe()
    )
    print(type_iv)
    lines.append("IV summary by option type:")
    lines.append(str(type_iv))
    lines.append("")

    print("\nDaily row count summary:")
    daily_count = df.groupby("trade_date").size()
    print(daily_count.describe())
    lines.append("Daily row count summary:")
    lines.append(str(daily_count.describe()))
    lines.append("")

    print("\nExtreme IV rows:")
    extreme_high = df[df["smoothed_iv"] > 1.0].copy()
    extreme_low = df[df["smoothed_iv"] < 0.10].copy()

    print("smoothed_iv > 1.0:", len(extreme_high))
    print("smoothed_iv < 0.10:", len(extreme_low))

    lines.append("Extreme IV rows:")
    lines.append(f"smoothed_iv > 1.0: {len(extreme_high)}")
    lines.append(f"smoothed_iv < 0.10: {len(extreme_low)}")
    lines.append("")

    if len(extreme_high) > 0:
        cols = [
            "trade_date",
            "time_bucket",
            "symbol",
            "expiry_code",
            "option_type",
            "strike",
            "future_price",
            "T",
            "moneyness",
            "log_moneyness",
            "moneyness_bucket",
            "smoothed_iv",
            "implied_vol",
            "delta",
            "gamma",
            "vega",
            "theta",
            "volume",
            "openInterest",
            "BP1",
            "AP1",
        ]

        high_sample = (
            extreme_high[cols]
            .sort_values("smoothed_iv", ascending=False)
            .head(200)
        )

        high_out = OUT_DIR / "smile_extreme_high_iv.csv"
        high_sample.to_csv(
            high_out,
            index=False,
            encoding="utf-8-sig",
        )

        lines.append("Extreme high IV sample:")
        lines.append(str(high_sample.head(50)))
        lines.append(f"Saved high IV sample: {high_out}")
        lines.append("")

    if len(extreme_low) > 0:
        cols = [
            "trade_date",
            "time_bucket",
            "symbol",
            "expiry_code",
            "option_type",
            "strike",
            "future_price",
            "T",
            "moneyness",
            "log_moneyness",
            "moneyness_bucket",
            "smoothed_iv",
            "implied_vol",
            "delta",
            "gamma",
            "vega",
            "theta",
            "volume",
            "openInterest",
            "BP1",
            "AP1",
        ]

        low_sample = (
            extreme_low[cols]
            .sort_values("smoothed_iv", ascending=True)
            .head(200)
        )

        low_out = OUT_DIR / "smile_extreme_low_iv.csv"
        low_sample.to_csv(
            low_out,
            index=False,
            encoding="utf-8-sig",
        )

        lines.append("Extreme low IV sample:")
        lines.append(str(low_sample.head(50)))
        lines.append(f"Saved low IV sample: {low_out}")
        lines.append("")

    print("\nDaily average IV by bucket...")
    daily_bucket = (
        df.groupby(["trade_date", "moneyness_bucket"], observed=False)["smoothed_iv"]
        .mean()
        .reset_index()
        .pivot(
            index="trade_date",
            columns="moneyness_bucket",
            values="smoothed_iv",
        )
        .reset_index()
    )

    daily_bucket_out = OUT_DIR / "daily_smile_bucket_iv.csv"
    daily_bucket.to_csv(
        daily_bucket_out,
        index=False,
        encoding="utf-8-sig",
    )

    lines.append("Daily bucket IV file:")
    lines.append(str(daily_bucket_out))
    lines.append("")

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved report:")
    print(REPORT_FILE)
    print("Saved daily bucket IV:")
    print(daily_bucket_out)


if __name__ == "__main__":
    main()