from pathlib import Path
import pandas as pd

from config.data_version import ALL_GREEKS_FILE
from config.trading_calendar import ABNORMAL_TRADING_DATES


REPORT_PATH = Path(
    "research/reports/rebuild_greeks_v1_1_qc_report.txt"
)


GREEK_COLUMNS = [
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():

    print("Reading rebuilt Greeks...")

    df = pd.read_parquet(ALL_GREEKS_FILE)

    lines = []

    lines.append("Rebuild Greeks v1.1 QC Report")
    lines.append("=" * 80)
    lines.append("")

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    lines.append("Dataset")
    lines.append("-" * 80)

    lines.append(f"Rows: {len(df):,}")

    if "trade_date" in df.columns:

        lines.append(
            f"Trade dates: {df['trade_date'].nunique()}"
        )

        lines.append(
            f"Date range: "
            f"{df['trade_date'].min()} "
            f"-> "
            f"{df['trade_date'].max()}"
        )

    if "expiry_code" in df.columns:

        lines.append(
            f"Expiry count: "
            f"{df['expiry_code'].nunique()}"
        )

    lines.append("")

    # --------------------------------------------------
    # NaN ratios
    # --------------------------------------------------

    lines.append("NaN Ratios")
    lines.append("-" * 80)

    for col in GREEK_COLUMNS:

        if col in df.columns:

            ratio = df[col].isna().mean()

            lines.append(
                f"{col:<10}: {ratio:.6%}"
            )

    if "implied_vol" in df.columns:

        ratio = df["implied_vol"].isna().mean()

        lines.append(
            f"{'implied_vol':<10}: {ratio:.6%}"
        )

    if "smoothed_iv" in df.columns:

        ratio = df["smoothed_iv"].isna().mean()

        lines.append(
            f"{'smoothed_iv':<10}: {ratio:.6%}"
        )

    lines.append("")

    # --------------------------------------------------
    # Greeks Summary
    # --------------------------------------------------

    summary_cols = [
        c for c in (
            GREEK_COLUMNS
            + ["implied_vol", "smoothed_iv"]
        )
        if c in df.columns
    ]

    if summary_cols:

        lines.append("Summary Statistics")
        lines.append("-" * 80)

        lines.append(
            str(
                df[summary_cols].describe()
            )
        )

        lines.append("")

    # --------------------------------------------------
    # Abnormal dates
    # --------------------------------------------------

    if "trade_date" in df.columns:

        abnormal_present = sorted(
            set(df["trade_date"].unique())
            &
            ABNORMAL_TRADING_DATES
        )

        lines.append("Abnormal Trading Dates")
        lines.append("-" * 80)

        if abnormal_present:

            lines.append(
                f"WARNING: Found abnormal dates: "
                f"{abnormal_present}"
            )

        else:

            lines.append(
                "PASS: No abnormal trading dates present."
            )

        lines.append("")

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("DONE")
    print("Saved:")
    print(REPORT_PATH)


if __name__ == "__main__":

    main()