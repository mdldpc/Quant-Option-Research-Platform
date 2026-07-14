from pathlib import Path
import pandas as pd

from analysis.session_filter import filter_regular_trading_session


RAW_DIR = Path("C:/Users/yyyjz/Desktop/2026intern/CFFEX.2026")


def main():
    files = sorted(list(RAW_DIR.rglob("*.csv.xz")))

    if not files:
        raise FileNotFoundError(f"No .csv.xz files found under {RAW_DIR}")

    def is_weekday_file(file_path):
        parts = file_path.name.split(".")
        date_str = parts[2]  # CFFEX.IF.20260102.csv.xz -> 20260102

        date = pd.to_datetime(date_str, format="%Y%m%d", errors="coerce")

        if pd.isna(date):
            return False
        
        return date.weekday() < 5


    trading_files = [f for f in files if is_weekday_file(f)]
    sample_files = trading_files[:10]

    results = []

    for file_path in sample_files:
        usecols = ["iRecvTime", "updateTime", "mTime", "symbol", "lastPrice"]

        df = pd.read_csv(
            file_path,
            compression="xz",
            usecols=usecols,
        )

        clean = filter_regular_trading_session(df)

        results.append(
            {
                "file": file_path.name,
                "rows_before": len(df),
                "rows_after": len(clean),
                "rows_removed": len(df) - len(clean),
                "removed_pct": (len(df) - len(clean)) / len(df) * 100 if len(df) > 0 else 0,
                "time_min_before": df["updateTime"].min(),
                "time_max_before": df["updateTime"].max(),
                "time_min_after": clean["updateTime"].min() if len(clean) > 0 else None,
                "time_max_after": clean["updateTime"].max() if len(clean) > 0 else None,
            }
        )

    out = pd.DataFrame(results)

    print(out)

    output_path = Path("research/exports/session_filter_test_summary.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print("\nSaved:")
    print(output_path)


if __name__ == "__main__":
    main()