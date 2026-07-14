import pandas as pd

from framework.reporting.translations import tr


def build_appendix(report):
    """
    Build Appendix for the Chinese white paper.
    """

    report.heading1(tr("APPENDIX"))

    build_directory(report)
    build_environment(report)
    build_version_history(report)


# ==========================================================
# Appendix A
# ==========================================================

def build_directory(report):

    report.heading2("附录 A 项目目录结构")

    report.paragraph(
        "本附录介绍量化期权研究平台的整体目录结构。"
        "项目采用模块化设计，各目录负责数据处理、策略研究、"
        "投资组合、风险管理、自动化报告等不同职责。"
    )

    df = pd.DataFrame(
        [
            ["framework/data", "数据读取、加载与预处理"],
            ["framework/market", "市场数据及交易时段处理"],
            ["framework/strategy", "策略构建与信号生成"],
            ["framework/portfolio", "投资组合与持仓管理"],
            ["framework/risk", "Greeks、风险分析及对冲"],
            ["framework/monitoring", "监控及预警"],
            ["framework/reporting", "Word 报告及图表生成"],
            ["scripts", "研究脚本及自动化流水线"],
            ["research/exports", "CSV / Parquet 输出"],
            ["research/reports", "生成的白皮书及研究报告"],
        ],
        columns=[
            "目录",
            "主要职责",
        ],
    )

    report.table(
        dataframe=df,
        title="表 A.1 项目目录结构",
        caption="量化期权研究平台采用模块化目录设计，各目录负责不同研究功能。",
    )

    report.page_break()


# ==========================================================
# Appendix B
# ==========================================================

def build_environment(report):

    report.heading2("附录 B 软件环境")

    report.paragraph(
        "本项目主要采用 Python 数据科学生态开发，"
        "并结合 GitHub 进行版本管理。"
    )

    env = pd.DataFrame(
        [
            ["操作系统", "Windows 11"],
            ["Python", "3.14"],
            ["数据处理", "Pandas、NumPy、PyArrow"],
            ["科学计算", "SciPy"],
            ["绘图", "Matplotlib"],
            ["Word 文档", "python-docx"],
            ["版本控制", "Git / GitHub"],
        ],
        columns=[
            "组成部分",
            "环境",
        ],
    )

    report.table(
        dataframe=env,
        title="表 B.1 软件环境",
        caption="项目主要开发环境及所使用的软件工具。",
    )

    report.page_break()


# ==========================================================
# Appendix C
# ==========================================================

def build_version_history(report):

    report.heading2("附录 C 项目版本历史")

    report.paragraph(
        "平台在研究过程中经历多个迭代版本，"
        "逐步增加策略、投资组合、风险监控、自动化及双语文档等功能。"
    )

    history = pd.DataFrame(
        [
            [
                "v1.0",
                "七项目标研究报告",
                "完成第一阶段研究内容。",
            ],
            [
                "v1.1",
                "投资组合平台",
                "加入 PositionBook、NAV 与 Greeks。",
            ],
            [
                "v2.0",
                "风险监控",
                "增加风险引擎及监控模块。",
            ],
            [
                "v2.2",
                "技术文档",
                "整合完整英文技术白皮书。",
            ],
            [
                "v3.0",
                "双语平台",
                "完成中英文技术白皮书及自动化生成。",
            ],
        ],
        columns=[
            "版本",
            "名称",
            "主要更新",
        ],
    )

    report.table(
        dataframe=history,
        title="表 C.1 项目版本历史",
        caption="量化期权研究平台主要版本演进。",
    )

    report.paragraph()

    report.paragraph(
        "至此，本平台已经形成从数据处理、波动率分析、策略研究、"
        "投资组合管理、风险监控、自动化报告到中英文技术文档的完整研究框架。"
    )

    report.page_break()