from pathlib import Path
import argparse
import pandas as pd

from docx import Document
from docxcompose.composer import Composer

from framework.reporting.word_report import WordReport
from framework.reporting import charts


DEFAULT_BASE_DOCX = Path("research/reports/Seven_Goal_Project_Report_v1.docx")
OUT_ADDENDUM = Path("research/reports/phase_ii_addendum_v2_2.docx")
OUT_FINAL = Path("research/reports/quant_option_complete_documentation_v2_2.docx")

NAV_FILE = Path("research/exports/portfolio_nav_timeseries_v1_1.csv")
CLEAN_SUMMARY_FILE = Path("research/exports/clean_session_summary_v1_1.csv")


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def add_phase_ii_cover(report: WordReport):
    report.title("Phase II Addendum")
    report.paragraph("Portfolio, Risk, Hedge, Monitoring, Calendar Strategy, and Reporting Extension", bold=True)
    report.paragraph("Quant Option Research Platform")
    report.paragraph("Author: Jingzhe Yang")
    report.paragraph("")
    report.paragraph(
        "This addendum extends the original Seven-Goal Project Report. "
        "The Seven-Goal Report is preserved as the Phase I foundation, while this section "
        "documents the additional platform capabilities developed afterward."
    )
    report.page_break()


def add_completion_map(report: WordReport, nav_df: pd.DataFrame, clean_df: pd.DataFrame):
    report.heading1("A1. Phase II Completion Map")

    active_days = int((nav_df["positions"] > 0).sum()) if not nav_df.empty else 0

    df = pd.DataFrame(
        [
            ["Market data cleaning", "Completed", "Auction, lunch break, after-close, invalid quote filtering"],
            ["Greeks monitoring", "Completed", "Delta, Gamma, Vega, Theta exposure tracking"],
            ["Exposure risk monitoring", "Completed", "Normal / warning / critical portfolio state classification"],
            ["Hedge recommendation", "Completed", "Risk rules and executable hedge plan translation"],
            ["Calendar strategy", "Completed", "Calendar spread registered and connected to portfolio/risk layer"],
            ["Additional strategies", "Completed", "Long ATM Strangle and Long Call Butterfly added"],
            ["Portfolio layer", "Completed", "PositionBook, PnL Engine, NAV Engine"],
            ["Daily pipeline", "Completed", "Clean session, portfolio timeseries, performance report"],
            ["Word reporting", "Completed", "Research report and addendum generation"],
        ],
        columns=["Task", "Status", "Details"],
    )

    report.dataframe(df)

    report.paragraph("")
    report.paragraph(f"Filtered sessions available: {len(clean_df)}")
    report.paragraph(f"Portfolio timeseries trading days: {len(nav_df)}")
    report.paragraph(f"Active position days: {active_days}")

    report.page_break()


def add_market_cleaning(report: WordReport, clean_df: pd.DataFrame):
    report.heading1("A2. Market Cleaning and Session Filtering")

    report.paragraph(
        "The market layer was extended to explicitly clean auction-period observations, "
        "lunch-break observations, after-close records, invalid prices, crossed quotes, invalid IV values, "
        "and invalid Greeks. Filtered sessions are stored by trade date."
    )

    if not clean_df.empty:
        built = int((clean_df["status"] == "built").sum()) if "status" in clean_df.columns else len(clean_df)
        skipped = int((clean_df["status"] == "skipped_exists").sum()) if "status" in clean_df.columns else 0

        total_raw = clean_df["raw_rows"].fillna(0).sum() if "raw_rows" in clean_df.columns else 0
        total_clean = clean_df["clean_rows"].fillna(0).sum() if "clean_rows" in clean_df.columns else 0
        removed = total_raw - total_clean

        summary = pd.DataFrame(
            [
                ["Rows processed", len(clean_df)],
                ["Built sessions", built],
                ["Skipped existing sessions", skipped],
                ["Total raw rows", f"{total_raw:,.0f}"],
                ["Total clean rows", f"{total_clean:,.0f}"],
                ["Total removed rows", f"{removed:,.0f}"],
            ],
            columns=["Metric", "Value"],
        )
        report.dataframe(summary)

    report.heading2("Cleaning Rules")
    for item in [
        "Remove call auction observations.",
        "Remove lunch-break observations.",
        "Remove after-close observations.",
        "Remove invalid or crossed quotes.",
        "Remove invalid price, IV, or Greeks observations.",
        "Store cleaned output as parquet files by trade date.",
    ]:
        report.bullet(item)

    report.page_break()


