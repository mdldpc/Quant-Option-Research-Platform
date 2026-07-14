from pathlib import Path

import pandas as pd

from framework.market.trading_filter import TradingFilter


DATA_FILE = Path(
    "research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet"
)


def main():

    print("=" * 80)
    print("Trading Filter Test v1.1")
    print("=" * 80)

    df = pd.read_parquet(DATA_FILE)

    print()
    print("Raw rows :", len(df))

    cleaned = TradingFilter.clean(df)

    print("Clean rows:", len(cleaned))
    print("Removed   :", len(df) - len(cleaned))

    print()

    if "updateTime" in cleaned.columns:

        print("Session check")

        sample = cleaned["updateTime"].astype(int).head(10)

        print(sample.tolist())

    print()

    print("First five rows")

    print(cleaned.head())

    report = []

    report.append("Trading Filter Test v1.1")
    report.append("=" * 80)
    report.append("")

    report.append(f"Raw rows      : {len(df)}")
    report.append(f"Clean rows    : {len(cleaned)}")
    report.append(f"Removed rows  : {len(df)-len(cleaned)}")

    report_path = Path(
        "research/reports/trading_filter_test_v1_1_report.txt"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    cleaned.to_csv(
        "research/exports/trading_filter_cleaned_sample_v1_1.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print()
    print("DONE")
    print("Saved:")
    print(report_path)
    print(
        "research/exports/trading_filter_cleaned_sample_v1_1.csv"
    )


if __name__ == "__main__":
    main()