from pathlib import Path
import numpy as np
import pandas as pd

SOURCE_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\smile_dataset_near_2026H1.parquet"
)

PREVIEW_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\smile_dataset_near_preview.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\smile_dataset_near_summary.txt"
)


KEEP_COLS = [
    "trade_date",
    "time_bucket",
    "symbol",
    "expiry_code",
    "option_type",
    "strike",
    "future_price",
    "T",
    "implied_vol",
    "smoothed_iv",
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
    "volume",
    "openInterest",
    "BP1",
    "AP1",
]


def main():
    print("Reading all Greeks dataset...")
    df = pd.read_parquet(SOURCE_FILE, columns=KEEP_COLS)

    print("Source shape:")
    print(df.shape)

    print("Finding near expiry for each trade_date/time_bucket...")

    near_map = (
        df.groupby(["trade_date", "time_bucket"], as_index=False)
        .agg(near_T=("T", "min"))
    )

    df = df.merge(
        near_map,
        on=["trade_date", "time_bucket"],
        how="left",
    )

    print("Filtering near expiry rows...")
    near_df = df[df["T"] == df["near_T"]].copy()

    near_df["term_rank"] = 1

    print("Near smile shape:")
    print(near_df.shape)

    print("Calculating moneyness...")
    near_df["moneyness"] = near_df["strike"] / near_df["future_price"]
    near_df["log_moneyness"] = np.log(near_df["moneyness"])
    near_df["abs_log_moneyness"] = near_df["log_moneyness"].abs()

    print("Creating moneyness buckets...")

    bins = [
        -np.inf,
        0.90,
        0.95,
        0.98,
        1.02,
        1.05,
        1.10,
        np.inf,
    ]

    labels = [
        "deep_low_moneyness",
        "low_moneyness",
        "slightly_low_moneyness",
        "atm",
        "slightly_high_moneyness",
        "high_moneyness",
        "deep_high_moneyness",
    ]

    near_df["moneyness_bucket"] = pd.cut(
        near_df["moneyness"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )

    ordered_cols = [
        "trade_date",
        "time_bucket",
        "term_rank",
        "symbol",
        "expiry_code",
        "option_type",
        "strike",
        "future_price",
        "T",
        "moneyness",
        "log_moneyness",
        "abs_log_moneyness",
        "moneyness_bucket",
        "smoothed_iv",
        "implied_vol",
        "delta",
        "gamma",
        "vega",
        "theta",
        "vanna",
        "vomma",
        "speed",
        "volume",
        "openInterest",
        "BP1",
        "AP1",
    ]

    near_df = near_df[ordered_cols].sort_values(
        ["trade_date", "time_bucket", "expiry_code", "strike", "option_type"]
    )

    print("\nFinal shape:")
    print(near_df.shape)

    print("\nTrade dates:")
    print(near_df["trade_date"].nunique())

    print("\nUnique expiry codes:")
    print(near_df["expiry_code"].nunique())

    print("\nOption type counts:")
    print(near_df["option_type"].value_counts())

    print("\nMoneyness bucket counts:")
    print(near_df["moneyness_bucket"].value_counts(dropna=False).sort_index())

    print("\nIV summary:")
    print(near_df["smoothed_iv"].describe())

    print("Saving outputs...")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    near_df.to_parquet(OUT_FILE, index=False)

    near_df.head(100_000).to_csv(
        PREVIEW_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("====================================")
    lines.append("Near Smile Dataset Summary")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
    lines.append(f"Output file: {OUT_FILE}")
    lines.append(f"Preview CSV: {PREVIEW_CSV}")
    lines.append("")
    lines.append(f"Final shape: {near_df.shape}")
    lines.append(f"Trade dates: {near_df['trade_date'].nunique()}")
    lines.append(f"Unique expiry codes: {near_df['expiry_code'].nunique()}")
    lines.append("")
    lines.append("Option type counts:")
    lines.append(str(near_df["option_type"].value_counts()))
    lines.append("")
    lines.append("Moneyness bucket counts:")
    lines.append(str(near_df["moneyness_bucket"].value_counts(dropna=False).sort_index()))
    lines.append("")
    lines.append("Smoothed IV summary:")
    lines.append(str(near_df["smoothed_iv"].describe()))
    lines.append("")
    lines.append("Log moneyness summary:")
    lines.append(str(near_df["log_moneyness"].describe()))
    lines.append("")
    lines.append("Rows by trade_date summary:")
    lines.append(str(near_df.groupby("trade_date").size().describe()))

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved parquet:")
    print(OUT_FILE)
    print("Saved preview:")
    print(PREVIEW_CSV)
    print("Saved report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()