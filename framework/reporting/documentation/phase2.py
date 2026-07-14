from framework.reporting.documentation import tables, figures
from framework.reporting.documentation.strategy_registry import get_registry
from framework.reporting.documentation.strategy_card import build_strategy_card

def build_phase2(report, nav_df, clean_df):
    report.heading1("Part II - Quant Research Platform")

    build_architecture(report)
    build_strategy_library(report)
    build_portfolio(report, nav_df)
    build_risk(report, nav_df)
    build_hedge(report)
    build_automation(report)
    build_performance(report, nav_df)
    build_future(report)


def build_architecture(report):
    report.heading1("9. System Architecture")

    layers = [
        ["Data", "Data loading, inventory checks, trading-day discovery"],
        ["Market", "Trading session rules and market-data filtering"],
        ["Strategy", "Strategy registry and trade construction"],
        ["Portfolio", "PositionBook, PnL Engine, NAV Engine"],
        ["Risk", "Greeks exposure, risk rules, hedge translator"],
        ["Monitoring", "GreekMonitor, PortfolioMonitor, AlertEngine"],
        ["Reporting", "Text reports, Word reports, charts, reusable sections"],
    ]

    import pandas as pd
    report.dataframe(pd.DataFrame(layers, columns=["Layer", "Responsibility"]))

    report.page_break()


def build_strategy_library(report):
    report.heading1("10. Expanded Strategy Library")

    registry = get_registry()

    report.paragraph(
        "The strategy layer has evolved from a single prototype volatility strategy into a "
        "structured strategy library. Each strategy is represented as a StrategyRecord, which "
        "contains its research motivation, construction rules, Greeks profile, evidence status, "
        "performance summary, limitations, and future roadmap."
    )

    report.heading2("Strategy Registry Summary")

    report.table(
        dataframe=registry.summary_table(),
        title="Table 10.1 Strategy Registry Summary",
        caption=(
            "Summary of the option strategies currently registered in the platform, "
            "including strategy category, implementation stage, portfolio integration, "
            "risk monitoring, and hedge support."
        ),
    )

    report.paragraph(
        "The registry-based design makes the documentation extensible. Future strategies such "
        "as iron condor, diagonal spread, ratio spread, and volatility arbitrage can be added by "
        "registering a new strategy record instead of rewriting the report builder."
    )

    report.page_break()

    for record in registry.all():
        build_strategy_card(
            report=report,
            record=record,
            performance_rows=registry.performance_for(record),
        )


