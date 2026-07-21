from pathlib import Path

from framework.reporting.publication_pipeline import (
    PublicationPipeline,
)

from framework.reporting.report_models import (
    ReportData,
)

import framework.reporting.publication_pipeline as pipeline_module



def fake_convert(
    self,
    docx_path,
    output_dir=None,
):

    pdf = (
        Path(output_dir)
        /
        "report.pdf"
    )

    pdf.write_text(
        "fake pdf",
        encoding="utf-8"
    )

    return pdf



def test_publication_pipeline(tmp_path):


    # -------------------------
    # Mock PDF conversion
    # -------------------------

    pipeline_module.PDFExporter.convert = fake_convert



    data = ReportData(

        strategy_name="test",

        display_name="Test Strategy",

        description="Demo",

        performance_metrics={
            "Sharpe":1.2
        },

        trade_statistics={
            "win_rate":0.5
        }

    )


    pipeline = PublicationPipeline()


    result = pipeline.publish(
        data,
        tmp_path,
    )


    assert result.docx_path.exists()

    assert result.pdf_path.exists()

    assert result.markdown_path.exists()


    assert result.docx_path.suffix == ".docx"

    assert result.pdf_path.suffix == ".pdf"

    assert result.markdown_path.suffix == ".md"