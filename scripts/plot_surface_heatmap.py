from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\exports\daily_surface_bucket_iv.csv"
)

FIG_DIR = Path(
    r"D:\Quant_Option_Project\research\figures"
)

BUCKET_ORDER = [
    "moneyness_lt_0_90",
    "moneyness_0_90_0_95",
    "moneyness_0_95_0_98",
    "moneyness_0_98_1_02",
    "moneyness_1_02_1_05",
    "moneyness_1_05_1_10",
    "moneyness_gt_1_10",
]

BUCKET_LABELS = {
    "moneyness_lt_0_90": "<0.90",
    "moneyness_0_90_0_95": "0.90-0.95",
    "moneyness_0_95_0_98": "0.95-0.98",
    "moneyness_0_98_1_02": "0.98-1.02",
    "moneyness_1_02_1_05": "1.02-1.05",
    "moneyness_1_05_1_10": "1.05-1.10",
    "moneyness_gt_1_10": ">1.10",
}


def save_plot(fig, filename):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / filename
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print("Saved:", out)


def main():
    print("Reading daily surface bucket IV...")
    df = pd.read_csv(DATA_FILE)

    print("Shape:")
    print(df.shape)

    available = [
        c for c in BUCKET_ORDER
        if c in df.columns
    ]

    print("Available buckets:")
    print(available)

    df = df.sort_values("trade_date").copy()

    # Matrix: rows = moneyness buckets, columns = dates
    heatmap_data = (
        df.set_index("trade_date")[available]
        .T
    )

    display_labels = [
        BUCKET_LABELS[c]
        for c in available
    ]

    # -------------------------------
    # 1. Full H1 heatmap
    # -------------------------------
    fig, ax = plt.subplots(figsize=(16, 6))

    im = ax.imshow(
        heatmap_data.values,
        aspect="auto",
        interpolation="nearest",
    )

    ax.set_title("Near-Expiry Volatility Surface Heatmap")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Moneyness Bucket")

    ax.set_yticks(range(len(display_labels)))
    ax.set_yticklabels(display_labels)

    # 控制 x 轴不要太密
    x_positions = list(range(0, len(df), max(1, len(df) // 10)))
    x_labels = [
        str(df["trade_date"].iloc[i])
        for i in x_positions
    ]

    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha="right")

    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    cbar.set_label("Average Smoothed IV")

    save_plot(fig, "surface_heatmap_near_h1.png")
    plt.close(fig)

    # -------------------------------
    # 2. January heatmap
    # -------------------------------
    jan = df[df["trade_date"].astype(str).str.startswith("202601")].copy()

    if not jan.empty:
        jan_data = jan.set_index("trade_date")[available].T

        fig, ax = plt.subplots(figsize=(14, 6))
        im = ax.imshow(
            jan_data.values,
            aspect="auto",
            interpolation="nearest",
        )

        ax.set_title("Near-Expiry Volatility Surface Heatmap - January 2026")
        ax.set_xlabel("Trade Date")
        ax.set_ylabel("Moneyness Bucket")
        ax.set_yticks(range(len(display_labels)))
        ax.set_yticklabels(display_labels)

        x_positions = list(range(len(jan)))
        x_labels = jan["trade_date"].astype(str).tolist()

        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)

        cbar = fig.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        cbar.set_label("Average Smoothed IV")

        save_plot(fig, "surface_heatmap_near_202601.png")
        plt.close(fig)

    # -------------------------------
    # 3. March heatmap
    # -------------------------------
    mar = df[df["trade_date"].astype(str).str.startswith("202603")].copy()

    if not mar.empty:
        mar_data = mar.set_index("trade_date")[available].T

        fig, ax = plt.subplots(figsize=(14, 6))
        im = ax.imshow(
            mar_data.values,
            aspect="auto",
            interpolation="nearest",
        )

        ax.set_title("Near-Expiry Volatility Surface Heatmap - March 2026")
        ax.set_xlabel("Trade Date")
        ax.set_ylabel("Moneyness Bucket")
        ax.set_yticks(range(len(display_labels)))
        ax.set_yticklabels(display_labels)

        x_positions = list(range(len(mar)))
        x_labels = mar["trade_date"].astype(str).tolist()

        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)

        cbar = fig.colorbar(im, ax=ax)
        cbar.ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        cbar.set_label("Average Smoothed IV")

        save_plot(fig, "surface_heatmap_near_202603.png")
        plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()