from pathlib import Path
import pandas as pd

DATA_FILE = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet"
)

OUT_DIR = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026\final_view"
)

SAMPLE_N = 100_000

GREEKS = [
    "implied_vol",
    "smoothed_iv",
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Reading dataset...")
    df = pd.read_parquet(DATA_FILE)

    print("Shape:", df.shape)

    print("Creating preview sample...")
    preview = df.head(SAMPLE_N)
    preview.to_csv(
        OUT_DIR / "greeks_preview_100k.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Creating daily row counts...")
    daily = (
        df.groupby("trade_date")
        .size()
        .reset_index(name="row_count")
    )
    daily.to_csv(
        OUT_DIR / "daily_row_counts.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Creating Greeks summary...")
    summary = df[GREEKS].describe().T
    summary.to_csv(
        OUT_DIR / "greeks_summary.csv",
        encoding="utf-8-sig",
    )

    print("Creating columns file...")
    columns = pd.DataFrame({"column": df.columns})
    columns.to_csv(
        OUT_DIR / "columns.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Creating Excel overview...")
    with pd.ExcelWriter(
        OUT_DIR / "final_dataset_overview.xlsx",
        engine="openpyxl",
    ) as writer:
        pd.DataFrame(
            {
                "item": [
                    "dataset",
                    "rows",
                    "columns",
                    "start_date",
                    "end_date",
                    "unique_trade_dates",
                    "excluded_date",
                ],
                "value": [
                    "all_greeks_2026H1.parquet",
                    len(df),
                    df.shape[1],
                    df["trade_date"].min(),
                    df["trade_date"].max(),
                    df["trade_date"].nunique(),
                    "20260505",
                ],
            }
        ).to_excel(writer, sheet_name="Overview", index=False)

        daily.to_excel(writer, sheet_name="Daily Rows", index=False)
        summary.to_excel(writer, sheet_name="Greeks Summary")
        columns.to_excel(writer, sheet_name="Columns", index=False)

        preview.head(5000).to_excel(
            writer,
            sheet_name="Preview 5000",
            index=False,
        )

    print("\nDONE")
    print("Saved to:")
    print(OUT_DIR)


if __name__ == "__main__":
    main()