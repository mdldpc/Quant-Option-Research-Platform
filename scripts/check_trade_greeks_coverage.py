import pandas as pd


GREEKS_FILE = "research/exports/smile_dataset_near_preview.csv"
TRADES_FILE = "research/exports/option_trade_dataset.csv"


def main():
    greeks = pd.read_csv(GREEKS_FILE)
    trades = pd.read_csv(TRADES_FILE)

    greeks["trade_date"] = greeks["trade_date"].astype(int)
    trades["entry_date"] = trades["entry_date"].astype(int)
    trades["exit_date"] = trades["exit_date"].astype(int)

    print("Greeks shape:", greeks.shape)
    print("Trades shape:", trades.shape)

    print("\nGreeks date range:")
    print(greeks["trade_date"].min(), greeks["trade_date"].max())

    print("\nTrade date range:")
    print(trades["entry_date"].min(), trades["exit_date"].max())

    required = []

    for i, row in trades.iterrows():
        entry = int(row["entry_date"])
        exit_ = int(row["exit_date"])
        expiry = int(row["expiry_code"])
        strike = float(row["strike"])

        dates = (
            greeks.loc[
                (greeks["trade_date"] >= entry)
                & (greeks["trade_date"] <= exit_),
                "trade_date",
            ]
            .drop_duplicates()
            .sort_values()
        )

        print(f"\nTrade {i+1}: {entry} -> {exit_}, expiry={expiry}, strike={strike}")
        print(f"Dates found in greeks: {len(dates)}")

        for d in dates:
            for option_type in ["C", "P"]:
                subset = greeks[
                    (greeks["trade_date"] == d)
                    & (greeks["expiry_code"] == expiry)
                    & (greeks["strike"] == strike)
                    & (greeks["option_type"] == option_type)
                ]

                required.append(
                    {
                        "trade_id": i + 1,
                        "date": d,
                        "expiry_code": expiry,
                        "strike": strike,
                        "option_type": option_type,
                        "rows_found": len(subset),
                    }
                )

    out = pd.DataFrame(required)

    if out.empty:
        print("\nNo overlapping records found.")
        print("This preview dataset is not sufficient for portfolio Greeks coverage.")
        return

    print("\nCoverage summary:")
    print(out.groupby(["trade_id", "option_type"])["rows_found"].sum())

    print("\nMissing rows:")
    missing = out[out["rows_found"] == 0]
    print(missing.head(50))

    output = "research/exports/trade_greeks_coverage_check.csv"
    out.to_csv(output, index=False)

    print("\nSaved:")
    print(output)


if __name__ == "__main__":
    main()