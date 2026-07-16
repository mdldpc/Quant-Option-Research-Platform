from framework.reporting.report_models import ReportData


def test_report_data_creation():

    report = ReportData(
        strategy_name="test_strategy"
    )


    assert report.strategy_name == "test_strategy"

    assert report.performance_metrics == {}

    assert report.trade_statistics == {}

    assert report.risk_metrics == {}