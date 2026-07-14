from pathlib import Path

from framework.portfolio.position_book import (
    Position,
    PositionBook,
)


OUT_CSV = Path(
    "research/exports/position_book_v1_1.csv"
)

OUT_REPORT = Path(
    "research/reports/position_book_test_v1_1_report.txt"
)


def main():

    book = PositionBook()

    p1 = Position(
        trade_id=1,
        strategy="long_atm_strangle",
        quantity=1,
        entry_date=20260119,
        entry_price=177.9,
        current_price=177.9,
        market_value=177.9,
    )

    p2 = Position(
        trade_id=2,
        strategy="calendar_spread",
        quantity=2,
        entry_date=20260119,
        entry_price=126.3,
        current_price=126.3,
        market_value=252.6,
    )

    book.add(p1)
    book.add(p2)

    book.update_price(
        trade_id=1,
        current_price=190.0,
    )

    summary = book.summary()

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []

    lines.append("Position Book Test v1.1")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Positions    : {book.size()}")
    lines.append(f"Market Value : {book.market_value():.2f}")
    lines.append("")
    lines.append(summary.to_string(index=False))

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("DONE")
    print("Positions:", book.size())
    print("Market Value:", book.market_value())
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()