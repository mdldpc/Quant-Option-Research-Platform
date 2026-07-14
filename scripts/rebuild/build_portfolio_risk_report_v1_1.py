from pathlib import Path
import argparse
import pandas as pd

from framework.strategy.strategy_registry import STRATEGIES
from framework.risk.position_loader import build_portfolio_positions
from framework.risk.risk_report import build_risk_report


OUT_REPORT = Path("research/reports/portfolio_risk_hedge_report_v1_1.txt")
OUT_CSV = Path("research/exports/portfolio_risk_hedge_recommendations_v1_1.csv")
OUT_POSITIONS = Path("research/exports/portfolio_open_positions_v1_1.csv")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--trade-date",
        type=int,
        required=True,
        help="Trade date in YYYYMMDD format.",
    )

    args = parser.parse_args()

    positions = build_portfolio_positions(
        strategy_configs=STRATEGIES,
        trade_date=args.trade_date,
    )

    OUT_POSITIONS.parent.mkdir(parents=True, exist_ok=True)

    if positions.empty:
        positions.to_csv(OUT_POSITIONS, index=False, encoding="utf-8-sig")
        print("No open positions on:", args.trade_date)
        return

    positions.to_csv(OUT_POSITIONS, index=False, encoding="utf-8-sig")

    exposure, rec_df, plan_df = build_risk_report(
        positions=positions,
        report_path=OUT_REPORT,
        trade_date=args.trade_date,
    )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    plan_df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    print("DONE")
    print("Trade Date :", args.trade_date)
    print("Open Positions:", len(positions))
    print("Saved:")
    print(OUT_POSITIONS)
    print(OUT_REPORT)
    print(OUT_CSV)


if __name__ == "__main__":
    main()