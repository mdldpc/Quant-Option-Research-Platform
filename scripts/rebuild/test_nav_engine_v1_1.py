from pathlib import Path

from framework.portfolio.position_book import (
    Position,
    PositionBook,
)

from framework.portfolio.nav import NAVEngine


OUT_REPORT = Path(
    "research/reports/nav_engine_test_v1_1_report.txt"
)


def main():

    book = PositionBook()

    book.add(
        Position(
            trade_id=1,
            strategy="long_atm_strangle",
            quantity=1,
            entry_date=20260119,
            entry_price=177.9,
            current_price=190.0,
            market_value=190.0,
        )
    )

    book.add(
        Position(
            trade_id=2,
            strategy="calendar_spread",
            quantity=2,
            entry_date=20260119,
            entry_price=126.3,
            current_price=120.0,
            market_value=240.0,
        )
    )

    nav_engine = NAVEngine(
        initial_capital=1_000_000
    )

    nav = nav_engine.update(book)

    OUT_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []

    lines.append("NAV Engine Test v1.1")
    lines.append("=" * 80)
    lines.append("")

    lines.append(
        f"Initial Capital : {nav.initial_capital:,.2f}"
    )

    lines.append(
        f"Market Value    : {nav.total_market_value:,.2f}"
    )

    lines.append(
        f"Unrealized PnL  : {nav.unrealized_pnl:,.2f}"
    )

    lines.append(
        f"Current NAV     : {nav.current_nav:,.2f}"
    )

    lines.append(
        f"Cumulative Ret  : {nav.cumulative_return:.6%}"
    )

    lines.append(
        f"Drawdown        : {nav.drawdown:.6%}"
    )

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("DONE")
    print("Saved:")
    print(OUT_REPORT)


if __name__ == "__main__":
    main()