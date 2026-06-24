import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.paths import (
    OPTION_TRADE_DATASET,
    BACKTEST_DIR,
    EXPORTS_DIR,
    REPORTS_DIR,
)

from utils.io import save_parquet, save_csv, save_text
from backtest.engine import run_option_backtest, format_backtest_report

import pandas as pd


OUT_FILE = BACKTEST_DIR / "option_strategy_backtest_v2.parquet"
OUT_CSV = EXPORTS_DIR / "option_strategy_backtest_v2.csv"
REPORT_FILE = REPORTS_DIR / "option_strategy_backtest_v2_report.txt"


def main():
    print("Reading option trade dataset...")
    trades = pd.read_parquet(OPTION_TRADE_DATASET)

    print("Source shape:")
    print(trades.shape)

    backtest_df, stats = run_option_backtest(trades)

    print("\nBacktest shape:")
    print(backtest_df.shape)

    print("\nStats:")
    for k, v in stats.items():
        print(f"{k}: {v}")

    save_parquet(backtest_df, OUT_FILE)
    save_csv(backtest_df, OUT_CSV)

    report = format_backtest_report(
        stats,
        title="OPTION STRATEGY BACKTEST V2 REPORT",
    )

    report += "\n\nTrade Table:\n"
    report += str(backtest_df)

    save_text(report, REPORT_FILE)

    print("\nDONE")


if __name__ == "__main__":
    main()