from pathlib import Path

import pandas as pd

from framework.reporting.performance_report import PerformanceReportBuilder


NAV_FILE = Path("research/exports/portfolio_nav_timeseries_v1_1.csv")
OUT_REPORT = Path("research/reports/performance_report_v1_1.txt")


def main():
    nav_df = pd.read_csv(NAV_FILE)

    summary = PerformanceReportBuilder.summarize(nav_df)

    report_text = PerformanceReportBuilder.build_text_report(
        summary=summary,
        nav_df=nav_df,
    )

    PerformanceReportBuilder.write_text_report(
        report_text=report_text,
        path=OUT_REPORT,
    )

    print("DONE")
    print("Saved:")
    print(OUT_REPORT)


if __name__ == "__main__":
    main()