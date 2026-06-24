from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_greeks_summary.parquet"
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


def main():
    print("Reading daily Greeks summary...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:")
    print(df.shape)

    df["trade_date_dt"] = pd.to_datetime(df["trade_date"].astype(str))

    # -------------------------------
    # Prepare wide delta data
    # -------------------------------
    wide = (
        df.pivot(
            index="trade_date",
            columns="moneyness_bucket",
            values="delta_mean",
        )
        .reset_index()
        .sort_values("trade_date")
    )

    available = [
        b for b in BUCKET_ORDER
        if b in wide.columns
    ]

    x_labels = [
        BUCKET_LABELS[b]
        for b in available
    ]

    # -------------------------------
    # 1. Overall Delta Profile
    # -------------------------------
    overall = df.groupby(
        "moneyness_bucket",
        observed=False,
    )["delta_mean"].mean()

    overall = overall.reindex(available)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        x_labels,
        overall.values,
        marker="o",
        linewidth=2,
    )

    ax.axhline(0, linestyle="--", linewidth=1)

    ax.set_title("Overall Delta Profile by Moneyness")
    ax.set_xlabel("Moneyness Bucket: Strike / Future")
    ax.set_ylabel("Mean Delta")
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=30, ha="right")

    save_plot(fig, "delta_profile_overall.png")
    plt.close(fig)

    # -------------------------------
    # 2. Monthly Delta Profile
    # -------------------------------
    df["month"] = df["trade_date"].astype(str).str[:6]

    monthly = (
        df.groupby(
            ["month", "moneyness_bucket"],
            observed=False,
        )["delta_mean"]
        .mean()
        .reset_index()
    )

    monthly_wide = (
        monthly.pivot(
            index="month",
            columns="moneyness_bucket",
            values="delta_mean",
        )
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    for _, row in monthly_wide.iterrows():
        ax.plot(
            x_labels,
            row[available].values,
            marker="o",
            linewidth=1.8,
            label=row["month"],
        )

    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_title("Monthly Delta Profile by Moneyness")
    ax.set_xlabel("Moneyness Bucket: Strike / Future")
    ax.set_ylabel("Mean Delta")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Month", fontsize=8)

    plt.xticks(rotation=30, ha="right")

    save_plot(fig, "delta_profile_monthly.png")
    plt.close(fig)

    # -------------------------------
    # 3. Daily Delta Heatmap
    # -------------------------------
    heatmap_data = wide.set_index("trade_date")[available].T

    fig, ax = plt.subplots(figsize=(16, 6))

    im = ax.imshow(
        heatmap_data.values,
        aspect="auto",
        interpolation="nearest",
        vmin=-1,
        vmax=1,
    )

    ax.set_title("Daily Delta Heatmap by Moneyness")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Moneyness Bucket")

    ax.set_yticks(range(len(available)))
    ax.set_yticklabels(x_labels)

    step = max(1, len(wide) // 10)
    x_positions = list(range(0, len(wide), step))
    x_date_labels = [
        str(wide["trade_date"].iloc[i])
        for i in x_positions
    ]

    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        x_date_labels,
        rotation=45,
        ha="right",
    )

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Mean Delta")

    save_plot(fig, "delta_heatmap_daily.png")
    plt.close(fig)

    # -------------------------------
    # 4. ATM Delta Through Time
    # -------------------------------
    atm = df[df["moneyness_bucket"] == "atm"].copy()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        atm["trade_date_dt"],
        atm["delta_mean"],
        linewidth=2,
    )

    ax.axhline(0, linestyle="--", linewidth=1)

    ax.set_title("ATM Delta Through Time")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("ATM Mean Delta")
    ax.grid(True, alpha=0.3)

    save_plot(fig, "atm_delta_through_time.png")
    plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()