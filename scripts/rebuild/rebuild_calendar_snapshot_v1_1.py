from pathlib import Path
import pandas as pd

from analysis.execution_snapshot import (
    build_strategy_snapshot,
    save_strategy_snapshot,
)


INPUT_FILE = Path("research/datasets/calendar_spread_dataset_2026H1_v1_1.parquet")

OUT_DATASET = Path("research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet")
OUT_CSV = Path("research/exports/calendar_daily_snapshot_2026H1_v1_1.csv")
OUT_REPORT = Path("research/reports/calendar_daily_snapshot_v1_1_report.txt")


def main():
    print("Reading calendar spread dataset v1.1...")
    df = pd.read_parquet(INPUT_FILE)

    print("Source shape:")
    print(df.shape)

    df["trade_date"] = df["trade_date"].astype(int)

    snapshot = build_strategy_snapshot(
        df=df,
        strategy_name="calendar_spread",
        group_cols=["trade_date", "near_expiry", "next_expiry"],
        price_col="calendar_price",
        time_col="time_bucket",
        target_time_bucket=None,
        max_time_distance=None,
        fallback_to_latest=True,
        allow_negative_price=True,
    )

    snapshot = snapshot.sort_values(
        ["trade_date", "near_expiry", "next_expiry"]
    ).reset_index(drop=True)

    save_strategy_snapshot(
        snapshot=snapshot,
        dataset_path=OUT_DATASET,
        csv_path=OUT_CSV,
        report_path=OUT_REPORT,
        price_col="calendar_price",
    )

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()