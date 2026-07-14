from pathlib import Path
import argparse

import pandas as pd

from framework.data.trading_days import (
    find_available_trade_dates,
    filter_trade_dates,
)
from framework.strategy.strategy_registry import STRATEGIES
from framework.risk.position_loader import build_portfolio_positions
from framework.portfolio.position_book import Position, PositionBook
from framework.portfolio.pnl_engine import PnLEngine
from framework.portfolio.nav import NAVEngine
from framework.risk.risk_report import build_risk_report


FILTERED_SESSION_ROOT = Path("data/filtered_sessions")

OUT_NAV = Path("research/exports/portfolio_nav_timeseries_v1_1.csv")
OUT_PNL = Path("research/exports/portfolio_pnl_timeseries_v1_1.csv")
OUT_REPORT = Path("research/reports/portfolio_status_timeseries_v1_1_report.txt")


def infer_price(row):
    for col in [
        "strangle_price",
        "butterfly_price",
        "calendar_price",
    ]:
        if col in row and pd.notna(row[col]):
            return float(abs(row[col]))

    return 0.0


def build_position_book(positions_df):
    book = PositionBook()

    for i, row in positions_df.reset_index(drop=True).iterrows():
        current_price = infer_price(row)

        entry_price = row.get("entry_price")

        if entry_price is None or pd.isna(entry_price):
            entry_price = current_price

        entry_price = float(abs(entry_price))
        current_price = float(abs(current_price))

        entry_date = row.get(
            "entry_trade_date",
            row.get("trade_date"),
        )

        book.add(
            Position(
                trade_id=i + 1,
                strategy=str(row.get("strategy")),
                quantity=1,
                entry_date=int(entry_date),
                entry_price=entry_price,
                current_price=current_price,
                market_value=current_price,
                status="open",
            )
        )

    return book


def resolve_dates(args):
    if args.trade_dates:
        return [
            int(x.strip())
            for x in args.trade_dates.split(",")
            if x.strip()
        ]

    dates = find_available_trade_dates(
        FILTERED_SESSION_ROOT
    )

    dates = filter_trade_dates(
        dates,
        start_date=args.start_date,
        end_date=args.end_date,
    )

    return dates


def build_one_day(
    trade_date: int,
    nav_engine: NAVEngine,
):
    positions_df = build_portfolio_positions(
        strategy_configs=STRATEGIES,
        trade_date=trade_date,
    )

    if positions_df.empty:
        nav = nav_engine.update(PositionBook())

        nav_row = {
            "trade_date": trade_date,
            "positions": 0,
            "market_value": 0.0,
            "unrealized_pnl": 0.0,
            "current_nav": nav.current_nav,
            "cumulative_return": nav.cumulative_return,
            "drawdown": nav.drawdown,
            "net_delta": 0.0,
            "net_gamma": 0.0,
            "net_vega": 0.0,
            "net_theta": 0.0,
            "risk_status": "flat",
            "critical_risks": 0,
            "warning_risks": 0,
        }

        return nav_row, []

    book = build_position_book(positions_df)

    pnl_table = PnLEngine.position_pnl_table(book)
    portfolio_pnl = PnLEngine.portfolio_pnl(book)
    nav = nav_engine.update(book)

    exposure, rec_df, plan_df = build_risk_report(
        positions=positions_df,
        report_path=Path(
            "research/reports/portfolio_status_timeseries_risk_detail_v1_1.txt"
        ),
        trade_date=trade_date,
    )

    critical = int(
        (rec_df["risk_level"] == "critical").sum()
    )

    warning = int(
        (rec_df["risk_level"] == "warning").sum()
    )

    if critical > 0:
        risk_status = "critical"
    elif warning > 0:
        risk_status = "warning"
    else:
        risk_status = "normal"

    nav_row = {
        "trade_date": trade_date,
        "positions": portfolio_pnl.positions,
        "market_value": portfolio_pnl.total_market_value,
        "unrealized_pnl": portfolio_pnl.total_unrealized_pnl,
        "current_nav": nav.current_nav,
        "cumulative_return": nav.cumulative_return,
        "drawdown": nav.drawdown,
        "net_delta": exposure.net_delta,
        "net_gamma": exposure.net_gamma,
        "net_vega": exposure.net_vega,
        "net_theta": exposure.net_theta,
        "risk_status": risk_status,
        "critical_risks": critical,
        "warning_risks": warning,
    }

    pnl_rows = []

    for _, row in pnl_table.iterrows():
        d = row.to_dict()
        d["trade_date"] = trade_date
        pnl_rows.append(d)

    return nav_row, pnl_rows


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--trade-dates",
        type=str,
        default=None,
        help="Comma-separated trade dates, e.g. 20260119,20260126",
    )

    parser.add_argument(
        "--start-date",
        type=int,
        default=None,
        help="Optional start date in YYYYMMDD format.",
    )

    parser.add_argument(
        "--end-date",
        type=int,
        default=None,
        help="Optional end date in YYYYMMDD format.",
    )

    parser.add_argument(
        "--initial-capital",
        type=float,
        default=1_000_000,
    )

    args = parser.parse_args()

    dates = resolve_dates(args)

    nav_engine = NAVEngine(
        initial_capital=args.initial_capital,
    )

    nav_rows = []
    pnl_rows = []
    skipped_dates = []

    for trade_date in dates:
        print("Processing:", trade_date)

        nav_row, rows = build_one_day(
            trade_date=trade_date,
            nav_engine=nav_engine,
        )

        if nav_row is None:
            skipped_dates.append(trade_date)
            continue

        nav_rows.append(nav_row)
        pnl_rows.extend(rows)

    nav_df = pd.DataFrame(nav_rows)
    pnl_df = pd.DataFrame(pnl_rows)

    OUT_NAV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    nav_df.to_csv(
        OUT_NAV,
        index=False,
        encoding="utf-8-sig",
    )

    pnl_df.to_csv(
        OUT_PNL,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("Portfolio Status Timeseries v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Initial Capital : {args.initial_capital:,.2f}")
    lines.append(f"Dates found     : {len(dates)}")
    lines.append(f"Dates processed : {len(nav_df)}")
    lines.append(f"Dates skipped   : {len(skipped_dates)}")
    lines.append("")

    if skipped_dates:
        lines.append("Skipped Dates")
        lines.append("-" * 80)
        lines.append(", ".join(str(x) for x in skipped_dates))
        lines.append("")

    lines.append("NAV Timeseries")
    lines.append("-" * 80)

    if nav_df.empty:
        lines.append("No portfolio positions found.")
    else:
        lines.append(nav_df.to_string(index=False))

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("DONE")
    print("Dates found:", len(dates))
    print("Dates processed:", len(nav_df))
    print("Dates skipped:", len(skipped_dates))
    print("Saved:")
    print(OUT_NAV)
    print(OUT_PNL)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()