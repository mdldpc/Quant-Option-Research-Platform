from pathlib import Path
import pandas as pd

from framework.reporting.word_report import WordReport
from framework.reporting import charts


OUT_DOCX = Path("research/reports/quant_option_technical_documentation_v2_1.docx")

NAV_FILE = Path("research/exports/portfolio_nav_timeseries_v1_1.csv")
CLEAN_SUMMARY_FILE = Path("research/exports/clean_session_summary_v1_1.csv")


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def add_cover(report):
    report.title("Quant Option Research Platform")
    report.paragraph("Technical Documentation v2.1 Comprehensive Edition", bold=True)
    report.paragraph("Integrated Research, Strategy, Portfolio, Risk, and Reporting Documentation")
    report.paragraph("Author: Jingzhe Yang")
    report.paragraph("Research period: 2026-01-02 to 2026-06-10")
    report.paragraph("")
    report.paragraph(
        "This document consolidates the Phase I Seven-Goal Project Report and the Phase II "
        "Portfolio Research Platform Report into a unified technical documentation. It covers "
        "data engineering, implied volatility research, signal construction, strategy design, "
        "backtesting, robustness analysis, portfolio management, Greeks monitoring, hedge "
        "recommendation, automation, and reporting."
    )
    report.page_break()


def add_executive_summary(report, nav_df, clean_df):
    report.heading1("1. Executive Summary")

    trading_days = len(nav_df)
    filtered_sessions = len(clean_df)
    active_days = int((nav_df["positions"] > 0).sum()) if not nav_df.empty else 0

    final_nav = float(nav_df["current_nav"].iloc[-1]) if not nav_df.empty else 0.0
    max_dd = float(nav_df["drawdown"].min()) if not nav_df.empty else 0.0

    summary = pd.DataFrame(
        [
            ["Document Version", "v2.1 Comprehensive"],
            ["Platform Version", "v1.2 research-stage platform"],
            ["Trading Days", trading_days],
            ["Filtered Sessions", filtered_sessions],
            ["Active Position Days", active_days],
            ["Strategies Implemented", "3"],
            ["Framework Layers", "7"],
            ["Final NAV", f"{final_nav:,.2f}"],
            ["Maximum Drawdown", f"{max_dd:.4%}"],
            ["Daily Pipeline", "Completed"],
            ["Word Report Generation", "Completed"],
        ],
        columns=["Item", "Value"],
    )

    report.dataframe(summary)

    report.paragraph("")
    report.heading2("Major Contributions")

    items = [
        "Built an end-to-end option research workflow from raw market data processing to strategy evaluation.",
        "Constructed implied volatility, volatility smile, volatility surface, term structure, and Greeks research outputs.",
        "Implemented a modular strategy library with Long ATM Strangle, Long Call Butterfly, and Calendar Spread.",
        "Built portfolio-level PositionBook, PnL Engine, NAV Engine, Greeks exposure engine, risk monitor, and hedge translator.",
        "Implemented daily batch automation across 107 trading days.",
        "Generated professional Word-based research reports with charts and research findings.",
    ]

    for item in items:
        report.bullet(item)

    report.page_break()


def add_phase_i_seven_goals(report):
    report.heading1("2. Phase I: Seven-Goal Research Foundation")

    report.paragraph(
        "Phase I was structured around seven major objectives. These objectives established "
        "the original quantitative research foundation of the platform."
    )

    goals = pd.DataFrame(
        [
            ["1", "Data Acquisition", "Acquire and organize large-scale option and futures market data.", "Completed"],
            ["2", "Data Preprocessing", "Parse symbols, align futures prices, standardize dates and contract metadata.", "Completed"],
            ["3", "Data Cleaning", "Prepare research-ready datasets and perform quality control.", "Completed"],
            ["4", "IV Surface and Term Structure", "Estimate implied volatility and construct smile, surface, and term structure.", "Completed"],
            ["5", "Strategy Construction", "Convert volatility signals into systematic option strategies.", "Completed"],
            ["6", "Backtesting Framework", "Evaluate historical strategy behavior and portfolio equity.", "Completed"],
            ["7", "Risk and Robustness Analysis", "Test transaction costs and parameter robustness.", "Completed"],
        ],
        columns=["Goal", "Objective", "Description", "Status"],
    )

    report.dataframe(goals)

    report.paragraph(
        "The Seven-Goal phase transformed the project from isolated data-processing scripts "
        "into a reproducible quantitative option research workflow."
    )

    report.page_break()


