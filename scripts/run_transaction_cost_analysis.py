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

from config.settings import (
    TRANSACTION_COST_GRID,
)

from backtest.engine import run_option_backtest
from utils.io import save_csv, save_text


OUT_CSV = EXPORTS_DIR / "transaction_cost_analysis.csv"
OUT_REPORT = REPORTS_DIR / "transaction_cost_analysis_report.txt"


def main():

    print("Reading option trades...")

    trades = pd.read_parquet(OPTION_TRADE_DATASET)

    print("Shape:")
    print(trades.shape)

    results = []

    print("\nRunning sensitivity analysis...\n")

    for cost in TRANSACTION_COST_GRID:

        _, stats = run_option_backtest(
            trades,
            total_transaction_cost=cost,
        )

        stats["transaction_cost"] = cost

        results.append(stats)

        print(
            f"Cost={cost:.3%} | "
            f"Return={stats['total_return']:.2%} | "
            f"Sharpe={stats['sharpe_per_trade']:.3f}"
        )

    result_df = pd.DataFrame(results)

    result_df = result_df[
        [
            "transaction_cost",
            "trade_count",
            "win_rate",
            "avg_return",
            "total_return",
            "sharpe_per_trade",
            "profit_factor",
            "max_drawdown",
            "avg_holding_days",
        ]
    ]

    print("\nResult Table")
    print(result_df)

    save_csv(result_df, OUT_CSV)

    report = []
    report.append("=" * 60)
    report.append("Transaction Cost Sensitivity Analysis")
    report.append("=" * 60)
    report.append("")
    report.append(result_df.to_string(index=False))

    save_text(
        "\n".join(report),
        OUT_REPORT,
    )

    print("\nDONE")


if __name__ == "__main__":
    main()