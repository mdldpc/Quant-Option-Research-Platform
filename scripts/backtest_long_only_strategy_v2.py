from pathlib import Path
import pandas as pd
import numpy as np

TRADE_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\long_only_trades.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\backtest_long_only_v2.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\backtest_long_only_v2.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\backtest_long_only_v2_report.txt"
)

CONVERSION_RATIO = 0.10
INITIAL_EQUITY = 1.0


def calculate_drawdown(equity):
    running_max = equity.cummax()
    return (equity - running_max) / running_max


def main():
    print("Reading trades...")
    trades = pd.read_parquet(TRADE_FILE)

    print("Trades shape:")
    print(trades.shape)

    if trades.empty:
        print("No trades.")
        return

    trades = trades.sort_values("entry_date_dt").copy()

    trades["strategy_return"] = trades["iv_return"] * CONVERSION_RATIO
    trades["equity"] = (1 + trades["strategy_return"]).cumprod() * INITIAL_EQUITY
    trades["drawdown"] = calculate_drawdown(trades["equity"])

    total_return = trades["equity"].iloc[-1] / INITIAL_EQUITY - 1
    win_rate = (trades["strategy_return"] > 0).mean()
    avg_return = trades["strategy_return"].mean()
    std_return = trades["strategy_return"].std()
    sharpe_per_trade = np.nan if std_return == 0 else avg_return / std_return * np.sqrt(len(trades))
    max_drawdown = trades["drawdown"].min()
    avg_holding = trades["holding_days"].mean()

    profit = trades.loc[trades["strategy_return"] > 0, "strategy_return"].sum()
    loss = -trades.loc[trades["strategy_return"] < 0, "strategy_return"].sum()
    profit_factor = np.inf if loss == 0 else profit / loss

    print("\n============================")
    print("BACKTEST V2 SUMMARY")
    print("============================")
    print(f"Conversion Ratio     : {CONVERSION_RATIO:.2%}")
    print(f"Trades               : {len(trades)}")
    print(f"Win Rate             : {win_rate:.2%}")
    print(f"Average Return       : {avg_return:.2%}")
    print(f"Total Return         : {total_return:.2%}")
    print(f"Sharpe per Trade     : {sharpe_per_trade:.3f}")
    print(f"Max Drawdown         : {max_drawdown:.2%}")
    print(f"Average Holding      : {avg_holding:.2f} days")
    print(f"Profit Factor        : {profit_factor:.3f}")

    print("\nTrades:")
    print(
        trades[
            [
                "entry_date",
                "exit_date",
                "holding_days",
                "entry_near_iv",
                "exit_near_iv",
                "iv_return",
                "strategy_return",
                "equity",
                "drawdown",
                "exit_reason",
            ]
        ]
    )

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    trades.to_parquet(OUT_FILE, index=False)
    trades.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("============================")
    lines.append("BACKTEST V2 REPORT")
    lines.append("============================")
    lines.append("")
    lines.append(f"Conversion Ratio: {CONVERSION_RATIO:.2%}")
    lines.append(f"Trades: {len(trades)}")
    lines.append(f"Win Rate: {win_rate:.2%}")
    lines.append(f"Average Return: {avg_return:.2%}")
    lines.append(f"Total Return: {total_return:.2%}")
    lines.append(f"Sharpe per Trade: {sharpe_per_trade:.3f}")
    lines.append(f"Maximum Drawdown: {max_drawdown:.2%}")
    lines.append(f"Average Holding Days: {avg_holding:.2f}")
    lines.append(f"Profit Factor: {profit_factor:.3f}")
    lines.append("")
    lines.append("Trade Table:")
    lines.append(str(trades))

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("\nDONE")
    print("Saved:")
    print(OUT_FILE)
    print(OUT_CSV)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()