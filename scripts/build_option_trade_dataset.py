from pathlib import Path
import numpy as np
import pandas as pd

GREEKS_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

TRADES_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\long_only_trades.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\option_trade_dataset.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\option_trade_dataset.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\option_trade_dataset_report.txt"
)

PRICE_COL = "option_price"

MIN_ENTRY_DAYS_TO_EXPIRY = 25


def select_entry_atm_straddle(day_df):
    day_df = day_df.copy()
    day_df["days_to_expiry"] = day_df["T"] * 365

    eligible = day_df[
        day_df["days_to_expiry"] >= MIN_ENTRY_DAYS_TO_EXPIRY
    ].copy()

    if eligible.empty:
        return None

    near_t = eligible["T"].min()
    near = eligible[eligible["T"] == near_t].copy()

    near["abs_log_moneyness"] = np.abs(
        np.log(near["strike"] / near["future_price"])
    )

    atm_by_bucket = (
        near.groupby("time_bucket")["abs_log_moneyness"]
        .min()
        .reset_index()
        .rename(columns={"abs_log_moneyness": "min_abs_log_moneyness"})
    )

    near = near.merge(atm_by_bucket, on="time_bucket", how="left")

    atm = near[
        near["abs_log_moneyness"] == near["min_abs_log_moneyness"]
    ].copy()

    pair_counts = (
        atm.groupby(["expiry_code", "strike"])
        .agg(
            rows=("symbol", "count"),
            call_rows=("option_type", lambda x: (x == "C").sum()),
            put_rows=("option_type", lambda x: (x == "P").sum()),
            avg_volume=("volume", "mean"),
            avg_open_interest=("openInterest", "mean"),
            median_days_to_expiry=("days_to_expiry", "median"),
        )
        .reset_index()
    )

    pair_counts = pair_counts[
        (pair_counts["call_rows"] > 0)
        & (pair_counts["put_rows"] > 0)
    ].copy()

    if pair_counts.empty:
        return None

    selected = pair_counts.sort_values(
        ["rows", "avg_volume", "avg_open_interest"],
        ascending=False,
    ).iloc[0]

    expiry = selected["expiry_code"]
    strike = selected["strike"]

    selected_rows = day_df[
        (day_df["expiry_code"] == expiry)
        & (day_df["strike"] == strike)
        & (day_df[PRICE_COL] > 0)
    ].copy()

    call_price = selected_rows.loc[
        selected_rows["option_type"] == "C", PRICE_COL
    ].median()

    put_price = selected_rows.loc[
        selected_rows["option_type"] == "P", PRICE_COL
    ].median()

    if pd.isna(call_price) or pd.isna(put_price):
        return None

    return {
        "expiry_code": expiry,
        "strike": strike,
        "entry_call_price": call_price,
        "entry_put_price": put_price,
        "entry_straddle_price": call_price + put_price,
        "entry_rows": len(selected_rows),
        "entry_avg_future_price": selected_rows["future_price"].median(),
        "entry_T": selected_rows["T"].median(),
        "entry_days_to_expiry": selected_rows["T"].median() * 365,
    }


def price_exit_straddle(day_df, expiry, strike):
    rows = day_df[
        (day_df["expiry_code"] == expiry)
        & (day_df["strike"] == strike)
        & (day_df[PRICE_COL] > 0)
    ].copy()

    if rows.empty:
        return None

    call_price = rows.loc[
        rows["option_type"] == "C", PRICE_COL
    ].median()

    put_price = rows.loc[
        rows["option_type"] == "P", PRICE_COL
    ].median()

    if pd.isna(call_price) or pd.isna(put_price):
        return None

    return {
        "exit_call_price": call_price,
        "exit_put_price": put_price,
        "exit_straddle_price": call_price + put_price,
        "exit_rows": len(rows),
        "exit_avg_future_price": rows["future_price"].median(),
        "exit_T": rows["T"].median(),
        "exit_days_to_expiry": rows["T"].median() * 365,
    }


