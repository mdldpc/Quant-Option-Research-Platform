from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\exports\daily_smile_bucket_iv.csv"
)

FIG_DIR = Path(
    r"D:\Quant_Option_Project\research\figures"
)

BUCKET_ORDER = [
    "deep_low_moneyness",
    "low_moneyness",
    "slightly_low_moneyness",
    "atm",
    "slightly_high_moneyness",
    "high_moneyness",
    "deep_high_moneyness",
]

BUCKET_LABELS = {
    "deep_low_moneyness": "<0.90",
    "low_moneyness": "0.90-0.95",
    "slightly_low_moneyness": "0.95-0.98",
    "atm": "0.98-1.02",
    "slightly_high_moneyness": "1.02-1.05",
    "high_moneyness": "1.05-1.10",
    "deep_high_moneyness": ">1.10",
}


def save_plot(fig, filename):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / filename
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print("Saved:", out)


def format_percent_axis(ax):
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))


def main():
    print("Reading daily smile bucket IV...")
    df = pd.read_csv(DATA_FILE)

    print("Shape:")
    print(df.shape)

    available_buckets = [
        b for b in BUCKET_ORDER
        if b in df.columns
    ]

    print("Available buckets:")
    print(available_buckets)

    df["trade_date_dt"] = pd.to_datetime(df["trade_date"].astype(str))

    # -------------------------------
    # 1. Overall average smile
    # -------------------------------
    overall = df[available_buckets].mean()

    x_labels = [
        BUCKET_LABELS[b]
        for b in available_buckets
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        x_labels,
        overall.values,
        marker="o",
        linewidth=2,
    )

    ax.set_title("Overall Near-Expiry Volatility Smile")
    ax.set_xlabel("Moneyness Bucket: Strike / Future")
    ax.set_ylabel("Average Smoothed IV")
    format_percent_axis(ax)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=30, ha="right")

    save_plot(fig, "smile_bucket_overall.png")
    plt.close(fig)

    # -------------------------------
    # 2. Monthly average smile
    # -------------------------------
    df["month"] = df["trade_date"].astype(str).str[:6]

    monthly = (
        df.groupby("month")[available_buckets]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    for _, row in monthly.iterrows():
        ax.plot(
            x_labels,
            row[available_buckets].values,
            marker="o",
            linewidth=1.8,
            label=row["month"],
        )

    ax.set_title("Monthly Near-Expiry Volatility Smile")
    ax.set_xlabel("Moneyness Bucket: Strike / Future")
    ax.set_ylabel("Average Smoothed IV")
    format_percent_axis(ax)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Month", fontsize=8)
    plt.xticks(rotation=30, ha="right")

    save_plot(fig, "smile_bucket_monthly.png")
    plt.close(fig)

    # -------------------------------
    # 3. Daily ATM vs wings
    # -------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))

    if "atm" in available_buckets:
        ax.plot(
            df["trade_date_dt"],
            df["atm"],
            label="ATM",
            linewidth=2,
        )

    if "deep_low_moneyness" in available_buckets:
        ax.plot(
            df["trade_date_dt"],
            df["deep_low_moneyness"],
            label="Deep low moneyness",
            linewidth=1.5,
        )

    if "deep_high_moneyness" in available_buckets:
        ax.plot(
            df["trade_date_dt"],
            df["deep_high_moneyness"],
            label="Deep high moneyness",
            linewidth=1.5,
        )

    ax.set_title("Daily ATM IV vs Smile Wings")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Average Smoothed IV")
    format_percent_axis(ax)
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_plot(fig, "daily_atm_vs_wings.png")
    plt.close(fig)

    # -------------------------------
    # 4. Smile skew proxy
    # -------------------------------
    if (
        "deep_low_moneyness" in available_buckets
        and "deep_high_moneyness" in available_buckets
    ):
        df["left_minus_right_wing"] = (
            df["deep_low_moneyness"]
            - df["deep_high_moneyness"]
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(
            df["trade_date_dt"],
            df["left_minus_right_wing"],
            linewidth=2,
        )
        ax.axhline(0, linestyle="--", linewidth=1)

        ax.set_title("Smile Skew Proxy: Left Wing - Right Wing")
        ax.set_xlabel("Trade Date")
        ax.set_ylabel("IV Difference")
        format_percent_axis(ax)
        ax.grid(True, alpha=0.3)

        save_plot(fig, "smile_skew_proxy_left_minus_right.png")
        plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()