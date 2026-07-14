from pathlib import Path
import pandas as pd


ATM_FILE = Path("research/datasets/atm_signal_2026H1.parquet")
CAL_FILE = Path("research/datasets/calendar_signal_2026H1.parquet")

OUT_DATASET = Path("research/datasets/signal_relationship_2026H1.parquet")
OUT_CSV = Path("research/exports/signal_relationship_2026H1.csv")
OUT_REPORT = Path("research/reports/signal_relationship_summary.txt")


def classify_signal_type(row):
    if row["atm_entry_signal"] and row["calendar_entry_signal"]:
        return "agreement"
    if row["atm_entry_signal"] and not row["calendar_entry_signal"]:
        return "atm_only"
    if (not row["atm_entry_signal"]) and row["calendar_entry_signal"]:
        return "calendar_only"
    return "none"


def main():
    print("Reading ATM signal...")
    atm = pd.read_parquet(ATM_FILE)

    print("Reading Calendar signal...")
    cal = pd.read_parquet(CAL_FILE)

    atm = atm[
        [
            "trade_date",
            "signal_value",
            "signal_score",
            "iv_score",
            "slope_score",
            "entry_signal",
            "exit_signal",
            "signal_state",
        ]
    ].copy()

    atm = atm.rename(
        columns={
            "signal_value": "atm_signal_value",
            "signal_score": "atm_signal_score",
            "entry_signal": "atm_entry_signal",
            "exit_signal": "atm_exit_signal",
            "signal_state": "atm_signal_state",
        }
    )

    cal = cal[
        [
            "trade_date",
            "next_minus_near_iv",
            "spread_zscore",
            "entry_signal",
            "exit_signal",
        ]
    ].copy()

    cal = cal.rename(
        columns={
            "next_minus_near_iv": "calendar_spread",
            "spread_zscore": "calendar_zscore",
            "entry_signal": "calendar_entry_signal",
            "exit_signal": "calendar_exit_signal",
        }
    )

    atm["trade_date"] = atm["trade_date"].astype(int)
    cal["trade_date"] = cal["trade_date"].astype(int)

    rel = atm.merge(cal, on="trade_date", how="inner")

    rel["signal_type"] = rel.apply(classify_signal_type, axis=1)
    rel["confirmed_entry"] = rel["signal_type"] == "agreement"

    rel["any_entry"] = rel["atm_entry_signal"] | rel["calendar_entry_signal"]

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    rel.to_parquet(OUT_DATASET, index=False)
    rel.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    total = len(rel)
    atm_entry = int(rel["atm_entry_signal"].sum())
    cal_entry = int(rel["calendar_entry_signal"].sum())
    confirmed = int(rel["confirmed_entry"].sum())
    any_entry = int(rel["any_entry"].sum())

    lines = []
    lines.append("Signal Relationship Summary")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"ATM signal file: {ATM_FILE}")
    lines.append(f"Calendar signal file: {CAL_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Rows: {total}")
    lines.append(f"ATM entry days: {atm_entry}")
    lines.append(f"Calendar entry days: {cal_entry}")
    lines.append(f"Confirmed entry days: {confirmed}")
    lines.append(f"Any entry days: {any_entry}")
    lines.append("")
    lines.append(f"ATM entry rate: {atm_entry / total:.2%}")
    lines.append(f"Calendar entry rate: {cal_entry / total:.2%}")
    lines.append(f"Confirmation rate among ATM entries: {confirmed / atm_entry:.2%}" if atm_entry else "N/A")
    lines.append(f"Confirmation rate among Calendar entries: {confirmed / cal_entry:.2%}" if cal_entry else "N/A")
    lines.append("")
    lines.append("Signal type counts:")
    lines.append(str(rel["signal_type"].value_counts()))
    lines.append("")
    lines.append("Confirmed entry dates:")
    lines.append(str(rel.loc[
        rel["confirmed_entry"],
        [
            "trade_date",
            "atm_signal_score",
            "iv_score",
            "slope_score",
            "calendar_spread",
            "calendar_zscore",
        ],
    ]))
    lines.append("")
    lines.append("ATM only dates:")
    lines.append(str(rel.loc[
        rel["signal_type"] == "atm_only",
        ["trade_date", "atm_signal_score", "calendar_zscore"],
    ]))
    lines.append("")
    lines.append("Calendar only dates:")
    lines.append(str(rel.loc[
        rel["signal_type"] == "calendar_only",
        ["trade_date", "atm_signal_score", "calendar_zscore"],
    ]))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()