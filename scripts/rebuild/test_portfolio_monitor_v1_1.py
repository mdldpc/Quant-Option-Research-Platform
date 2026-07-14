from pathlib import Path

from framework.strategy.strategy_registry import STRATEGIES
from framework.risk.position_loader import build_portfolio_positions
from framework.monitoring.portfolio_monitor import PortfolioMonitor


OUT_CSV = Path(
    "research/exports/portfolio_monitor_history_v1_1.csv"
)

OUT_REPORT = Path(
    "research/reports/portfolio_monitor_test_v1_1_report.txt"
)


TEST_DATES = [
    20260119,
    20260226,
    20260428,
]


def main():

    monitor = PortfolioMonitor()

    lines = []

    lines.append("Portfolio Monitor Test v1.1")
    lines.append("=" * 80)
    lines.append("")

    for trade_date in TEST_DATES:

        positions = build_portfolio_positions(
            strategy_configs=STRATEGIES,
            trade_date=trade_date,
        )

        status = monitor.update(
            positions=positions,
            timestamp=str(trade_date),
        )

        lines.append(f"Trade date      : {trade_date}")
        lines.append(f"Positions       : {status.position_count}")
        lines.append(f"Overall Status  : {status.overall_status}")
        lines.append(f"Critical Risks  : {status.critical_risks}")
        lines.append(f"Warning Risks   : {status.warning_risks}")
        lines.append("")

        lines.append("Recommendations")

        for rec in status.recommendations:

            lines.append(
                f"  {rec.risk_type:<8}"
                f"{rec.risk_level:<10}"
                f"{rec.action}"
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("")

    history = monitor.history()

    OUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    history.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines.append("")
    lines.append("History")
    lines.append("=" * 80)
    lines.append(history.to_string(index=False))

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("DONE")
    print("Snapshots:", monitor.size())
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()