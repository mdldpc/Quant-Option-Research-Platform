from pathlib import Path
import pandas as pd


TRADES_FILE = Path("research/exports/option_strategy_backtest_v2.csv")
SNAPSHOT_FILE = Path("research/datasets/strangle_daily_snapshot_2026H1.parquet")

OUT_CSV = Path("research/exports/strangle_strategy_backtest.csv")
OUT_REPORT = Path("research/reports/strangle_strategy_backtest_report.txt")


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
            (snap["trade_date"] == entry)
            & (snap["expiry_code"] == expiry)
        ]

        exit_row = snap[
            (snap["trade_date"] == exit_)
            & (snap["expiry_code"] == expiry)
        ]

        if entry_row.empty or exit_row.empty:
            rows.append({
                "trade_id": i + 1,
                "status": "missing_snapshot",
                "entry_date": entry,
                "exit_date": exit_,
                "expiry_code": expiry,
            })
            continue

        entry_row = entry_row.iloc[-1]
        exit_row = exit_row.iloc[-1]

        entry_price = entry_row["strangle_price"]
        exit_price = exit_row["strangle_price"]

        if pd.isna(entry_price) or pd.isna(exit_price) or entry_price <= 0:
            status = "invalid_price"
            option_pnl = None
            option_return = None
        else:
            status = "ok"
            option_pnl = exit_price - entry_price
            option_return = option_pnl / entry_price

        rows.append({
            "trade_id": i + 1,
            "strategy": "long_atm_strangle",
            "status": status,
            "entry_date": entry,
            "exit_date": exit_,
            "holding_days": trade["holding_days"],
            "expiry_code": expiry,

            "entry_call_symbol": entry_row["call_symbol"],
            "entry_put_symbol": entry_row["put_symbol"],
            "entry_call_strike": entry_row["call_strike"],
            "entry_put_strike": entry_row["put_strike"],
            "entry_call_price": entry_row["call_price"],
            "entry_put_price": entry_row["put_price"],
            "entry_strangle_price": entry_price,

            "exit_call_symbol": exit_row["call_symbol"],
            "exit_put_symbol": exit_row["put_symbol"],
            "exit_call_strike": exit_row["call_strike"],
            "exit_put_strike": exit_row["put_strike"],
            "exit_call_price": exit_row["call_price"],
            "exit_put_price": exit_row["put_price"],
            "exit_strangle_price": exit_price,

            "option_pnl": option_pnl,
            "option_return": option_return,
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
    lines.append("Long ATM Strangle Backtest Report")
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
            "expiry_code",
            "entry_call_strike",
            "entry_put_strike",
            "entry_strangle_price",
            "exit_strangle_price",
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