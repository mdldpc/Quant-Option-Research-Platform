from pathlib import Path
import pandas as pd

OPTION_TRADE_FILE = Path(
    r"D:\Quant_Option_Project\research\backtest\option_trade_dataset.parquet"
)

GREEKS_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\missing_option_trade_inspection.csv"
)


def main():
    trades = pd.read_parquet(OPTION_TRADE_FILE)

    missing = trades[trades["status"] != "ok"].copy()

    print("Missing trades:")
    print(missing)

    if missing.empty:
        print("No missing trades.")
        return

    cols = [
        "trade_date",
        "symbol",
        "option_type",
        "strike",
        "expiry_code",
        "option_price",
        "lastPrice",
        "future_price",
        "T",
        "volume",
        "openInterest",
    ]

    needed_dates = sorted(set(missing["exit_date"].astype(str)))

    df = pd.read_parquet(GREEKS_FILE, columns=cols)
    df["trade_date"] = df["trade_date"].astype(str)
    df = df[df["trade_date"].isin(needed_dates)].copy()

    outputs = []

    for _, row in missing.iterrows():
        exit_date = str(row["exit_date"])
        expiry = row.get("expiry_code")
        strike = row.get("strike")

        day = df[df["trade_date"] == exit_date].copy()

        print("\n==============================")
        print("Exit date:", exit_date)
        print("Expected expiry:", expiry)
        print("Expected strike:", strike)
        print("Rows on exit date:", len(day))

        print("\nExpiry counts:")
        print(day["expiry_code"].value_counts().sort_index())

        if pd.notna(expiry):
            same_expiry = day[day["expiry_code"] == expiry].copy()
            print("\nRows same expiry:", len(same_expiry))

            print("\nAvailable strikes in same expiry:")
            print(
                same_expiry["strike"]
                .drop_duplicates()
                .sort_values()
                .to_list()
            )

            if pd.notna(strike):
                same_strike = same_expiry[same_expiry["strike"] == strike].copy()
                print("\nRows same expiry + strike:", len(same_strike))

                if not same_strike.empty:
                    print("\nOption type counts:")
                    print(same_strike["option_type"].value_counts())

                    print("\nSample:")
                    print(same_strike.head(20))

                nearby = same_expiry[
                    (same_expiry["strike"] >= strike - 300)
                    & (same_expiry["strike"] <= strike + 300)
                ].copy()

                nearby_summary = (
                    nearby.groupby(["strike", "option_type"])
                    .agg(
                        rows=("symbol", "count"),
                        median_price=("option_price", "median"),
                        median_last=("lastPrice", "median"),
                        median_future=("future_price", "median"),
                        avg_volume=("volume", "mean"),
                        avg_oi=("openInterest", "mean"),
                    )
                    .reset_index()
                    .sort_values(["strike", "option_type"])
                )

                print("\nNearby strike summary:")
                print(nearby_summary)

                nearby_summary["missing_entry_date"] = row["entry_date"]
                nearby_summary["missing_exit_date"] = exit_date
                nearby_summary["expected_expiry"] = expiry
                nearby_summary["expected_strike"] = strike

                outputs.append(nearby_summary)

    if outputs:
        out = pd.concat(outputs, ignore_index=True)
        OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
        print("\nSaved inspection CSV:")
        print(OUT_CSV)


if __name__ == "__main__":
    main()