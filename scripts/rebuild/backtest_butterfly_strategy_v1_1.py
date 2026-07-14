from pathlib import Path
import pandas as pd

from framework.strategy.contracts import BacktestResult
from framework.strategy.backtest_engine import (
    compute_equity_curve,
    summarize_backtest,
    write_backtest_report,
)


TRADES_FILE = Path("research/exports/option_strategy_backtest_v2.csv")
SNAPSHOT_FILE = Path("research/datasets/butterfly_daily_snapshot_2026H1_v1_1.parquet")

OUT_CSV = Path("research/exports/butterfly_strategy_backtest_v1_1.csv")
OUT_REPORT = Path("research/reports/butterfly_strategy_backtest_v1_1_report.txt")


def main():

    trades = pd.read_csv(TRADES_FILE)
    snap = pd.read_parquet(SNAPSHOT_FILE)

    trades = trades[trades["status"] == "ok"].copy()

    snap["trade_date"] = snap["trade_date"].astype(int)
    snap["expiry_code"] = snap["expiry_code"].astype(int)

    rows = []

    for i, trade in trades.reset_index(drop=True).iterrows():

        entry = int(trade["entry_date"])
        exit_ = int(trade["exit_date"])
        expiry = int(trade["expiry_code"])

        entry_row = snap[
            (snap.trade_date == entry)
            & (snap.expiry_code == expiry)
        ]

        exit_row = snap[
            (snap.trade_date == exit_)
            & (snap.expiry_code == expiry)
        ]

        if entry_row.empty or exit_row.empty:

            rows.append(
                {
                    "trade_id": i + 1,
                    "strategy": "long_call_butterfly",
                    "status": "missing_snapshot",
                    "entry_date": entry,
                    "exit_date": exit_,
                    "expiry_code": expiry,
                }
            )
            continue

        entry_row = entry_row.iloc[-1]
        exit_row = exit_row.iloc[-1]

        entry_price = entry_row["butterfly_price"]
        exit_price = exit_row["butterfly_price"]

        if (
            pd.isna(entry_price)
            or pd.isna(exit_price)
            or entry_price <= 0
        ):

            status = "invalid_price"
            pnl = None
            ret = None

        else:

            status = "ok"
            pnl = exit_price - entry_price
            ret = pnl / entry_price

        rows.append(
            {
                "trade_id": i + 1,
                "strategy": "long_call_butterfly",
                "status": status,

                "entry_date": entry,
                "exit_date": exit_,
                "holding_days": trade["holding_days"],

                "expiry_code": expiry,

                "entry_price": entry_price,
                "exit_price": exit_price,

                "option_pnl": pnl,
                "option_return": ret,

                "entry_signal_score": trade["entry_signal_score"],
                "exit_signal_score": trade["exit_signal_score"],
                "exit_reason": trade["exit_reason"],
            }
        )

    out = pd.DataFrame(rows)

    out = compute_equity_curve(out)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    write_backtest_report(
        strategy_name="Long Call Butterfly v1.1",
        trades=out,
        report_path=OUT_REPORT,
    )

    stats = summarize_backtest(out)

    result = BacktestResult(
        strategy_name="long_call_butterfly",

        total_trades=stats["total_trades"],
        completed_trades=stats["completed_trades"],
        skipped_trades=stats["skipped_trades"],

        win_rate=stats["win_rate"],
        final_equity=stats["final_equity"],
        max_drawdown=stats["max_drawdown"],
        average_return=stats["average_return"],

        report_path=OUT_REPORT,
        trades_path=OUT_CSV,

        status="success",
        message="Long Call Butterfly v1.1 backtest completed.",
    )

    print(result)


if __name__ == "__main__":
    main()