def add_strategy_library(report: WordReport):
    report.heading1("A3. Expanded Strategy Library")

    report.paragraph(
        "The original Seven-Goal Report focused mainly on the prototype volatility signal strategy. "
        "Phase II expanded this into a modular strategy library."
    )

    df = pd.DataFrame(
        [
            ["ATM Straddle / Strangle Prototype", "Original Phase I signal strategy", "Volatility expansion and large movement"],
            ["Long ATM Strangle", "Long near-the-money call and put", "IV contraction and insufficient movement"],
            ["Long Call Butterfly", "Defined-risk convexity around selected strikes", "Path dependence and strike selection"],
            ["Calendar Spread", "Near/next expiry term-structure structure", "IV spread, theta, and term-structure shift"],
        ],
        columns=["Strategy", "Purpose", "Primary Risk"],
    )

    report.dataframe(df)

    report.heading2("Architecture Benefit")
    for item in [
        "Strategies are registered through a unified strategy registry.",
        "Each strategy can define its own constructor, snapshot file, trade output, backtest output, and report path.",
        "Once registered, the strategy can reuse portfolio, risk, monitoring, hedge, and reporting layers.",
        "This makes future strategies such as iron condor, diagonal spread, ratio spread, and volatility arbitrage easier to add.",
    ]:
        report.bullet(item)

    report.page_break()


def add_signal_score_provenance(report: WordReport):
    report.heading1("A4. Signal Score and the Origin of the 80 Threshold")

    report.paragraph(
        "A distinction must be made between the signal score and the threshold value."
    )

    df = pd.DataFrame(
        [
            ["Signal score", "A computed research indicator derived from volatility-related features."],
            ["80", "A threshold applied to the signal score to decide whether the signal is strong enough for entry."],
            ["Interpretation", "If signal_score >= 80, the strategy treats the condition as a high-confidence entry signal."],
        ],
        columns=["Concept", "Meaning"],
    )

    report.dataframe(df)

    report.heading2("Where Does 80 Come From?")

    report.paragraph(
        "The value 80 is not itself calculated from market data. It is a cutoff parameter applied "
        "after the signal score has already been computed. In other words, the workflow is:"
    )

    for item in [
        "First compute signal features such as ATM IV, IV z-score, term-structure slope, and related volatility indicators.",
        "Then combine or normalize these features into a signal score.",
        "Then compare the score against the entry threshold.",
        "The threshold 80 represents the chosen high-confidence cutoff on the signal score scale.",
    ]:
        report.numbered(item)

    report.heading2("Important Methodology Note")

    report.paragraph(
        "To document the exact formula, the implementation file that calculates signal_score must be cited directly. "
        "If the code computes signal_score using percentile rank, z-score scaling, weighted features, or a clipped 0-100 transformation, "
        "that formula should be copied into this section. If no explicit formula exists and 80 was selected manually, the document "
        "must state that 80 is a research threshold parameter rather than a data-derived value."
    )

    report.heading2("Recommended Final Wording")

    report.paragraph(
        "The signal score is computed first from volatility features. The value 80 is the entry threshold, "
        "not the score formula itself. It was selected as a high-confidence cutoff and evaluated through robustness tests "
        "against nearby threshold values. Future versions should calibrate this cutoff using longer historical samples, "
        "transaction-cost-aware backtesting, and walk-forward validation."
    )

    report.page_break()


