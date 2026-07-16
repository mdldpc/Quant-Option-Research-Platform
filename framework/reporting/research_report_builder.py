from pathlib import Path

from framework.reporting.word_report import WordReport
from framework.reporting.report_models import ReportData



class ResearchReportBuilder:
    """
    Generate research report document
    from standardized ReportData.
    """



    def __init__(
        self,
        language="en",
    ):

        self.language = language



    def build(
        self,
        report_data: ReportData,
        output_path,
    ):

        doc = WordReport(
            language=self.language
        )


        # -------------------------
        # Cover
        # -------------------------

        doc.title(
            report_data.display_name
        )


        doc.paragraph(
            report_data.description
        )


        doc.page_break()



        # -------------------------
        # Performance
        # -------------------------

        doc.heading1(
            "Performance Summary"
        )


        for key, value in (
            report_data.performance_metrics.items()
        ):

            doc.paragraph(
                f"{key}: {value}"
            )



        # -------------------------
        # Trade Statistics
        # -------------------------

        doc.heading1(
            "Trade Statistics"
        )


        for key, value in (
            report_data.trade_statistics.items()
        ):

            doc.paragraph(
                f"{key}: {value}"
            )



        # -------------------------
        # Risk
        # -------------------------

        doc.heading1(
            "Risk Metrics"
        )


        for key, value in (
            report_data.risk_metrics.items()
        ):

            doc.paragraph(
                f"{key}: {value}"
            )



        # -------------------------
        # Charts
        # -------------------------

        if report_data.charts:

            doc.heading1(
                "Charts"
            )


            for name, path in (
                report_data.charts.items()
            ):

                doc.figure(
                    image=path,
                    title=name,
                )


        doc.save(
            output_path
        )


        return Path(output_path)