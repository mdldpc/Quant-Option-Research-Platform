import pandas as pd

IV_PATH = r"D:\Quant_Option_Project\data_parquet\iv_sample.parquet"


def main():

    df = pd.read_parquet(IV_PATH)

    failed = df[
        df["implied_vol"].isna()
    ].copy()

    print("Failed IV Count:")
    print(len(failed))

    print("\nFailure Rate:")
    print(len(failed) / len(df))

    print("\nSample Failures:")
    print(
        failed[
            [
                "symbol",
                "option_type",
                "strike",
                "option_price",
                "future_price",
                "T",
            ]
        ].head(50)
    )

    print("\nPrice Statistics:")
    print(
        failed[
            [
                "option_price",
                "future_price",
                "strike",
            ]
        ].describe()
    )


if __name__ == "__main__":
    main()