from pathlib import Path

import pandas as pd

from framework.reporting.documentation import tables, figures
from framework.reporting.documentation.strategy_registry import get_registry
from framework.reporting.translations import tr
from framework.reporting.documentation_cn import tables_cn

def build_phase2(report, nav_df, clean_df):
    """
    Build Part II of the Chinese technical white paper.

    Chapter 9 is completed in the current version.
    Chapters 10–16 remain as placeholders and will be
    implemented progressively.
    """

    report.heading1(tr("PART_II"))

    build_chapter9(report)
    build_chapter10(report)
    build_chapter11(report, nav_df)
    build_chapter12(report, nav_df)
    build_chapter13(report)
    build_chapter14(report)
    build_chapter15(report, nav_df)
    build_chapter16(report)


# ==========================================================
# Chapter 9
# ==========================================================

def build_chapter9(report):
    report.heading1(tr("CHAPTER_9"))

    report.paragraph(
        "第二阶段在第一阶段研究工作的基础上，进一步构建了完整的量化期权研究平台。"
        "平台采用模块化架构设计，将数据处理、策略研究、投资组合管理、风险监控、"
        "对冲建议及自动化报告等功能划分为相互独立且可扩展的模块。"
    )

    report.paragraph(
        "这种分层架构降低了各模块之间的耦合程度，提高了系统的可维护性、"
        "可复现性与后续扩展能力，并为未来增加新的策略、风险模型、"
        "数据源和自动化执行模块奠定了基础。"
    )

    report.heading2(tr("CH9_1"))

    architecture = pd.DataFrame(
        [
            [
                "数据层",
                "市场数据读取、数据加载、交易日识别与数据库存检查",
            ],
            [
                "市场层",
                "交易时段规则、市场数据过滤与数据质量控制",
            ],
            [
                "策略层",
                "策略注册、信号生成及期权交易结构构建",
            ],
            [
                "投资组合层",
                "PositionBook、PnL Engine 与 NAV Engine",
            ],
            [
                "风险层",
                "Greeks 聚合、风险规则、风险分类及对冲建议",
            ],
            [
                "监控层",
                "GreekMonitor、PortfolioMonitor 与 AlertEngine",
            ],
            [
                "报告层",
                "文本报告、Word 白皮书、研究图表及可复用文档模块",
            ],
        ],
        columns=[
            "系统层级",
            "主要职责",
        ],
    )

    report.table(
        dataframe=architecture,
        title=tr("TABLE_9_1_TITLE"),
        caption=(
            "量化期权研究平台采用自下而上的模块化分层设计。"
            "各层分别承担数据处理、策略研究、投资组合管理、风险监控、"
            "系统监测与自动化报告等职责，并通过标准化接口完成信息传递。"
        ),
    )

    report.paragraph(
        "平台整体采用流水线式的数据传递机制。上一层模块产生的标准化输出，"
        "将作为下一层模块的输入，从而保证不同研究步骤之间具有一致的数据口径，"
        "并支持流程重跑、结果复核及后续功能扩展。"
    )

    report.page_break()


# ==========================================================
# Chapter 10
# ==========================================================

def build_chapter10(report):
    report.heading1(tr("CHAPTER_10"))

    registry = get_registry()

    report.paragraph(
        "策略层已经由第一阶段的单一波动率策略原型，扩展为结构化、"
        "可注册且便于维护的策略库。平台通过统一的 StrategyRecord "
        "保存每项策略的研究动机、构建规则、Greeks 特征、证据状态、"
        "表现摘要、当前局限及后续研究路线。"
    )

    report.heading2("10.1 策略注册表概览")

    summary = registry.summary_table().copy()

    column_map = {
        "Strategy ID": "策略编号",
        "Strategy": "策略名称",
        "Name": "策略名称",
        "Category": "策略类别",
        "Stage": "实现阶段",
        "Status": "当前状态",
        "Portfolio": "投资组合接入",
        "Portfolio Integration": "投资组合接入",
        "Risk": "风险监控",
        "Risk Monitoring": "风险监控",
        "Hedge": "对冲支持",
        "Hedge Support": "对冲支持",
    }

    summary = summary.rename(
        columns={
            column: column_map.get(column, column)
            for column in summary.columns
        }
    )

    report.table(
        dataframe=summary,
        title=tr("TABLE_10_1_TITLE"),
        caption=(
            "当前已注册期权策略的总体情况，包括策略类别、实现阶段、"
            "投资组合接入、风险监控及对冲支持状态。"
        ),
    )

    report.paragraph(
        "基于注册表的架构提高了策略层的扩展能力。未来增加铁鹰式、"
        "对角价差、比例价差或波动率相对价值策略时，只需注册新的"
        "策略记录，无需重新编写整套文档生成流程。"
    )

    report.heading2("10.2 当前核心策略")

    strategies = [
        (
            "Long ATM Strangle",
            "多头 ATM 宽跨式",
            "通过同时持有看涨期权与看跌期权建立多头波动率敞口，"
            "适用于预期标的资产将出现较大波动、但方向不确定的市场环境。",
        ),
        (
            "Long Call Butterfly",
            "多头看涨蝶式价差",
            "通过三档执行价格构建风险有限的凸性结构，"
            "适用于预期标的价格将在中间执行价格附近运行的市场环境。",
        ),
        (
            "Calendar Spread",
            "日历价差",
            "通过近月与远月期权之间的相对定价差异建立期限结构敞口，"
            "适用于研究波动率期限结构和时间价值差异。",
        ),
    ]

    for english_name, chinese_name, description in strategies:
        report.heading3(f"{chinese_name}（{english_name}）")
        report.paragraph(description)

    report.paragraph(
        "当前策略卡片模块采用统一 StrategyRecord 架构，"
        "后续版本将进一步扩展更多策略类型及详细案例分析。"
        "策略的数值表现和证据状态仍以当前 Strategy Registry 中的数据为准。"
    )

    report.page_break()

