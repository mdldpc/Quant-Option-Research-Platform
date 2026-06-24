from pathlib import Path
import pandas as pd

ROOT = Path(r"D:\Quant_Option_Project\data_parquet\batch_2026")

DATES = [
    "20260114",
    "20260115",
]


def analyze_one_day(trade_date):
    file = ROOT / f"trade_date={trade_date}" / "iv_table.parquet"

    print("\n" + "=" * 70)
    print("Analyzing:", trade_date)

    if not file.exists():
        print("File not found:")
        print(file)
        return

    df = pd.read_parquet(file)

    total = len(df)
    failed = df[df["implied_vol"].isna()].copy()

    print("Total rows:", total)
    print("Failed rows:", len(failed))

    if total > 0:
        print("Failure ratio:", len(failed) / total)
        print("Valid IV ratio:", 1 - len(failed) / total)

    if len(failed) == 0:
        print("No failed IV rows.")
        return

    print("\nFailed by expiry_code:")
    print(failed["expiry_code"].value_counts())

    print("\nFailed by option_type:")
    print(failed["option_type"].value_counts())

    print("\nTop failed symbols:")
    print(failed["symbol"].value_counts().head(30))

    print("\nFailed price summary:")
    print(
        failed[
            [
                "option_price",
                "future_price",
                "strike",
                "T",
            ]
        ].describe()
    )

    print("\nFailed moneyness summary:")
    failed["moneyness"] = failed["strike"] / failed["future_price"]

    print(
        failed["moneyness"]
        .describe()
    )

    print("\nFailed moneyness buckets:")

    bins = [
        0.0,
        0.8,
        0.9,
        0.95,
        1.05,
        1.1,
        1.2,
        10.0,
    ]

    labels = [
        "<0.8",
        "0.8-0.9",
        "0.9-0.95",
        "0.95-1.05 ATM",
        "1.05-1.1",
        "1.1-1.2",
        ">1.2",
    ]

    failed["moneyness_bucket"] = pd.cut(
        failed["moneyness"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )

    print(
        failed["moneyness_bucket"]
        .value_counts()
        .sort_index()
    )

    print("\nSample failed rows:")
    print(
        failed[
            [
                "symbol",
                "expiry_code",
                "option_type",
                "strike",
                "future_price",
                "option_price",
                "T",
                "moneyness",
            ]
        ].head(50)
    )


def main():
    for d in DATES:
        analyze_one_day(d)


if __name__ == "__main__":
    main()