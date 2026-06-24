from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_iv_summary.parquet"
)

FIG_DIR = Path(
    r"D:\Quant_Option_Project\research\figures"
)


def save_plot(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / name
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print("Saved:", out)


def main():
    print("Reading daily IV summary...")
    df = pd.read_parquet(DATA_FILE)

    df["trade_date_dt"] = pd.to_datetime(df["trade_date"].astype(str))

    print("Shape:", df.shape)

    # 1. Near IV daily mean
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["trade_date_dt"], df["near_iv_mean"])
    ax.set_title("Daily Near ATM IV Mean")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Near ATM IV")
    ax.grid(True)
    save_plot(fig, "daily_near_iv_mean.png")
    plt.close(fig)

    # 2. Near / Next / Third IV
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["trade_date_dt"], df["near_iv_mean"], label="Near")
    ax.plot(df["trade_date_dt"], df["next_iv_mean"], label="Next")
    ax.plot(df["trade_date_dt"], df["third_iv_mean"], label="Third")
    ax.set_title("Daily ATM IV by Term")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("ATM IV")
    ax.legend()
    ax.grid(True)
    save_plot(fig, "daily_atm_iv_by_term.png")
    plt.close(fig)

    # 3. Next - Near spread
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["trade_date_dt"], df["next_minus_near_iv_mean"])
    ax.axhline(0, linestyle="--")
    ax.set_title("Daily Next - Near ATM IV Spread")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Next - Near IV")
    ax.grid(True)
    save_plot(fig, "daily_next_minus_near_iv.png")
    plt.close(fig)

    # 4. Third - Near spread
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["trade_date_dt"], df["third_minus_near_iv_mean"])
    ax.axhline(0, linestyle="--")
    ax.set_title("Daily Third - Near ATM IV Spread")
    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Third - Near IV")
    ax.grid(True)
    save_plot(fig, "daily_third_minus_near_iv.png")
    plt.close(fig)

    print("\nDONE")
    print("Figures saved to:")
    print(FIG_DIR)


if __name__ == "__main__":
    main()