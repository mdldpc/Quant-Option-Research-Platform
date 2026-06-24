import pandas as pd

OPTION_TABLE = r"D:\Quant_Option_Project\data_parquet\option_table_sample.parquet"


def main():
    df = pd.read_parquet(OPTION_TABLE)

    df["expiry_code"] = df["symbol"].str.extract(r"IO(\d{4})")[0]

    print("Expiry codes found:")
    print(sorted(df["expiry_code"].dropna().unique()))

    print("\nRows by expiry:")
    print(df["expiry_code"].value_counts().sort_index())

    print("\nSymbols by expiry:")
    print(
        df.groupby("expiry_code")["symbol"]
        .nunique()
        .sort_index()
    )

    print("\nSample symbols:")
    for expiry in sorted(df["expiry_code"].dropna().unique()):
        sample = (
            df[df["expiry_code"] == expiry]["symbol"]
            .drop_duplicates()
            .head(10)
            .tolist()
        )
        print(expiry, sample)


if __name__ == "__main__":
    main()