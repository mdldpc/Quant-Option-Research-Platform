from __future__ import annotations

import pandas as pd

from framework.reporting import charts


class ReportSections:

    @staticmethod
    def executive_summary(
        report,
        nav_df: pd.DataFrame,
        clean_df: pd.DataFrame,
    ):
        report.heading1("1. Executive Summary")

        trading_days = len(nav_df)
        processed_sessions = len(clean_df)

        active_df = nav_df[nav_df["positions"] > 0].copy() if not nav_df.empty else pd.DataFrame()

        final_nav = float(nav_df["current_nav"].iloc[-1]) if not nav_df.empty else 0.0
        max_drawdown = float(nav_df["drawdown"].min()) if not nav_df.empty else 0.0
        active_days = len(active_df)

        summary = pd.DataFrame(
            [
                ["Platform Version", "v1.2"],
                ["Trading Days", trading_days],
                ["Filtered Sessions", processed_sessions],
                ["Active Position Days", active_days],
                ["Strategies", 3],
                ["Framework Modules", 7],
                ["Final NAV", f"{final_nav:,.2f}"],
                ["Max Drawdown", f"{max_drawdown:.4%}"],
                ["Daily Pipeline", "Completed"],
                ["Risk Monitoring", "Completed"],
                ["Research Report", "Completed"],
            ],
            columns=["Item", "Value"],
        )

        report.dataframe(summary)

        report.paragraph()
        report.paragraph(
            "The Quant Option Research Platform has completed a stable research-stage "
            "implementation. The platform supports market-data cleaning, option strategy "
            "construction, portfolio aggregation, PnL and NAV calculation, Greeks monitoring, "
            "risk assessment, hedge recommendation, and automated reporting."
        )

        report.paragraph()
        report.heading2("Key Findings")

        findings = [
            f"The system processed {trading_days} trading days and generated a full portfolio time series.",
            f"The portfolio was active on {active_days} trading days under the current strategy rules.",
            f"The final NAV was {final_nav:,.2f}, with maximum drawdown of {max_drawdown:.4%}.",
            "Risk monitoring successfully classified flat, normal, warning, and critical states.",
            "The current version is suitable as a research platform; production-grade backtesting and execution simulation remain future work.",
        ]

        for item in findings:
            report.bullet(item)

        report.page_break()

    @staticmethod
    def architecture(report):
        report.heading1("2. Platform Architecture")

        report.paragraph(
            "The platform follows a layered architecture. Each module has a narrow "
            "responsibility and can evolve independently."
        )

        arch = pd.DataFrame(
            [
                ["Data", "Data loading, inventory checks, trading-day discovery"],
                ["Market", "Trading sessions and market-data filtering"],
                ["Strategy", "Option strategy construction and registry"],
                ["Portfolio", "PositionBook, PnL engine, NAV engine"],
                ["Risk", "Greeks aggregation, hedge rules, hedge translator"],
                ["Monitoring", "GreekMonitor, PortfolioMonitor, AlertEngine"],
                ["Reporting", "Text, Word, and chart-based reports"],
            ],
            columns=["Framework", "Responsibility"],
        )

        report.dataframe(arch)

        report.page_break()

    @staticmethod
    def strategy_overview(report):
        report.heading1("3. Strategy Overview")

        strategy = pd.DataFrame(
            [
                [
                    "Long ATM Strangle",
                    "Long volatility exposure using near-at-the-money call and put.",
                    "Sensitive to realized movement and implied volatility.",
                ],
                [
                    "Long Call Butterfly",
                    "Defined-risk convexity structure around selected strikes.",
                    "Sensitive to strike selection and underlying path.",
                ],
                [
                    "Calendar Spread",
                    "Term-structure position between near and next expiries.",
                    "Sensitive to IV spread, time decay, and term-structure shifts.",
                ],
            ],
            columns=["Strategy", "Research Objective", "Primary Risk"],
        )

        report.dataframe(strategy)

        report.page_break()

    @staticmethod
    def performance(
        report,
        nav_df: pd.DataFrame,
    ):
        report.heading1("4. Portfolio Performance")

        if nav_df.empty:
            report.paragraph("No portfolio history available.")
            report.page_break()
            return

        df = nav_df.copy().sort_values("trade_date")

        final_nav = float(df["current_nav"].iloc[-1])
        max_nav = float(df["current_nav"].max())
        min_nav = float(df["current_nav"].min())
        total_pnl = float(df["unrealized_pnl"].sum())
        worst_pnl = float(df["unrealized_pnl"].min())
        best_pnl = float(df["unrealized_pnl"].max())
        max_dd = float(df["drawdown"].min())

        perf_summary = pd.DataFrame(
            [
                ["Final NAV", f"{final_nav:,.2f}"],
                ["Highest NAV", f"{max_nav:,.2f}"],
                ["Lowest NAV", f"{min_nav:,.2f}"],
                ["Total Unrealized PnL Sum", f"{total_pnl:,.2f}"],
                ["Best Daily PnL", f"{best_pnl:,.2f}"],
                ["Worst Daily PnL", f"{worst_pnl:,.2f}"],
                ["Maximum Drawdown", f"{max_dd:.4%}"],
            ],
            columns=["Metric", "Value"],
        )

        report.dataframe(perf_summary)

        report.paragraph()
        report.heading2("NAV Curve")
        report.image(charts.draw_nav(df))

        report.heading2("Unrealized PnL")
        report.image(charts.draw_pnl(df))

        report.heading2("Drawdown")
        report.image(charts.draw_drawdown(df))

        report.paragraph()
        report.heading2("Performance Findings")

        findings = [
            f"The final NAV is {final_nav:,.2f}.",
            f"The worst daily unrealized PnL is {worst_pnl:,.2f}.",
            f"The maximum drawdown over the research period is {max_dd:.4%}.",
            "Flat days are included in the time series so the report represents the full trading calendar.",
        ]

        for item in findings:
            report.bullet(item)

        report.page_break()

    @staticmethod
    def greeks(
        report,
        nav_df: pd.DataFrame,
    ):
        report.heading1("5. Risk & Greeks Monitoring")

        if nav_df.empty:
            report.paragraph("No Greeks history available.")
            report.page_break()
            return

        df = nav_df.copy().sort_values("trade_date")

        risk_counts = (
            df["risk_status"]
            .fillna("unknown")
            .value_counts()
            .reindex(["flat", "normal", "warning", "critical"], fill_value=0)
        )

        risk_summary = pd.DataFrame(
            [
                ["Flat Days", int(risk_counts["flat"])],
                ["Normal Days", int(risk_counts["normal"])],
                ["Warning Days", int(risk_counts["warning"])],
                ["Critical Days", int(risk_counts["critical"])],
                ["Max Absolute Delta", f"{df['net_delta'].abs().max():.6f}"],
                ["Max Absolute Vega", f"{df['net_vega'].abs().max():.2f}"],
                ["Max Absolute Theta", f"{df['net_theta'].abs().max():.2f}"],
            ],
            columns=["Metric", "Value"],
        )

        report.dataframe(risk_summary)

        report.paragraph()
        report.heading2("Risk Status Distribution")
        report.image(charts.draw_risk_status(df), width=5.5)

        report.heading2("Net Vega Exposure")
        report.image(charts.draw_vega(df))

        report.heading2("Net Delta Exposure")
        report.image(charts.draw_delta(df))

        report.paragraph()
        report.heading2("Risk Findings")

        findings = [
            f"The platform identified {int(risk_counts['warning'])} warning days and {int(risk_counts['critical'])} critical days.",
            f"The largest absolute Vega exposure was {df['net_vega'].abs().max():.2f}.",
            f"The largest absolute Delta exposure was {df['net_delta'].abs().max():.6f}.",
            "Vega exposure is currently the most important monitored risk dimension for this strategy set.",
            "Hedge recommendations are generated from the same risk engine used by the monitoring layer.",
        ]

        for item in findings:
            report.bullet(item)

        report.page_break()

    @staticmethod
    def limitations(report):
        report.heading1("6. Current Limitations")

        items = [
            "The current dataset only covers 2026 year-to-date.",
            "Strategy signals and open-position windows remain limited under the current rule set.",
            "Transaction costs, slippage, and realistic fill simulation are not fully modeled yet.",
            "Hedge instrument specifications still require empirical calibration.",
            "The report is generated from research-stage outputs and should not be interpreted as production trading performance.",
        ]

        for item in items:
            report.bullet(item)

        report.page_break()

    @staticmethod
    def future_work(report):
        report.heading1("7. Future Work")

        future = [
            "Automatic trade generation across all available trading days.",
            "Historical backtesting engine with complete trade lifecycle.",
            "Execution simulator with bid-ask spread, slippage, and transaction costs.",
            "Empirical hedge calibration using historical Greeks exposure.",
            "Portfolio dashboard with NAV, PnL, Greeks, drawdown, and risk status.",
            "Automatic PDF generation for external review.",
            "GitHub v1.1 release with updated README, architecture documentation, and report artifacts.",
        ]

        for item in future:
            report.bullet(item)

        report.page_break()