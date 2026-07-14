from pathlib import Path
import pandas as pd

from analysis.session_filter import filter_regular_trading_session


RAW_DIR = Path("C:/Users/yyyjz/Desktop/2026intern/CFFEX.2026")
OUTPUT_DIR = Path("data/cleaned_sessions")


def is_weekday_file(file_path: Path) -> bool:
    parts = file_path.name.split(".")
    if len(parts) < 3:
        return False

    date_str = parts[2]
    date = pd.to_datetime(date_str, format="%Y%m%d", errors="coerce")

    if pd.isna(date):
        return False

    return date.weekday() < 5


def output_path_for(file_path: Path) -> Path:
    date_str = file_path.name.split(".")[2]
    return OUTPUT_DIR / f"CFFEX.IF.{date_str}.session_clean.parquet"


def process_one_file(file_path: Path) -> dict:
    out_path = output_path_for(file_path)

    if out_path.exists():
        return {
            "file": file_path.name,
            "status": "skipped_exists",
            "rows_before": None,
            "rows_after": None,
            "rows_removed": None,
            "removed_pct": None,
            "output": str(out_path),
        }

    df = pd.read_csv(file_path, compression="xz")

    rows_before = len(df)

    clean = filter_regular_trading_session(df, time_col="updateTime")

    rows_after = len(clean)
    rows_removed = rows_before - rows_after
    removed_pct = rows_removed / rows_before * 100 if rows_before > 0 else 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(out_path, index=False)

    return {
        "file": file_path.name,
        "status": "processed",
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": rows_removed,
        "removed_pct": removed_pct,
        "output": str(out_path),
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(RAW_DIR.rglob("*.csv.xz"))
    trading_files = [f for f in files if is_weekday_file(f)]

    print(f"Raw files found: {len(files)}")
    print(f"Weekday files found: {len(trading_files)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    results = []

    for i, file_path in enumerate(trading_files, start=1):
        print(f"[{i}/{len(trading_files)}] {file_path.name}")

        try:
            result = process_one_file(file_path)
            results.append(result)

            print(
                f"  {result['status']} | "
                f"before={result['rows_before']} | "
                f"after={result['rows_after']} | "
                f"removed_pct={result['removed_pct']}"
            )

        except Exception as e:
            result = {
                "file": file_path.name,
                "status": "error",
                "error": str(e),
            }
            results.append(result)
            print(f"  ERROR: {e}")

        # 每处理一天就保存一次 summary，方便中断恢复
        summary = pd.DataFrame(results)
        summary_path = OUTPUT_DIR / "session_cleaning_summary.csv"
        summary.to_csv(summary_path, index=False)

    print()
    print("DONE")
    print(f"Summary saved to: {OUTPUT_DIR / 'session_cleaning_summary.csv'}")


if __name__ == "__main__":
    main()