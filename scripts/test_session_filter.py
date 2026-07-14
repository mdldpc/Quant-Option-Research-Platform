from pathlib import Path
import pandas as pd

from analysis.session_filter import filter_regular_trading_session


RAW_DIR = Path("C:/Users/yyyjz/Desktop/2026intern/CFFEX.2026")


def find_one_raw_file():
    files = list(RAW_DIR.rglob("*.csv.xz"))
    if not files:
        raise FileNotFoundError(f"No .csv.xz files found under {RAW_DIR}")
    return files[0]


def main():
    file_path = find_one_raw_file()

    print("Testing file:")
    print(file_path)

    usecols = ["iRecvTime", "updateTime", "mTime", "symbol", "lastPrice"]

    df = pd.read_csv(
        file_path,
        compression="xz",
        usecols=usecols,
    )

    print("\nBefore filter:")
    print(df.shape)
    print(df["updateTime"].min(), df["updateTime"].max())

    clean = filter_regular_trading_session(df)

    print("\nAfter filter:")
    print(clean.shape)
    print(clean["updateTime"].min(), clean["updateTime"].max())

    print("\nRows removed:")
    print(len(df) - len(clean))

    print("\nRemoved percentage:")
    print((len(df) - len(clean)) / len(df) * 100)


if __name__ == "__main__":
    main()