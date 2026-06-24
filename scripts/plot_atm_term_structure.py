from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_atm_term_structure_2026H1.parquet"
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
    print("Reading daily ATM term structure...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:")
    print(df.shape)

    df["trade_date_dt"] = pd.to_datetime(df["trade_date"].astype(str))

    # -------------------------------
    # 1. Overall ATM term structure
    # -------------------------------
    overall = (
        df.groupby("term_rank")
        .agg(
            atm_iv_mean=("atm_iv_mean", "mean"),
            days_to_expiry_mean=("days_to_expiry_mean", "mean"),
            row_count=("row_count", "sum"),
        )
        .reset_index()
        .sort_values("term_rank")
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        overall["days_to_expiry_mean"],
        overall["atm_iv_mean"],
        marker="o",
        linewidth=2,
    )

    for _, row in overall.iterrows():
        ax.annotate(
            f"Rank {int(row['term_rank'])}",
            (row["days_to_expiry_mean"], row["atm_iv_mean"]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=9,
        )

    ax.set_title("Overall ATM IV Term Structure")
    ax.set_xlabel("Average Days to Expiry")
    ax.set_ylabel("Average ATM IV")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    save_plot(fig, "atm_term_structure_overall.png")
    plt.close(fig)

    # -------------------------------
    # 2. Monthly ATM term structure
    # -------------------------------
    df["month"] = df["trade_date"].astype(str).str[:6]

    monthly = (
        df.groupby(["month", "term_rank"])
        .agg(
            atm_iv_mean=("atm_iv_mean", "mean"),
            days_to_expiry_mean=("days_to_expiry_mean", "mean"),
        )
        .reset_index()
        .sort_values(["month", "term_rank"])
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    for month, g in monthly.groupby("month"):
        ax.plot(
            g["days_to_expiry_mean"],
            g["atm_iv_mean"],
            marker="o",
            linewidth=1.8,
            label=month,
        )

    ax.set_title("Monthly ATM IV Term Structure")
    ax.set_xlabel("Average Days to Expiry")
    ax.set_ylabel("Average ATM IV")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)
    ax.legend(title="Month", fontsize=8)

    save_plot(fig, "atm_term_structure_monthly.png")
    plt.close(fig)

    # -------------------------------
    # 3. Daily Near / Next / Third ATM IV
    # -------------------------------
    wide = (
        df.pivot(
            index="trade_date",
            columns="term_rank",
            values="atm_iv_mean",
        )
        .reset_index()
        .sort_values("trade_date")
    )

    wide["trade_date_dt"] = pd.to_datetime(
        wide["trade_date"].astype(str)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    if 1 in wide.columns:
        ax.plot(
            wide["trade_date_dt"],
            wide[1],
            linewidth=2,
            label="Near / Rank 1",
        )

    if 2 in wide.columns:
        ax.plot(
            wide["trade_date_dt"],
            wide[2],
            linewidth=2,
            label="Next / Rank 2",
        )

    if 3 in wide.columns:
        ax.plot(
            wide["trade_date_dt"],
            wide[3],
            linewidth=2,
            label="Third / Rank 3",
        )

    if 4 in wide.columns:
        ax.plot(
            wide["trade_date_dt"],
            wide[4],
            linewidth=2,
            label="Fourth / Rank 4",
        )

    ax.set_title("Daily ATM IV by Term Rank")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("ATM IV")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)
    ax.legend()

    save_plot(fig, "daily_atm_iv_by_term_rank.png")
    plt.close(fig)

    # -------------------------------
    # 4. Daily Term Slope
    # -------------------------------
    if 1 in wide.columns and 2 in wide.columns:
        wide["next_minus_near"] = wide[2] - wide[1]

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(
            wide["trade_date_dt"],
            wide["next_minus_near"],
            linewidth=2,
        )

        ax.axhline(0, linestyle="--", linewidth=1)

        ax.set_title("Daily ATM Term Structure Slope: Next - Near")
        ax.set_xlabel("Trade Date")
        ax.set_ylabel("ATM IV Difference")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax.grid(True, alpha=0.3)

        save_plot(fig, "daily_atm_term_slope_next_minus_near.png")
        plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()