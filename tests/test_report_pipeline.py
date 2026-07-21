from pathlib import Path

import framework.reporting.publication_pipeline as pipeline_module

import pandas as pd

from framework.runner import (
    run_strategy_report,
)

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

def test_run_strategy_report(tmp_path):

    pipeline_module.PDFExporter.convert = fake_convert

    trades = pd.DataFrame(
        {

            "trade_id":[1],

            "status":[
                "constructed"
            ],

            "entry_butterfly_price":[
                10
            ],

            "exit_butterfly_price":[
                12
            ],

        }
    )


    report_path = (
        tmp_path
        /
        "report.docx"
    )


    trades_path = (
        tmp_path
        /
        "trades.csv"
    )


    result = run_strategy_report(

        strategy_name=
        "long_call_butterfly",

        trades=trades,

        report_path=
        report_path,

        trades_path=
        trades_path,

    )


    assert result.docx_path.exists()

    assert result.pdf_path.exists()

    assert result.markdown_path.exists()


    assert report_path.exists()