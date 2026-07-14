from pathlib import Path
import pandas as pd

from framework.strategy.strategy_registry import (
    list_strategies,
    get_strategy,
)


SUMMARY_CSV = Path("research/exports/backtest_all_strategies_v1_1_summary.csv")
SUMMARY_REPORT = Path("research/reports/backtest_all_strategies_v1_1_summary.txt")


def run_one_strategy(strategy_name: str):
    cfg = get_strategy(strategy_name)

    trades = pd.read_csv(cfg["trade_output"])

    backtester_cls = cfg["backtester"]
    backtester = backtester_cls(trades)

    out = backtester.run()

    result = backtester.finalize(
        out=out,
        report_path=cfg["backtest_report"],
        trades_path=cfg["backtest_output"],
    )

    return result


def main():
    print("=" * 80)
    print("Backtesting All Strategies v1.1")
    print("=" * 80)

    results = []

    for strategy_name in list_strategies():
        print()
        print("-" * 80)
        print("Running:", strategy_name)
        print("-" * 80)

        result = run_one_strategy(strategy_name)
        results.append(result)

        print(result)

    summary = pd.DataFrame([
        {
            "strategy": r.strategy_name,
            "total_trades": r.total_trades,
            "completed_trades": r.completed_trades,
            "skipped_trades": r.skipped_trades,
            "win_rate": r.win_rate,
            "avg_return": r.average_return,
            "final_equity": r.final_equity,
            "max_drawdown": r.max_drawdown,
            "status": r.status,
            "report_path": str(r.report_path),
            "trades_path": str(r.trades_path),
        }
        for r in results
    ])

    summary = summary.sort_values(
        "final_equity",
        ascending=False,
    ).reset_index(drop=True)

    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_REPORT.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(SUMMARY_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Backtest All Strategies v1.1 Summary")
    lines.append("=" * 80)
    lines.append("")
    lines.append(summary.to_string(index=False))

    SUMMARY_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(summary)

    print()
    print("DONE")
    print("Saved:")
    print(SUMMARY_CSV)
    print(SUMMARY_REPORT)


if __name__ == "__main__":
    main()