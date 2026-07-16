from pathlib import Path

from framework.reporting.report_models import ReportData



class MarkdownReportBuilder:
    """
    Generate GitHub-friendly
    Markdown research summaries.
    """



    def build(
        self,
        report_data: ReportData,
        output_path,
    ) -> Path:


        output_path = Path(
            output_path
        )


        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        lines = []


        # -------------------------
        # Title
        # -------------------------

        lines.append(
            f"# {report_data.display_name}"
        )

        lines.append("")



        # -------------------------
        # Description
        # -------------------------

        if report_data.description:

            lines.append(
                "## Strategy Overview"
            )

            lines.append("")

            lines.append(
                report_data.description
            )

            lines.append("")



        # -------------------------
        # Performance
        # -------------------------

        lines.append(
            "## Performance Summary"
        )

        lines.append("")


        for key, value in (
            report_data.performance_metrics.items()
        ):

            lines.append(
                f"- **{key}**: {value}"
            )


        lines.append("")



        # -------------------------
        # Trade Statistics
        # -------------------------

        lines.append(
            "## Trade Statistics"
        )

        lines.append("")


        for key, value in (
            report_data.trade_statistics.items()
        ):

            lines.append(
                f"- **{key}**: {value}"
            )


        lines.append("")



        # -------------------------
        # Risk
        # -------------------------

        if report_data.risk_metrics:


            lines.append(
                "## Risk Metrics"
            )

            lines.append("")


            for key, value in (
                report_data.risk_metrics.items()
            ):

                lines.append(
                    f"- **{key}**: {value}"
                )


            lines.append("")



        # -------------------------
        # Charts
        # -------------------------

        if report_data.charts:


            lines.append(
                "## Charts"
            )

            lines.append("")


            for name, path in (
                report_data.charts.items()
            ):

                lines.append(
                    f"- {name}: `{path}`"
                )


        output_path.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )


        return output_path