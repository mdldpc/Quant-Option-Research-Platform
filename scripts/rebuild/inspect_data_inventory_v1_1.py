from pathlib import Path

from framework.data.trading_days import find_available_trade_dates


SECTIONS = {
    "cleaned_sessions": Path("data/cleaned_sessions"),
    "filtered_sessions": Path("data/filtered_sessions"),
    "research_datasets": Path("research/datasets"),
    "research_exports": Path("research/exports"),
    "research_reports": Path("research/reports"),
}

OUT_REPORT = Path("research/reports/data_inventory_v1_1_report.txt")


def safe_find_dates(path: Path):
    if not path.exists():
        return []
    return find_available_trade_dates(path)


def count_files(path: Path, pattern="*"):
    if not path.exists():
        return 0
    return len(list(path.rglob(pattern)))


def format_dates(dates, max_show=20):
    if not dates:
        return "None"

    shown = dates[:max_show]
    text = ", ".join(str(x) for x in shown)

    if len(dates) > max_show:
        text += f", ... ({len(dates) - max_show} more)"

    return text


def main():
    lines = []

    lines.append("Project Data Inventory v1.1")
    lines.append("=" * 80)
    lines.append("")

    for name, path in SECTIONS.items():
        dates = safe_find_dates(path)

        lines.append(name)
        lines.append("-" * 80)
        lines.append(f"Path        : {path}")
        lines.append(f"Exists      : {path.exists()}")
        lines.append(f"Files       : {count_files(path)}")
        lines.append(f"Parquet     : {count_files(path, '*.parquet')}")
        lines.append(f"CSV         : {count_files(path, '*.csv')}")
        lines.append(f"Reports txt : {count_files(path, '*.txt')}")
        lines.append(f"Trade Dates : {len(dates)}")
        lines.append(f"Dates       : {format_dates(dates)}")
        lines.append("")

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_REPORT)


if __name__ == "__main__":
    main()