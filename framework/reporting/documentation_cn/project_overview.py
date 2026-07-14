def build_project_overview(report):

    report.heading1(
        "项目概览"
    )

    report.paragraph(
        "本量化期权研究平台旨在建立一套完整的期权研究基础设施，"
        "覆盖市场数据处理、隐含波动率建模、策略研究、"
        "投资组合管理、风险监控、对冲建议以及自动化报告生成。"
    )


    report.heading2(
        "研究流程"
    )

    report.paragraph(
        """
原始市场数据

        ↓

数据清洗与标准化

        ↓

隐含波动率与 Greeks 计算

        ↓

策略构建与回测

        ↓

投资组合管理

        ↓

风险监控与对冲建议

        ↓

自动化研究报告
        """
    )


    report.heading2(
        "核心模块"
    )

    report.bullet(
        "数据工程模块：处理期权、期货及市场微观结构数据"
    )

    report.bullet(
        "波动率研究模块：构建 IV、Smile、Surface 与 Term Structure"
    )

    report.bullet(
        "策略模块：支持多种期权策略注册和扩展"
    )

    report.bullet(
        "风险模块：计算 Greeks 并生成风险状态"
    )

    report.bullet(
        "报告模块：自动生成中英文技术白皮书"
    )

    report.page_break()