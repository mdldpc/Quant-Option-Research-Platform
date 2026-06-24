from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

BACKTEST_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\option_strategy_backtest.parquet"
)

FIG_DIR = Path(
    r"D:\Quant_Option_Project\research\figures"
)


def save_plot(fig, filename):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / filename
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print("Saved:", out)


def main():
    print("Reading option strategy backtest...")
    df = pd.read_parquet(BACKTEST_FILE)

    print("Shape:")
    print(df.shape)

    df["entry_date_dt"] = pd.to_datetime(df["entry_date"].astype(str))
    df["exit_date_dt"] = pd.to_datetime(df["exit_date"].astype(str))
    df = df.sort_values("entry_date_dt").reset_index(drop=True)
    df["trade_id"] = range(1, len(df) + 1)

    # -------------------------------
    # 1. Equity Curve
    # -------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        df["trade_id"],
        df["equity"],
        marker="o",
        linewidth=2,
    )

    ax.set_title("Option Strategy Equity Curve")
    ax.set_xlabel("Trade #")
    ax.set_ylabel("Equity")
    ax.grid(True, alpha=0.3)

    save_plot(fig, "option_equity_curve.png")
    plt.close(fig)

    # -------------------------------
    # 2. Drawdown Curve
    # -------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        df["trade_id"],
        df["drawdown"],
        marker="o",
        linewidth=2,
    )

    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_title("Option Strategy Drawdown")
    ax.set_xlabel("Trade #")
    ax.set_ylabel("Drawdown")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    save_plot(fig, "option_drawdown_curve.png")
    plt.close(fig)

    # -------------------------------
    # 3. Trade Return Bar Chart
    # -------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        df["trade_id"],
        df["net_return"],
    )

    ax.axhline(0, linestyle="--", linewidth=1)

    ax.set_title("Option Strategy Trade Returns")
    ax.set_xlabel("Trade #")
    ax.set_ylabel("Net Return")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, axis="y", alpha=0.3)

    save_plot(fig, "option_trade_returns.png")
    plt.close(fig)

    # -------------------------------
    # 4. Equity + Drawdown Dashboard
    # -------------------------------
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    axes[0].plot(
        df["trade_id"],
        df["equity"],
        marker="o",
        linewidth=2,
    )
    axes[0].set_title("Option Strategy Equity and Drawdown")
    axes[0].set_ylabel("Equity")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        df["trade_id"],
        df["drawdown"],
        marker="o",
        linewidth=2,
    )
    axes[1].axhline(0, linestyle="--", linewidth=1)
    axes[1].set_xlabel("Trade #")
    axes[1].set_ylabel("Drawdown")
    axes[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axes[1].grid(True, alpha=0.3)

    save_plot(fig, "option_equity_drawdown_dashboard.png")
    plt.close(fig)

    # -------------------------------
    # 5. Return Distribution
    # -------------------------------
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.hist(
        df["net_return"],
        bins=max(3, min(10, len(df))),
        edgecolor="black",
    )

    ax.axvline(0, linestyle="--", linewidth=1)

    ax.set_title("Option Strategy Return Distribution")
    ax.set_xlabel("Net Return")
    ax.set_ylabel("Frequency")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, axis="y", alpha=0.3)

    save_plot(fig, "option_return_distribution.png")
    plt.close(fig)

    # -------------------------------
    # 6. Holding Days Distribution
    # -------------------------------
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.bar(
        df["trade_id"],
        df["holding_days"],
    )

    ax.set_title("Option Strategy Holding Days")
    ax.set_xlabel("Trade #")
    ax.set_ylabel("Holding Days")
    ax.grid(True, axis="y", alpha=0.3)

    save_plot(fig, "option_holding_days.png")
    plt.close(fig)

    # -------------------------------
    # 7. Entry IV vs Return
    # -------------------------------
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        df["entry_straddle_price"],
        df["net_return"],
        s=60,
    )

    ax.axhline(0, linestyle="--", linewidth=1)

    ax.set_title("Entry Straddle Price vs Option Return")
    ax.set_xlabel("Entry Straddle Price")
    ax.set_ylabel("Net Return")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    save_plot(fig, "option_entry_iv_vs_return.png")
    plt.close(fig)

    # -------------------------------
    # 8. Signal Score vs Return
    # -------------------------------
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        df["entry_signal_score"],
        df["net_return"],
        s=60,
    )

    ax.axhline(0, linestyle="--", linewidth=1)

    ax.set_title("Signal Score vs Option Return")
    ax.set_xlabel("Entry Signal Score")
    ax.set_ylabel("Net Return")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    save_plot(fig, "option_signal_score_vs_return.png")
    plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()