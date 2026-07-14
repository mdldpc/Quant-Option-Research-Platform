from framework.reporting.word_report import WordReport
from framework.reporting.documentation.cover import build_cover
from framework.reporting.documentation.toc import build_toc
from framework.reporting.documentation.executive_summary import build_executive_summary
from framework.reporting.documentation.phase1 import build_phase1
from framework.reporting.documentation.phase2 import build_phase2
from framework.reporting.documentation.appendix import build_appendix


class DocumentationBuilder:

    def __init__(self, nav_df, clean_df):
        self.nav_df = nav_df
        self.clean_df = clean_df
        self.report = WordReport()

    def build(self):
        build_cover(self.report)
        build_toc(self.report)

        build_executive_summary(
            report=self.report,
            nav_df=self.nav_df,
            clean_df=self.clean_df,
        )

        build_phase1(self.report)

        build_phase2(
            report=self.report,
            nav_df=self.nav_df,
            clean_df=self.clean_df,
        )

        build_appendix(self.report)

        return self.report

    def save(self, path):
        self.report.save(path)