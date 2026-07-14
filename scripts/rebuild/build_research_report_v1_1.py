from pathlib import Path

import pandas as pd

from framework.reporting.word_report import WordReport
from framework.reporting.sections import ReportSections


OUT_DOCX = Path(
    "research/reports/quant_option_research_report_v1_2.docx"
)

NAV_FILE = Path(
    "research/exports/portfolio_nav_timeseries_v1_1.csv"
)

CLEAN_SUMMARY_FILE = Path(
    "research/exports/clean_session_summary_v1_1.csv"
)


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def main():
    nav_df = safe_read_csv(NAV_FILE)
    clean_df = safe_read_csv(CLEAN_SUMMARY_FILE)

    report = WordReport()

    report.title("Quant Option Research Platform")
    report.paragraph("Portfolio Research Report v1.2", bold=True)
    report.paragraph("Research period: 2026-01-02 to 2026-06-10")
    report.paragraph("Author: Jingzhe Yang")
    report.paragraph("")
    report.paragraph(
        "This report summarizes the current research platform, including market data "
        "cleaning, option strategy construction, portfolio PnL, NAV, Greeks monitoring, "
        "risk classification, hedge recommendations, and automated reporting."
    )

    report.page_break()

    ReportSections.executive_summary(
        report=report,
        nav_df=nav_df,
        clean_df=clean_df,
    )

    ReportSections.architecture(
        report=report,
    )

    ReportSections.strategy_overview(
        report=report,
    )

    ReportSections.performance(
        report=report,
        nav_df=nav_df,
    )

    ReportSections.greeks(
        report=report,
        nav_df=nav_df,
    )

    ReportSections.limitations(
        report=report,
    )

    ReportSections.future_work(
        report=report,
    )

    report.save(OUT_DOCX)

    print("DONE")
    print("Saved:")
    print(OUT_DOCX)


if __name__ == "__main__":
    main()