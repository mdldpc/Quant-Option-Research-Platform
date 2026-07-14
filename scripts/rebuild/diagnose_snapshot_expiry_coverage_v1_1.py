from pathlib import Path
import pandas as pd


STRANGLE_SNAPSHOT = Path("research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet")
BUTTERFLY_SNAPSHOT = Path("research/datasets/butterfly_daily_snapshot_2026H1_v1_1.parquet")
CALENDAR_SNAPSHOT = Path("research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet")

BACKTEST_FILES = {
    "strangle": Path("research/exports/strangle_strategy_backtest_v1_1.csv"),
    "butterfly": Path("research/exports/butterfly_strategy_backtest_v1_1.csv"),
    "calendar": Path("research/exports/calendar_strategy_backtest_v1_1.csv"),
}

OUT_CSV = Path("research/exports/snapshot_expiry_coverage_v1_1.csv")
OUT_REPORT = Path("research/reports/snapshot_expiry_coverage_v1_1_report.txt")


def expiry_list(df, trade_date):
    x = df[df["trade_date"].astype(int) == int(trade_date)]
    if x.empty:
        return ""
    return ",".join(str(int(v)) for v in sorted(x["expiry_code"].dropna().unique()))


def calendar_pair_list(df, trade_date):
    x = df[df["trade_date"].astype(int) == int(trade_date)]
    if x.empty:
        return ""
    pairs = (
        x[["near_expiry", "next_expiry"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["near_expiry", "next_expiry"])
    )
    return ",".join(
        f"{int(r.near_expiry)}/{int(r.next_expiry)}"
        for _, r in pairs.iterrows()
    )


def main():
    strangle = pd.read_parquet(STRANGLE_SNAPSHOT)
    butterfly = pd.read_parquet(BUTTERFLY_SNAPSHOT)
    calendar = pd.read_parquet(CALENDAR_SNAPSHOT)

    rows = []

    for strategy, f in BACKTEST_FILES.items():
        bt = pd.read_csv(f)

        for _, r in bt.iterrows():
            entry = int(r["entry_date"])
            exit_ = int(r["exit_date"])

            rows.append({
                "strategy": strategy,
                "trade_id": r["trade_id"],
                "status": r["status"],
                "entry_date": entry,
                "exit_date": exit_,
                "trade_expiry_code": r.get("expiry_code"),
                "trade_near_expiry": r.get("near_expiry"),
                "trade_next_expiry": r.get("next_expiry"),

                "entry_strangle_expiries": expiry_list(strangle, entry),
                "exit_strangle_expiries": expiry_list(strangle, exit_),

                "entry_butterfly_expiries": expiry_list(butterfly, entry),
                "exit_butterfly_expiries": expiry_list(butterfly, exit_),

                "entry_calendar_pairs": calendar_pair_list(calendar, entry),
                "exit_calendar_pairs": calendar_pair_list(calendar, exit_),
            })

    out = pd.DataFrame(rows)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Snapshot Expiry Coverage Diagnostic v1.1")
    lines.append("=" * 80)
    lines.append("")
    lines.append("Non-OK trades with available snapshot coverage:")
    lines.append(str(out[out["status"] != "ok"]))
    lines.append("")
    lines.append("Full coverage table:")
    lines.append(str(out))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()