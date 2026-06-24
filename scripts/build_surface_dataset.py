from pathlib import Path
import pandas as pd
import numpy as np

SOURCE_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\smile_dataset_near_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\surface_dataset_near_2026H1.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\surface_dataset_near_preview.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\surface_dataset_near_summary.txt"
)

# 使用固定 moneyness 网格，方便后面画 heatmap / surface
GRID_BINS = [
    -np.inf,
    0.90,
    0.95,
    0.98,
    1.02,
    1.05,
    1.10,
    np.inf,
]

GRID_LABELS = [
    "moneyness_lt_0_90",
    "moneyness_0_90_0_95",
    "moneyness_0_95_0_98",
    "moneyness_0_98_1_02",
    "moneyness_1_02_1_05",
    "moneyness_1_05_1_10",
    "moneyness_gt_1_10",
]


def main():
    print("Reading near smile dataset...")
    df = pd.read_parquet(SOURCE_FILE)

    print("Source shape:")
    print(df.shape)

    print("Filtering valid rows...")
    df = df[
        df["smoothed_iv"].notna()
        & np.isfinite(df["smoothed_iv"])
        & df["moneyness"].notna()
        & np.isfinite(df["moneyness"])
    ].copy()

    print("Valid shape:")
    print(df.shape)

    print("Assigning surface moneyness grid...")
    df["surface_moneyness_bucket"] = pd.cut(
        df["moneyness"],
        bins=GRID_BINS,
        labels=GRID_LABELS,
        include_lowest=True,
    )

    print("Building surface dataset...")

    # 一行 = trade_date × time_bucket × moneyness bucket
    # 对同一个 bucket 内的所有合约取平均 IV
    surface = (
        df.groupby(
            [
                "trade_date",
                "time_bucket",
                "surface_moneyness_bucket",
            ],
            observed=False,
        )
        .agg(
            smoothed_iv_mean=("smoothed_iv", "mean"),
            smoothed_iv_median=("smoothed_iv", "median"),
            smoothed_iv_std=("smoothed_iv", "std"),
            implied_vol_mean=("implied_vol", "mean"),
            row_count=("symbol", "count"),
            avg_moneyness=("moneyness", "mean"),
            avg_log_moneyness=("log_moneyness", "mean"),
            avg_abs_log_moneyness=("abs_log_moneyness", "mean"),
            avg_T=("T", "mean"),
            call_count=("option_type", lambda x: (x == "C").sum()),
            put_count=("option_type", lambda x: (x == "P").sum()),
            volume_sum=("volume", "sum"),
            openInterest_sum=("openInterest", "sum"),
        )
        .reset_index()
    )

    print("Surface shape:")
    print(surface.shape)

    print("Adding date-level metadata...")
    surface["trade_date_dt"] = pd.to_datetime(
        surface["trade_date"].astype(str)
    )

    surface = surface.sort_values(
        [
            "trade_date",
            "time_bucket",
            "surface_moneyness_bucket",
        ]
    )

    print("\nBucket counts:")
    print(surface["surface_moneyness_bucket"].value_counts().sort_index())

    print("\nIV summary:")
    print(surface["smoothed_iv_mean"].describe())

    print("\nRow count summary:")
    print(surface["row_count"].describe())

    print("Saving outputs...")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    surface.to_parquet(OUT_FILE, index=False)

    surface.head(100_000).to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("====================================")
    lines.append("Near Surface Dataset Summary")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
    lines.append(f"Output file: {OUT_FILE}")
    lines.append(f"Preview CSV: {OUT_CSV}")
    lines.append("")
    lines.append(f"Source shape: {df.shape}")
    lines.append(f"Surface shape: {surface.shape}")
    lines.append("")
    lines.append(f"Trade dates: {surface['trade_date'].nunique()}")
    lines.append(f"Time buckets: {surface[['trade_date', 'time_bucket']].drop_duplicates().shape[0]}")
    lines.append("")
    lines.append("Surface moneyness bucket counts:")
    lines.append(
        str(surface["surface_moneyness_bucket"].value_counts().sort_index())
    )
    lines.append("")
    lines.append("Smoothed IV mean summary:")
    lines.append(str(surface["smoothed_iv_mean"].describe()))
    lines.append("")
    lines.append("Row count summary:")
    lines.append(str(surface["row_count"].describe()))
    lines.append("")
    lines.append("Average IV by bucket:")
    lines.append(
        str(
            surface.groupby(
                "surface_moneyness_bucket",
                observed=False,
            )["smoothed_iv_mean"].mean()
        )
    )

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved parquet:")
    print(OUT_FILE)
    print("Saved preview:")
    print(OUT_CSV)
    print("Saved report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()