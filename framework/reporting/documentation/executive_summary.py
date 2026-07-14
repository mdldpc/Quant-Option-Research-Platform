from framework.reporting.documentation import tables


def build_executive_summary(report, nav_df, clean_df):
    report.heading1("Executive Summary")

    report.dataframe(
        tables.project_snapshot(
            nav_df=nav_df,
            clean_df=clean_df,
        )
    )

    report.paragraph("")
    report.heading2("Major Contributions")

    items = [
        "Built an end-to-end option research workflow from raw market data to strategy evaluation.",
        "Constructed implied volatility, volatility smile, volatility surface, term structure, and Greeks research outputs.",
        "Implemented market-session cleaning for auction, lunch break, after-close, and invalid observations.",
        "Expanded the strategy layer from a prototype strategy into a modular strategy library.",
        "Built PositionBook, PnL Engine, NAV Engine, Exposure Engine, Risk Monitor, Hedge Translator, and Alert Engine.",
        "Implemented a daily pipeline that processes 107 trading days and generates portfolio time series and reports.",
        "Built a reusable Word-based reporting system for external presentation and future GitHub release.",
    ]

    for item in items:
        report.bullet(item)

    report.page_break()