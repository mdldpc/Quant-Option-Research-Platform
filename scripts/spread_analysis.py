import pandas as pd

RAW_PATH = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

USECOLS = [
    "symbol",
    "BP1",
    "AP1"
]

NROWS = 1_000_000


def main():

    print("Reading data...")

    df = pd.read_csv(
        RAW_PATH,
        compression="xz",
        usecols=USECOLS,
        nrows=NROWS
    )

    df["symbol"] = df["symbol"].str.strip()

    opt = df[
        df["symbol"].str.startswith("IO")
    ].copy()

    total = len(opt)

    both_side = (
        (opt["BP1"] > 0)
        & (opt["AP1"] > 0)
    )

    bid_only = (
        (opt["BP1"] > 0)
        & (opt["AP1"] == 0)
    )

    ask_only = (
        (opt["BP1"] == 0)
        & (opt["AP1"] > 0)
    )

    no_quote = (
        (opt["BP1"] == 0)
        & (opt["AP1"] == 0)
    )

    print("\nTotal Option Rows:")
    print(total)

    print("\nBoth Sides:")
    print(both_side.sum())
    print(f"{both_side.mean():.2%}")

    print("\nBid Only:")
    print(bid_only.sum())
    print(f"{bid_only.mean():.2%}")

    print("\nAsk Only:")
    print(ask_only.sum())
    print(f"{ask_only.mean():.2%}")

    print("\nNo Quote:")
    print(no_quote.sum())
    print(f"{no_quote.mean():.2%}")


if __name__ == "__main__":
    main()