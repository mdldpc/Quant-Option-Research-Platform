from pathlib import Path
import pandas as pd


INPUT_FILE = Path("research/exports/daily_signal_features.csv")

OUT_DATASET = Path("research/datasets/atm_signal_2026H1.parquet")
OUT_CSV = Path("research/exports/atm_signal_2026H1.csv")
OUT_REPORT = Path("research/reports/atm_signal_summary.txt")


ENTRY_SCORE = 80
EXIT_SCORE = 40


def classify_state(score: float) -> str:
    if score >= ENTRY_SCORE:
        return "entry"
    if score <= EXIT_SCORE:
        return "exit"
    return "hold"


def classify_strength(score: float) -> str:
    if score >= 80:
        return "strong"
    if score >= 60:
        return "medium"
    if score >= 40:
        return "weak"
    return "none"


def main():
    print("Reading daily signal features...")
    df = pd.read_csv(INPUT_FILE)

    out = df.copy()

    out["trade_date"] = out["trade_date"].astype(int)
    out["signal_name"] = "atm_signal"
    out["signal_source"] = "market_opportunity_score"
    out["signal_value"] = out["signal_score"]

    out["entry_signal"] = out["signal_score"] >= ENTRY_SCORE
    out["exit_signal"] = out["signal_score"] <= EXIT_SCORE

    out["signal_state"] = out["signal_score"].apply(classify_state)
    out["signal_strength_v1_1"] = out["signal_score"].apply(classify_strength)

    keep_cols = [
        "trade_date",
        "trade_date_dt",
        "signal_name",
        "signal_source",
        "signal_value",
        "signal_score",
        "iv_score",
        "slope_score",
        "entry_signal",
        "exit_signal",
        "signal_state",
        "signal_strength",
        "signal_strength_v1_1",
        "long_signal",
        "near_iv",
        "next_iv",
        "term_slope_next_near",
        "near_iv_zscore",
        "near_iv_percentile_20d",
    ]

    out = out[keep_cols]

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_DATASET, index=False)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("ATM Signal Dataset Summary")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input file: {INPUT_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Entry score threshold: {ENTRY_SCORE}")
    lines.append(f"Exit score threshold: {EXIT_SCORE}")
    lines.append("")
    lines.append(f"Rows: {len(out)}")
    lines.append(f"Trade dates: {out['trade_date'].nunique()}")
    lines.append("")
    lines.append("Signal score summary:")
    lines.append(str(out["signal_score"].describe()))
    lines.append("")
    lines.append("Signal state counts:")
    lines.append(str(out["signal_state"].value_counts()))
    lines.append("")
    lines.append("Entry signal count:")
    lines.append(str(out["entry_signal"].value_counts()))
    lines.append("")
    lines.append("Exit signal count:")
    lines.append(str(out["exit_signal"].value_counts()))
    lines.append("")
    lines.append("Signal component summary:")
    lines.append(str(out[["iv_score", "slope_score"]].describe()))
    lines.append("")
    lines.append("Entry signal dates:")
    lines.append(str(out.loc[out["entry_signal"], ["trade_date", "signal_score", "iv_score", "slope_score"]]))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()