def add_backtest_and_transaction_cost(report: WordReport):
    report.heading1("A5. Backtesting and Transaction Cost Results")

    report.paragraph(
        "The original Seven-Goal Report included prototype backtesting and robustness analysis. "
        "Those results remain part of the official Phase I evidence and should be interpreted as proof-of-framework rather than production alpha validation."
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

    report.heading2("Transaction Cost and Robustness Analysis")

    tests = pd.DataFrame(
        [
            ["Transaction cost sweep", "Evaluates strategy return sensitivity under different cost assumptions."],
            ["Threshold sensitivity", "Tests performance under alternative entry thresholds."],
            ["Holding-period sensitivity", "Tests robustness to different maximum holding periods."],
            ["Robustness dashboard", "Visualizes how performance changes under parameter variations."],
        ],
        columns=["Test", "Purpose"],
    )
    report.dataframe(tests)

    report.heading2("Interpretation")
    for item in [
        "The strategy prototype generated positive performance within the limited sample.",
        "Transaction cost analysis was considered in Phase I, but production execution assumptions remain incomplete.",
        "The small number of trades means results should be interpreted cautiously.",
        "The main contribution is a reusable backtesting and robustness framework.",
    ]:
        report.bullet(item)

    report.page_break()


def add_portfolio_risk_hedge(report: WordReport, nav_df: pd.DataFrame):
    report.heading1("A6. Portfolio, Greeks Monitoring, Exposure Risk, and Hedge Plan")

    report.paragraph(
        "Phase II added a portfolio operating layer. Strategy outputs are converted into positions, "
        "then monitored through PnL, NAV, Greeks exposure, risk status, alert generation, and hedge recommendation."
    )

    components = pd.DataFrame(
        [
            ["PositionBook", "Maintains current open positions"],
            ["PnLEngine", "Computes position and portfolio unrealized PnL"],
            ["NAVEngine", "Tracks NAV, return, and drawdown"],
            ["ExposureEngine", "Aggregates Delta, Gamma, Vega, and Theta"],
            ["HedgeRules", "Classifies risk and recommends hedge actions"],
            ["HedgeTranslator", "Converts hedge recommendations into executable plan format"],
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


def add_portfolio_performance(report: WordReport, nav_df: pd.DataFrame):
    report.heading1("A7. Portfolio NAV and PnL Monitoring")

    if nav_df.empty:
        report.paragraph("No portfolio NAV time series is available.")
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


def add_automation_and_reporting(report: WordReport):
    report.heading1("A8. Daily Pipeline and Reporting Automation")

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

    for item in [
        "The daily pipeline can regenerate core outputs with one command.",
        "Flat days are included in the NAV and risk time series.",
        "Reports can be regenerated from standardized CSV and parquet outputs.",
        "The reporting framework is designed to support future PDF export and GitHub release artifacts.",
    ]:
        report.bullet(item)

    report.page_break()


def add_future_work(report: WordReport):
    report.heading1("A9. Updated Future Work")

    for item in [
        "Fully document the exact signal_score formula from source code.",
        "Expand historical coverage beyond 2026.",
        "Implement automatic trade generation across all available trading days.",
        "Build a complete backtesting engine with trade lifecycle, costs, slippage, and bid-ask spread.",
        "Calibrate hedge instrument exposure empirically using historical Greeks.",
        "Improve chart formatting and add more presentation-ready visualizations.",
        "Update GitHub with README, project architecture, sample reports, and release notes.",
    ]:
        report.bullet(item)


def build_phase_ii_addendum(path: Path, nav_df: pd.DataFrame, clean_df: pd.DataFrame):
    report = WordReport()

    add_phase_ii_cover(report)
    add_completion_map(report, nav_df, clean_df)
    add_market_cleaning(report, clean_df)
    add_strategy_library(report)
    add_signal_score_provenance(report)
    add_backtest_and_transaction_cost(report)
    add_portfolio_risk_hedge(report, nav_df)
    add_portfolio_performance(report, nav_df)
    add_automation_and_reporting(report)
    add_future_work(report)

    report.save(path)


def merge_docx(base_docx: Path, addendum_docx: Path, output_docx: Path):
    base = Document(str(base_docx))
    composer = Composer(base)

    addendum = Document(str(addendum_docx))
    composer.append(addendum)

    output_docx.parent.mkdir(parents=True, exist_ok=True)
    composer.save(str(output_docx))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base-docx",
        type=str,
        default=str(DEFAULT_BASE_DOCX),
        help="Path to the original Seven-Goal Project Report docx.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=str(OUT_FINAL),
        help="Output merged documentation path.",
    )

    args = parser.parse_args()

    base_docx = Path(args.base_docx)
    output_docx = Path(args.output)

    if not base_docx.exists():
        raise FileNotFoundError(
            f"Base Seven-Goal report not found: {base_docx}. "
            f"Pass the correct path with --base-docx."
        )

    nav_df = safe_read_csv(NAV_FILE)
    clean_df = safe_read_csv(CLEAN_SUMMARY_FILE)

    build_phase_ii_addendum(
        path=OUT_ADDENDUM,
        nav_df=nav_df,
        clean_df=clean_df,
    )

    merge_docx(
        base_docx=base_docx,
        addendum_docx=OUT_ADDENDUM,
        output_docx=output_docx,
    )

    print("DONE")
    print("Saved addendum:")
    print(OUT_ADDENDUM)
    print("Saved final merged document:")
    print(output_docx)


if __name__ == "__main__":
    main()