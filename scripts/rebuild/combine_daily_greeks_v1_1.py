from pathlib import Path
import pandas as pd

from config.data_version import ALL_GREEKS_FILE
from config.trading_calendar import is_abnormal_trading_date


DAILY_ROOT = Path("data_parquet/batch_2026_v1_1_daily")
OUT_FILE = ALL_GREEKS_FILE
OUT_REPORT = Path("research/reports/combine_daily_greeks_v1_1_report.txt")


def extract_trade_date(path: Path) -> int:
    return int(path.parent.name.replace("trade_date=", ""))


def main():
    files = sorted(DAILY_ROOT.glob("trade_date=*/greeks_v1_1.parquet"))

    rows = []
    parts = []

    for f in files:
        trade_date = extract_trade_date(f)

        if is_abnormal_trading_date(trade_date):
            continue

        df = pd.read_parquet(f)
        df["trade_date"] = trade_date
        
        rows.append({
            "trade_date": trade_date,
            "file": str(f),
            "rows": len(df),
        })

        parts.append(df)

    if not parts:
        raise FileNotFoundError("No daily greeks_v1_1.parquet files found.")

    out = pd.concat(parts, ignore_index=True)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_FILE, index=False)

    summary = pd.DataFrame(rows)

    lines = []
    lines.append("Combine Daily Greeks v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Daily root: {DAILY_ROOT}")
    lines.append(f"Output file: {OUT_FILE}")
    lines.append("")
    lines.append(f"Daily files: {len(summary)}")
    lines.append(f"Total rows: {len(out)}")
    lines.append(f"Trade dates: {out['trade_date'].nunique()}")
    lines.append("")
    lines.append("Rows by daily file:")
    lines.append(str(summary["rows"].describe()))
    lines.append("")
    lines.append("First / Last dates:")
    lines.append(f"{summary['trade_date'].min()} -> {summary['trade_date'].max()}")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_FILE)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()