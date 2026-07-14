from pathlib import Path
import pandas as pd

from analysis.risk_management import recommend_risk_action


INPUT_FILE = Path("research/datasets/portfolio_greeks_2026H1.parquet")

OUT_DATASET = Path("research/datasets/portfolio_exposure_risk_2026H1.parquet")
OUT_CSV = Path("research/exports/portfolio_exposure_risk_2026H1.csv")
OUT_REPORT = Path("research/reports/portfolio_exposure_risk_summary.txt")


THRESHOLDS = {
    "delta": 0.30,
    "gamma": 0.004,
    "vega": 1500,
    "theta": 1200,
}


def classify_risk_level(row):
    warning_count = int(row["warning_count"])

    if warning_count >= 3:
        return "high"
    if warning_count >= 1:
        return "medium"
    return "low"


def main():
    print("Reading portfolio Greeks...")
    df = pd.read_parquet(INPUT_FILE)

    df = df.copy()

    for col in [
        "net_delta",
        "net_gamma",
        "net_vega",
        "net_theta",
        "net_vanna",
        "net_vomma",
    ]:
        df[col] = df[col].astype(float)

    df["delta_warning"] = df["net_delta"].abs() > THRESHOLDS["delta"]
    df["gamma_warning"] = df["net_gamma"].abs() > THRESHOLDS["gamma"]
    df["vega_warning"] = df["net_vega"].abs() > THRESHOLDS["vega"]
    df["theta_warning"] = df["net_theta"].abs() > THRESHOLDS["theta"]

    warning_cols = [
        "delta_warning",
        "gamma_warning",
        "vega_warning",
        "theta_warning",
    ]

    df["warning_count"] = df[warning_cols].fillna(False).sum(axis=1)
    df["risk_level"] = df.apply(classify_risk_level, axis=1)
    df["risk_flag"] = df["risk_level"].isin(["medium", "high"])

    df["recommended_action"] = df.apply(recommend_risk_action, axis=1)

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(OUT_DATASET, index=False)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Portfolio Exposure Risk Summary")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input file: {INPUT_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append("Thresholds:")
    for k, v in THRESHOLDS.items():
        lines.append(f"- {k}: {v}")

    lines.append("")
    lines.append(f"Rows: {len(df)}")
    lines.append(f"Trades: {df['trade_id'].nunique()}")

    lines.append("")
    lines.append("Risk level counts:")
    lines.append(str(df["risk_level"].value_counts()))

    lines.append("")
    lines.append("Warning counts:")
    for col in warning_cols:
        lines.append(f"{col}: {int(df[col].sum())}")

    lines.append("")
    lines.append("Rows with risk flags:")
    risk_rows = df[df["risk_flag"]]

    if risk_rows.empty:
        lines.append("No risk flags.")
    else:
        lines.append(
            str(
                risk_rows[
                    [
                        "trade_id",
                        "trade_date",
                        "net_delta",
                        "net_gamma",
                        "net_vega",
                        "net_theta",
                        "warning_count",
                        "risk_level",
                        "recommended_action",
                    ]
                ]
            )
        )

    lines.append("")
    lines.append("Recommended action counts:")
    lines.append(str(df["recommended_action"].value_counts()))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()