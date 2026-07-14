from pathlib import Path
import pandas as pd


INPUT_FILE = Path("research/datasets/butterfly_dataset_2026H1.parquet")

OUT_DATASET = Path("research/datasets/butterfly_dataset_filtered_2026H1.parquet")
OUT_CSV = Path("research/exports/butterfly_dataset_filtered_preview.csv")
OUT_REPORT = Path("research/reports/butterfly_dataset_filtered_report.txt")


def main():
    print("Reading butterfly dataset...")
    df = pd.read_parquet(INPUT_FILE)

    print("Source shape:")
    print(df.shape)

    filtered = df.copy()

    filtered = filtered[
        (filtered["is_symmetric"] == True)
        & (filtered["butterfly_price"].notna())
        & (filtered["butterfly_price"] > 0)
    ].copy()

    print("Filtered shape:")
    print(filtered.shape)

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    filtered.to_parquet(OUT_DATASET, index=False)
    filtered.head(100000).to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Filtered Long Call Butterfly Dataset Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input file: {INPUT_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Source rows: {len(df)}")
    lines.append(f"Filtered rows: {len(filtered)}")
    lines.append(f"Removed rows: {len(df) - len(filtered)}")
    lines.append(f"Remaining ratio: {len(filtered) / len(df):.2%}")
    lines.append("")
    lines.append("Butterfly price summary:")
    lines.append(str(filtered["butterfly_price"].describe()))
    lines.append("")
    lines.append("Net Greeks summary:")
    lines.append(str(filtered[["net_delta", "net_gamma", "net_vega", "net_theta"]].describe()))
    lines.append("")
    lines.append("Rows by trade_date summary:")
    lines.append(str(filtered.groupby("trade_date").size().describe()))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()