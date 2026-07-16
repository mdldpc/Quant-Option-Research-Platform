from pathlib import Path

from framework.reporting.report_models import ReportData
from framework.reporting.research_report_builder import (
    ResearchReportBuilder,
)



def test_research_report_builder(
    tmp_path
):

    output = (
        tmp_path
        /
        "report.docx"
    )


    data = ReportData(

        strategy_name="test",

        display_name="Test Strategy",

        description="Demo",

        performance_metrics={
            "return":0.1
        },

        trade_statistics={
            "win_rate":0.5
        },

    )


    builder = ResearchReportBuilder()


    result = builder.build(
        data,
        output
    )


    assert result.exists()

    assert result.suffix == ".docx"