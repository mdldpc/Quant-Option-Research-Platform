from pathlib import Path
import pandas as pd
import numpy as np

SOURCE_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\smile_dataset_near_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_greeks_summary.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\daily_greeks_summary.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\daily_greeks_summary_report.txt"
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

BUCKET_ORDER = [
    "deep_low_moneyness",
    "low_moneyness",
    "slightly_low_moneyness",
    "atm",
    "slightly_high_moneyness",
    "high_moneyness",
    "deep_high_moneyness",
]


def main():
    print("Reading near smile dataset...")
    df = pd.read_parquet(SOURCE_FILE)

    print("Source shape:")
    print(df.shape)

    print("Filtering valid rows...")
    df = df[
        df["moneyness_bucket"].notna()
        & df["smoothed_iv"].notna()
    ].copy()

    for col in GREEKS:
        df = df[np.isfinite(df[col])]

    print("Valid shape:")
    print(df.shape)

    print("Building daily Greeks summary...")

    agg_dict = {
        "row_count": ("symbol", "count"),
        "volume_sum": ("volume", "sum"),
        "openInterest_sum": ("openInterest", "sum"),
        "iv_mean": ("smoothed_iv", "mean"),
        "iv_median": ("smoothed_iv", "median"),
    }

    for greek in GREEKS:
        agg_dict[f"{greek}_mean"] = (greek, "mean")
        agg_dict[f"{greek}_median"] = (greek, "median")
        agg_dict[f"{greek}_std"] = (greek, "std")
        agg_dict[f"{greek}_min"] = (greek, "min")
        agg_dict[f"{greek}_max"] = (greek, "max")

    daily = (
        df.groupby(
            ["trade_date", "moneyness_bucket"],
            observed=False,
        )
        .agg(**agg_dict)
        .reset_index()
    )

    print("Daily Greeks summary shape:")
    print(daily.shape)

    daily["trade_date_dt"] = pd.to_datetime(
        daily["trade_date"].astype(str)
    )

    daily = daily.sort_values(
        ["trade_date", "moneyness_bucket"]
    )

    print("\nBucket counts:")
    print(daily["moneyness_bucket"].value_counts().sort_index())

    print("\nGamma summary:")
    print(daily["gamma_mean"].describe())

    print("\nVega summary:")
    print(daily["vega_mean"].describe())

    print("\nTheta summary:")
    print(daily["theta_mean"].describe())

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
    lines.append("Daily Greeks Summary Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
    lines.append(f"Output parquet: {OUT_FILE}")
    lines.append(f"Output csv: {OUT_CSV}")
    lines.append("")
    lines.append(f"Source shape: {df.shape}")
    lines.append(f"Daily shape: {daily.shape}")
    lines.append("")
    lines.append(f"Trade dates: {daily['trade_date'].nunique()}")
    lines.append("")
    lines.append("Bucket counts:")
    lines.append(str(daily["moneyness_bucket"].value_counts().sort_index()))
    lines.append("")
    lines.append("IV mean by bucket:")
    lines.append(
        str(
            daily.groupby("moneyness_bucket", observed=False)["iv_mean"]
            .mean()
        )
    )
    lines.append("")
    for greek in GREEKS:
        lines.append(f"{greek} mean summary:")
        lines.append(str(daily[f"{greek}_mean"].describe()))
        lines.append("")

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


if __name__ == "__main__":
    main()