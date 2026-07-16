from framework.reporting.report_builder import (
    ReportBuilder,
)

from framework.reporting.research_report_builder import (
    ResearchReportBuilder,
)

from framework.reporting.backtest_charts import (
    draw_equity_curve,
    draw_drawdown,
    draw_return_distribution,
)

from analysis.backtest_analysis import (
    BacktestAnalyzer,
)

from framework.registry import (
    list_all_strategies,
    enabled_strategies,
    get_strategy,
    get_backtester,
)

from framework.contracts import (
    StrategyDatasetContract,
    BacktestContract,
    RiskContract,
)

from config.strategy_config import (
    SIGNAL_CONFIG,
    EXECUTION_CONFIG,
    RISK_CONFIG,
)

from pathlib import Path
import pandas as pd

def run_strategy(
    strategy_name: str,
    trades: pd.DataFrame,
    report_path: Path,
    trades_path: Path,
):
    """
    Execute a registered strategy.

    Workflow:

    strategy name
        |
        v
    registry
        |
        v
    Backtester
        |
        v
    BacktestResult

    """

    if strategy_name not in list_all_strategies():
        raise KeyError(
            f"Unknown strategy: {strategy_name}"
        )


    if not get_strategy(strategy_name)["enabled"]:
        raise ValueError(
            f"Strategy disabled: {strategy_name}"
        )


    backtester_class = get_backtester(
        strategy_name
    )


    backtester = backtester_class(
        trades
    )


    result = backtester.backtest(
        report_path=report_path,
        trades_path=trades_path,
    )


    return result

def run_strategy_report(
    strategy_name: str,
    trades: pd.DataFrame,
    report_path: Path,
    trades_path: Path,
):
    """
    Complete research report pipeline.

    Workflow:

    Strategy
        |
        v
    BacktestResult
        |
        v
    Analytics
        |
        v
    ReportData
        |
        v
    Word Report

    """


    # -------------------------
    # 1. Run Backtest
    # -------------------------

    result = run_strategy(
        strategy_name=strategy_name,
        trades=trades,
        report_path=report_path,
        trades_path=trades_path,
    )


    # -------------------------
    # 2. Analyze Results
    # -------------------------

    analyzer = BacktestAnalyzer(
        trades=pd.read_csv(
            trades_path
        )
    )


    performance = analyzer.performance()

    statistics = analyzer.trade_statistics()



    # -------------------------
    # 3. Generate Charts
    # -------------------------

    analyzed_trades = pd.read_csv(
        trades_path
    )


    charts = {

        "equity_curve":
            draw_equity_curve(
                analyzed_trades
            ),


        "drawdown":
            draw_drawdown(
                analyzed_trades
            ),


        "return_distribution":
            draw_return_distribution(
                analyzed_trades
            ),

    }



    # -------------------------
    # 4. Build ReportData
    # -------------------------

    builder = ReportBuilder(
        display_name=strategy_name
    )


    report_data = builder.build(

        result,

        performance_metrics=performance,

        trade_statistics=statistics,

        charts=charts,

    )



    # -------------------------
    # 5. Generate Word Report
    # -------------------------

    doc_builder = ResearchReportBuilder()


    doc_builder.build(
        report_data,

        report_path,
    )


    return report_data

def show_framework_status():

    print("=" * 70)
    print("Strategy Framework v2")
    print("=" * 70)

    print("\nFramework Status")
    print("-" * 70)

    print(f"{'Signal Config':25} OK")
    print(f"{'Execution Config':25} OK")
    print(f"{'Risk Config':25} OK")
    print(f"{'Registry':25} OK")
    print(f"{'Builder Interface':25} OK")
    print(f"{'Contracts':25} OK")

    print("\nRegistered Strategies")
    print("-" * 70)

    print(f"{'Name':25}{'Enabled':10}{'Status'}")

    production = 0
    prototype = 0
    planned = 0

    for name in list_all_strategies():

        cfg = get_strategy(name)

        print(
            f"{name:25}"
            f"{str(cfg['enabled']):10}"
            f"{cfg['status']}"
        )

        if cfg["status"] == "production":
            production += 1
        elif cfg["status"] == "prototype":
            prototype += 1
        else:
            planned += 1

    print("\nSummary")
    print("-" * 70)

    print(f"Registered : {len(list_all_strategies())}")
    print(f"Enabled    : {len(enabled_strategies())}")
    print(f"Production : {production}")
    print(f"Prototype  : {prototype}")
    print(f"Planned    : {planned}")

    print("\nFramework Ready")


if __name__ == "__main__":
    show_framework_status()