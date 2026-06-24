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

from config.settings import TRANSACTION_COST_GRID
from analysis.parameter_sweep import run_parameter_sweep
from backtest.engine import run_option_backtest
from utils.io import save_csv, save_text


OUT_CSV = EXPORTS_DIR / "cost_sweep_v2.csv"
OUT_REPORT = REPORTS_DIR / "cost_sweep_v2_report.txt"


def cost_backtest_wrapper(trades, cost):
    _, stats = run_option_backtest(
        trades,
        total_transaction_cost=cost,
    )
    return stats


def main():
    print("Reading option trade dataset...")
    trades = pd.read_parquet(OPTION_TRADE_DATASET)

    print("Shape:")
    print(trades.shape)

    result = run_parameter_sweep(
        base_data=trades,
        param_name="transaction_cost",
        values=TRANSACTION_COST_GRID,
        run_func=cost_backtest_wrapper,
    )

    save_csv(result, OUT_CSV)

    report = []
    report.append("=" * 60)
    report.append("Cost Sweep V2 Report")
    report.append("=" * 60)
    report.append("")
    report.append(result.to_string(index=False))

    save_text("\n".join(report), OUT_REPORT)

    print("\nDONE")


if __name__ == "__main__":
    main()