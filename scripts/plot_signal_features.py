from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\daily_signal_features.parquet"
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
    print("Reading signal features...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:")
    print(df.shape)

    df["trade_date_dt"] = pd.to_datetime(df["trade_date"].astype(str))
    df = df.sort_values("trade_date_dt").copy()

    signal_df = df[df["long_signal"] == 1].copy()

    print("Signal days:")
    print(len(signal_df))

    # -------------------------------
    # 1. Signal score through time
    # -------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        df["trade_date_dt"],
        df["signal_score"],
        linewidth=2,
        label="Signal Score",
    )

    ax.axhline(
        80,
        linestyle="--",
        linewidth=1.5,
        label="Long threshold = 80",
    )

    ax.scatter(
        signal_df["trade_date_dt"],
        signal_df["signal_score"],
        s=40,
        label="Long signal days",
        zorder=3,
    )

    ax.set_title("Long-only Volatility Signal Score")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Signal Score")
    ax.set_ylim(-5, 105)
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_plot(fig, "signal_score_through_time.png")
    plt.close(fig)

    # -------------------------------
    # 2. Near IV with signal days
    # -------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        df["trade_date_dt"],
        df["near_iv"],
        linewidth=2,
        label="Near ATM IV",
    )

    ax.plot(
        df["trade_date_dt"],
        df["near_iv_roll_mean"],
        linewidth=1.8,
        linestyle="--",
        label="20D rolling mean",
    )

    lower_band = (
        df["near_iv_roll_mean"]
        - df["near_iv_roll_std"]
    )

    ax.plot(
        df["trade_date_dt"],
        lower_band,
        linewidth=1.5,
        linestyle=":",
        label="Mean - 1 Std",
    )

    ax.scatter(
        signal_df["trade_date_dt"],
        signal_df["near_iv"],
        s=40,
        label="Long signal days",
        zorder=3,
    )

    ax.set_title("Near ATM IV with Long Signal Days")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Near ATM IV")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_plot(fig, "near_iv_with_signal_days.png")
    plt.close(fig)

    # -------------------------------
    # 3. Term slope with signal days
    # -------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        df["trade_date_dt"],
        df["term_slope_next_near"],
        linewidth=2,
        label="Next - Near ATM IV",
    )

    ax.axhline(
        0,
        linestyle="--",
        linewidth=1,
        label="Zero slope",
    )

    ax.scatter(
        signal_df["trade_date_dt"],
        signal_df["term_slope_next_near"],
        s=40,
        label="Long signal days",
        zorder=3,
    )

    ax.set_title("ATM Term Slope with Long Signal Days")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Next - Near ATM IV")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_plot(fig, "term_slope_with_signal_days.png")
    plt.close(fig)

    # -------------------------------
    # 4. Signal strength distribution
    # -------------------------------
    order = [
        "none",
        "weak",
        "medium",
        "strong",
        "very_strong",
    ]

    counts = (
        df["signal_strength"]
        .value_counts()
        .reindex(order)
        .fillna(0)
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.bar(
        counts.index.astype(str),
        counts.values,
    )

    ax.set_title("Signal Strength Distribution")
    ax.set_xlabel("Signal Strength")
    ax.set_ylabel("Number of Days")
    ax.grid(True, axis="y", alpha=0.3)

    save_plot(fig, "signal_strength_distribution.png")
    plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()