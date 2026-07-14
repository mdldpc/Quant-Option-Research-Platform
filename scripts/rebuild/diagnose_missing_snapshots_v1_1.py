from pathlib import Path
import pandas as pd

from config.trading_calendar import ABNORMAL_TRADING_DATES


BACKTEST_FILES = {
    "strangle": Path("research/exports/strangle_strategy_backtest_v1_1.csv"),
    "butterfly": Path("research/exports/butterfly_strategy_backtest_v1_1.csv"),
    "calendar": Path("research/exports/calendar_strategy_backtest_v1_1.csv"),
}

SNAPSHOT_FILES = {
    "strangle": Path("research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet"),
    "butterfly": Path("research/datasets/butterfly_daily_snapshot_2026H1_v1_1.parquet"),
    "calendar": Path("research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet"),
}

OUT_CSV = Path("research/exports/missing_snapshot_diagnostic_v1_1.csv")
OUT_REPORT = Path("research/reports/missing_snapshot_diagnostic_v1_1_report.txt")


def classify_row(strategy, row, snap):
    status = row["status"]

    if status == "ok":
        return "ok"

    entry = int(row["entry_date"])
    exit_ = int(row["exit_date"])

    if entry in ABNORMAL_TRADING_DATES or exit_ in ABNORMAL_TRADING_DATES:
        return "expected_missing_abnormal_date"

    entry_exists = (snap["trade_date"].astype(int) == entry).any()
    exit_exists = (snap["trade_date"].astype(int) == exit_).any()

    if not entry_exists and not exit_exists:
        return "missing_entry_and_exit_snapshot"

    if not entry_exists:
        return "missing_entry_snapshot"

    if not exit_exists:
        return "missing_exit_snapshot"

    if strategy in ["strangle", "butterfly"]:
        expiry = row.get("expiry_code")

        if pd.notna(expiry):
            expiry = int(expiry)

            entry_pair = snap[
                (snap["trade_date"].astype(int) == entry)
                & (snap["expiry_code"].astype(int) == expiry)
            ]

            exit_pair = snap[
                (snap["trade_date"].astype(int) == exit_)
                & (snap["expiry_code"].astype(int) == expiry)
            ]

            if entry_pair.empty and exit_pair.empty:
                return "missing_entry_and_exit_expiry_pair"

            if entry_pair.empty:
                return "missing_entry_expiry_pair"

            if exit_pair.empty:
                return "missing_exit_expiry_pair"

        return "unknown_missing_snapshot"

    if strategy == "calendar":
        near_expiry = row.get("near_expiry")
        next_expiry = row.get("next_expiry")

        if pd.notna(near_expiry) and pd.notna(next_expiry):
            near_expiry = int(float(near_expiry))
            next_expiry = int(float(next_expiry))

            exit_pair = snap[
                (snap["trade_date"].astype(int) == exit_)
                & (snap["near_expiry"].astype(int) == near_expiry)
                & (snap["next_expiry"].astype(int) == next_expiry)
            ]

            if exit_pair.empty:
                return "missing_exit_calendar_pair"

        return "unknown_calendar_missing"

    return "unknown"


def main():
    rows = []

    for strategy, backtest_file in BACKTEST_FILES.items():
        print("Reading:", strategy)

        bt = pd.read_csv(backtest_file)
        snap = pd.read_parquet(SNAPSHOT_FILES[strategy])
        snap["trade_date"] = snap["trade_date"].astype(int)

        for _, row in bt.iterrows():
            diagnosis = classify_row(strategy, row, snap)

            rows.append({
                "strategy": strategy,
                "trade_id": row.get("trade_id"),
                "status": row.get("status"),
                "diagnosis": diagnosis,
                "entry_date": row.get("entry_date"),
                "exit_date": row.get("exit_date"),
                "expiry_code": row.get("expiry_code"),
                "near_expiry": row.get("near_expiry"),
                "next_expiry": row.get("next_expiry"),
            })

    out = pd.DataFrame(rows)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Missing Snapshot Diagnostic v1.1")
    lines.append("=" * 80)
    lines.append("")
    lines.append("Diagnosis counts:")
    lines.append(str(out["diagnosis"].value_counts()))
    lines.append("")
    lines.append("Diagnosis by strategy:")
    lines.append(str(pd.crosstab(out["strategy"], out["diagnosis"])))
    lines.append("")
    lines.append("Non-OK rows:")
    lines.append(str(out[out["diagnosis"] != "ok"]))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()