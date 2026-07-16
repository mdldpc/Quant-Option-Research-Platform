from framework.reporting.markdown_report import (
    MarkdownReportBuilder,
)

from framework.reporting.report_models import (
    ReportData,
)



def test_markdown_report(tmp_path):


    output = (
        tmp_path
        /
        "summary.md"
    )


    data = ReportData(

        strategy_name="test",

        display_name="Test Strategy",

        description="Demo Strategy",

        performance_metrics={
            "Sharpe":1.2
        },

        trade_statistics={
            "Win Rate":0.5
        }

    )


    builder = MarkdownReportBuilder()


    result = builder.build(
        data,
        output
    )


    assert result.exists()

    assert result.suffix == ".md"


    content = (
        result.read_text(
            encoding="utf-8"
        )
    )


    assert "# Test Strategy" in content

    assert "Sharpe" in content