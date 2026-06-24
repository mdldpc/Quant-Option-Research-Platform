from pathlib import Path
import pandas as pd

DATA_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\final_view\daily_greeks_summary.csv"
)

GREEKS = [
    "implied_vol",
    "smoothed_iv",
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():
    print("Reading dataset...")
    df = pd.read_parquet(DATA_FILE)

    print("Creating daily summary...")

    summary = (
        df.groupby("trade_date")
        .agg(
            row_count=("symbol", "count"),

            implied_vol_mean=("implied_vol", "mean"),
            implied_vol_median=("implied_vol", "median"),
            implied_vol_std=("implied_vol", "std"),

            smoothed_iv_mean=("smoothed_iv", "mean"),
            smoothed_iv_median=("smoothed_iv", "median"),
            smoothed_iv_std=("smoothed_iv", "std"),

            delta_mean=("delta", "mean"),
            delta_abs_sum=("delta", lambda x: x.abs().sum()),

            gamma_mean=("gamma", "mean"),
            gamma_sum=("gamma", "sum"),

            vega_mean=("vega", "mean"),
            vega_sum=("vega", "sum"),

            theta_mean=("theta", "mean"),
            theta_sum=("theta", "sum"),

            vanna_mean=("vanna", "mean"),
            vanna_sum=("vanna", "sum"),

            vomma_mean=("vomma", "mean"),
            vomma_sum=("vomma", "sum"),

            speed_mean=("speed", "mean"),
            speed_sum=("speed", "sum"),
        )
        .reset_index()
    )

    summary.to_csv(
        OUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print("DONE")
    print("Saved to:")
    print(OUT_FILE)
    print("\nPreview:")
    print(summary.head(20))


if __name__ == "__main__":
    main()