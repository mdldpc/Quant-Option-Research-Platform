from framework.reporting.report_builder import ReportBuilder

from framework.strategy.contracts import BacktestResult

from pathlib import Path

def test_report_builder():


    result = BacktestResult(

        strategy_name="test_strategy",

        total_trades=10,

        completed_trades=10,

        skipped_trades=0,

        win_rate=0.5,

        final_equity=1.1,

        max_drawdown=-0.05,

        average_return=0.01,

    )


    builder = ReportBuilder(
        display_name="Test Strategy"
    )


    report = builder.build(
        result,

        performance_metrics={
            "sharpe_ratio":1.2
        },

        charts={
            "equity_curve": Path(
                "equity.png"
            )
        },

        trade_statistics={
            "win_rate":0.5
        }

    )


    assert report.strategy_name == "test_strategy"


    assert report.display_name == "Test Strategy"


    assert report.performance_metrics["sharpe_ratio"] == 1.2


    assert (
        report.charts["equity_curve"]
        ==
        Path("equity.png")
    )