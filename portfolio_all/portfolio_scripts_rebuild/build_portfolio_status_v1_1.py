from pathlib import Path
import argparse
import pandas as pd

from framework.strategy.strategy_registry import STRATEGIES
from framework.risk.position_loader import build_portfolio_positions
from framework.portfolio.position_book import Position, PositionBook
from framework.portfolio.pnl_engine import PnLEngine
from framework.portfolio.nav import NAVEngine
from framework.risk.risk_report import build_risk_report
from framework.reporting.portfolio_report import (
    PortfolioReportBuilder,
    PortfolioReportData,
)


OUT_POSITIONS = Path("research/exports/portfolio_status_positions_v1_1.csv")
OUT_PNL = Path("research/exports/portfolio_status_pnl_v1_1.csv")
OUT_HEDGE = Path("research/exports/portfolio_status_hedge_plan_v1_1.csv")
OUT_REPORT = Path("research/reports/portfolio_status_v1_1_report.txt")


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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--trade-date",
        type=int,
        required=True,
        help="Trade date in YYYYMMDD format.",
    )

    parser.add_argument(
        "--initial-capital",
        type=float,
        default=1_000_000,
    )

    args = parser.parse_args()

    positions_df = build_portfolio_positions(
        strategy_configs=STRATEGIES,
        trade_date=args.trade_date,
    )

    OUT_POSITIONS.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    if positions_df.empty:
        positions_df.to_csv(
            OUT_POSITIONS,
            index=False,
            encoding="utf-8-sig",
        )
        print("No open positions:", args.trade_date)
        return

    book = build_position_book(positions_df)

    pnl_table = PnLEngine.position_pnl_table(book)
    portfolio_pnl = PnLEngine.portfolio_pnl(book)

    nav_engine = NAVEngine(
        initial_capital=args.initial_capital,
    )
    nav = nav_engine.update(book)

    exposure, rec_df, plan_df = build_risk_report(
        positions=positions_df,
        report_path=Path(
            "research/reports/portfolio_status_risk_detail_v1_1.txt"
        ),
        trade_date=args.trade_date,
    )

    critical = int((rec_df["risk_level"] == "critical").sum())
    warning = int((rec_df["risk_level"] == "warning").sum())

    if critical > 0:
        risk_status = "critical"
    elif warning > 0:
        risk_status = "warning"
    else:
        risk_status = "normal"

    report_data = PortfolioReportData(
        trade_date=args.trade_date,
        initial_capital=args.initial_capital,
        current_nav=nav.current_nav,
        unrealized_pnl=nav.unrealized_pnl,
        cumulative_return=nav.cumulative_return,
        drawdown=nav.drawdown,
        positions=portfolio_pnl.positions,
        market_value=portfolio_pnl.total_market_value,
        net_delta=exposure.net_delta,
        net_gamma=exposure.net_gamma,
        net_vega=exposure.net_vega,
        net_theta=exposure.net_theta,
        risk_status=risk_status,
    )

    report_text = PortfolioReportBuilder.build_text_report(
        data=report_data,
        pnl_table=pnl_table,
        hedge_plan=plan_df,
    )

    positions_df.to_csv(
        OUT_POSITIONS,
        index=False,
        encoding="utf-8-sig",
    )

    pnl_table.to_csv(
        OUT_PNL,
        index=False,
        encoding="utf-8-sig",
    )

    plan_df.to_csv(
        OUT_HEDGE,
        index=False,
        encoding="utf-8-sig",
    )

    PortfolioReportBuilder.write_text_report(
        report_text=report_text,
        path=OUT_REPORT,
    )

    print("DONE")
    print("Saved:")
    print(OUT_POSITIONS)
    print(OUT_PNL)
    print(OUT_HEDGE)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()