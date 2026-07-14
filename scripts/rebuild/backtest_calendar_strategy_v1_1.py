from pathlib import Path
import pandas as pd

from framework.strategy.contracts import BacktestResult
from framework.strategy.backtest_engine import (
    compute_equity_curve,
    summarize_backtest,
    write_backtest_report,
)


TRADES_FILE = Path("research/exports/option_strategy_backtest_v2.csv")
SNAPSHOT_FILE = Path("research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet")

OUT_CSV = Path("research/exports/calendar_strategy_backtest_v1_1.csv")
OUT_REPORT = Path("research/reports/calendar_strategy_backtest_v1_1_report.txt")


def main():
    trades = pd.read_csv(TRADES_FILE)
    snap = pd.read_parquet(SNAPSHOT_FILE)

    trades = trades[trades["status"] == "ok"].copy()

    snap["trade_date"] = snap["trade_date"].astype(int)
    snap["near_expiry"] = snap["near_expiry"].astype(int)
    snap["next_expiry"] = snap["next_expiry"].astype(int)

    rows = []

    for i, trade in trades.reset_index(drop=True).iterrows():
        entry = int(trade["entry_date"])
        exit_ = int(trade["exit_date"])

        entry_rows = snap[snap["trade_date"] == entry]
        exit_rows = snap[snap["trade_date"] == exit_]

        if entry_rows.empty or exit_rows.empty:
            rows.append({
                "trade_id": i + 1,
                "strategy": "calendar_spread",
                "status": "missing_snapshot",
                "entry_date": entry,
                "exit_date": exit_,
            })
            continue

        entry_row = entry_rows.iloc[-1]

        near_expiry = int(entry_row["near_expiry"])
        next_expiry = int(entry_row["next_expiry"])

        exit_match = exit_rows[
            (exit_rows["near_expiry"] == near_expiry)
            & (exit_rows["next_expiry"] == next_expiry)
        ]

        if exit_match.empty:
            rows.append({
                "trade_id": i + 1,
                "strategy": "calendar_spread",
                "status": "missing_exit_pair",
                "entry_date": entry,
                "exit_date": exit_,
                "near_expiry": near_expiry,
                "next_expiry": next_expiry,
            })
            continue

        exit_row = exit_match.iloc[-1]

        entry_price = entry_row["calendar_price"]
        exit_price = exit_row["calendar_price"]

        capital_base = abs(entry_price)

        if pd.isna(entry_price) or pd.isna(exit_price) or capital_base <= 0:
            status = "invalid_price"
            pnl = None
            ret = None
        else:
            status = "ok"
            pnl = exit_price - entry_price
            ret = pnl / capital_base

        rows.append({
            "trade_id": i + 1,
            "strategy": "calendar_spread",
            "status": status,
            "entry_date": entry,
            "exit_date": exit_,
            "holding_days": trade["holding_days"],

            "near_expiry": near_expiry,
            "next_expiry": next_expiry,

            "entry_calendar_price": entry_price,
            "exit_calendar_price": exit_price,
            "capital_base": capital_base,

            "entry_iv_spread": entry_row.get("iv_spread"),
            "exit_iv_spread": exit_row.get("iv_spread"),

            "entry_near_straddle_price": entry_row.get("near_straddle_price"),
            "entry_next_straddle_price": entry_row.get("next_straddle_price"),
            "exit_near_straddle_price": exit_row.get("near_straddle_price"),
            "exit_next_straddle_price": exit_row.get("next_straddle_price"),

            "option_pnl": pnl,
            "option_return": ret,

            "entry_signal_score": trade["entry_signal_score"],
            "exit_signal_score": trade["exit_signal_score"],
            "exit_reason": trade["exit_reason"],
        })

    out = pd.DataFrame(rows)
    out = compute_equity_curve(out)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    write_backtest_report(
        strategy_name="Calendar Spread v1.1",
        trades=out,
        report_path=OUT_REPORT,
    )

    stats = summarize_backtest(out)

    result = BacktestResult(
        strategy_name="calendar_spread",
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
        message="Calendar Spread v1.1 backtest completed.",
    )

    print(result)


if __name__ == "__main__":
    main()