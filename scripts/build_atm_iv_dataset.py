from pathlib import Path
import pandas as pd
import numpy as np

SOURCE_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\datasets\atm_iv_dataset_2026H1.parquet"
)

EXPORT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\atm_iv_dataset_preview.csv"
)


GREEKS = [
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():
    print("Reading source dataset...")
    df = pd.read_parquet(SOURCE_FILE)

    print("Source shape:", df.shape)

    required_cols = [
        "trade_date",
        "time_bucket",
        "expiry_code",
        "symbol",
        "option_type",
        "strike",
        "future_price",
        "T",
        "smoothed_iv",
        "implied_vol",
    ] + GREEKS

    df = df[required_cols].copy()

    print("Working shape:", df.shape)

    print("Calculating ATM distance...")
    df["abs_moneyness"] = (df["strike"] - df["future_price"]).abs()

    print("Selecting ATM strike per trade_date/time_bucket/expiry_code...")

    atm_strike = (
        df.groupby(
            ["trade_date", "time_bucket", "expiry_code"],
            as_index=False
        )
        .agg(
            atm_strike=("strike", lambda x: x.iloc[0])
        )
    )

    idx = (
        df.groupby(
            ["trade_date", "time_bucket", "expiry_code"]
        )["abs_moneyness"]
        .idxmin()
    )

    atm_base = df.loc[idx, [
        "trade_date",
        "time_bucket",
        "expiry_code",
        "strike",
        "future_price",
        "T",
        "abs_moneyness",
    ]].copy()

    atm_base = atm_base.rename(
        columns={
            "strike": "atm_strike",
        }
    )

    print("ATM base shape:", atm_base.shape)

    print("Filtering rows at ATM strike...")
    df_atm = df.merge(
        atm_base[
            [
                "trade_date",
                "time_bucket",
                "expiry_code",
                "atm_strike",
            ]
        ],
        left_on=[
            "trade_date",
            "time_bucket",
            "expiry_code",
            "strike",
        ],
        right_on=[
            "trade_date",
            "time_bucket",
            "expiry_code",
            "atm_strike",
        ],
        how="inner",
    )

    print("ATM rows shape:", df_atm.shape)

    print("Building Call side...")
    call_cols = {
        "symbol": "call_symbol",
        "smoothed_iv": "call_iv",
        "implied_vol": "call_raw_iv",
        "delta": "call_delta",
        "gamma": "call_gamma",
        "vega": "call_vega",
        "theta": "call_theta",
        "vanna": "call_vanna",
        "vomma": "call_vomma",
        "speed": "call_speed",
    }

    calls = (
        df_atm[df_atm["option_type"] == "C"]
        .sort_values(["trade_date", "time_bucket", "expiry_code"])
        .drop_duplicates(
            ["trade_date", "time_bucket", "expiry_code", "atm_strike"]
        )
        [
            [
                "trade_date",
                "time_bucket",
                "expiry_code",
                "atm_strike",
            ] + list(call_cols.keys())
        ]
        .rename(columns=call_cols)
    )

    print("Call rows:", len(calls))

    print("Building Put side...")
    put_cols = {
        "symbol": "put_symbol",
        "smoothed_iv": "put_iv",
        "implied_vol": "put_raw_iv",
        "delta": "put_delta",
        "gamma": "put_gamma",
        "vega": "put_vega",
        "theta": "put_theta",
        "vanna": "put_vanna",
        "vomma": "put_vomma",
        "speed": "put_speed",
    }

    puts = (
        df_atm[df_atm["option_type"] == "P"]
        .sort_values(["trade_date", "time_bucket", "expiry_code"])
        .drop_duplicates(
            ["trade_date", "time_bucket", "expiry_code", "atm_strike"]
        )
        [
            [
                "trade_date",
                "time_bucket",
                "expiry_code",
                "atm_strike",
            ] + list(put_cols.keys())
        ]
        .rename(columns=put_cols)
    )

    print("Put rows:", len(puts))

    print("Combining Call and Put...")
    result = atm_base.merge(
        calls,
        on=[
            "trade_date",
            "time_bucket",
            "expiry_code",
            "atm_strike",
        ],
        how="left",
    )

    result = result.merge(
        puts,
        on=[
            "trade_date",
            "time_bucket",
            "expiry_code",
            "atm_strike",
        ],
        how="left",
    )

    print("Combined shape:", result.shape)

    print("Calculating ATM IV...")
    result["atm_iv"] = result[["call_iv", "put_iv"]].mean(axis=1)

    result["has_call"] = result["call_iv"].notna()
    result["has_put"] = result["put_iv"].notna()
    result["has_both"] = result["has_call"] & result["has_put"]

    result["call_put_iv_spread"] = result["call_iv"] - result["put_iv"]

    ordered_cols = [
        "trade_date",
        "time_bucket",
        "expiry_code",
        "atm_strike",
        "future_price",
        "abs_moneyness",
        "T",
        "atm_iv",
        "call_iv",
        "put_iv",
        "call_put_iv_spread",
        "has_call",
        "has_put",
        "has_both",
        "call_symbol",
        "put_symbol",
        "call_raw_iv",
        "put_raw_iv",
        "call_delta",
        "put_delta",
        "call_gamma",
        "put_gamma",
        "call_vega",
        "put_vega",
        "call_theta",
        "put_theta",
        "call_vanna",
        "put_vanna",
        "call_vomma",
        "put_vomma",
        "call_speed",
        "put_speed",
    ]

    result = result[ordered_cols].sort_values(
        ["trade_date", "time_bucket", "expiry_code"]
    )

    print("\nFinal shape:")
    print(result.shape)

    print("\nCoverage:")
    print("Trade dates:", result["trade_date"].nunique())
    print("Expiry codes:", result["expiry_code"].nunique())

    print("\nCall/Put availability:")
    print(result[["has_call", "has_put", "has_both"]].mean())

    print("\nATM IV summary:")
    print(result["atm_iv"].describe())

    print("\nSaving parquet...")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_parquet(OUT_FILE, index=False)

    print("Saving preview CSV...")
    EXPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    result.head(100_000).to_csv(
        EXPORT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nDONE")
    print("Saved parquet:")
    print(OUT_FILE)
    print("Saved preview:")
    print(EXPORT_CSV)


if __name__ == "__main__":
    main()