# ==========================================================
# Chapter 11
# ==========================================================

def build_chapter11(report, nav_df):

    report.heading1(tr("CHAPTER_11"))

    report.paragraph(
        "投资组合管理模块负责将策略层生成的交易结果统一转换为标准化持仓，"
        "并进一步完成损益计算、净值更新、风险汇总及绩效分析。"
        "该模块是连接策略研究、风险监控、对冲建议及自动化报告的核心集成层。"
    )

    # ------------------------------------------------------
    # 11.1 Design Objectives
    # ------------------------------------------------------

    report.heading2("11.1 设计目标")

    report.paragraph(
        "Portfolio Engine 的设计目标是统一管理不同策略生成的持仓，"
        "并建立标准化的数据流，使后续风险分析、绩效评估及自动化报告"
        "能够共享同一套投资组合数据。"
    )

    objectives = [
        "将不同策略输出转换为统一的投资组合持仓。",
        "持续维护当前未平仓头寸。",
        "计算持仓层面及投资组合层面的损益。",
        "维护净值（NAV）、累计收益率及最大回撤。",
        "向风险监控模块提供统一的 Greeks 信息。",
        "支持空仓交易日和有持仓交易日。"
    ]

    for item in objectives:
        report.bullet(item)

    # ------------------------------------------------------
    # 11.2 Portfolio Architecture
    # ------------------------------------------------------

    report.heading2("11.2 投资组合架构")

    report.paragraph(
        "投资组合管理模块位于策略层与风险层之间。"
        "不同策略首先生成标准化交易结果，随后进入 PositionBook，"
        "再依次完成损益计算、净值更新、风险聚合及报告生成。"
    )

    architecture = """
Strategy Layer
│
├── Long ATM Strangle
├── Long Call Butterfly
└── Calendar Spread

↓

PositionBook

↓

PnL Engine

↓

NAV Engine

↓

Risk Engine

↓

Hedge Recommendation

↓

Monitoring

↓

Research Report
"""

    report.code_block(architecture)

    # ------------------------------------------------------
    # 11.3 Core Components
    # ------------------------------------------------------

    report.heading2("11.3 核心组件")

    components = pd.DataFrame(
        [
            ["PositionBook", "保存全部未平仓持仓及对应市场信息。"],
            ["PnL Engine", "计算持仓损益及投资组合收益。"],
            ["NAV Engine", "更新净值、累计收益率及回撤。"],
            ["Risk Snapshot", "汇总投资组合 Greeks 与风险状态。"],
            ["Portfolio Report", "向研究报告及自动化系统提供统一输出。"],
        ],
        columns=[
            "模块",
            "主要职责",
        ],
    )

    report.table(
        dataframe=components,
        title="表 11.1 投资组合核心组件",
        caption=(
            "投资组合管理模块由多个相互协作的组件组成，"
            "分别负责持仓管理、损益计算、净值维护及风险汇总。"
        ),
    )

    report.paragraph(
        "模块之间采用统一的数据接口连接。"
        "各组件均可独立维护，同时能够共享统一的数据格式，"
        "提高系统可扩展性和后续开发效率。"
    )

    # ------------------------------------------------------
    # 11.4 PositionBook Example
    # ------------------------------------------------------

    report.heading2("11.4 PositionBook 示例")

    report.paragraph(
        "PositionBook 保存当前所有未平仓头寸。"
        "每条记录均包含策略来源、交易信息、Greeks、持仓数量及当前市场价值，"
        "作为整个 Portfolio Engine 的基础数据对象。"
    )

    report.code_block(
"""PositionBook
├── Strategy ID
├── Entry Date
├── Option Symbol
├── Quantity
├── Entry Price
├── Current Price
├── Delta
├── Gamma
├── Vega
├── Theta
└── Unrealized PnL"""
    )

    report.paragraph(
        "采用统一的数据结构后，不同策略能够共享同一套投资组合管理、"
        "风险分析及自动化报告模块，而无需针对每种策略单独开发管理逻辑。"
    )

    # ------------------------------------------------------
    # 11.5 Summary
    # ------------------------------------------------------

    report.heading2("11.5 本章总结")

    findings = [
        "建立统一的 PositionBook 管理全部持仓。",
        "投资组合层完成损益计算与净值维护。",
        "风险监控模块共享统一的 Greeks 数据。",
        "Portfolio Engine 成为连接策略、风险和自动化系统的核心模块。",
        "模块化设计提高了平台的可维护性和扩展能力。"
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()

# ==========================================================
# Chapter 12
# ==========================================================

def build_chapter12(report, nav_df):

    report.heading1(tr("CHAPTER_12"))

    report.paragraph(
        "风险监控模块负责持续汇总投资组合 Greeks，识别潜在风险来源，"
        "并根据预设规则生成风险状态和风险提示。"
    )

    # ------------------------------------------------------
    # 12.1
    # ------------------------------------------------------

    report.heading2("12.1 Greeks 聚合")

    report.paragraph(
        "系统首先对投资组合中所有持仓的 Greeks 进行逐笔计算，"
        "随后按照 Delta、Gamma、Vega 和 Theta 四项主要风险指标"
        "完成投资组合层面的风险聚合。"
    )

    report.bullet("Delta：方向性风险。")
    report.bullet("Gamma：Delta 对价格变化的敏感度。")
    report.bullet("Vega：波动率风险。")
    report.bullet("Theta：时间价值损耗。")

    # ------------------------------------------------------
    # 12.2
    # ------------------------------------------------------

    report.heading2("12.2 风险状态分类")

    report.paragraph(
        "系统根据投资组合 Greeks 与预设风险阈值，将当前组合划分为"
        "Normal、Warning 和 Critical 三类风险状态。"
    )

    risk_table = pd.DataFrame(
        [
            ["Normal", "风险处于安全范围。"],
            ["Warning", "部分 Greeks 接近风险阈值。"],
            ["Critical", "风险暴露已超过建议范围，需要及时调整。"],
        ],
        columns=[
            "风险等级",
            "说明",
        ],
    )

    report.table(
        dataframe=risk_table,
        title="表 12.1 风险等级说明",
        caption="系统采用三级风险分类，对投资组合当前风险状态进行统一描述。",
    )

    # ------------------------------------------------------
    # 12.3
    # ------------------------------------------------------

    report.heading2("12.3 风险可视化")

    report.paragraph(
        "风险监控模块同时生成多个图形，用于展示风险随时间变化情况。"
    )

    report.figure(
        image=figures.risk_status_bar(nav_df),
        title=tr("FIG_12_1_TITLE"),
        caption=(
            "研究样本期内投资组合日度风险状态的分布情况。"
            "系统根据预设风险阈值，将各交易日划分为正常、预警或严重风险状态。"
        ),
        width=5.5,
    )

    report.figure(
        image=figures.vega_curve(nav_df),
        title=tr("FIG_12_2_TITLE"),
        caption=(
            "投资组合净 Vega 敞口在研究样本期内的变化。"
            "正值表示组合对隐含波动率上升具有正向敏感性，"
            "负值则表示组合存在空头波动率敞口。"
        ),
        width=6.5,
    )

    report.figure(
        image=figures.delta_curve(nav_df),
        title=tr("FIG_12_3_TITLE"),
        caption=(
            "投资组合净 Delta 敞口在研究样本期内的变化。"
            "该图反映组合整体方向性风险及其随时间的变化。"
        ),
        width=6.5,
    )

    report.paragraph(
        "上述风险图能够帮助研究人员快速识别组合风险是否持续累积，"
        "以及当前风险主要来自方向性风险还是波动率风险。"
    )

    report.page_break()


# ==========================================================
# Chapter 13
# ==========================================================

def build_chapter13(report):
    report.heading1(tr("CHAPTER_13"))

    report.paragraph(
        "对冲建议模块为投资组合风险管理提供决策支持。当前平台不会自动执行"
        "交易，而是根据投资组合风险敞口识别主要风险来源，并向研究人员或"
        "投资组合管理者提供相应的风险缓释建议。该设计将策略生成、投资组合"
        "管理、风险监控与对冲决策划分为相互独立的模块。"
    )

    # ------------------------------------------------------
    # 13.1
    # ------------------------------------------------------

    report.heading2("13.1 设计目标")

    objectives = [
        "将投资组合风险敞口转化为可执行的对冲建议。",
        "降低过度集中的方向性、波动率及时间价值风险。",
        "建立透明且可重复的规则驱动对冲逻辑。",
        "在不自动执行交易的前提下支持量化研究流程。",
        "为未来基于优化模型的自动化对冲模块奠定基础。",
    ]

    for item in objectives:
        report.bullet(item)

    # ------------------------------------------------------
    # 13.2
    # ------------------------------------------------------

    report.heading2("13.2 为什么采用对冲建议模式")

    report.paragraph(
        "当前平台的主要定位是量化研究，而不是实盘交易执行。因此，对冲结果"
        "以建议形式输出，而不会直接修改投资组合持仓。研究人员需要在执行任何"
        "交易之前，对风险敞口、市场流动性和交易成本进行人工复核。"
    )

    status = pd.DataFrame(
        [
            ["研究阶段", "规则驱动的对冲建议"],
            ["交易执行", "人工执行"],
            ["风险复核", "人工确认"],
            ["未来方向", "自动化交易执行模块"],
        ],
        columns=[
            "组成部分",
            "当前状态",
        ],
    )

    report.table(
        dataframe=status,
        title="表 13.1 对冲建议模块当前状态",
        caption=(
            "当前平台将风险识别与交易执行相互分离，"
            "由系统生成建议，再由研究人员完成审核。"
        ),
    )

    # ------------------------------------------------------
    # 13.3
    # ------------------------------------------------------

    report.heading2("13.3 对冲决策流程")

    pipeline = [
        "Portfolio Greeks",
        "",
        "      │",
        "      ▼",
        "",
        "Risk Aggregation",
        "",
        "      │",
        "      ▼",
        "",
        "Risk Classification",
        "",
        "      │",
        "      ▼",
        "",
        "Rule Engine",
        "",
        "      │",
        "      ▼",
        "",
        "Hedge Recommendation",
        "",
        "      │",
        "      ▼",
        "",
        "Human Review",
    ]

    report.code_block("\n".join(pipeline))

    report.paragraph(
        "对冲建议模块接收风险监控模块输出的标准化投资组合敞口，"
        "随后依据风险状态和预设规则识别需要处理的风险，并生成对应建议。"
    )

    # ------------------------------------------------------
    # 13.4
    # ------------------------------------------------------

    report.heading2("13.4 风险敞口与对冲工具映射")

    translation = pd.DataFrame(
        [
            [
                "较大正 Delta",
                "方向性风险",
                "卖出股指期货",
            ],
            [
                "较大负 Delta",
                "方向性风险",
                "买入股指期货",
            ],
            [
                "较大负 Vega",
                "波动率风险",
                "增加多头波动率敞口",
            ],
            [
                "较大正 Vega",
                "波动率风险",
                "降低多头波动率敞口",
            ],
            [
                "较大负 Theta",
                "时间价值损耗",
                "减少权利金多头持仓",
            ],
            [
                "较大 Gamma",
                "凸性风险",
                "调整期权组合结构",
            ],
        ],
        columns=[
            "观测到的风险敞口",
            "主要风险",
            "建议对冲方式",
        ],
    )

    report.table(
        dataframe=translation,
        title="表 13.2 风险敞口与对冲建议映射",
        caption=(
            "系统根据不同 Greeks 风险敞口，将投资组合风险映射至"
            "股指期货或期权结构等潜在对冲工具。"
        ),
    )

    # ------------------------------------------------------
    # 13.5
    # ------------------------------------------------------

    report.heading2("13.5 规则驱动决策模块")

    report.paragraph(
        "当前对冲建议模块采用透明的规则驱动逻辑。系统首先判断各项 Greeks "
        "是否达到预警或严重风险状态，再根据匹配规则生成相应的风险缓释建议。"
    )

    rule_flow = [
        "Portfolio Exposure",
        "      │",
        "      ▼",
        "Risk Level Check",
        "      │",
        "      ▼",
        "Rule Match",
        "      │",
        "      ▼",
        "Hedge Action",
        "      │",
        "      ▼",
        "Recommendation Output",
    ]

    report.code_block("\n".join(rule_flow))

    rule_table = pd.DataFrame(
        [
            [
                "Delta 正常",
                "无需操作",
                "方向性风险处于阈值范围内。",
            ],
            [
                "Delta 预警或严重",
                "期货对冲",
                "使用股指期货降低方向性风险。",
            ],
            [
                "Vega 预警或严重",
                "波动率对冲",
                "使用期权结构降低过度集中的波动率风险。",
            ],
            [
                "Gamma 预警或严重",
                "调整组合结构",
                "降低凸性集中度或重新平衡期权结构。",
            ],
            [
                "Theta 预警或严重",
                "降低权利金敞口",
                "减少时间价值损耗过高的持仓。",
            ],
        ],
        columns=[
            "触发条件",
            "建议措施",
            "主要原因",
        ],
    )

    report.table(
        dataframe=rule_table,
        title="表 13.3 对冲建议规则",
        caption=(
            "规则模块根据风险状态生成标准化建议，"
            "以保证不同交易日的判断逻辑保持一致。"
        ),
    )

    # ------------------------------------------------------
    # 13.6
    # ------------------------------------------------------

    report.heading2("13.6 对冲建议示例")

    examples = pd.DataFrame(
        [
            [
                "净 Delta",
                "0.033",
                "正常",
                "无需操作",
                "组合方向性敞口较低。",
            ],
            [
                "净 Vega",
                "-993.32",
                "预警",
                "监控或降低空头 Vega",
                "较大负 Vega 表明组合对波动率上升较为敏感。",
            ],
            [
                "净 Theta",
                "-365.22",
                "预警",
                "监控时间价值损耗",
                "负 Theta 表明组合持续承受权利金衰减。",
            ],
            [
                "净 Gamma",
                "0.0013",
                "正常",
                "无需操作",
                "当前凸性风险较低。",
            ],
        ],
        columns=[
            "风险指标",
            "观测值",
            "风险等级",
            "建议措施",
            "解释",
        ],
    )

    report.table(
        dataframe=examples,
        title="表 13.4 对冲建议示例",
        caption=(
            "该示例展示规则模块如何将投资组合 Greeks "
            "转化为可供人工复核的风险管理建议。"
        ),
    )

    report.paragraph(
        "以上结果均属于决策支持信息。当前平台不会自动执行对冲交易，"
        "最终操作仍需结合市场流动性、成交价格及交易成本进行人工判断。"
    )

    # ------------------------------------------------------
    # 13.7
    # ------------------------------------------------------

    report.heading2("13.7 当前局限")

    limitations = [
        "当前对冲建议以规则为基础，尚未使用优化模型。",
        "对冲规模仍为近似估计，尚未结合交易成本进行系统校准。",
        "尚未实现自动成交和执行模拟。",
        "买卖价差、滑点及流动性限制尚未被完整纳入。",
        "当前模块的定位是决策支持，而不是自动交易执行。",
    ]

    for item in limitations:
        report.bullet(item)

    # ------------------------------------------------------
    # 13.8
    # ------------------------------------------------------

    report.heading2("13.8 未来自动化对冲模块")

    roadmap = [
        "Current Stage",
        "Rule-Based Recommendation",
        "",
        "      │",
        "      ▼",
        "",
        "Optimization-Based Hedge Sizing",
        "",
        "      │",
        "      ▼",
        "",
        "Transaction-Cost-Aware Selection",
        "",
        "      │",
        "      ▼",
        "",
        "Execution Simulation",
        "",
        "      │",
        "      ▼",
        "",
        "Automatic Hedge Engine",
    ]

    report.code_block("\n".join(roadmap))

    report.paragraph(
        "长期目标是将当前规则驱动的建议系统升级为基于优化模型的自动化"
        "对冲模块，并同时考虑交易成本、市场流动性、对冲有效性及"
        "投资组合约束。"
    )

    report.page_break()


# ==========================================================
# Chapter 14
# ==========================================================

def build_chapter14(report):
    report.heading1(tr("CHAPTER_14"))

    report.paragraph(
        "自动化框架将量化期权研究平台的主要模块整合为标准化日度流程。"
        "平台无需逐一手工运行脚本，即可依次完成数据清洗、策略生成、"
        "投资组合管理、风险监控、对冲建议及报告生成。"
    )

    # ------------------------------------------------------
    # 14.1
    # ------------------------------------------------------

    report.heading2("14.1 设计目标")

    objectives = [
        "自动完成日度量化研究流程。",
        "减少数据处理和报告生成中的人工干预。",
        "生成可复现的研究输出。",
        "支持投资组合的日度监控。",
        "为未来定时任务和生产部署做好准备。",
    ]

    for item in objectives:
        report.bullet(item)

    # ------------------------------------------------------
    # 14.2
    # ------------------------------------------------------

    report.heading2("14.2 日度流水线架构")

    pipeline = [
        "Market Data",
        "",
        "      │",
        "      ▼",
        "",
        "Session Cleaning",
        "",
        "      │",
        "      ▼",
        "",
        "Strategy Engine",
        "",
        "      │",
        "      ▼",
        "",
        "Portfolio Engine",
        "",
        "      │",
        "      ▼",
        "",
        "Risk Engine",
        "",
        "      │",
        "      ▼",
        "",
        "Hedge Recommendation",
        "",
        "      │",
        "      ▼",
        "",
        "Automated Reports",
    ]

    report.code_block("\n".join(pipeline))

    report.paragraph(
        "各模块均生成标准化输出，并将其作为下一阶段的输入。"
        "这种模块化流水线提高了研究过程的可复现性、可维护性和扩展能力。"
    )

    # ------------------------------------------------------
    # 14.3
    # ------------------------------------------------------

    report.heading2("14.3 端到端工作流程")

    workflow = pd.DataFrame(
        [
            ["1", "市场数据", "读取期权与期货市场数据"],
            ["2", "数据清洗", "过滤集合竞价、午间休市及异常观测值"],
            ["3", "策略模块", "生成期权交易信号和策略持仓"],
            ["4", "投资组合模块", "更新 PositionBook、净值和损益"],
            ["5", "风险模块", "聚合 Greeks 并完成风险分类"],
            ["6", "对冲模块", "生成对冲建议"],
            ["7", "报告模块", "生成 Word 白皮书和研究报告"],
        ],
        columns=[
            "阶段",
            "模块",
            "主要输出",
        ],
    )

    report.table(
        dataframe=workflow,
        title="表 14.1 端到端研究流程",
        caption=(
            "日度流水线按照固定顺序执行各模块，"
            "保证研究报告来自一致且可重复的数据处理过程。"
        ),
    )

    # ------------------------------------------------------
    # 14.4
    # ------------------------------------------------------

    report.heading2("14.4 自动化报告生成")

    report.paragraph(
        "报告系统能够自动将投资组合统计数据、风险指标、策略说明、"
        "表格和图形组织为正式技术白皮书。相同的报告框架既可用于"
        "学术研究，也可支持内部管理报告和 GitHub 项目展示。"
    )

    report.code_block(
        """Daily Pipeline

      │
      ▼

CSV / Parquet

      │
      ▼

Portfolio Statistics

      │
      ▼

Word Builder

      │
      ▼

Technical White Paper"""
    )

    # ------------------------------------------------------
    # 14.5
    # ------------------------------------------------------

    report.heading2("14.5 当前自动化功能")

    automation = pd.DataFrame(
        [
            ["日度流水线", "自动重建清洗后的交易时段数据"],
            ["投资组合模块", "更新净值、损益和投资组合状态"],
            ["风险模块", "生成日度投资组合风险指标"],
            ["报告模块", "生成 Word 技术白皮书"],
            ["研究输出", "导出 CSV 和 Parquet 数据集"],
        ],
        columns=[
            "模块",
            "当前功能",
        ],
    )

    report.table(
        dataframe=automation,
        title="表 14.2 当前自动化功能",
        caption=(
            "自动化模块减少了重复性人工操作，"
            "并保证中间数据集和报告输出可以重新生成。"
        ),
    )

    # ------------------------------------------------------
    # 14.6
    # ------------------------------------------------------

    report.heading2("14.6 可复现性")

    reproducibility = [
        "每个处理阶段均生成标准化中间结果。",
        "投资组合指标由清洗后的数据确定性生成。",
        "研究报告能够根据最新结果自动重建。",
        "使用相同输入时，各模块能够重复得到一致输出。",
    ]

    for item in reproducibility:
        report.bullet(item)

    # ------------------------------------------------------
    # 14.7
    # ------------------------------------------------------

    report.heading2("14.7 未来生产部署")

    roadmap = [
        "Current Research Platform",
        "",
        "      │",
        "      ▼",
        "",
        "Scheduled Daily Execution",
        "",
        "      │",
        "      ▼",
        "",
        "Cloud Deployment",
        "",
        "      │",
        "      ▼",
        "",
        "Automatic Monitoring",
        "",
        "      │",
        "      ▼",
        "",
        "Production Quant Platform",
    ]

    report.code_block("\n".join(roadmap))

    report.paragraph(
        "后续工作将逐步接入任务调度、云端部署、自动监控及交易执行基础设施，"
        "使当前研究平台进一步发展为具有生产能力的量化研究系统。"
    )

    report.page_break()


# ==========================================================
# Chapter 15
# ==========================================================

# ==========================================================
# Chapter 15
# ==========================================================

def build_chapter15(report, nav_df):
    report.heading1(tr("CHAPTER_15"))

    if nav_df.empty:
        report.paragraph("当前没有可用的投资组合时间序列数据。")
        report.page_break()
        return

    # ------------------------------------------------------
    # 15.1
    # ------------------------------------------------------

    report.heading2("15.1 评价目标")

    report.paragraph(
        "本章评估当前投资组合研究平台在可用样本期内的整体表现。"
        "其目的并非宣称策略已经具备稳定盈利能力，而是检验策略、"
        "投资组合、风险、对冲及自动化模块在联合运行时的表现。"
    )

    objectives = [
        "衡量完整交易日历下的投资组合净值稳定性。",
        "评估有持仓交易日的未实现损益变化。",
        "计算投资组合回撤和下行压力。",
        "比较有持仓期与空仓期的分布。",
        "对当前平台输出进行研究阶段的综合评价。",
    ]

    for item in objectives:
        report.bullet(item)

    # ------------------------------------------------------
    # 15.2
    # ------------------------------------------------------

    report.heading2("15.2 绩效概览")

    summary = tables_cn.portfolio_summary(nav_df).copy()

    summary_column_map = {
        "Metric": "指标",
        "Value": "数值",
    }

    summary = summary.rename(columns=summary_column_map)

    report.table(
        dataframe=summary,
        title="表 15.1 投资组合绩效概览",
        caption="当前研究样本期内投资组合的主要绩效和风险统计指标。",
    )

    total_days = len(nav_df)

    active_days = (
        int((nav_df["positions"] > 0).sum())
        if "positions" in nav_df.columns
        else 0
    )

    flat_days = total_days - active_days

    dashboard = pd.DataFrame(
        [
            ["交易日总数", total_days],
            ["有持仓交易日", active_days],
            ["空仓交易日", flat_days],
            [
                "持仓活跃比例",
                f"{active_days / total_days:.2%}"
                if total_days
                else "不适用",
            ],
            ["评价状态", "研究阶段平台评价"],
        ],
        columns=[
            "指标",
            "数值",
        ],
    )

    report.table(
        dataframe=dashboard,
        title="表 15.2 投资组合活跃度",
        caption=(
            "平台处理完整交易日历，但仅在信号触发时建立持仓，"
            "符合信号驱动型期权研究框架的特征。"
        ),
    )

    # ------------------------------------------------------
    # 15.3
    # ------------------------------------------------------

    report.heading2("15.3 净值分析")

    report.paragraph(
        "投资组合净值反映未平仓头寸按市场价格计量后的账户价值。"
        "当前样本中，大部分交易日的净值接近初始资金，主要原因是"
        "有持仓交易日数量有限，并且研究阶段采用了相对保守的持仓规模。"
    )

    report.figure(
        image=figures.nav_curve(nav_df),
        title=tr("FIG_15_1_TITLE"),
        caption=(
            "研究样本期内的日度投资组合净值。大部分交易日净值接近"
            "初始资金，反映当前策略触发频率和持仓规模均较为有限。"
        ),
        width=6.5,
    )

    # ------------------------------------------------------
    # 15.4
    # ------------------------------------------------------

    report.heading2("15.4 未实现损益分析")

    report.paragraph(
        "未实现损益反映当前未平仓头寸的日度盯市变化。"
        "多数空仓交易日的损益为零，而有持仓期间则形成相对集中的"
        "正向或负向损益观测值。"
    )

    report.figure(
        image=figures.pnl_bar(nav_df),
        title=tr("FIG_15_2_TITLE"),
        caption=(
            "当前未平仓头寸形成的日度未实现损益。"
            "投资组合损益主要集中于存在有效持仓的交易日。"
        ),
        width=6.5,
    )

    # ------------------------------------------------------
    # 15.5
    # ------------------------------------------------------

    report.heading2("15.5 回撤分析")

    report.paragraph(
        "回撤衡量投资组合净值相对于历史峰值的下降幅度。"
        "由于平台包含大量空仓日，并使用研究阶段的持仓规模，"
        "账户层面的绝对回撤相对有限，但回撤曲线仍能识别"
        "组合表现较弱的时间区间。"
    )

    report.figure(
        image=figures.drawdown_curve(nav_df),
        title=tr("FIG_15_3_TITLE"),
        caption=(
            "投资组合净值相对于历史峰值的下降幅度。"
            "该图用于识别样本期内损失较为集中的时间区间。"
        ),
        width=6.5,
    )

    # ------------------------------------------------------
    # 15.6
    # ------------------------------------------------------

    report.heading2("15.6 策略贡献")

    report.paragraph(
        "当前投资组合表现主要由多头波动率、蝶式价差及日历价差等"
        "策略结构共同形成。不同策略具有不同的损益特征，"
        "因此需要在投资组合层面进一步研究资金分配与风险预算。"
    )

    contribution = pd.DataFrame(
        [
            [
                "多头 ATM 宽跨式",
                "表现混合",
                "多头波动率基准策略",
            ],
            [
                "多头看涨蝶式价差",
                "当前样本相对稳定",
                "风险有限的凸性结构",
            ],
            [
                "日历价差",
                "当前样本表现较弱",
                "仍需进一步校准的期限结构策略",
            ],
        ],
        columns=[
            "策略",
            "当前贡献",
            "解释",
        ],
    )

    report.table(
        dataframe=contribution,
        title="表 15.3 策略贡献概览",
        caption=(
            "不同策略在当前样本中呈现差异化表现，"
            "说明后续需要建立更完善的资金分配规则。"
        ),
    )

    # ------------------------------------------------------
    # 15.7
    # ------------------------------------------------------

    report.heading2("15.7 风险解读")

    report.paragraph(
        "投资组合表现应与第 12 章的风险分析结合解读。"
        "部分负向损益出现在 Vega 和 Theta 敞口较高的阶段，"
        "说明绩效分析必须与 Greeks 风险监控及对冲建议共同使用。"
    )

    findings = [
        "净值稳定性部分源于研究阶段较为保守的持仓规模。",
        "损益集中于有持仓交易日，而非均匀分布于全部交易日。",
        "账户层面的回撤较小，但仍可用于识别表现较弱的阶段。",
        "不同策略贡献存在差异，未来需要建立资金分配和风险预算规则。",
    ]

    for item in findings:
        report.bullet(item)

    # ------------------------------------------------------
    # 15.8
    # ------------------------------------------------------

    report.heading2("15.8 当前局限")

    limitations = [
        "当前评价仅使用可用的 2026 年研究样本。",
        "绩效指标主要基于盯市未实现损益。",
        "已实现损益、交易成本、滑点、买卖价差和成交模拟尚未完整接入。",
        "策略资金分配及持仓规模规则仍较为简化。",
        "当前结果应被视为平台有效性验证，而不是最终 Alpha 验证。",
    ]

    for item in limitations:
        report.bullet(item)

    report.page_break()

# ==========================================================
# Chapter 16
# ==========================================================

def build_chapter16(report):
    report.heading1(tr("CHAPTER_16"))

    report.paragraph(
        "本章中文版内容将在后续阶段完成，重点总结当前研究样本、"
        "交易成本、执行模拟、信号模型和对冲校准方面的局限，"
        "并说明后续研究与平台开发方向。"
    )

    report.page_break()

# ==========================================================
# Chapter 16
# ==========================================================

def build_chapter16(report):
    report.heading1(tr("CHAPTER_16"))

    report.paragraph(
        "当前量化期权研究平台已经完成从数据处理、波动率研究、策略构建，"
        "到投资组合管理、风险监控、对冲建议和自动化报告的整体流程。"
        "但由于样本范围、成交模拟和策略校准仍然有限，当前结果应被视为"
        "研究平台的阶段性成果。"
    )

    report.heading2("16.1 当前局限")

    limitations = [
        "当前研究样本主要覆盖 2026 年上半年。",
        "部分策略完成的历史交易数量仍然有限。",
        "交易成本、买卖价差、滑点和成交模拟尚未完整实现。",
        "信号评分公式仍需通过正式 Signal Engine 进行标准化记录。",
        "对冲规模和风险阈值仍需基于历史数据完成经验校准。",
        "当前策略表现尚未经过独立样本外测试。",
    ]

    for item in limitations:
        report.bullet(item)

    report.heading2("16.2 后续研究方向")

    future = [
        "扩展至更长时间区间和更多市场状态。",
        "建立完整的历史交易生命周期回测。",
        "接入交易成本、滑点、买卖价差及现实成交假设。",
        "基于历史 Greeks 敞口校准对冲工具和对冲规模。",
        "完善 Strategy Card 中文模块及双语研究文档。",
        "建立样本外测试和滚动窗口验证框架。",
        "增加自动任务调度、云端部署和实时监控。",
        "完成 GitHub 中英文 README、示例输出及正式 Release。",
    ]

    for item in future:
        report.bullet(item)

    report.heading2("16.3 平台发展路线")

    roadmap = [
        "Research Prototype",
        "",
        "      │",
        "      ▼",
        "",
        "Modular Research Platform",
        "",
        "      │",
        "      ▼",
        "",
        "Large-Sample Validation",
        "",
        "      │",
        "      ▼",
        "",
        "Execution Simulation",
        "",
        "      │",
        "      ▼",
        "",
        "Production Quant Platform",
    ]

    report.code_block("\n".join(roadmap))

    report.paragraph(
        "后续开发将继续坚持模块化、可复现和风险优先的原则。"
        "平台的长期目标并非仅用于展示单一策略，而是建立一套能够支持"
        "数据研究、策略验证、投资组合构建和风险管理的完整量化研究基础设施。"
    )

    report.page_break()