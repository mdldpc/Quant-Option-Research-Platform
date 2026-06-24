import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd

from config.paths import (
    OPTION_TRADE_DATASET,
    EXPORTS_DIR,
    REPORTS_DIR,
)

from analysis.experiments import (
    threshold_experiment,
    holding_experiment,
    cost_experiment,
)

from utils.io import save_csv, save_text


OUT_CSV = EXPORTS_DIR / "robustness_suite_results.csv"
OUT_REPORT = REPORTS_DIR / "robustness_suite_report.txt"


def run_suite():

    print("Reading option trades...")
    trades = pd.read_parquet(OPTION_TRADE_DATASET)

    print("Shape:", trades.shape)

    results = []

    # =========================
    # 1. Threshold Sweep
    # =========================
    thresholds = [70, 75, 80, 85, 90]

    print("\nRunning Threshold Sweep...")
    for t in thresholds:
        res = threshold_experiment(trades, t)
        res["experiment"] = "threshold"
        results.append(res)

    # =========================
    # 2. Holding Sweep
    # =========================
    holdings = [3, 5, 7, 10, 15]

    print("\nRunning Holding Sweep...")
    for h in holdings:
        res = holding_experiment(trades, h)
        res["experiment"] = "holding"
        results.append(res)

    # =========================
    # 3. Cost Sweep
    # =========================
    costs = [0.0, 0.001, 0.002, 0.005]

    print("\nRunning Cost Sweep...")
    for c in costs:
        res = cost_experiment(trades, c)
        res["experiment"] = "cost"
        results.append(res)

    # =========================
    # Final Output
    # =========================
    result_df = pd.DataFrame(results)

    print("\nFinal Results:")
    print(result_df)

    save_csv(result_df, OUT_CSV)

    report = []
    report.append("=" * 60)
    report.append("ROBUSTNESS SUITE REPORT (V1)")
    report.append("=" * 60)
    report.append("")
    report.append(result_df.to_string(index=False))

    save_text("\n".join(report), OUT_REPORT)

    print("\nDONE")


if __name__ == "__main__":
    run_suite()