from pathlib import Path

from framework.portfolio.position_book import Position, PositionBook
from framework.portfolio.pnl_engine import PnLEngine


OUT_CSV = Path("research/exports/pnl_engine_position_pnl_v1_1.csv")
OUT_REPORT = Path("research/reports/pnl_engine_test_v1_1_report.txt")


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

    position_pnl = PnLEngine.position_pnl_table(book)
    portfolio_pnl = PnLEngine.portfolio_pnl(book)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    position_pnl.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("PnL Engine Test v1.1")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Positions            : {portfolio_pnl.positions}")
    lines.append(f"Total Market Value   : {portfolio_pnl.total_market_value:.2f}")
    lines.append(f"Total Unrealized PnL : {portfolio_pnl.total_unrealized_pnl:.2f}")
    lines.append(f"Average Return       : {portfolio_pnl.average_return:.6f}")
    lines.append("")
    lines.append("Position PnL")
    lines.append("-" * 80)
    lines.append(position_pnl.to_string(index=False))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()