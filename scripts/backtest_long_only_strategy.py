from pathlib import Path
import pandas as pd
import numpy as np

TRADE_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\long_only_trades.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\backtest_summary.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\backtest_summary.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\backtest_report.txt"
)


def calculate_drawdown(equity):

    running_max = equity.cummax()

    drawdown = (equity - running_max) / running_max

    return drawdown


def main():

    print("Reading trades...")

    trades = pd.read_parquet(TRADE_FILE)

    print("Trades shape:")
    print(trades.shape)

    if len(trades) == 0:
        print("No trades.")
        return

    ##################################################
    # cumulative equity
    ##################################################

    initial_equity = 1.0

    equity = [initial_equity]

    for r in trades["iv_return"]:
        equity.append(equity[-1] * (1 + r))

    equity = equity[1:]

    trades["equity"] = equity

    ##################################################
    # drawdown
    ##################################################

    trades["drawdown"] = calculate_drawdown(trades["equity"])

    ##################################################
    # statistics
    ##################################################

    total_return = trades["equity"].iloc[-1] - 1

    annualized_return = (
        (1 + total_return) **
        (252 / trades["holding_days"].sum())
        - 1
    )

    win_rate = (trades["iv_return"] > 0).mean()

    avg_return = trades["iv_return"].mean()

    std_return = trades["iv_return"].std()

    if std_return == 0:
        sharpe = np.nan
    else:
        sharpe = (
            avg_return /
            std_return *
            np.sqrt(len(trades))
        )

    max_drawdown = trades["drawdown"].min()

    avg_holding = trades["holding_days"].mean()

    ##################################################
    # profit factor
    ##################################################

    profit = trades.loc[
        trades["iv_return"] > 0,
        "iv_return"
    ].sum()

    loss = -trades.loc[
        trades["iv_return"] < 0,
        "iv_return"
    ].sum()

    if loss == 0:
        profit_factor = np.inf
    else:
        profit_factor = profit / loss

    ##################################################
    # report
    ##################################################

    print("\n============================")
    print("BACKTEST SUMMARY")
    print("============================")

    print(f"Trades              : {len(trades)}")
    print(f"Win Rate            : {win_rate:.2%}")
    print(f"Average Return      : {avg_return:.2%}")
    print(f"Total Return        : {total_return:.2%}")
    print(f"Annualized Return   : {annualized_return:.2%}")
    print(f"Sharpe              : {sharpe:.3f}")
    print(f"Max Drawdown        : {max_drawdown:.2%}")
    print(f"Average Holding     : {avg_holding:.2f} days")
    print(f"Profit Factor       : {profit_factor:.3f}")

    ##################################################
    # save
    ##################################################

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    trades.to_parquet(OUT_FILE, index=False)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    trades.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    lines = []

    lines.append("============================")
    lines.append("BACKTEST REPORT")
    lines.append("============================")
    lines.append("")
    lines.append(f"Trades: {len(trades)}")
    lines.append(f"Win Rate: {win_rate:.2%}")
    lines.append(f"Average Return: {avg_return:.2%}")
    lines.append(f"Total Return: {total_return:.2%}")
    lines.append(f"Annualized Return: {annualized_return:.2%}")
    lines.append(f"Sharpe Ratio: {sharpe:.3f}")
    lines.append(f"Maximum Drawdown: {max_drawdown:.2%}")
    lines.append(f"Average Holding Days: {avg_holding:.2f}")
    lines.append(f"Profit Factor: {profit_factor:.3f}")
    lines.append("")
    lines.append("Trade Table")
    lines.append(str(trades))

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("\nDONE")

    print("Saved:")

    print(OUT_FILE)
    print(OUT_CSV)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()