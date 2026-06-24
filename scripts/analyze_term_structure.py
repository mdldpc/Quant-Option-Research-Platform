from pathlib import Path
import pandas as pd

SUMMARY_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_iv_summary.parquet"
)

OUT_REPORT = Path(
    r"D:\Quant_Option_Project\research\reports\term_structure_analysis_report.txt"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\term_structure_extreme_days.csv"
)


def main():
    print("Reading daily IV summary...")
    df = pd.read_parquet(SUMMARY_FILE)

    df = df.sort_values("trade_date").copy()

    spread = "next_minus_near_iv_mean"

    print("Shape:")
    print(df.shape)

    total_days = len(df)

    contango_days = (df[spread] > 0).sum()
    backwardation_days = (df[spread] < 0).sum()
    flat_days = (df[spread].abs() <= 0.001).sum()

    print("\nMarket Regime Counts:")
    print("Total days:", total_days)
    print("Contango days:", contango_days)
    print("Backwardation days:", backwardation_days)
    print("Flat days:", flat_days)

    top_contango = df.sort_values(spread, ascending=False).head(10)
    top_backwardation = df.sort_values(spread, ascending=True).head(10)

    high_near_iv = df.sort_values("near_iv_mean", ascending=False).head(10)
    low_near_iv = df.sort_values("near_iv_mean", ascending=True).head(10)

    corr = df[
        [
            "near_iv_mean",
            "next_iv_mean",
            "third_iv_mean",
            spread,
        ]
    ].corr()

    extreme = pd.concat(
        [
            top_contango.assign(category="top_contango"),
            top_backwardation.assign(category="top_backwardation"),
            high_near_iv.assign(category="high_near_iv"),
            low_near_iv.assign(category="low_near_iv"),
        ],
        ignore_index=True,
    )

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    extreme.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []

    lines.append("====================================")
    lines.append("Term Structure Analysis Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {SUMMARY_FILE}")
    lines.append(f"Shape: {df.shape}")
    lines.append("")
    lines.append("Date Range:")
    lines.append(f"{df['trade_date'].min()} - {df['trade_date'].max()}")
    lines.append("")
    lines.append("Market Regime Counts:")
    lines.append(f"Total days: {total_days}")
    lines.append(f"Contango days: {contango_days}")
    lines.append(f"Backwardation days: {backwardation_days}")
    lines.append(f"Flat days: {flat_days}")
    lines.append("")
    lines.append("Market Regime Ratios:")
    lines.append(f"Contango ratio: {contango_days / total_days:.2%}")
    lines.append(f"Backwardation ratio: {backwardation_days / total_days:.2%}")
    lines.append(f"Flat ratio: {flat_days / total_days:.2%}")
    lines.append("")
    lines.append("Average IV Levels:")
    lines.append(str(df[["near_iv_mean", "next_iv_mean", "third_iv_mean"]].mean()))
    lines.append("")
    lines.append("Average Term Spreads:")
    lines.append(
        str(
            df[
                [
                    "next_minus_near_iv_mean",
                    "third_minus_near_iv_mean",
                    "fourth_minus_near_iv_mean",
                ]
            ].mean()
        )
    )
    lines.append("")
    lines.append("Top 10 Contango Days:")
    lines.append(
        str(
            top_contango[
                [
                    "trade_date",
                    "near_iv_mean",
                    "next_iv_mean",
                    "third_iv_mean",
                    spread,
                ]
            ]
        )
    )
    lines.append("")
    lines.append("Top 10 Backwardation Days:")
    lines.append(
        str(
            top_backwardation[
                [
                    "trade_date",
                    "near_iv_mean",
                    "next_iv_mean",
                    "third_iv_mean",
                    spread,
                ]
            ]
        )
    )
    lines.append("")
    lines.append("Top 10 High Near IV Days:")
    lines.append(
        str(
            high_near_iv[
                [
                    "trade_date",
                    "near_iv_mean",
                    "next_iv_mean",
                    "third_iv_mean",
                    spread,
                ]
            ]
        )
    )
    lines.append("")
    lines.append("Top 10 Low Near IV Days:")
    lines.append(
        str(
            low_near_iv[
                [
                    "trade_date",
                    "near_iv_mean",
                    "next_iv_mean",
                    "third_iv_mean",
                    spread,
                ]
            ]
        )
    )
    lines.append("")
    lines.append("Correlation Matrix:")
    lines.append(str(corr))
    lines.append("")
    lines.append("Interpretation Notes:")
    lines.append("- Positive next_minus_near_iv_mean indicates contango.")
    lines.append("- Negative next_minus_near_iv_mean indicates backwardation.")
    lines.append("- Extreme backwardation often appears near expiry or abnormal market conditions.")
    lines.append("- This report is descriptive only and does not define trading rules.")

    OUT_REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved report:")
    print(OUT_REPORT)
    print("Saved extreme days:")
    print(OUT_CSV)

    print("\nSummary:")
    print("Total days:", total_days)
    print("Contango days:", contango_days)
    print("Backwardation days:", backwardation_days)
    print("Flat days:", flat_days)

    print("\nTop Contango:")
    print(top_contango[["trade_date", spread]].head(10))

    print("\nTop Backwardation:")
    print(top_backwardation[["trade_date", spread]].head(10))

    print("\nCorrelation:")
    print(corr)


if __name__ == "__main__":
    main()