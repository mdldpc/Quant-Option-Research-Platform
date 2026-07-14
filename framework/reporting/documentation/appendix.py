import pandas as pd


def build_appendix(report):
    report.heading1("Appendix")

    build_directory(report)
    build_environment(report)
    build_version_history(report)


def build_directory(report):
    report.heading1("Appendix A. Project Directory")

    df = pd.DataFrame(
        [
            ["framework/data", "Data loading and trading-day discovery"],
            ["framework/market", "Trading sessions and filters"],
            ["framework/strategy", "Strategy registry and construction"],
            ["framework/portfolio", "PositionBook, PnL, NAV"],
            ["framework/risk", "Exposure, hedge rules, hedge translator"],
            ["framework/monitoring", "GreekMonitor, PortfolioMonitor, AlertEngine"],
            ["framework/reporting", "Text, Word, charts, documentation builder"],
            ["scripts/rebuild", "Batch rebuild scripts and daily pipeline"],
            ["research/exports", "Generated CSV outputs"],
            ["research/reports", "Generated reports and documentation"],
        ],
        columns=["Path", "Purpose"],
    )

    report.dataframe(df)
    report.page_break()


def build_environment(report):
    report.heading1("Appendix B. Software Environment")

    df = pd.DataFrame(
        [
            ["Operating System", "Windows 11"],
            ["Programming Language", "Python 3.14"],
            ["Data Processing", "Pandas, NumPy, PyArrow"],
            ["Scientific Computing", "SciPy"],
            ["Visualization", "Matplotlib"],
            ["Reporting", "python-docx"],
            ["Version Control", "Git / GitHub"],
        ],
        columns=["Component", "Description"],
    )

    report.dataframe(df)
    report.page_break()


def build_version_history(report):
    report.heading1("Appendix C. Version History")

    df = pd.DataFrame(
        [
            ["v1.0", "Seven-Goal Project Report", "Phase I research foundation"],
            ["v1.1", "Portfolio/Risk Platform", "Portfolio, Greeks, hedge, monitoring"],
            ["v1.2", "Chart Report", "Word report with NAV, PnL, Greeks charts"],
            ["v2.2", "Complete Documentation", "Seven-Goal report plus Phase II addendum"],
            ["v3.0", "Technical White Paper", "Reorganized full documentation architecture"],
        ],
        columns=["Version", "Name", "Description"],
    )

    report.dataframe(df)