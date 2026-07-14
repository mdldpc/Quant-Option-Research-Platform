from pathlib import Path
import pandas as pd


INPUT_FILE = Path("research/datasets/term_structure_wide.parquet")

OUT_DATASET = Path("research/datasets/calendar_signal_2026H1.parquet")
OUT_CSV = Path("research/exports/calendar_signal_2026H1.csv")
OUT_REPORT = Path("research/reports/calendar_signal_summary.txt")


ROLLING_WINDOW = 20
ENTRY_Z = 1.0
EXIT_Z = 0.2


def main():
    print("Reading term structure dataset...")
    df = pd.read_parquet(INPUT_FILE)

    df = df.copy()
    df["trade_date"] = df["trade_date"].astype(int)

    required_cols = [
        "trade_date",
        "time_bucket",
        "near_expiry",
        "near_iv",
        "near_strike",
        "near_future",
        "next_expiry",
        "next_iv",
        "next_strike",
        "next_future",
        "next_minus_near_iv",
    ]

    df = df[required_cols].dropna(subset=["near_iv", "next_iv", "next_minus_near_iv"])

    daily = (
        df.groupby("trade_date", as_index=False)
        .agg(
            near_iv=("near_iv", "mean"),
            next_iv=("next_iv", "mean"),
            next_minus_near_iv=("next_minus_near_iv", "mean"),
            near_expiry=("near_expiry", "first"),
            next_expiry=("next_expiry", "first"),
            near_strike=("near_strike", "median"),
            next_strike=("next_strike", "median"),
            near_future=("near_future", "mean"),
            next_future=("next_future", "mean"),
        )
        .sort_values("trade_date")
    )

    daily["spread_mean"] = (
        daily["next_minus_near_iv"]
        .rolling(ROLLING_WINDOW, min_periods=5)
        .mean()
    )

    daily["spread_std"] = (
        daily["next_minus_near_iv"]
        .rolling(ROLLING_WINDOW, min_periods=5)
        .std()
    )

    daily["spread_zscore"] = (
        (daily["next_minus_near_iv"] - daily["spread_mean"])
        / daily["spread_std"]
    )

    # Entry: next IV is unusually high relative to near IV.
    daily["entry_signal"] = daily["spread_zscore"] >= ENTRY_Z

    # Exit: spread has normalized.
    daily["exit_signal"] = daily["spread_zscore"].abs() <= EXIT_Z

    daily["strategy_view"] = "short_next_vol_long_near_vol"

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    daily.to_parquet(OUT_DATASET, index=False)
    daily.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Calendar Signal Summary")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input file: {INPUT_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Rolling window: {ROLLING_WINDOW}")
    lines.append(f"Entry z-score threshold: {ENTRY_Z}")
    lines.append(f"Exit z-score threshold: {EXIT_Z}")
    lines.append("")
    lines.append(f"Rows: {len(daily)}")
    lines.append(f"Trade dates: {daily['trade_date'].nunique()}")
    lines.append("")
    lines.append("next_minus_near_iv summary:")
    lines.append(str(daily["next_minus_near_iv"].describe()))
    lines.append("")
    lines.append("spread_zscore summary:")
    lines.append(str(daily["spread_zscore"].describe()))
    lines.append("")
    lines.append("Entry signal count:")
    lines.append(str(daily["entry_signal"].value_counts()))
    lines.append("")
    lines.append("Exit signal count:")
    lines.append(str(daily["exit_signal"].value_counts()))
    lines.append("")
    lines.append("Entry signal dates:")
    lines.append(str(daily.loc[daily["entry_signal"], ["trade_date", "next_minus_near_iv", "spread_zscore"]]))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()