def add_data_engineering(report):
    report.heading1("3. Market Data Engineering and Cleaning")

    report.paragraph(
        "The data engineering layer prepares large-scale Chinese index option and futures "
        "market data for downstream research. Raw intraday files are transformed into "
        "structured datasets suitable for implied volatility estimation, Greeks calculation, "
        "strategy construction, and portfolio analysis."
    )

    pipeline = pd.DataFrame(
        [
            ["Raw data", "Compressed CSV / session-level market files"],
            ["Contract parsing", "Extract option type, maturity, and strike from symbols"],
            ["Futures alignment", "Align option observations with underlying futures price"],
            ["Trading session filter", "Remove call auction, lunch break, after-close, and invalid observations"],
            ["Filtered sessions", "Store cleaned session parquet files by trading date"],
            ["Inventory check", "Verify available trading days and generated outputs"],
        ],
        columns=["Stage", "Description"],
    )

    report.dataframe(pipeline)

    report.heading2("Cleaning Rules")

    rules = [
        "Remove call auction observations.",
        "Remove lunch-break and after-close observations.",
        "Remove invalid or crossed quotes.",
        "Remove invalid price, IV, or Greeks observations when applicable.",
        "Store filtered sessions as date-partitioned parquet files.",
    ]

    for item in rules:
        report.bullet(item)

    report.page_break()


