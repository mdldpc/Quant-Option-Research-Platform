from pathlib import Path
import re
import pandas as pd

from config.data_version import CLEANED_SESSION_DIR


OUT_CSV = Path("research/exports/cleaned_session_inventory_v1_1.csv")
OUT_REPORT = Path("research/reports/cleaned_session_inventory_report_v1_1.txt")


SMALL_FILE_MB_THRESHOLD = 5.0


def extract_date(path: Path) -> int | None:
    m = re.search(r"(\d{8})", path.name)
    if not m:
        return None
    return int(m.group(1))


def main():
    files = sorted(CLEANED_SESSION_DIR.glob("*.session_clean.parquet"))

    rows = []

    for f in files:
        size_mb = f.stat().st_size / 1024 / 1024

        rows.append({
            "file": f.name,
            "trade_date": extract_date(f),
            "size_mb": size_mb,
            "small_file_flag": size_mb < SMALL_FILE_MB_THRESHOLD,
        })

    out = pd.DataFrame(rows).sort_values("trade_date")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Cleaned Session Inventory QC")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input directory: {CLEANED_SESSION_DIR}")
    lines.append(f"Files: {len(out)}")
    lines.append(f"Small file threshold MB: {SMALL_FILE_MB_THRESHOLD}")
    lines.append("")
    lines.append("File size summary:")
    lines.append(str(out["size_mb"].describe()))
    lines.append("")
    lines.append("Small files:")
    small = out[out["small_file_flag"]]
    if small.empty:
        lines.append("None")
    else:
        lines.append(str(small[["trade_date", "file", "size_mb"]]))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()