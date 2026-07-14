from pathlib import Path
import pandas as pd


def compute_equity_curve(
    trades: pd.DataFrame,
    return_col: str = "option_return",
) -> pd.DataFrame:
    ok = trades[trades["status"] == "ok"].copy()

    if ok.empty:
        trades["gross_return"] = None
        trades["net_return"] = None
        trades["equity"] = None
        trades["drawdown"] = None
        return trades

    ok["gross_return"] = ok[return_col]
    ok["net_return"] = ok[return_col]
    ok["equity"] = (1 + ok["net_return"]).cumprod()
    ok["drawdown"] = ok["equity"] / ok["equity"].cummax() - 1

    return trades.merge(
        ok[["trade_id", "gross_return", "net_return", "equity", "drawdown"]],
        on="trade_id",
        how="left",
    )


def summarize_backtest(
    trades: pd.DataFrame,
    return_col: str = "option_return",
) -> dict:
    ok = trades[trades["status"] == "ok"].copy()

    if ok.empty:
        return {
            "total_trades": len(trades),
            "completed_trades": 0,
            "skipped_trades": len(trades),
            "win_rate": 0.0,
            "final_equity": 1.0,
            "max_drawdown": 0.0,
            "average_return": 0.0,
        }

    return {
        "total_trades": len(trades),
        "completed_trades": len(ok),
        "skipped_trades": len(trades) - len(ok),
        "win_rate": float((ok[return_col] > 0).mean()),
        "final_equity": float(ok["equity"].iloc[-1]),
        "max_drawdown": float(ok["drawdown"].min()),
        "average_return": float(ok[return_col].mean()),
    }


def write_backtest_report(
    strategy_name: str,
    trades: pd.DataFrame,
    report_path: Path,
    return_col: str = "option_return",
) -> None:
    ok = trades[trades["status"] == "ok"].copy()

    lines = []
    lines.append(f"{strategy_name} Backtest Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Total trades: {len(trades)}")
    lines.append("")
    lines.append("Status counts:")
    lines.append(str(trades["status"].value_counts()))
    lines.append("")

    if not ok.empty:
        lines.append("Return summary:")
        lines.append(str(ok[return_col].describe()))
        lines.append("")
        lines.append(f"Final equity: {ok['equity'].iloc[-1]}")
        lines.append(f"Max drawdown: {ok['drawdown'].min()}")
        lines.append(f"Win rate: {(ok[return_col] > 0).mean()}")
        lines.append("")
        lines.append("Trades:")
        lines.append(str(ok))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")