def main():
    print("Reading signal trades...")
    trades = pd.read_parquet(TRADES_FILE)

    print("Trades shape:")
    print(trades.shape)

    needed_dates = sorted(
        set(trades["entry_date"].astype(str))
        | set(trades["exit_date"].astype(str))
    )

    print("Needed dates:")
    print(needed_dates)

    print("Reading Greeks dataset...")

    cols = [
        "trade_date",
        "time_bucket",
        "symbol",
        "option_type",
        "strike",
        "expiry_code",
        "future_price",
        "T",
        "option_price",
        "lastPrice",
        "volume",
        "openInterest",
    ]

    df = pd.read_parquet(GREEKS_FILE, columns=cols)

    if PRICE_COL not in df.columns:
        raise ValueError(f"Missing price column: {PRICE_COL}")

    df["trade_date"] = df["trade_date"].astype(str)

    df = df[df["trade_date"].isin(needed_dates)].copy()

    print("Filtered Greeks shape:")
    print(df.shape)

    results = []

    for _, trade in trades.iterrows():
        entry_date = str(trade["entry_date"])
        exit_date = str(trade["exit_date"])

        entry_df = df[df["trade_date"] == entry_date].copy()
        exit_df = df[df["trade_date"] == exit_date].copy()

        entry_info = select_entry_atm_straddle(entry_df)

        if entry_info is None:
            results.append({
                "entry_date": entry_date,
                "exit_date": exit_date,
                "status": "missing_entry_straddle",
            })
            continue

        exit_info = price_exit_straddle(
            exit_df,
            entry_info["expiry_code"],
            entry_info["strike"],
        )

        if exit_info is None:
            results.append({
                "entry_date": entry_date,
                "exit_date": exit_date,
                "status": "missing_exit_straddle",
                **entry_info,
            })
            continue

        entry_price = entry_info["entry_straddle_price"]
        exit_price = exit_info["exit_straddle_price"]

        option_return = (
            (exit_price - entry_price) / entry_price
            if entry_price > 0
            else np.nan
        )

        results.append({
            "entry_date": entry_date,
            "exit_date": exit_date,
            "holding_days": trade["holding_days"],
            "status": "ok",
            "signal_iv_return": trade["iv_return"],
            "entry_signal_score": trade["entry_signal_score"],
            "exit_signal_score": trade["exit_signal_score"],
            **entry_info,
            **exit_info,
            "option_pnl": exit_price - entry_price,
            "option_return": option_return,
            "exit_reason": trade["exit_reason"],
        })

    out = pd.DataFrame(results)

    print("\nOption trade dataset shape:")
    print(out.shape)

    print("\nStatus counts:")
    print(out["status"].value_counts())

    ok = out[out["status"] == "ok"].copy()

    if not ok.empty:
        print("\nOption return summary:")
        print(ok["option_return"].describe())

        print("\nTrades:")
        print(
            ok[
                [
                    "entry_date",
                    "exit_date",
                    "expiry_code",
                    "strike",
                    "entry_days_to_expiry",
                    "exit_days_to_expiry",
                    "entry_straddle_price",
                    "exit_straddle_price",
                    "option_return",
                    "signal_iv_return",
                    "exit_reason",
                ]
            ]
        )

    print("Saving outputs...")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_FILE, index=False)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("====================================")
    lines.append("Option Trade Dataset Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Trades source: {TRADES_FILE}")
    lines.append(f"Greeks source: {GREEKS_FILE}")
    lines.append(f"Output: {OUT_FILE}")
    lines.append("")
    lines.append(f"Min entry days to expiry: {MIN_ENTRY_DAYS_TO_EXPIRY}")
    lines.append(f"Shape: {out.shape}")
    lines.append("")
    lines.append("Status counts:")
    lines.append(str(out["status"].value_counts()))
    lines.append("")

    if not ok.empty:
        lines.append("Option return summary:")
        lines.append(str(ok["option_return"].describe()))
        lines.append("")
        lines.append("Trades:")
        lines.append(str(ok))

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("\nDONE")
    print("Saved:")
    print(OUT_FILE)
    print(OUT_CSV)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()