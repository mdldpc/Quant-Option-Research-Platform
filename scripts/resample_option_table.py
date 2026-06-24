import pandas as pd

OPTION_TABLE = (
    r"D:\Quant_Option_Project\data_parquet"
    r"\batch_test\trade_date=20250102\option_table.parquet"
)

OUT_PATH = (
    r"D:\Quant_Option_Project\data_parquet"
    r"\batch_test\trade_date=20250102\option_table_10s.parquet"
)


def main():
    print("Reading option table...")
    df = pd.read_parquet(OPTION_TABLE)

    print("Original rows:")
    print(len(df))

    # iRecvTime 是纳秒级时间戳
    # 转成秒级 timestamp bucket
    df["time_bucket"] = df["iRecvTime"] // 10_000_000_000

    # 每个 symbol 每秒保留最后一条
    df = (
        df.sort_values("iRecvTime")
        .groupby(["symbol", "time_bucket"], as_index=False)
        .tail(1)
        .copy()
    )

    print("\nResampled rows:")
    print(len(df))

    print("\nCompression ratio:")
    print(len(df) / pd.read_parquet(OPTION_TABLE).shape[0])

    print("\nSymbols:")
    print(df["symbol"].nunique())

    print("\nSample:")
    print(df.head(20))

    df.to_parquet(OUT_PATH, index=False)

    print("\nSaved to:")
    print(OUT_PATH)


if __name__ == "__main__":
    main()