def build_portfolio(report, nav_df):

    import pandas as pd
    from pathlib import Path


    report.heading1("11. Portfolio Engine")


    report.paragraph(
        "The Portfolio Engine converts strategy-level outputs into portfolio-level "
        "positions, PnL, NAV, and performance statistics. It provides the integration "
        "layer between individual option strategies and portfolio-level monitoring, "
        "risk management, hedge recommendation, and reporting."
    )


    # =========================================================
    # 11.1
    # =========================================================

    report.heading2("11.1 Design Objective")


    objectives = [

        "Convert strategy outputs into standardized portfolio positions.",

        "Track open positions across trading days.",

        "Calculate position-level and portfolio-level PnL.",

        "Maintain NAV, cumulative return, and drawdown history.",

        "Provide portfolio information for risk monitoring.",

        "Support both active trading days and flat days.",

    ]


    for x in objectives:
        report.bullet(x)



    # =========================================================
    # 11.2 Architecture
    # =========================================================


    report.heading2("11.2 Portfolio Architecture")


    report.paragraph(
        "The Portfolio Engine transforms individual strategy signals into a unified "
        "portfolio workflow. Each strategy generates positions, which are standardized "
        "through PositionBook before entering PnL, NAV, risk, hedge, and reporting modules."
    )


    architecture = [

        "Strategy Layer",

        "│",

        "├── Long ATM Strangle",

        "├── Long Call Butterfly",

        "└── Calendar Spread",

        "",

        "↓",

        "",

        "PositionBook",

        "",

        "↓",

        "",

        "PnL Engine",

        "",

        "↓",

        "",

        "NAV Engine",

        "",

        "↓",

        "",

        "Risk Engine",

        "",

        "↓",

        "",

        "Hedge Recommendation",

        "",

        "↓",

        "",

        "Monitoring",

        "",

        "↓",

        "",

        "Research Report",

    ]


    report.code_block("\n".join(architecture))



    # =========================================================
    # 11.3 Components
    # =========================================================


    report.heading2("11.3 Core Components")


    components = pd.DataFrame(

        [

            [
                "PositionBook",
                "Stores standardized open positions and market information."
            ],

            [
                "PnL Engine",
                "Calculates position-level and portfolio-level unrealized PnL."
            ],

            [
                "NAV Engine",
                "Updates account NAV, return, and drawdown."
            ],

            [
                "Risk Engine",
                "Aggregates portfolio Greeks and exposure."
            ],

            [
                "Hedge Engine",
                "Generates risk reduction recommendations."
            ],

            [
                "Reporting Engine",
                "Produces automated research reports."
            ],

        ],

        columns=[
            "Component",
            "Function"
        ]

    )


    report.dataframe(components)



    # =========================================================
    # 11.4 PositionBook
    # =========================================================

    # Prefer the richer PnL file for PositionBook example
    pnl_path = Path("research/exports/portfolio_status_pnl_v1_1.csv")
    position_path = Path("research/exports/portfolio_status_positions_v1_1.csv")

    if pnl_path.exists():
        raw = pd.read_csv(pnl_path)
    elif position_path.exists():
        raw = pd.read_csv(position_path)
    else:
        raw = pd.DataFrame()

    if not raw.empty:
        column_map = {
            "trade_id": "Trade ID",
            "strategy": "Strategy",
            "quantity": "Quantity",
            "entry_price": "Entry Price",
            "current_price": "Current Price",
            "market_value": "Market Value",
            "unrealized_pnl": "Unrealized PnL",
            "unrealized_return": "Unrealized Return",
            "status": "Status",
        }

        available = {k: v for k, v in column_map.items() if k in raw.columns}

        position_table = raw[list(available.keys())].rename(columns=available)

        preferred_order = [
            "Trade ID",
            "Strategy",
            "Quantity",
            "Entry Price",
            "Current Price",
            "Market Value",
            "Unrealized PnL",
            "Unrealized Return",
            "Status",
        ]

        position_table = position_table[
            [c for c in preferred_order if c in position_table.columns]
        ].head(10)

        numeric_columns = [
            "Entry Price",
            "Current Price",
            "Market Value",
            "Unrealized PnL",
            "Unrealized Return",
        ]

        for col in numeric_columns:
            if col in position_table.columns:
                position_table[col] = pd.to_numeric(
                    position_table[col],
                    errors="coerce",
                ).round(4)

    else:
        position_table = pd.DataFrame(
            [
                [1, "Long ATM Strangle", 1, 177.9, 179.3, 179.3, 1.4, 0.0079, "open"],
                [2, "Long Call Butterfly", 1, 4.5, 5.1, 5.1, 0.6, 0.1333, "open"],
                [3, "Calendar Spread", 1, 126.3, 89.4, 89.4, -36.9, -0.2922, "open"],
            ],
            columns=[
                "Trade ID",
                "Strategy",
                "Quantity",
                "Entry Price",
                "Current Price",
                "Market Value",
                "Unrealized PnL",
                "Unrealized Return",
                "Status",
            ],
        )

    report.heading2("11.4 Example PositionBook")

    report.paragraph(
        "The following snapshot illustrates how positions from different strategies "
        "are standardized inside the PositionBook before portfolio-level PnL, NAV, "
        "risk, and hedge calculations are performed."
    )

    report.dataframe(position_table)



    # =========================================================
    # 11.5 Position Lifecycle
    # =========================================================


    report.heading2("11.5 Position Lifecycle")


    lifecycle = [

        "Signal Generation",

        "        │",

        "        ▼",

        "Strategy Construction",

        "        │",

        "        ▼",

        "Position Standardization",

        "        │",

        "        ▼",

        "PositionBook",

        "        │",

        "        ▼",

        "PnL Calculation",

        "        │",

        "        ▼",

        "Risk Aggregation",

        "        │",

        "        ▼",

        "Hedge Recommendation",

        "        │",

        "        ▼",

        "Portfolio Report",

    ]


    report.code_block(
        "\n".join(lifecycle)
    )



    # =========================================================
    # 11.6 PnL
    # =========================================================


    report.heading2("11.6 PnL Engine")


    report.paragraph(

        "The PnL Engine converts position-level market changes into portfolio-level "
        "performance statistics."

    )


    pnl_items = [

        "Position unrealized PnL = quantity × (current price - entry price).",

        "Position return measures performance relative to entry cost.",

        "Portfolio PnL aggregates all open positions.",

        "Current implementation focuses on mark-to-market unrealized PnL."

    ]


    for x in pnl_items:

        report.bullet(x)



    report.heading2("11.6.1 Example PnL Calculation")


    pnl_example = pd.DataFrame(

        [

            [
                "Calendar Spread",

                126.3,

                89.4,

                -36.9

            ]

        ],

        columns=[

            "Strategy",

            "Entry",

            "Current",

            "PnL"

        ]

    )


    report.dataframe(pnl_example)



    # =========================================================
    # 11.7 NAV
    # =========================================================


    report.heading2("11.7 NAV Engine")


    nav_flow = [

        "Initial Capital",

        "      │",

        "      ▼",

        "Portfolio PnL",

        "      │",

        "      ▼",

        "Current NAV",

        "      │",

        "      ▼",

        "Peak NAV",

        "      │",

        "      ▼",

        "Drawdown",

    ]


    report.code_block(
        "\n".join(nav_flow)
    )


    for x in [

        "Current NAV = Initial Capital + Portfolio PnL.",

        "Cumulative return measures NAV growth relative to initial capital.",

        "Drawdown measures decline from historical NAV peak.",

    ]:

        report.bullet(x)



    # =========================================================
    # 11.8 Flat days
    # =========================================================


    report.heading2("11.8 Flat-Day Handling")


    for x in [

        "Flat days represent trading days without active positions.",

        "Including flat days maintains a complete portfolio timeline.",

        "Flat days improve interpretation of return and risk history.",

        "Flat days are classified separately from active portfolio states."

    ]:

        report.bullet(x)



    # =========================================================
    # 11.9 Snapshot
    # =========================================================


    report.heading2("11.9 Portfolio Snapshot")


    if not nav_df.empty:


        snapshot = pd.DataFrame(

            [

                [
                    "Trading Days",
                    len(nav_df)
                ],

                [
                    "Active Days",
                    int((nav_df["positions"] > 0).sum())
                ],

                [
                    "Flat Days",
                    int((nav_df["positions"] == 0).sum())
                ],

                [
                    "Strategies",
                    3
                ],

                [
                    "Latest Risk Status",
                    nav_df.iloc[-1]["risk_status"]
                ],

            ],

            columns=[
                "Metric",
                "Value"
            ]

        )


        report.dataframe(snapshot)



    # =========================================================
    # Finish
    # =========================================================


    report.heading2("11.10 Limitations and Future Work")


    for x in [

        "Realized PnL accounting should be separated from unrealized PnL.",

        "Transaction cost and execution modeling require further integration.",

        "Capital allocation and margin management can be improved.",

        "Future versions should connect Portfolio Engine with automatic execution simulation."

    ]:

        report.bullet(x)


    report.page_break()


