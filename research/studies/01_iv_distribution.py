from pathlib import Path

import pandas as pd

from config.paths import PROJECT_ROOT
from analysis.plotting import plot_histogram, plot_boxplot
from analysis.statistics import describe_distribution


# ==========================================
# Paths
# ==========================================

DATA_PATH = (
    PROJECT_ROOT
    / "research"
    / "summaries"
    / "daily_atm_term_structure_2026H1.parquet"
)

EXPORT_DIR = PROJECT_ROOT / "research" / "exports"
REPORT_DIR = PROJECT_ROOT / "research" / "reports"
FIGURE_DIR = PROJECT_ROOT / "research" / "figures"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("Reading dataset...")
    df = pd.read_parquet(DATA_PATH)

    print("Shape:")
    print(df.shape)
    print()

    print("Columns:")
    print(df.columns.tolist())
    print()

    # -------------------------------------------------
    # Select IV column
    # -------------------------------------------------

    iv_candidates = [
        c for c in df.columns
        if "iv" in c.lower()
    ]

    print("Possible IV columns:")
    print(iv_candidates)
    print()

    if len(iv_candidates) == 0:
        raise ValueError("No IV column found.")

    iv_col = "atm_iv_mean"

    if iv_col not in df.columns:
        iv_col = iv_candidates[0]

    print(f"Using IV column: {iv_col}")
    print()

    # -------------------------------------------------
    # Descriptive statistics
    # -------------------------------------------------

    summary = describe_distribution(df[iv_col])

    summary_path = EXPORT_DIR / "iv_distribution_summary.csv"
    summary.to_csv(summary_path, index=False)

    # -------------------------------------------------
    # Figures
    # -------------------------------------------------

    plot_histogram(
        series=df[iv_col],
        title="Daily ATM Implied Volatility Distribution",
        xlabel="ATM Implied Volatility",
        save_path=FIGURE_DIR / "iv_distribution_histogram.png",
        bins=30,
    )

    plot_boxplot(
        series=df[iv_col],
        title="Daily ATM Implied Volatility Box Plot",
        ylabel="ATM Implied Volatility",
        save_path=FIGURE_DIR / "iv_distribution_boxplot.png",
    )

    # -------------------------------------------------
    # Report
    # -------------------------------------------------

    report_path = REPORT_DIR / "iv_distribution_report.txt"

    with open(report_path, "w", encoding="utf-8") as f:

        f.write("Study 01\n")
        f.write("Daily ATM Implied Volatility Distribution\n")
        f.write("=" * 60)
        f.write("\n\n")

        f.write("Dataset\n")
        f.write("-" * 60)
        f.write("\n")
        f.write(f"Source file: {DATA_PATH}\n")
        f.write(f"Shape: {df.shape}\n")
        f.write(f"IV column used: {iv_col}\n")
        f.write("\n")

        f.write("Descriptive Statistics\n")
        f.write("-" * 60)
        f.write("\n")
        f.write(summary.to_string(index=False))
        f.write("\n\n")

        f.write("Figures\n")
        f.write("-" * 60)
        f.write("\n")
        f.write("1. iv_distribution_histogram.png\n")
        f.write("2. iv_distribution_boxplot.png\n")
        f.write("\n")

        f.write("Preliminary Interpretation\n")
        f.write("-" * 60)
        f.write("\n")
        f.write(
            "Daily ATM implied volatility is summarized using mean, median, "
            "standard deviation, selected percentiles, skewness, and kurtosis. "
            "The histogram and box plot are generated to inspect the empirical "
            "distribution, concentration range, and potential outliers.\n"
        )

    print(summary)
    print()
    print(f"Saved summary: {summary_path}")
    print(f"Saved report: {report_path}")
    print("DONE")


if __name__ == "__main__":
    main()