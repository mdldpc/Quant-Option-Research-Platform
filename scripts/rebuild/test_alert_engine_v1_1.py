from pathlib import Path

from framework.strategy.strategy_registry import STRATEGIES
from framework.risk.position_loader import build_portfolio_positions
from framework.monitoring.portfolio_monitor import PortfolioMonitor
from framework.monitoring.alert_engine import AlertEngine


TEST_DATES = [
    20260119,
    20260226,
    20260428,
]

OUT_CSV = Path(
    "research/exports/alert_history_v1_1.csv"
)

OUT_REPORT = Path(
    "research/reports/alert_engine_test_v1_1_report.txt"
)


def main():

    portfolio_monitor = PortfolioMonitor()
    alert_engine = AlertEngine()

    lines = []

    lines.append("Alert Engine Test v1.1")
    lines.append("=" * 80)
    lines.append("")

    for trade_date in TEST_DATES:

        positions = build_portfolio_positions(
            strategy_configs=STRATEGIES,
            trade_date=trade_date,
        )

        status = portfolio_monitor.update(
            positions,
            timestamp=str(trade_date),
        )

        event = alert_engine.update(status)

        lines.append(f"Trade Date : {trade_date}")
        lines.append(f"Status     : {status.overall_status}")

        if event is None:
            lines.append("Alert      : None")
        else:
            lines.append(f"Level      : {event.level}")
            lines.append(f"Message    : {event.message}")

        lines.append("")
        lines.append("-" * 80)
        lines.append("")

    history = alert_engine.history()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    history.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines.append("")
    lines.append("History")
    lines.append("=" * 80)

    if history.empty:
        lines.append("No alerts generated.")
    else:
        lines.append(history.to_string(index=False))

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("DONE")
    print("Alerts:", alert_engine.size())
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()