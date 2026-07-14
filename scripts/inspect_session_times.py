from pathlib import Path
import pandas as pd

from config.paths import PROJECT_ROOT


RAW_DIR = Path("C:/Users/yyyjz/Desktop/2026intern/CFFEX.2026")


def find_one_raw_file():
    files = list(RAW_DIR.rglob("*.csv.xz"))
    if not files:
        raise FileNotFoundError(f"No .csv.xz files found under {RAW_DIR}")
    return files[0]


def main():
    file_path = find_one_raw_file()
    print("Inspecting file:")
    print(file_path)

    usecols = ["iRecvTime", "updateTime", "mTime", "symbol", "lastPrice"]
    df = pd.read_csv(file_path, compression="xz", usecols=usecols, nrows=500000)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nHead:")
    print(df.head())

    print("\nupdateTime value counts:")
    print(df["updateTime"].value_counts().head(30))

    print("\nmTime value counts:")
    print(df["mTime"].value_counts().head(30))

    print("\nupdateTime min/max:")
    print(df["updateTime"].min(), df["updateTime"].max())

    print("\nmTime min/max:")
    print(df["mTime"].min(), df["mTime"].max())


if __name__ == "__main__":
    main()