from framework.reporting.documentation_cn import tables_cn


def build_executive_summary(report, nav_df, clean_df):
    report.heading1("执行摘要")

    report.dataframe(
        tables_cn.project_snapshot(
            nav_df=nav_df,
            clean_df=clean_df,
        )
    )

    report.paragraph("")
    report.heading2("主要成果")

    items = [
        "建立了从原始市场数据处理到策略评估的端到端期权研究流程。",
        "完成了隐含波动率、波动率微笑、波动率曲面、期限结构及希腊字母等研究输出。",
        "实现了针对集合竞价、午间休市、收盘后数据及无效观测值的交易时段清洗机制。",
        "将原有的单一策略原型扩展为模块化、可注册和可维护的策略库。",
        "构建了 PositionBook、PnL Engine、NAV Engine、Exposure Engine、Risk Monitor、Hedge Translator 和 Alert Engine。",
        "实现了覆盖 107 个交易日的日度处理流程，并生成投资组合时间序列与研究报告。",
        "建立了可复用的 Word 报告生成系统，为后续 GitHub 发布及双语展示提供支持。",
    ]

    for item in items:
        report.bullet(item)

    report.page_break()