def build_risk(report, risk_df):
    import pandas as pd

    report.heading1("12. Greeks and Risk Monitoring")

    report.paragraph(
        "The Risk Engine continuously evaluates portfolio exposure by aggregating "
        "option Greeks across all open positions. Instead of reacting only after "
        "profit and loss have changed, the system identifies potential risks "
        "before large portfolio losses occur. The resulting risk status is then "
        "used by the Hedge Recommendation Engine to determine whether additional "
        "risk reduction actions are required."
    )

    # ==========================================================
    # 12.1 Why Greeks Matter
    # ==========================================================

    report.heading2("12.1 Why Greeks Matter")

    report.paragraph(
        "Portfolio profit and loss is ultimately driven by changes in the "
        "underlying market, implied volatility, and the passage of time. "
        "These effects are summarized by the option Greeks, making Greeks "
        "the fundamental inputs of the portfolio risk monitoring system."
    )

    greek_flow = [
        "Underlying Market",
        "",
        "      │",
        "      ▼",
        "",
        " Option Price Changes",
        "",
        "      │",
        "      ▼",
        "",
        "Delta / Gamma / Vega / Theta",
        "",
        "      │",
        "      ▼",
        "",
        "Portfolio Exposure",
        "",
        "      │",
        "      ▼",
        "",
        "Risk Engine",
    ]

    report.code_block("\n".join(greek_flow))

    greek_table = pd.DataFrame(
        [
            [
                "Delta",
                "Directional exposure",
                "Monitor sensitivity to underlying price movement.",
            ],
            [
                "Gamma",
                "Convexity",
                "Measure how quickly Delta changes as the underlying moves.",
            ],
            [
                "Vega",
                "Volatility exposure",
                "Monitor changes in implied volatility.",
            ],
            [
                "Theta",
                "Time decay",
                "Measure portfolio value erosion through time.",
            ],
        ],
        columns=[
            "Greek",
            "Primary Risk",
            "Role in Portfolio",
        ],
    )

    report.dataframe(greek_table)

    report.paragraph(
        "Although profit and loss is the final outcome observed by investors, "
        "Greeks provide earlier indications of changing portfolio risk. The "
        "Risk Engine therefore monitors Greeks continuously instead of waiting "
        "for realized losses to occur."
    )

    # ==========================================================
    # 12.2 Portfolio Greeks Aggregation
    # ==========================================================

    report.heading2("12.2 Portfolio Greeks Aggregation")

    report.paragraph(
        "Each individual option strategy contributes its own Greeks to the "
        "overall portfolio. The Portfolio Engine aggregates these exposures "
        "across all open positions before risk classification is performed."
    )

    aggregation = [
        "Individual Strategy Greeks",
        "",
        "ATM Strangle",
        "Δ Γ V Θ",
        "",
        "Butterfly",
        "Δ Γ V Θ",
        "",
        "Calendar Spread",
        "Δ Γ V Θ",
        "",
        "      │",
        "      ▼",
        "",
        "Portfolio Greeks",
        "",
        "      │",
        "      ▼",
        "",
        "Risk Classification",
    ]

    report.code_block("\n".join(aggregation))

    report.paragraph(
        "Portfolio Greeks are computed as the sum of the position-level Greeks. "
        "Each position contributes according to its quantity and exposure."
    )

    aggregation_table = pd.DataFrame(
        [
            ["Portfolio Delta", "Σ Position Delta"],
            ["Portfolio Gamma", "Σ Position Gamma"],
            ["Portfolio Vega", "Σ Position Vega"],
            ["Portfolio Theta", "Σ Position Theta"],
        ],
        columns=[
            "Portfolio Metric",
            "Aggregation Rule",
        ],
    )

    report.dataframe(aggregation_table)

    report.paragraph(
        "Aggregated Greeks provide a concise description of the overall portfolio "
        "risk profile and form the direct inputs of the Risk Engine."
    )

    # ==========================================================
    # 12.3 Risk Threshold Framework
    # ==========================================================

    report.heading2("12.3 Risk Threshold Framework")

    report.paragraph(
        "After portfolio Greeks have been aggregated, each exposure is compared "
        "against predefined portfolio risk limits. The monitoring framework "
        "determines whether the current exposure remains acceptable or whether "
        "additional attention is required."
    )

    threshold_flow = [
        "Portfolio Greeks",
        "",
        "      │",
        "      ▼",
        "",
        "Threshold Evaluation",
        "",
        "      │",
        "      ▼",
        "",
        "Risk Classification",
        "",
        "      │",
        "      ▼",
        "",
        "Normal / Warning / Critical",
    ]

    report.code_block("\n".join(threshold_flow))

    report.paragraph(
        "This threshold-based framework enables the platform to detect excessive "
        "risk before large portfolio losses materialize."
    )

    # ==========================================================
    # 12.4 Risk Classification Logic
    # ==========================================================

    report.heading2("12.4 Risk Classification Logic")

    report.paragraph(
        "The portfolio risk state is determined according to the aggregated "
        "Greek exposures. Individual Greeks are evaluated first, after which "
        "an overall portfolio risk status is assigned."
    )

    classification = [
        "Exposure Within Limits",
        "",
        "      │",
        "      ▼",
        "",
        "NORMAL",
        "",
        "      │",
        "Threshold Breached",
        "      ▼",
        "",
        "WARNING",
        "",
        "      │",
        "Large Exposure",
        "      ▼",
        "",
        "CRITICAL",
    ]

    report.code_block("\n".join(classification))

    classification_table = pd.DataFrame(
        [
            [
                "Normal",
                "Portfolio Greeks remain within acceptable limits.",
            ],
            [
                "Warning",
                "One or more portfolio exposures approach predefined limits.",
            ],
            [
                "Critical",
                "Portfolio exposure exceeds acceptable limits and immediate risk mitigation should be considered.",
            ],
        ],
        columns=[
            "Risk Status",
            "Interpretation",
        ],
    )

    report.dataframe(classification_table)

    report.paragraph(
        "The assigned risk status becomes the direct input to the Hedge "
        "Recommendation Engine described in the following chapter."
    )

        # ==========================================================
    # 12.5 Historical Risk Behaviour
    # ==========================================================

    report.heading2("12.5 Historical Risk Behaviour")

    report.paragraph(
        "The portfolio risk profile evolves over time as positions are opened, "
        "closed, and marked to market. Historical monitoring allows the research "
        "platform to identify periods of elevated exposure and evaluate how "
        "portfolio risk changes throughout the sample."
    )

    if risk_df.empty:

        report.paragraph(
            "Historical risk data are currently unavailable."
        )

    else:

        summary = pd.DataFrame(

            [

                [
                    "Trading Days",
                    len(risk_df)
                ],

                [
                    "Normal Days",
                    int((risk_df["risk_status"] == "normal").sum())
                ],

                [
                    "Warning Days",
                    int((risk_df["risk_status"] == "warning").sum())
                ],

                [
                    "Critical Days",
                    int((risk_df["risk_status"] == "critical").sum())
                ],

            ],

            columns=[
                "Metric",
                "Value"
            ]

        )

        report.dataframe(summary)

    report.paragraph(
        "Historical risk monitoring provides a higher-level view of portfolio "
        "stability than individual daily observations."
    )



    # ==========================================================
    # 12.6 Risk Dashboard
    # ==========================================================

    report.heading2("12.6 Portfolio Risk Dashboard")

    report.paragraph(
        "The portfolio dashboard summarizes the major sources of risk currently "
        "being monitored by the platform."
    )

    dashboard = pd.DataFrame(

        [

            [
                "Direction",
                "Net Delta",
                "Continuously monitored"
            ],

            [
                "Convexity",
                "Net Gamma",
                "Continuously monitored"
            ],

            [
                "Volatility",
                "Net Vega",
                "Continuously monitored"
            ],

            [
                "Time Decay",
                "Net Theta",
                "Continuously monitored"
            ],

            [
                "Overall Status",
                "Risk Status",
                "Normal / Warning / Critical"
            ],

        ],

        columns=[
            "Risk Category",
            "Metric",
            "Monitoring"
        ]

    )

    report.dataframe(dashboard)

    report.paragraph(
        "The dashboard serves as the operational interface between the Portfolio "
        "Engine and the Risk Engine."
    )



    # ==========================================================
    # 12.7 Risk Case Study
    # ==========================================================

    report.heading2("12.7 Risk Case Study")

    report.paragraph(
        "The following example illustrates how portfolio Greeks are translated "
        "into an overall portfolio risk assessment."
    )

    case_table = pd.DataFrame(

        [

            [
                "Net Vega",
                "-993.32",
                "Large short volatility exposure"
            ],

            [
                "Net Delta",
                "0.033",
                "Nearly direction neutral"
            ],

            [
                "Net Gamma",
                "0.0013",
                "Limited convexity exposure"
            ],

            [
                "Net Theta",
                "-365.22",
                "Time decay remains significant"
            ],

            [
                "Risk Status",
                "Warning",
                "Further monitoring recommended"
            ],

        ],

        columns=[
            "Metric",
            "Observed Value",
            "Interpretation"
        ]

    )

    report.dataframe(case_table)

    report.paragraph(
        "Rather than relying solely on portfolio profit and loss, the Risk "
        "Engine identifies which specific Greek is responsible for the current "
        "portfolio risk profile."
    )



    # ==========================================================
    # 12.8 Link to Hedge Recommendation
    # ==========================================================

    report.heading2("12.8 Connection to Hedge Recommendation")

    hedge_flow = [

        "Portfolio Greeks",

        "",

        "      │",

        "      ▼",

        "",

        "Risk Aggregation",

        "",

        "      │",

        "      ▼",

        "",

        "Risk Classification",

        "",

        "      │",

        "      ▼",

        "",

        "Hedge Recommendation",

        "",

        "      │",

        "      ▼",

        "",

        "Portfolio Adjustment",

    ]

    report.code_block(
        "\n".join(hedge_flow)
    )

    report.paragraph(
        "Risk monitoring does not directly modify portfolio positions. Instead, "
        "it provides standardized exposure information to the Hedge Recommendation "
        "Engine, which determines whether hedging actions are required."
    )



    # ==========================================================
    # Existing Charts
    # ==========================================================

    report.heading2("12.9 Historical Charts")

    report.paragraph(
        "The following figures summarize the historical evolution of portfolio "
        "risk exposures during the current research sample."
    )

    if not risk_df.empty:
        report.heading2("12.9.1 Risk Summary")

        report.dataframe(tables.risk_summary(risk_df))

        report.figure(
            image=figures.risk_status_bar(risk_df),
            title="Figure 12.1 Portfolio Risk Status Distribution",
            caption=(
                "Distribution of daily portfolio risk classifications across the "
                "research sample. Each trading day is categorized as Normal, Warning, "
                "or Critical according to the predefined portfolio exposure thresholds."
            ),
            width=5.5,
        )

        report.figure(
            image=figures.vega_curve(risk_df),
            title="Figure 12.2 Portfolio Net Vega Exposure",
            caption=(
                "Historical evolution of aggregate portfolio Vega. Positive values "
                "indicate increasing sensitivity to implied volatility, while negative "
                "values represent short-volatility exposure."
            ),
            width=6.5,
        )

        report.figure(
            image=figures.delta_curve(risk_df),
            title="Figure 12.3 Portfolio Net Delta Exposure",
            caption=(
                "Historical aggregate portfolio Delta. The chart summarizes directional "
                "market exposure throughout the research period and provides an indication "
                "of overall directional neutrality."
            ),
            width=6.5,
        )
    else:
        report.paragraph("No historical risk chart data are currently available.")

    report.page_break()


