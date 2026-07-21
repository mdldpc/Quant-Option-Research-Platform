from dataclasses import dataclass
from pathlib import Path

from framework.reporting.research_report_builder import (
    ResearchReportBuilder,
)

from framework.reporting.pdf_exporter import (
    PDFExporter,
)

from framework.reporting.markdown_report import (
    MarkdownReportBuilder,
)

from framework.reporting.report_models import (
    ReportData,
)


@dataclass
class PublicationResult:
    """
    Output paths of published research package.
    """

    docx_path: Path

    pdf_path: Path

    markdown_path: Path



class PublicationPipeline:
    """
    Complete research publication pipeline.

    Flow:

    ReportData
        |
        +--> DOCX
        |
        +--> PDF
        |
        +--> Markdown

    """


    def __init__(
        self,
        language="en",
    ):

        self.language = language



    def publish(
        self,
        report_data: ReportData,
        output_dir,
    ) -> PublicationResult:


        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        docx_path = (
            output_dir
            /
            "report.docx"
        )


        pdf_path = (
            output_dir
            /
            "report.pdf"
        )


        markdown_path = (
            output_dir
            /
            "summary.md"
        )


        # -------------------------
        # DOCX
        # -------------------------

        ResearchReportBuilder(
            language=self.language
        ).build(
            report_data,
            docx_path,
        )


        # -------------------------
        # PDF
        # -------------------------

        PDFExporter().convert(
            docx_path,
            output_dir,
        )


        # -------------------------
        # Markdown
        # -------------------------

        MarkdownReportBuilder().build(
            report_data,
            markdown_path,
        )


        return PublicationResult(

            docx_path=docx_path,

            pdf_path=pdf_path,

            markdown_path=markdown_path,

        )