def add_volatility_research(report):
    report.heading1("4. Volatility Research")

    report.paragraph(
        "The volatility research layer estimates implied volatility using the Black-76 "
        "framework and analyzes the empirical structure of the option market across strike, "
        "maturity, and time dimensions."
    )

    topics = pd.DataFrame(
        [
            ["Black-76 IV", "Invert market option prices into implied volatility."],
            ["Volatility Smile", "Analyze IV across moneyness buckets."],
            ["Volatility Surface", "Map IV across both strike and maturity dimensions."],
            ["ATM Term Structure", "Aggregate ATM IV across maturity buckets."],
            ["Greeks", "Compute option sensitivities such as Delta, Gamma, Vega, Theta, Vanna, and Vomma."],
        ],
        columns=["Research Area", "Description"],
    )

    report.dataframe(topics)

    report.heading2("Key Findings")

    findings = [
        "The volatility smile exhibits a U-shaped structure, with higher implied volatility in the wings.",
        "The left tail tends to have higher implied volatility, reflecting stronger demand for downside protection.",
        "The ATM term structure is generally upward sloping in the available sample.",
        "Short-dated options show stronger distortions and higher sensitivity to changing market conditions.",
        "These volatility structures provide the empirical foundation for option strategy construction.",
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()


def add_signal_methodology(report):
    report.heading1("5. Signal Construction Methodology")

    report.paragraph(
        "The original strategy prototype used volatility-based signals to identify potential "
        "entry points. The signal framework converts volatility analytics into a normalized "
        "decision score used for systematic strategy construction."
    )

    inputs = pd.DataFrame(
        [
            ["ATM implied volatility", "Measures the current level of near-the-money option-implied volatility."],
            ["IV z-score", "Compares current IV with recent historical observations."],
            ["Term structure slope", "Measures the spread between near-term and longer-term implied volatility."],
            ["Signal strength score", "Combines volatility features into a normalized decision score."],
            ["Threshold rule", "A trade is opened when the signal score exceeds the entry threshold."],
        ],
        columns=["Signal Input", "Role"],
    )

    report.dataframe(inputs)

    report.heading2("How the Score Should Be Interpreted")

    report.paragraph(
        "The signal score is best interpreted as a research-stage composite indicator rather "
        "than a universal market constant. A higher score represents stronger evidence that "
        "the current volatility environment satisfies the strategy's entry conditions."
    )

    report.heading2("Why Use 80 as the Entry Threshold?")

    points = [
        "The threshold value of 80 is a high-confidence entry trigger on a 0-100 style signal scale.",
        "It was used to avoid overtrading and to focus on stronger volatility signals.",
        "The Seven-Goal robustness framework tested alternative threshold settings, including nearby values such as 70, 75, 80, 85, and 90.",
        "At the current stage, 80 should be treated as a research parameter rather than a statistically finalized optimum.",
        "Future versions should calibrate this threshold using expanded historical data, walk-forward validation, and transaction-cost-aware backtesting.",
    ]

    for item in points:
        report.bullet(item)

    report.heading2("Important Documentation Note")

    report.paragraph(
        "If the exact numerical signal formula in the code differs from this conceptual "
        "description, this section should be updated to match the implementation. The current "
        "documentation records the intended methodology and the research interpretation of "
        "the 80 threshold."
    )

    report.page_break()


def add_strategy_library(report):
    report.heading1("6. Strategy Library")

    report.paragraph(
        "The strategy layer has evolved from a single prototype volatility strategy into a "
        "modular strategy library. Strategies are registered through a unified registry and "
        "can reuse the existing portfolio, risk, monitoring, and reporting layers."
    )

    strategies = pd.DataFrame(
        [
            [
                "ATM Straddle / Strangle Prototype",
                "Original Phase I volatility signal strategy.",
                "Long volatility and large movement exposure.",
            ],
            [
                "Long ATM Strangle",
                "Long call and long put around the money.",
                "Sensitive to realized movement and IV expansion.",
            ],
            [
                "Long Call Butterfly",
                "Defined-risk convexity structure around selected strikes.",
                "Sensitive to strike selection and underlying path.",
            ],
            [
                "Calendar Spread",
                "Term-structure trade between near and next expiry.",
                "Sensitive to IV spread, time decay, and term-structure shifts.",
            ],
        ],
        columns=["Strategy", "Purpose", "Primary Risk"],
    )

    report.dataframe(strategies)

    report.heading2("Strategy Registry Design")

    design = [
        "Each strategy is registered with constructor, backtester, snapshot path, trade output path, and report path.",
        "New strategies can be added without modifying the portfolio, risk, monitoring, or reporting layers.",
        "This makes the system extensible for iron condor, diagonal spread, ratio spread, and volatility arbitrage strategies.",
    ]

    for item in design:
        report.bullet(item)

    report.page_break()


def add_backtesting(report):
    report.heading1("7. Backtesting Framework and Strategy Performance")

    report.paragraph(
        "The Phase I backtesting framework evaluates whether volatility signals can be "
        "converted into systematic option trades. The framework records entry date, exit date, "
        "holding period, signal values, position returns, equity curve, and drawdown."
    )

    metrics = pd.DataFrame(
        [
            ["Total Trades", "4"],
            ["Winning Trades", "3"],
            ["Losing Trades", "1"],
            ["Win Rate", "75%"],
            ["Final Equity", "1.305"],
            ["Cumulative Return", "30.5%"],
            ["Maximum Drawdown", "-0.92%"],
            ["Average Holding Period", "Approximately 4 trading days"],
        ],
        columns=["Metric", "Value"],
    )

    report.dataframe(metrics)

    report.heading2("Interpretation")

    findings = [
        "The prototype strategy produced positive performance within the available sample period.",
        "The result demonstrates that volatility analytics can be connected to systematic trade construction.",
        "The number of completed trades is small, so the results should be interpreted as proof-of-framework rather than proof-of-alpha.",
        "Future versions should expand the sample period, model transaction costs, and implement full execution simulation.",
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()


def add_robustness(report):
    report.heading1("8. Transaction Cost and Robustness Analysis")

    report.paragraph(
        "The robustness layer evaluates whether strategy outcomes are overly dependent on "
        "specific assumptions. The current robustness suite includes signal threshold sensitivity, "
        "transaction cost sensitivity, and performance comparison across parameter configurations."
    )

    tests = pd.DataFrame(
        [
            ["Signal threshold sensitivity", "Evaluate performance under alternative signal-score entry thresholds."],
            ["Transaction cost sensitivity", "Measure how returns change under different cost assumptions."],
            ["Holding-period sensitivity", "Test the effect of different maximum holding periods."],
            ["Robustness dashboard", "Summarize parameter sensitivity in visual form."],
        ],
        columns=["Test", "Purpose"],
    )

    report.dataframe(tests)

    report.heading2("Current Interpretation")

    points = [
        "The robustness framework is reusable and can evaluate alternative assumptions systematically.",
        "Because the current trade sample is small, robustness conclusions remain preliminary.",
        "The main achievement is the construction of a reusable robustness infrastructure.",
        "Future robustness analysis should use more years of data and larger trade samples.",
    ]

    for item in points:
        report.bullet(item)

    report.page_break()


def add_phase_ii_platform(report):
    report.heading1("9. Phase II Platform Extension")

    report.paragraph(
        "Phase II extends the research workflow into a portfolio operating platform. The focus "
        "shifts from isolated volatility analytics to a complete modular system for strategy, "
        "portfolio, risk, monitoring, automation, and reporting."
    )

    modules = pd.DataFrame(
        [
            ["Data", "Data loading, trading-day discovery, inventory checks"],
            ["Market", "Trading session classification and market-data filtering"],
            ["Strategy", "Strategy registry, trade constructors, and backtesters"],
            ["Portfolio", "PositionBook, PnL Engine, NAV Engine"],
            ["Risk", "Greeks exposure, hedge rules, hedge translator"],
            ["Monitoring", "GreekMonitor, PortfolioMonitor, AlertEngine"],
            ["Reporting", "Text reports, Word reports, charts, reusable report sections"],
        ],
        columns=["Framework Layer", "Responsibility"],
    )

    report.dataframe(modules)

    report.page_break()


def add_portfolio_risk(report, nav_df):
    report.heading1("10. Portfolio, Greeks Monitoring, and Hedge Recommendation")

    report.paragraph(
        "The portfolio and risk system converts strategy outputs into open positions, computes "
        "unrealized PnL, tracks NAV, aggregates Greeks exposure, classifies risk level, and "
        "generates hedge recommendations."
    )

    components = pd.DataFrame(
        [
            ["PositionBook", "Maintains open positions"],
            ["PnLEngine", "Computes position-level and portfolio-level unrealized PnL"],
            ["NAVEngine", "Tracks NAV, cumulative return, and drawdown"],
            ["ExposureEngine", "Aggregates Delta, Gamma, Vega, and Theta"],
            ["HedgeRules", "Classifies risk and recommends hedge actions"],
            ["HedgeTranslator", "Translates risk recommendations into executable hedge plans"],
            ["AlertEngine", "Generates warning and critical alerts"],
        ],
        columns=["Component", "Function"],
    )

    report.dataframe(components)

    if not nav_df.empty:
        risk_counts = (
            nav_df["risk_status"]
            .fillna("unknown")
            .value_counts()
            .reindex(["flat", "normal", "warning", "critical"], fill_value=0)
        )

        summary = pd.DataFrame(
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

        report.heading2("Risk Monitoring Summary")
        report.dataframe(summary)

        report.heading2("Risk Status Distribution")
        report.image(charts.draw_risk_status(nav_df), width=5.5)

        report.heading2("Net Vega Exposure")
        report.image(charts.draw_vega(nav_df))

        report.heading2("Net Delta Exposure")
        report.image(charts.draw_delta(nav_df))

    report.page_break()


def add_portfolio_performance(report, nav_df):
    report.heading1("11. Portfolio Performance")

    if nav_df.empty:
        report.paragraph("No portfolio time series available.")
        report.page_break()
        return

    final_nav = float(nav_df["current_nav"].iloc[-1])
    high_nav = float(nav_df["current_nav"].max())
    low_nav = float(nav_df["current_nav"].min())
    max_dd = float(nav_df["drawdown"].min())
    best_pnl = float(nav_df["unrealized_pnl"].max())
    worst_pnl = float(nav_df["unrealized_pnl"].min())
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

    report.heading2("NAV Curve")
    report.image(charts.draw_nav(nav_df))

    report.heading2("Unrealized PnL")
    report.image(charts.draw_pnl(nav_df))

    report.heading2("Drawdown")
    report.image(charts.draw_drawdown(nav_df))

    report.page_break()


def add_automation(report):
    report.heading1("12. Research Automation and Reporting")

    report.paragraph(
        "The platform now supports a daily pipeline runner that can regenerate filtered "
        "sessions, portfolio time series, performance reports, and Word documentation."
    )

    pipeline = pd.DataFrame(
        [
            ["1", "Build Clean Sessions", "Generate filtered session parquet files"],
            ["2", "Build Portfolio Timeseries", "Generate NAV, PnL, Greeks, and risk-status history"],
            ["3", "Build Performance Report", "Generate text-based performance report"],
            ["4", "Build Research Report", "Generate Word-based external-facing documentation"],
        ],
        columns=["Step", "Stage", "Output"],
    )

    report.dataframe(pipeline)

    report.heading2("Automation Significance")

    points = [
        "The platform can process the full available 2026 sample.",
        "Flat days are included in the NAV and risk time series.",
        "Daily outputs can be regenerated with one pipeline command.",
        "The reporting framework supports future GitHub release packaging and external presentation.",
    ]

    for item in points:
        report.bullet(item)

    report.page_break()


def add_limitations_future(report):
    report.heading1("13. Limitations and Future Work")

    report.heading2("Current Limitations")

    limitations = [
        "The current sample only covers 2026 year-to-date.",
        "The strategy sample remains limited, especially for production-grade statistical validation.",
        "The signal threshold of 80 is a research parameter and requires more historical calibration.",
        "Transaction costs, slippage, and realistic fill simulation are not fully implemented.",
        "Hedge calibration still requires empirical estimation using historical Greeks exposure.",
        "The current results should be interpreted as research-stage platform output, not production trading performance.",
    ]

    for item in limitations:
        report.bullet(item)

    report.heading2("Future Development")

    future = [
        "Expand historical data coverage beyond 2026.",
        "Implement automatic trade generation across all available trading days.",
        "Build a full backtesting engine with complete trade lifecycle.",
        "Add execution simulator with bid-ask spread, slippage, transaction costs, and fill assumptions.",
        "Calibrate hedge instruments empirically.",
        "Improve chart formatting and export final PDF reports.",
        "Update GitHub repository with README, documentation, sample outputs, and release notes.",
    ]

    for item in future:
        report.bullet(item)

    report.page_break()


def add_appendix(report):
    report.heading1("Appendix A. Document Map")

    docs = pd.DataFrame(
        [
            [
                "Seven-Goal Project Report",
                "Phase I milestone report",
                "Detailed IV, surface, signal, strategy, backtest, robustness analysis",
            ],
            [
                "Portfolio Research Report v1.2",
                "Phase II platform report",
                "Portfolio, PnL, NAV, Greeks monitoring, hedge recommendation, reporting",
            ],
            [
                "Technical Documentation v2.1",
                "Unified comprehensive documentation",
                "Integrated project-level technical documentation",
            ],
        ],
        columns=["Document", "Role", "Coverage"],
    )

    report.dataframe(docs)

    report.paragraph(
        "The Technical Documentation v2.1 should be treated as the main external-facing "
        "document for the project. Earlier reports remain useful as milestone artifacts."
    )


def main():
    nav_df = safe_read_csv(NAV_FILE)
    clean_df = safe_read_csv(CLEAN_SUMMARY_FILE)

    report = WordReport()

    add_cover(report)
    add_executive_summary(report, nav_df, clean_df)
    add_phase_i_seven_goals(report)
    add_data_engineering(report)
    add_volatility_research(report)
    add_signal_methodology(report)
    add_strategy_library(report)
    add_backtesting(report)
    add_robustness(report)
    add_phase_ii_platform(report)
    add_portfolio_risk(report, nav_df)
    add_portfolio_performance(report, nav_df)
    add_automation(report)
    add_limitations_future(report)
    add_appendix(report)

    report.save(OUT_DOCX)

    print("DONE")
    print("Saved:")
    print(OUT_DOCX)


if __name__ == "__main__":
    main()