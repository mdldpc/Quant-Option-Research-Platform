from pathlib import Path
import pandas as pd


TRADES_FILE = Path("research/exports/option_strategy_backtest_v2.csv")
SNAPSHOT_FILE = Path("research/datasets/calendar_daily_snapshot_2026H1.parquet")

OUT_CSV = Path("research/exports/calendar_strategy_backtest.csv")
OUT_REPORT = Path("research/reports/calendar_strategy_backtest_report.txt")


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

        entry_row = snap[snap["trade_date"] == entry]
        exit_row = snap[snap["trade_date"] == exit_]

        if entry_row.empty or exit_row.empty:
            rows.append({
                "trade_id": i + 1,
                "strategy": "calendar_spread",
                "status": "missing_snapshot",
                "entry_date": entry,
                "exit_date": exit_,
            })
            continue

        # Use the closest near/next pair available on entry date.
        entry_row = entry_row.iloc[-1]

        near_expiry = int(entry_row["near_expiry"])
        next_expiry = int(entry_row["next_expiry"])

        exit_match = exit_row[
            (exit_row["near_expiry"] == near_expiry)
            & (exit_row["next_expiry"] == next_expiry)
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

        if (
            pd.isna(entry_price)
            or pd.isna(exit_price)
            or capital_base <= 0
        ):
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

    ok = out[out["status"] == "ok"].copy()

    ok["gross_return"] = ok["option_return"]
    ok["net_return"] = ok["option_return"]
    ok["equity"] = (1 + ok["net_return"]).cumprod()
    ok["drawdown"] = ok["equity"] / ok["equity"].cummax() - 1

    out = out.merge(
        ok[["trade_id", "gross_return", "net_return", "equity", "drawdown"]],
        on="trade_id",
        how="left",
    )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Calendar Spread Backtest Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Trades file: {TRADES_FILE}")
    lines.append(f"Snapshot file: {SNAPSHOT_FILE}")
    lines.append("")
    lines.append(f"Total trades: {len(out)}")
    lines.append("Status counts:")
    lines.append(str(out["status"].value_counts()))
    lines.append("")

    if len(ok) > 0:
        lines.append("Return summary:")
        lines.append(str(ok["option_return"].describe()))
        lines.append("")
        lines.append(f"Final equity: {ok['equity'].iloc[-1]}")
        lines.append(f"Max drawdown: {ok['drawdown'].min()}")
        lines.append(f"Win rate: {(ok['option_return'] > 0).mean()}")
        lines.append("")
        lines.append("Trades:")
        lines.append(str(ok[[
            "trade_id",
            "entry_date",
            "exit_date",
            "near_expiry",
            "next_expiry",
            "entry_calendar_price",
            "exit_calendar_price",
            "entry_iv_spread",
            "exit_iv_spread",
            "option_pnl",
            "option_return",
            "equity",
            "drawdown",
        ]]))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()