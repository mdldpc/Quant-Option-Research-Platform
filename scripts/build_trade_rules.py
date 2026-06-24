from pathlib import Path
import pandas as pd
import numpy as np

SIGNAL_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\daily_signal_features.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\long_only_trades.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\long_only_trades.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\long_only_trades_report.txt"
)

MAX_HOLDING_DAYS = 10
EXIT_SCORE_THRESHOLD = 40


def main():
    print("Reading signal features...")
    df = pd.read_parquet(SIGNAL_FILE)

    df["trade_date_dt"] = pd.to_datetime(df["trade_date"].astype(str))
    df = df.sort_values("trade_date_dt").reset_index(drop=True)

    print("Source shape:")
    print(df.shape)

    trades = []
    in_position = False
    entry_idx = None

    for i in range(len(df)):
        row = df.iloc[i]

        if not in_position:
            if row["long_signal"] == 1:
                in_position = True
                entry_idx = i
            continue

        entry = df.iloc[entry_idx]
        holding_days = i - entry_idx

        exit_reason = None

        if row["signal_score"] <= EXIT_SCORE_THRESHOLD:
            exit_reason = "score_exit"

        if holding_days >= MAX_HOLDING_DAYS:
            exit_reason = "max_holding"

        is_last_day = i == len(df) - 1
        if is_last_day:
            exit_reason = "end_of_data"

        if exit_reason is not None:
            entry_iv = entry["near_iv"]
            exit_iv = row["near_iv"]

            iv_change = exit_iv - entry_iv
            iv_return = iv_change / entry_iv if entry_iv != 0 else np.nan

            trades.append(
                {
                    "entry_date": entry["trade_date"],
                    "entry_date_dt": entry["trade_date_dt"],
                    "exit_date": row["trade_date"],
                    "exit_date_dt": row["trade_date_dt"],
                    "holding_days": holding_days,
                    "entry_near_iv": entry_iv,
                    "exit_near_iv": exit_iv,
                    "iv_change": iv_change,
                    "iv_return": iv_return,
                    "entry_signal_score": entry["signal_score"],
                    "exit_signal_score": row["signal_score"],
                    "entry_term_slope": entry["term_slope_next_near"],
                    "exit_term_slope": row["term_slope_next_near"],
                    "entry_iv_zscore": entry["near_iv_zscore"],
                    "exit_iv_zscore": row["near_iv_zscore"],
                    "exit_reason": exit_reason,
                }
            )

            in_position = False
            entry_idx = None

    trades_df = pd.DataFrame(trades)

    print("\nTrades shape:")
    print(trades_df.shape)

    if not trades_df.empty:
        print("\nTrade summary:")
        print(trades_df[["holding_days", "iv_change", "iv_return"]].describe())

        print("\nExit reason counts:")
        print(trades_df["exit_reason"].value_counts())

        print("\nTrades:")
        print(trades_df)

    print("Saving outputs...")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    trades_df.to_parquet(OUT_FILE, index=False)
    trades_df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("====================================")
    lines.append("Long-only Trade Rules Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SIGNAL_FILE}")
    lines.append(f"Output parquet: {OUT_FILE}")
    lines.append(f"Output csv: {OUT_CSV}")
    lines.append("")
    lines.append(f"Max holding days: {MAX_HOLDING_DAYS}")
    lines.append(f"Exit score threshold: {EXIT_SCORE_THRESHOLD}")
    lines.append("")
    lines.append(f"Trades shape: {trades_df.shape}")
    lines.append("")

    if not trades_df.empty:
        lines.append("Trade summary:")
        lines.append(str(trades_df[["holding_days", "iv_change", "iv_return"]].describe()))
        lines.append("")
        lines.append("Exit reason counts:")
        lines.append(str(trades_df["exit_reason"].value_counts()))
        lines.append("")
        lines.append("Trades:")
        lines.append(str(trades_df))

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("\nDONE")
    print("Saved trades parquet:")
    print(OUT_FILE)
    print("Saved trades csv:")
    print(OUT_CSV)
    print("Saved report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()