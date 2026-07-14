from pathlib import Path
import pandas as pd

from framework.reporting.word_report import WordReport
from framework.reporting.sections import ReportSections


OUT_DOCX = Path(
    "research/reports/quant_option_technical_documentation_v2_0.docx"
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


def add_phase_i_overview(report: WordReport):
    report.heading1("1. Phase I Overview: Seven-Goal Research Foundation")

    report.paragraph(
        "Phase I established the original seven-goal research foundation of the "
        "Quant Option Research Platform. The main objective was to build an end-to-end "
        "quantitative option research workflow from raw market data processing to implied "
        "volatility modelling, Greeks calculation, volatility surface construction, strategy "
        "development, backtesting, and robustness analysis."
    )

    goals = pd.DataFrame(
        [
            ["1", "Data Acquisition", "Completed"],
            ["2", "Data Preprocessing", "Completed"],
            ["3", "Data Cleaning", "Completed"],
            ["4", "IV Surface and Term Structure", "Completed"],
            ["5", "Strategy Construction", "Completed"],
            ["6", "Backtesting Framework", "Completed"],
            ["7", "Risk and Robustness Analysis", "Completed"],
        ],
        columns=["Goal", "Objective", "Status"],
    )

    report.dataframe(goals)

    report.paragraph()
    report.paragraph(
        "The completion of Phase I transformed the project from isolated analytical scripts "
        "into a structured research workflow. The outputs from this phase include implied "
        "volatility datasets, Greeks summaries, volatility smile and surface figures, prototype "
        "trading strategies, backtesting outputs, and robustness analysis artifacts."
    )

    report.page_break()


def add_volatility_research(report: WordReport):
    report.heading1("2. Volatility Research")

    report.paragraph(
        "The volatility research layer focuses on implied volatility estimation and the "
        "empirical structure of the option market. Implied volatility is estimated using the "
        "Black-76 framework, with option prices aligned to corresponding futures prices."
    )

    topics = pd.DataFrame(
        [
            [
                "Implied Volatility",
                "Invert option prices into implied volatility using Black-76.",
            ],
            [
                "Volatility Smile",
                "Analyze IV variation across moneyness buckets.",
            ],
            [
                "Volatility Surface",
                "Map IV across strike and maturity dimensions.",
            ],
            [
                "Term Structure",
                "Analyze ATM IV across maturity buckets.",
            ],
            [
                "Greeks",
                "Compute sensitivities such as Delta, Gamma, Vega, Theta, Vanna and Vomma.",
            ],
        ],
        columns=["Research Area", "Description"],
    )

    report.dataframe(topics)

    report.paragraph()
    report.heading2("Key Findings")

    findings = [
        "The volatility smile shows a U-shaped structure, with higher IV in the wings.",
        "Left-tail implied volatility is generally higher, reflecting downside protection demand.",
        "The ATM term structure is generally upward sloping in the available sample.",
        "Short-dated options show stronger distortions and higher sensitivity to market conditions.",
        "These findings provide the empirical foundation for volatility-based strategy research.",
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()


def add_phase_ii_platform(report: WordReport):
    report.heading1("3. Phase II Overview: Platform Extension")

    report.paragraph(
        "Phase II extends the original research workflow into a modular portfolio research "
        "platform. The focus shifts from volatility analytics alone to a complete operating "
        "system for option strategy research, including market-data filtering, strategy registry, "
        "portfolio construction, PnL calculation, NAV tracking, risk monitoring, hedge "
        "recommendation, automated pipelines, and Word-based reporting."
    )

    modules = pd.DataFrame(
        [
            ["Data", "Data loading, trading-day discovery, data inventory"],
            ["Market", "Trading sessions, auction filtering, after-close filtering"],
            ["Strategy", "Strategy registry, trade constructors, backtesters"],
            ["Portfolio", "PositionBook, PnL engine, NAV engine"],
            ["Risk", "Exposure engine, hedge rules, hedge translator"],
            ["Monitoring", "GreekMonitor, PortfolioMonitor, AlertEngine"],
            ["Reporting", "TXT reports, Word reports, charts, reusable sections"],
        ],
        columns=["Framework Layer", "Responsibility"],
    )

    report.dataframe(modules)

    report.page_break()


def add_strategy_library(report: WordReport):
    report.heading1("4. Strategy Library")

    report.paragraph(
        "The current strategy library includes three option structures. These strategies are "
        "registered through a unified strategy registry and can be connected to portfolio, risk, "
        "monitoring, and reporting modules."
    )

    strategies = pd.DataFrame(
        [
            [
                "Long ATM Strangle",
                "Long volatility exposure using near-the-money call and put.",
                "Large movement and IV expansion.",
            ],
            [
                "Long Call Butterfly",
                "Defined-risk convexity structure around selected strikes.",
                "Strike selection and underlying path.",
            ],
            [
                "Calendar Spread",
                "Term-structure trade using near and next expiry options.",
                "IV spread, time decay, and term-structure shifts.",
            ],
        ],
        columns=["Strategy", "Purpose", "Primary Risk"],
    )

    report.dataframe(strategies)

    report.paragraph()
    report.heading2("Strategy Extension Capability")

    extensions = [
        "New strategies can be added through the existing strategy registry.",
        "Each strategy can define its own constructor, snapshot dataset, trade output, backtest output, and report path.",
        "Once registered, the strategy can reuse the existing portfolio, risk, monitoring, and reporting layers.",
        "This design allows future strategies such as iron condor, diagonal spread, ratio spread, and volatility arbitrage structures to be integrated without changing the core platform.",
    ]

    for item in extensions:
        report.bullet(item)

    report.page_break()


def add_portfolio_risk_system(report: WordReport, nav_df: pd.DataFrame):
    report.heading1("5. Portfolio, Risk, and Hedge System")

    report.paragraph(
        "The portfolio layer converts strategy outputs into open positions, computes unrealized "
        "PnL, tracks NAV, aggregates Greeks exposure, classifies portfolio risk, and generates "
        "hedge recommendations."
    )

    components = pd.DataFrame(
        [
            ["PositionBook", "Maintains current open positions"],
            ["PnLEngine", "Computes position-level and portfolio-level unrealized PnL"],
            ["NAVEngine", "Tracks NAV, cumulative return, and drawdown"],
            ["ExposureEngine", "Aggregates Delta, Gamma, Vega, and Theta"],
            ["HedgeRules", "Classifies risk level and recommends hedge actions"],
            ["HedgeTranslator", "Converts risk actions into executable hedge plan format"],
            ["AlertEngine", "Generates warning and critical risk alerts"],
        ],
        columns=["Component", "Function"],
    )

    report.dataframe(components)

    if not nav_df.empty:
        report.paragraph()
        report.heading2("Portfolio Risk Summary")

        risk_counts = (
            nav_df["risk_status"]
            .fillna("unknown")
            .value_counts()
            .reindex(["flat", "normal", "warning", "critical"], fill_value=0)
        )

        risk_summary = pd.DataFrame(
            [
                ["Trading Days", len(nav_df)],
                ["Flat Days", int(risk_counts["flat"])],
                ["Normal Days", int(risk_counts["normal"])],
                ["Warning Days", int(risk_counts["warning"])],
                ["Critical Days", int(risk_counts["critical"])],
                ["Max Absolute Delta", f"{nav_df['net_delta'].abs().max():.6f}"],
                ["Max Absolute Vega", f"{nav_df['net_vega'].abs().max():.2f}"],
                ["Max Absolute Theta", f"{nav_df['net_theta'].abs().max():.2f}"],
            ],
            columns=["Metric", "Value"],
        )

        report.dataframe(risk_summary)

    report.page_break()


def add_automation(report: WordReport):
    report.heading1("6. Research Automation")

    report.paragraph(
        "The platform now supports a daily pipeline runner that executes the main research "
        "workflow automatically. The pipeline builds clean sessions, generates portfolio "
        "time series, and produces performance reports."
    )

    pipeline = pd.DataFrame(
        [
            ["1", "Build Clean Sessions", "Generate filtered session parquet files"],
            ["2", "Build Portfolio Timeseries", "Generate NAV, PnL, Greeks, and risk status history"],
            ["3", "Build Performance Report", "Generate text-based performance summary"],
            ["4", "Build Word Report", "Generate external-facing research documentation"],
        ],
        columns=["Step", "Pipeline Stage", "Output"],
    )

    report.dataframe(pipeline)

    report.paragraph()
    report.heading2("Automation Significance")

    points = [
        "The platform can now process the full available 2026 trading sample.",
        "Flat days are included in NAV and risk time series for full trading-calendar coverage.",
        "Daily reports can be regenerated with a single command.",
        "This architecture supports future GitHub release packaging and reproducible research workflows.",
    ]

    for item in points:
        report.bullet(item)

    report.page_break()


def add_results_summary(report: WordReport, nav_df: pd.DataFrame):
    report.heading1("7. Results Summary")

    if nav_df.empty:
        report.paragraph("No NAV time series is available.")
        report.page_break()
        return

    final_nav = float(nav_df["current_nav"].iloc[-1])
    high_nav = float(nav_df["current_nav"].max())
    low_nav = float(nav_df["current_nav"].min())
    max_dd = float(nav_df["drawdown"].min())
    worst_pnl = float(nav_df["unrealized_pnl"].min())
    best_pnl = float(nav_df["unrealized_pnl"].max())
    active_days = int((nav_df["positions"] > 0).sum())

    summary = pd.DataFrame(
        [
            ["Final NAV", f"{final_nav:,.2f}"],
            ["Highest NAV", f"{high_nav:,.2f}"],
            ["Lowest NAV", f"{low_nav:,.2f}"],
            ["Maximum Drawdown", f"{max_dd:.4%}"],
            ["Best Daily PnL", f"{best_pnl:,.2f}"],
            ["Worst Daily PnL", f"{worst_pnl:,.2f}"],
            ["Active Position Days", active_days],
            ["Total Trading Days", len(nav_df)],
        ],
        columns=["Metric", "Value"],
    )

    report.dataframe(summary)

    report.paragraph()
    report.heading2("Interpretation")

    findings = [
        "The current portfolio results should be interpreted as research-stage output rather than validated production trading performance.",
        "The strategy library successfully connects to the portfolio, risk, monitoring, and reporting layers.",
        "Risk monitoring identifies warning and critical periods, especially when Vega exposure becomes large.",
        "The current active-position sample is still limited, so future backtesting must expand trade generation and execution realism.",
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()


def add_limitations_and_future(report: WordReport):
    report.heading1("8. Limitations and Future Work")

    report.heading2("Current Limitations")

    limitations = [
        "The current sample only covers 2026 year-to-date.",
        "Strategy signal generation and open-position windows are still limited.",
        "Transaction costs, slippage, bid-ask spread, and realistic fill simulation are not fully implemented.",
        "Hedge calibration still relies on placeholder or approximate exposure assumptions.",
        "The current report is research documentation and should not be interpreted as live trading validation.",
    ]

    for item in limitations:
        report.bullet(item)

    report.heading2("Future Development")

    future = [
        "Implement automatic trade generation across all available trading days.",
        "Build a full historical backtesting engine with complete trade lifecycle.",
        "Add execution simulator with transaction costs, slippage, and bid-ask spread.",
        "Calibrate hedge instruments empirically using historical Greeks exposure.",
        "Improve chart formatting and generate presentation-ready PDF reports.",
        "Update GitHub repository with README, documentation, sample outputs, and v1.1 release notes.",
    ]

    for item in future:
        report.bullet(item)

    report.page_break()


def add_appendix(report: WordReport):
    report.heading1("Appendix A. Document Relationship")

    relationship = pd.DataFrame(
        [
            [
                "Seven-Goal Project Report",
                "Phase I research documentation",
                "Data, IV, Greeks, surface, strategy, backtest, robustness",
            ],
            [
                "Portfolio Research Report v1.2",
                "Phase II platform documentation",
                "Portfolio, PnL, NAV, risk, monitoring, reporting",
            ],
            [
                "Technical Documentation v2.0",
                "Unified project documentation",
                "Combines research foundation and platform extension",
            ],
        ],
        columns=["Document", "Role", "Coverage"],
    )

    report.dataframe(relationship)

    report.paragraph()
    report.paragraph(
        "The Technical Documentation v2.0 document should become the main external-facing "
        "project document. Earlier reports remain valuable as milestone documents, while the "
        "technical documentation serves as the unified and continuously updated reference."
    )


def main():
    nav_df = safe_read_csv(NAV_FILE)
    clean_df = safe_read_csv(CLEAN_SUMMARY_FILE)

    report = WordReport()

    report.title("Quant Option Research Platform")
    report.paragraph("Technical Documentation v2.0", bold=True)
    report.paragraph("Integrated Research and Platform Report")
    report.paragraph("Author: Jingzhe Yang")
    report.paragraph("Research period: 2026-01-02 to 2026-06-10")
    report.paragraph("")
    report.paragraph(
        "This document consolidates the Phase I Seven-Goal Project Report and the Phase II "
        "Portfolio Research Report into a unified technical documentation for the Quant Option "
        "Research Platform."
    )

    report.page_break()

    add_phase_i_overview(report)
    add_volatility_research(report)
    add_phase_ii_platform(report)
    add_strategy_library(report)
    add_portfolio_risk_system(report, nav_df)
    add_automation(report)
    add_results_summary(report, nav_df)
    add_limitations_and_future(report)
    add_appendix(report)

    report.save(OUT_DOCX)

    print("DONE")
    print("Saved:")
    print(OUT_DOCX)


if __name__ == "__main__":
    main()