def build_hedge(report):
    report.heading1("13. Hedge Recommendation")

    report.paragraph(
        "The Hedge Recommendation Engine provides decision support for portfolio "
        "risk management. Instead of automatically executing trades, the current "
        "research platform evaluates portfolio exposures, identifies significant "
        "risk sources, and recommends appropriate hedge actions to the portfolio "
        "manager. This modular architecture separates strategy generation, "
        "portfolio management, risk monitoring, and hedge decision making into "
        "independent components."
    )

    report.heading2("13.1 Design Objectives")

    objectives = [

        "Translate portfolio risk exposures into actionable hedge recommendations.",

        "Reduce excessive directional, volatility, and time-decay risk.",

        "Provide transparent and repeatable rule-based hedge logic.",

        "Support research workflows without automatic trade execution.",

        "Prepare the platform for future optimization-based hedge engines.",

    ]

    for item in objectives:
        report.bullet(item)

    report.heading2("13.2 Why Hedge Recommendation?")

    report.paragraph(
        "The current platform focuses on quantitative research rather than live "
        "execution. Hedge outputs are therefore generated as recommendations "
        "instead of automatic trades. Researchers remain responsible for "
        "reviewing portfolio exposures before any execution takes place."
    )
    
    import pandas as pd

    status = pd.DataFrame(

        [

            ["Research Stage", "Rule-based recommendation"],

            ["Trade Execution", "Manual"],

            ["Risk Review", "Human validation"],

            ["Future Direction", "Automatic execution engine"],

        ],

        columns=[
            "Component",
            "Current Status",
        ],

    )

    report.dataframe(status)

    report.heading2("13.3 Hedge Decision Pipeline")

    pipeline = [

        "Portfolio Greeks",

        "",

        "      │",

        "      ▼",

        "",

        "Risk Aggregation",

        "",

        "      │",

        "      ▼",

        "",

        "Risk Classification",

        "",

        "      │",

        "      ▼",

        "",

        "Rule Engine",

        "",

        "      │",

        "      ▼",

        "",

        "Hedge Recommendation",

        "",

        "      │",

        "      ▼",

        "",

        "Trader Decision",

    ]

    report.code_block(
        "\n".join(pipeline)
    )

    report.paragraph(
        "The Hedge Recommendation Engine receives standardized portfolio risk "
        "information from the Risk Engine. Rule-based logic then evaluates "
        "portfolio exposures and generates appropriate hedge suggestions."
    )

    report.heading2("13.4 Exposure-to-Hedge Translation")

    translation = pd.DataFrame(

        [

            [

                "Large Positive Delta",

                "Directional Risk",

                "Sell Index Futures",

            ],

            [

                "Large Negative Delta",

                "Directional Risk",

                "Buy Index Futures",

            ],

            [

                "Large Negative Vega",

                "Volatility Risk",

                "Buy Volatility Exposure",

            ],

            [

                "Large Positive Vega",

                "Volatility Risk",

                "Reduce Long Volatility",

            ],

            [

                "Large Negative Theta",

                "Time Decay",

                "Reduce Long Premium Positions",

            ],

            [

                "Large Gamma",

                "Convexity",

                "Adjust Position Structure",

            ],

        ],

        columns=[

            "Observed Exposure",

            "Primary Risk",

            "Suggested Hedge",

        ],

    )

    report.dataframe(translation)    

    # ==========================================================
    # 13.5 Rule-Based Decision Engine
    # ==========================================================

    report.heading2("13.5 Rule-Based Decision Engine")

    report.paragraph(
        "The current Hedge Recommendation Engine uses transparent rule-based logic. "
        "Each portfolio exposure is evaluated against the corresponding risk status, "
        "then converted into a suggested hedge action if the exposure is material."
    )

    rule_flow = [
        "Portfolio Exposure",
        "      │",
        "      ▼",
        "Risk Level Check",
        "      │",
        "      ▼",
        "Rule Match",
        "      │",
        "      ▼",
        "Hedge Action",
        "      │",
        "      ▼",
        "Recommendation Output",
    ]

    report.code_block("\n".join(rule_flow))

    rule_table = pd.DataFrame(
        [
            [
                "Delta normal",
                "No action",
                "Directional exposure is within threshold.",
            ],
            [
                "Delta warning / critical",
                "Futures hedge",
                "Use index futures to reduce directional exposure.",
            ],
            [
                "Vega warning / critical",
                "Volatility hedge",
                "Use option structures to reduce excessive volatility exposure.",
            ],
            [
                "Gamma warning / critical",
                "Structure adjustment",
                "Reduce convexity concentration or rebalance option structures.",
            ],
            [
                "Theta warning / critical",
                "Premium reduction",
                "Reduce positions with excessive time decay.",
            ],
        ],
        columns=[
            "Condition",
            "Recommendation",
            "Reason",
        ],
    )

    report.dataframe(rule_table)

    # ==========================================================
    # 13.6 Example Hedge Decisions
    # ==========================================================

    report.heading2("13.6 Example Hedge Decisions")

    report.paragraph(
        "The following examples illustrate how the rule-based Hedge Recommendation "
        "Engine translates observed portfolio risk into decision-support outputs."
    )

    examples = pd.DataFrame(
        [
            [
                "Net Delta",
                "0.033",
                "Normal",
                "No action",
                "Directional exposure is small.",
            ],
            [
                "Net Vega",
                "-993.32",
                "Warning",
                "Monitor / reduce short Vega",
                "Large negative Vega indicates sensitivity to volatility increase.",
            ],
            [
                "Net Theta",
                "-365.22",
                "Warning",
                "Monitor time decay",
                "Negative Theta indicates ongoing premium decay.",
            ],
            [
                "Net Gamma",
                "0.0013",
                "Normal",
                "No action",
                "Convexity exposure is limited.",
            ],
        ],
        columns=[
            "Risk Metric",
            "Observed Value",
            "Risk Level",
            "Recommendation",
            "Explanation",
        ],
    )

    report.dataframe(examples)

    report.paragraph(
        "These examples are advisory. The current platform does not execute hedge "
        "transactions automatically; instead, it provides structured recommendations "
        "for human review."
    )

    # ==========================================================
    # 13.7 Current Limitations
    # ==========================================================

    report.heading2("13.7 Current Limitations")

    for item in [
        "Hedge recommendations are rule-based rather than optimization-based.",
        "Hedge sizing is approximate and not yet calibrated with transaction costs.",
        "Execution simulation is not yet implemented.",
        "Bid-ask spread, slippage, and liquidity constraints are not fully modeled.",
        "The current engine provides decision support rather than automatic execution.",
    ]:
        report.bullet(item)

    # ==========================================================
    # 13.8 Future Automatic Hedge Engine
    # ==========================================================

    report.heading2("13.8 Future Automatic Hedge Engine")

    roadmap = [
        "Current Stage",
        "Rule-Based Recommendation",
        "",
        "      │",
        "      ▼",
        "",
        "Optimization-Based Hedge Sizing",
        "",
        "      │",
        "      ▼",
        "",
        "Transaction-Cost-Aware Hedge Selection",
        "",
        "      │",
        "      ▼",
        "",
        "Execution Simulation",
        "",
        "      │",
        "      ▼",
        "",
        "Automatic Hedge Engine",
    ]

    report.code_block("\n".join(roadmap))

    report.paragraph(
        "The long-term objective is to evolve the current rule-based recommendation "
        "system into an optimization-based hedge engine that accounts for transaction "
        "costs, liquidity, hedge effectiveness, and portfolio constraints."
    )

    report.page_break()


