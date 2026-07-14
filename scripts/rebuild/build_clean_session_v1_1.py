from pathlib import Path
import argparse
import pandas as pd

from framework.data.loader import DataLoader
from framework.data.trading_days import (
    find_available_trade_dates,
    filter_trade_dates,
)
from framework.market.trading_filter import TradingFilter


INPUT_ROOT = Path("data/cleaned_sessions")
OUTPUT_ROOT = Path("data/filtered_sessions")

OUT_SUMMARY = Path("research/exports/clean_session_summary_v1_1.csv")
OUT_REPORT = Path("research/reports/build_clean_session_v1_1_report.txt")


def find_input_file(trade_date: int) -> Path:
    pattern = f"*{trade_date}*.parquet"
    files = sorted(INPUT_ROOT.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No session file found for {trade_date} under {INPUT_ROOT}"
        )

    return files[0]


def output_file(trade_date: int) -> Path:
    return OUTPUT_ROOT / f"trade_date={trade_date}" / "session_filtered_v1_1.parquet"


def build_one(trade_date: int, overwrite: bool = False) -> dict:
    in_file = find_input_file(trade_date)
    out_file = output_file(trade_date)

    if out_file.exists() and not overwrite:
        return {
            "trade_date": trade_date,
            "status": "skipped_exists",
            "input": str(in_file),
            "output": str(out_file),
            "raw_rows": None,
            "clean_rows": None,
            "removed_rows": None,
            "removed_ratio": None,
        }

    df = DataLoader.read_parquet(in_file)
    raw_rows = len(df)

    cleaned = TradingFilter.clean(df)
    clean_rows = len(cleaned)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_parquet(out_file, index=False)

    removed = raw_rows - clean_rows
    removed_ratio = removed / raw_rows if raw_rows > 0 else 0.0

    return {
        "trade_date": trade_date,
        "status": "built",
        "input": str(in_file),
        "output": str(out_file),
        "raw_rows": raw_rows,
        "clean_rows": clean_rows,
        "removed_rows": removed,
        "removed_ratio": removed_ratio,
    }


def resolve_dates(args) -> list[int]:
    if args.trade_date is not None:
        return [args.trade_date]

    dates = find_available_trade_dates(INPUT_ROOT)

    if args.start_date is not None or args.end_date is not None:
        dates = filter_trade_dates(
            dates,
            start_date=args.start_date,
            end_date=args.end_date,
        )

    return dates


def write_outputs(summary: pd.DataFrame):
    OUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(
        OUT_SUMMARY,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("Build Clean Session v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Rows processed : {len(summary)}")

    if not summary.empty:
        lines.append(f"Built          : {(summary['status'] == 'built').sum()}")
        lines.append(f"Skipped        : {(summary['status'] == 'skipped_exists').sum()}")
        lines.append("")
        lines.append(summary.to_string(index=False))

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--trade-date",
        type=int,
        default=None,
        help="Single trade date in YYYYMMDD format.",
    )

    parser.add_argument(
        "--start-date",
        type=int,
        default=None,
        help="Start date in YYYYMMDD format.",
    )

    parser.add_argument(
        "--end-date",
        type=int,
        default=None,
        help="End date in YYYYMMDD format.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing filtered session files.",
    )

    args = parser.parse_args()

    dates = resolve_dates(args)

    results = []

    for trade_date in dates:
        print("Processing:", trade_date)
        try:
            result = build_one(
                trade_date=trade_date,
                overwrite=args.overwrite,
            )
        except Exception as e:
            result = {
                "trade_date": trade_date,
                "status": "error",
                "input": "",
                "output": "",
                "raw_rows": None,
                "clean_rows": None,
                "removed_rows": None,
                "removed_ratio": None,
                "error": str(e),
            }

        results.append(result)

    summary = pd.DataFrame(results)
    write_outputs(summary)

    print("DONE")
    print("Dates:", len(dates))
    print("Saved:")
    print(OUT_SUMMARY)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()