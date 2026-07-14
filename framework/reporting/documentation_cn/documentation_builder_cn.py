from framework.reporting.word_report import WordReport

from framework.reporting.documentation_cn.cover import build_cover
from framework.reporting.documentation_cn.toc import build_toc
from framework.reporting.documentation_cn.executive_summary import (
    build_executive_summary,
)
from framework.reporting.documentation_cn.phase1 import build_phase1
from framework.reporting.documentation_cn.phase2 import build_phase2
from framework.reporting.documentation_cn.appendix import build_appendix
from framework.reporting.documentation_cn.project_overview import (
    build_project_overview,
)

class DocumentationBuilderCN:

    def __init__(self, nav_df, clean_df):
        self.nav_df = nav_df
        self.clean_df = clean_df

        self.report = WordReport(
            language="zh",
        )

    def build(self):
        build_cover(self.report)
        build_toc(self.report)
        build_project_overview(
            self.report
        )

        build_executive_summary(
            report=self.report,
            nav_df=self.nav_df,
            clean_df=self.clean_df,
        )

        build_phase1(
            report=self.report,
        )

        build_phase2(
            report=self.report,
            nav_df=self.nav_df,
            clean_df=self.clean_df,
        )

        build_appendix(self.report)

        return self.report

    def save(self, path):
        self.report.save(path)