def build_automation(report):

    import pandas as pd

    report.heading1("14. Automation and Reporting")

    report.paragraph(
        "The Automation Framework integrates all major components of the Quant "
        "Option Research Platform into a standardized daily workflow. Instead "
        "of manually executing individual scripts, the platform performs data "
        "cleaning, strategy generation, portfolio management, risk monitoring, "
        "hedge recommendation, and report generation through a reproducible "
        "pipeline."
    )

    # ==========================================================
    # 14.1 Design Objective
    # ==========================================================

    report.heading2("14.1 Design Objective")

    objectives = [

        "Automate the complete daily research workflow.",

        "Reduce manual intervention during data processing.",

        "Generate reproducible research outputs.",

        "Support daily portfolio monitoring.",

        "Prepare the platform for future scheduled execution.",

    ]

    for item in objectives:
        report.bullet(item)

    # ==========================================================
    # 14.2 Daily Pipeline Architecture
    # ==========================================================

    report.heading2("14.2 Daily Pipeline Architecture")

    pipeline = [

        "Market Data",

        "",

        "      │",

        "      ▼",

        "",

        "Session Cleaning",

        "",

        "      │",

        "      ▼",

        "",

        "Strategy Engine",

        "",

        "      │",

        "      ▼",

        "",

        "Portfolio Engine",

        "",

        "      │",

        "      ▼",

        "",

        "Risk Engine",

        "",

        "      │",

        "      ▼",

        "",

        "Hedge Recommendation",

        "",

        "      │",

        "      ▼",

        "",

        "Automated Reports",

    ]

    report.code_block("\n".join(pipeline))

    report.paragraph(
        "Each module produces standardized outputs that become the inputs of "
        "the following stage. This modular architecture improves reproducibility, "
        "maintainability, and future extensibility."
    )

    # ==========================================================
    # 14.3 End-to-End Workflow
    # ==========================================================

    report.heading2("14.3 End-to-End Workflow")

    workflow = pd.DataFrame(

        [

            ["1", "Market Data", "Load option and futures market data"],

            ["2", "Cleaning", "Filter auction, lunch-break and abnormal observations"],

            ["3", "Strategy", "Generate option trading signals"],

            ["4", "Portfolio", "Update PositionBook, NAV and PnL"],

            ["5", "Risk", "Aggregate Greeks and classify portfolio risk"],

            ["6", "Hedge", "Generate hedge recommendations"],

            ["7", "Reporting", "Generate Word documentation and research reports"],

        ],

        columns=[

            "Stage",

            "Module",

            "Main Output",

        ],

    )

    report.dataframe(workflow)

    report.paragraph(
        "The workflow guarantees that every research report is generated from "
        "the same deterministic sequence of processing steps."
    )

    # ==========================================================
    # 14.4 Automated Report Generation
    # ==========================================================

    report.heading2("14.4 Automated Report Generation")

    report.paragraph(
        "The reporting subsystem automatically converts portfolio statistics, "
        "risk metrics, strategy descriptions, tables, and figures into a "
        "publication-quality technical report. The same reporting framework "
        "supports academic research, management reporting, and GitHub "
        "documentation."
    )

    report.code_block(
"""
Daily Pipeline

      │

      ▼

CSV / Parquet

      │

      ▼

Portfolio Statistics

      │

      ▼

Word Builder

      │

      ▼

Technical White Paper
"""
    )

    # ==========================================================
    # 14.5 Current Automation Functions
    # ==========================================================

    report.heading2("14.5 Current Automation Functions")

    automation = pd.DataFrame(

        [

            [

                "Daily Pipeline",

                "Automatically rebuild clean sessions",

            ],

            [

                "Portfolio Engine",

                "Update NAV, PnL and portfolio status",

            ],

            [

                "Risk Engine",

                "Generate daily portfolio risk statistics",

            ],

            [

                "Reporting",

                "Generate Word technical documentation",

            ],

            [

                "Research Export",

                "Export CSV and Parquet datasets",

            ],

        ],

        columns=[

            "Module",

            "Current Function",

        ],

    )

    report.dataframe(automation)

    report.paragraph(
        "These automation modules eliminate repetitive manual processing while "
        "ensuring that all intermediate datasets remain reproducible."
    )

    # ==========================================================
    # 14.6 Reproducibility
    # ==========================================================

    report.heading2("14.6 Reproducibility")

    reproducibility = [

        "Each processing stage produces standardized intermediate outputs.",

        "Portfolio statistics are generated deterministically from cleaned datasets.",

        "Research reports are rebuilt automatically from the latest outputs.",

        "All processing modules are designed to be repeatable using identical inputs.",

    ]

    for item in reproducibility:
        report.bullet(item)

    # ==========================================================
    # 14.7 Future Production Deployment
    # ==========================================================

    report.heading2("14.7 Future Production Deployment")

    roadmap = [

        "Current Research Platform",

        "",

        "      │",

        "      ▼",

        "",

        "Scheduled Daily Execution",

        "",

        "      │",

        "      ▼",

        "",

        "Cloud Deployment",

        "",

        "      │",

        "      ▼",

        "",

        "Automatic Monitoring",

        "",

        "      │",

        "      ▼",

        "",

        "Production Quant Platform",

    ]

    report.code_block("\n".join(roadmap))

    report.paragraph(
        "Future work will integrate task scheduling, cloud deployment, "
        "automatic monitoring, and execution infrastructure, allowing the "
        "research platform to evolve into a production-ready quantitative "
        "research system."
    )

    report.page_break()


