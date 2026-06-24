from pathlib import Path
import numpy as np
import pandas as pd

TRADE_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\option_trade_dataset.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\option_strategy_backtest.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\option_strategy_backtest.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\option_strategy_backtest_report.txt"
)

INITIAL_EQUITY = 1.0
TRANSACTION_COST_PER_TRADE = 0.0


def calculate_drawdown(equity):
    running_max = equity.cummax()
    return (equity - running_max) / running_max


def main():
    print("Reading option trade dataset...")
    trades = pd.read_parquet(TRADE_FILE)

    print("Source shape:")
    print(trades.shape)

    trades = trades[trades["status"] == "ok"].copy()
    trades = trades.sort_values("entry_date").reset_index(drop=True)

    print("Valid trades:")
    print(len(trades))

    if trades.empty:
        print("No valid trades.")
        return

    trades["gross_return"] = trades["option_return"]
    trades["net_return"] = (
        trades["gross_return"] - TRANSACTION_COST_PER_TRADE
    )

    trades["equity"] = (
        (1 + trades["net_return"]).cumprod()
        * INITIAL_EQUITY
    )

    trades["drawdown"] = calculate_drawdown(trades["equity"])

    total_return = trades["equity"].iloc[-1] / INITIAL_EQUITY - 1
    win_rate = (trades["net_return"] > 0).mean()
    avg_return = trades["net_return"].mean()
    median_return = trades["net_return"].median()
    std_return = trades["net_return"].std()
    sharpe_per_trade = (
        np.nan
        if std_return == 0
        else avg_return / std_return * np.sqrt(len(trades))
    )
    max_drawdown = trades["drawdown"].min()
    avg_holding = trades["holding_days"].mean()

    profit = trades.loc[
        trades["net_return"] > 0,
        "net_return",
    ].sum()

    loss = -trades.loc[
        trades["net_return"] < 0,
        "net_return",
    ].sum()

    profit_factor = np.inf if loss == 0 else profit / loss

    print("\n============================")
    print("OPTION STRATEGY BACKTEST")
    print("============================")
    print(f"Valid trades         : {len(trades)}")
    print(f"Transaction cost     : {TRANSACTION_COST_PER_TRADE:.2%}")
    print(f"Win rate             : {win_rate:.2%}")
    print(f"Average return       : {avg_return:.2%}")
    print(f"Median return        : {median_return:.2%}")
    print(f"Total return         : {total_return:.2%}")
    print(f"Sharpe per trade     : {sharpe_per_trade:.3f}")
    print(f"Max drawdown         : {max_drawdown:.2%}")
    print(f"Average holding      : {avg_holding:.2f} days")
    print(f"Profit factor        : {profit_factor:.3f}")

    print("\nTrades:")
    print(
        trades[
            [
                "entry_date",
                "exit_date",
                "expiry_code",
                "strike",
                "entry_straddle_price",
                "exit_straddle_price",
                "gross_return",
                "net_return",
                "equity",
                "drawdown",
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
    lines.append("OPTION STRATEGY BACKTEST REPORT")
    lines.append("============================")
    lines.append("")
    lines.append(f"Trade file: {TRADE_FILE}")
    lines.append(f"Valid trades: {len(trades)}")
    lines.append(f"Transaction cost: {TRANSACTION_COST_PER_TRADE:.2%}")
    lines.append("")
    lines.append(f"Win rate: {win_rate:.2%}")
    lines.append(f"Average return: {avg_return:.2%}")
    lines.append(f"Median return: {median_return:.2%}")
    lines.append(f"Total return: {total_return:.2%}")
    lines.append(f"Sharpe per trade: {sharpe_per_trade:.3f}")
    lines.append(f"Maximum drawdown: {max_drawdown:.2%}")
    lines.append(f"Average holding days: {avg_holding:.2f}")
    lines.append(f"Profit factor: {profit_factor:.3f}")
    lines.append("")
    lines.append("Trades:")
    lines.append(str(trades))

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("\nDONE")
    print("Saved:")
    print(OUT_FILE)
    print(OUT_CSV)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()