def build_performance(report, nav_df):
    import pandas as pd

    report.heading1("15. Portfolio Performance")

    if nav_df.empty:
        report.paragraph("No portfolio time series available.")
        report.page_break()
        return

    # ==========================================================
    # 15.1 Evaluation Objective
    # ==========================================================

    report.heading2("15.1 Evaluation Objective")

    report.paragraph(
        "This chapter evaluates the observed performance of the portfolio-level "
        "research platform. The objective is not to claim final strategy profitability, "
        "but to summarize how the current strategy, portfolio, risk, hedge, and "
        "automation modules behave when they are run together on the available "
        "2026 research sample."
    )

    for item in [
        "Measure NAV stability across the available trading calendar.",
        "Evaluate unrealized PnL behaviour from active portfolio positions.",
        "Measure drawdown and downside pressure.",
        "Summarize active versus flat portfolio periods.",
        "Provide a research-stage interpretation of the current platform output.",
    ]:
        report.bullet(item)

    # ==========================================================
    # 15.2 Performance Dashboard
    # ==========================================================

    report.heading2("15.2 Performance Dashboard")

    report.dataframe(tables.portfolio_summary(nav_df))

    total_days = len(nav_df)
    active_days = int((nav_df["positions"] > 0).sum()) if "positions" in nav_df.columns else 0
    flat_days = total_days - active_days

    dashboard = pd.DataFrame(
        [
            ["Total Trading Days", total_days],
            ["Active Position Days", active_days],
            ["Flat Days", flat_days],
            ["Activity Ratio", f"{active_days / total_days:.2%}" if total_days else "N/A"],
            ["Evaluation Status", "Research-stage platform evaluation"],
        ],
        columns=["Metric", "Value"],
    )

    report.dataframe(dashboard)

    report.paragraph(
        "The dashboard shows that the current platform processes the full trading "
        "calendar while only holding active positions on a subset of days. This is "
        "consistent with a signal-driven option research framework."
    )

    # ==========================================================
    # 15.3 NAV Analysis
    # ==========================================================

    report.heading2("15.3 NAV Analysis")

    report.paragraph(
        "The NAV curve measures the portfolio-level account value after incorporating "
        "the mark-to-market impact of open positions. In the current sample, NAV remains "
        "close to the initial capital for most trading days, reflecting the limited number "
        "of active position days and the relatively small position scale used in the "
        "research-stage portfolio."
    )

    report.figure(
        image=figures.nav_curve(nav_df),
        title="Figure 15.1 Portfolio NAV Curve",
        caption=(
            "Daily portfolio net asset value across the available research sample. "
            "The NAV remains close to the initial capital for most trading days, "
            "reflecting the limited number of active position days and conservative "
            "research-stage position sizing."
        ),
        width=6.5,
    )

    # ==========================================================
    # 15.4 PnL Analysis
    # ==========================================================

    report.heading2("15.4 Unrealized PnL Analysis")

    report.paragraph(
        "Unrealized PnL captures daily mark-to-market changes from open positions. "
        "The current PnL profile shows that most days are flat, while active trading "
        "periods create concentrated positive or negative PnL observations."
    )

    report.figure(
        image=figures.pnl_bar(nav_df),
        title="Figure 15.2 Daily Unrealized PnL",
        caption=(
            "Daily mark-to-market unrealized profit and loss generated by active "
            "portfolio positions. Most trading days are flat, while active periods "
            "produce concentrated positive and negative PnL observations."
        ),
        width=6.5,
    )

    # ==========================================================
    # 15.5 Drawdown Analysis
    # ==========================================================

    report.heading2("15.5 Drawdown Analysis")

    report.paragraph(
        "Drawdown measures the decline of portfolio NAV from its running peak. "
        "Because the platform includes flat days and uses research-stage position "
        "sizes, drawdown remains limited in absolute account-level terms. The drawdown "
        "chart nevertheless identifies the periods when portfolio losses were most "
        "concentrated."
    )

    report.figure(
        image=figures.drawdown_curve(nav_df),
        title="Figure 15.3 Portfolio Drawdown",
        caption=(
            "Historical decline in portfolio NAV from its running peak. The chart "
            "identifies the periods in which portfolio losses were most concentrated "
            "during the current research sample."
        ),
        width=6.5,
    )

    # ==========================================================
    # 15.6 Strategy Contribution
    # ==========================================================

    report.heading2("15.6 Strategy Contribution")

    report.paragraph(
        "The current portfolio performance is driven by a small number of strategy "
        "families, including long-volatility, butterfly, and calendar-spread structures. "
        "Strategy-level evidence in Chapter 10 shows that different strategies contribute "
        "different PnL profiles: the butterfly structure is relatively stable in the current "
        "sample, while the calendar spread contributes larger downside observations."
    )

    contribution = pd.DataFrame(
        [
            ["Long ATM Strangle", "Mixed", "Long-volatility baseline strategy"],
            ["Long Call Butterfly", "Positive / stable in current sample", "Defined-risk convexity structure"],
            ["Calendar Spread", "Negative in current sample", "Term-structure strategy requiring further calibration"],
        ],
        columns=["Strategy", "Current Contribution", "Interpretation"],
    )

    report.dataframe(contribution)

    # ==========================================================
    # 15.7 Risk Interpretation
    # ==========================================================

    report.heading2("15.7 Risk Interpretation")

    report.paragraph(
        "Performance should be interpreted together with the risk analysis in Chapter 12. "
        "Several negative PnL observations occur during periods of elevated Vega and Theta "
        "exposure, especially when calendar-spread positions dominate the portfolio. This "
        "confirms the importance of connecting portfolio performance analysis with Greeks "
        "monitoring and hedge recommendation."
    )

    for item in [
        "NAV stability reflects conservative research-stage position sizing.",
        "PnL is concentrated on active position days rather than evenly distributed.",
        "Drawdown is limited at the account level but still useful for identifying weak periods.",
        "Strategy contribution is uneven, suggesting that future portfolio allocation rules are needed.",
    ]:
        report.bullet(item)

    # ==========================================================
    # 15.8 Current Limitations
    # ==========================================================

    report.heading2("15.8 Current Limitations")

    for item in [
        "The evaluation uses the available 2026 research sample only.",
        "The current performance statistics are based primarily on mark-to-market unrealized PnL.",
        "Realized PnL, transaction costs, slippage, bid-ask spread, and fill simulation are not fully integrated.",
        "Strategy allocation and position sizing rules are still simplified.",
        "The current results should be treated as platform validation rather than final alpha validation.",
    ]:
        report.bullet(item)

    report.page_break()


def build_future(report):
    report.heading1("16. Current Limitations and Future Work")

    limitations = [
        "The current sample only covers 2026 year-to-date.",
        "Some strategies have limited completed historical trade samples.",
        "Transaction costs, bid-ask spread, slippage, and fill simulation are not fully implemented.",
        "Signal score formula requires a formal Signal Engine for full documentation.",
        "Hedge calibration requires empirical estimation.",
    ]

    report.heading2("Current Limitations")
    for item in limitations:
        report.bullet(item)

    future = [
        "Build full automatic trade generation across all available trading days.",
        "Implement complete historical backtesting with trade lifecycle.",
        "Add transaction costs, slippage, bid-ask spread, and realistic fill assumptions.",
        "Calibrate hedge instruments using historical Greeks exposure.",
        "Generate Chinese version after the English v3.0 structure is frozen.",
        "Update GitHub with README, architecture documentation, sample outputs, and release notes.",
    ]

    report.heading2("Future Work")
    for item in future:
        report.bullet(item)

    report.page_break()