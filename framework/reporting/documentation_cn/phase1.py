from framework.reporting.documentation_cn import tables_cn
from framework.reporting.documentation import phase1_figures
from framework.reporting.translations import tr


def build_phase1(report):
    report.heading1(tr("PART_I"))

    build_background(report)
    build_dataset(report)
    build_preprocessing(report)
    build_volatility(report)
    build_signal(report)
    build_strategy(report)
    build_backtest(report)
    build_robustness(report)


# ==========================================================
# Chapter 1
# ==========================================================

def build_background(report):
    report.heading1(tr("CHAPTER_1"))

    report.paragraph(
        "第一阶段围绕量化期权研究平台最初设定的七项研究目标展开，"
        "旨在建立一套从原始期权市场数据处理，到隐含波动率建模、"
        "希腊字母分析、策略构建、回测及稳健性检验的端到端研究流程。"
    )

    goals = [
        "市场数据获取",
        "数据预处理",
        "数据清洗",
        "隐含波动率曲面与期限结构构建",
        "策略构建",
        "回测框架",
        "风险与稳健性分析",
    ]

    for item in goals:
        report.bullet(item)

    report.paragraph(
        "上述七项研究目标的完成，标志着本项目由若干相互独立的分析脚本，"
        "逐步发展成为一套具备数据处理、研究分析、策略验证和结果展示能力的"
        "可复现量化期权研究框架。"
    )

    report.page_break()


# ==========================================================
# Chapter 2
# ==========================================================

def build_dataset(report):
    report.heading1(tr("CHAPTER_2"))

    report.paragraph(
        "本项目使用中国股指期权与股指期货的日内市场数据。原始数据以"
        "压缩 CSV/XZ 文件形式存储，覆盖期权报价、成交记录、订单簿信息、"
        "期货价格、执行价格、到期月份及合约代码等字段。"
    )

    items = [
        "压缩后的原始数据规模约为 8 GB。",
        "全部解压后的数据规模超过 300 GB。",
        "每个交易日包含多个执行价格和多个到期月份的期权合约。",
        "Black-76 定价模型以对应期货价格作为标的资产价格输入。",
        "中间结果使用 CSV 和 Parquet 格式保存，以兼顾可复现性与处理效率。",
    ]

    for item in items:
        report.bullet(item)

    report.page_break()


# ==========================================================
# Chapter 3
# ==========================================================

def build_preprocessing(report):
    report.heading1(tr("CHAPTER_3"))

    report.paragraph(
        "在开展波动率估计和策略构建之前，需要对原始市场观测值进行标准化"
        "与清洗。数据预处理模块负责提取合约元数据、匹配对应期货价格、"
        "统一交易日期，并将期权价格整理为适合隐含波动率和希腊字母计算的"
        "研究数据集。"
    )

    checks = [
        "解析期权合约代码，识别看涨期权和看跌期权类型。",
        "从合约代码中提取执行价格与到期月份。",
        "将期权观测值与对应期货价格进行匹配。",
        "识别缺失或不完整的成交记录。",
        "识别不可用或无效的期权价格。",
        "检查隐含波动率求解是否收敛，并识别异常 IV 数值。",
        "验证波动率微笑、曲面、期限结构和希腊字母数据集。",
    ]

    for item in checks:
        report.bullet(item)

    report.paragraph(
        "通过上述处理，后续波动率分析、信号生成和策略模块能够基于"
        "内部结构一致、字段标准统一的研究数据集运行。"
    )

    report.page_break()


# ==========================================================
# Chapter 4
# ==========================================================

def build_volatility(report):
    report.heading1(tr("CHAPTER_4"))

    report.paragraph(
        "波动率分析模块采用 Black-76 模型估计期权隐含波动率，并研究"
        "隐含波动率的经验分布、波动率微笑、波动率曲面及期限结构。"
        "相关输出构成策略构建和投资组合风险分析的量化基础。"
    )

    report.heading2(tr("CH4_1"))

    report.paragraph(
        "由于本项目以期货价格作为标的资产价格，因此采用 Black-76 模型"
        "进行期权定价。通过对市场期权价格进行数值反解，可以得到隐含波动率。"
        "该指标随后被用于波动率微笑、曲面、期限结构、信号和希腊字母分析。"
    )

    report.heading2(tr("CH4_2"))

    report.paragraph(
        "在分析横截面波动率结构之前，本研究首先考察隐含波动率的经验分布。"
        "直方图用于展示隐含波动率观测值的整体分布形态，箱线图则用于识别"
        "中位数、离散程度及潜在极端值。"
    )

    report.figure(
        image=phase1_figures.iv_distribution_histogram(),
        title=tr("FIG_4_1_TITLE"),
        caption=(
            "研究样本中隐含波动率观测值的经验分布。该图展示了估计 IV "
            "的主要集中区间、离散程度及右尾特征。"
        ),
        width=6.5,
    )

    report.figure(
        image=phase1_figures.iv_distribution_boxplot(),
        title=tr("FIG_4_2_TITLE"),
        caption=(
            "隐含波动率观测值的箱线图，展示样本中位数、四分位区间以及"
            "可能存在的极端观测值。"
        ),
        width=6.5,
    )

    report.heading2(tr("CH4_3"))

    report.paragraph(
        "本研究按照价内外程度对隐含波动率观测值进行分组，从而构建波动率"
        "微笑。结果显示，波动率在两侧翼部均有所抬升，其中低价内外程度一侧"
        "更为明显，反映市场对下行尾部风险保护的需求。"
    )

    report.figure(
        image=phase1_figures.volatility_smile_overall(),
        title=tr("FIG_4_3_TITLE"),
        caption=(
            "近月期权在不同价内外程度分组下的平均隐含波动率。左侧翼部"
            "明显抬升，表明较低价内外程度期权具有更高的隐含波动率。"
        ),
        width=6.5,
    )

    report.paragraph(
        "波动率微笑表明，隐含波动率并非常数，而是随执行价格和价内外程度"
        "发生变化。因此，策略构建需要考虑执行价格维度，不能仅依赖单一的"
        "ATM 隐含波动率指标。"
    )

    report.heading2(tr("CH4_4"))

    report.paragraph(
        "波动率曲面同时刻画执行价格和到期时间两个维度上的隐含波动率。"
        "该二维结构能够综合展示期权市场如何在不同价内外程度和剩余期限下"
        "反映风险定价。"
    )

    report.figure(
        image=phase1_figures.volatility_surface_h1(),
        title=tr("FIG_4_4_TITLE"),
        caption=(
            "不同交易日和不同价内外程度分组下的近月隐含波动率。热力图同时"
            "展示了波动率曲面的时间序列变化和横截面结构。"
        ),
        width=6.5,
    )

    report.paragraph(
        "波动率曲面将波动率微笑和期限结构统一在同一分析对象中，对日历价差、"
        "到期月份选择及波动率状态识别具有重要意义。"
    )

    report.heading2(tr("CH4_5"))

    report.paragraph(
        "ATM 隐含波动率期限结构通过汇总不同到期月份的平值期权隐含波动率"
        "构建，用于描述隐含波动率从近月到远月的变化关系。"
    )

    report.figure(
        image=phase1_figures.atm_term_structure_overall(),
        title=tr("FIG_4_5_TITLE"),
        caption=(
            "不同到期顺序下的平均 ATM 隐含波动率。该曲线展示了期权隐含"
            "波动率由近月向远月变化的总体特征。"
        ),
        width=6.5,
    )

    report.paragraph(
        "ATM 隐含波动率期限结构为日历价差策略提供了直接的实证基础，"
        "因为此类策略的收益与近月和远月期权之间的相对定价密切相关。"
    )

    report.heading2(tr("CH4_6"))

    findings = [
        "隐含波动率观测值在样本中呈现较为明显的离散特征。",
        "波动率微笑整体呈现 U 型结构。",
        "左侧尾部隐含波动率更高，反映市场对下行风险保护的需求。",
        "波动率曲面同时刻画了价内外程度效应和期限效应。",
        "ATM 隐含波动率期限结构整体呈现一定程度的向上倾斜。",
        "短期限期权表现出更强的价格扭曲和风险敏感性。",
        "上述波动率结构为策略构建提供了实证基础。",
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()


# ==========================================================
# Chapter 5
# ==========================================================

def build_signal(report):
    report.heading1(tr("CHAPTER_5"))

    report.paragraph(
        "第一阶段的策略原型使用若干波动率相关指标识别潜在开仓时点。"
        "当前信号框架仍处于研究阶段，不应被解释为已经完成生产化验证的"
        "最终 Alpha 模型。"
    )

    report.heading2(tr("CH5_1"))

    inputs = [
        "ATM 隐含波动率",
        "隐含波动率 z-score",
        "期限结构斜率",
        "信号评分",
        "开仓阈值",
    ]

    for item in inputs:
        report.bullet(item)

    report.heading2(tr("CH5_2"))

    report.paragraph(
        "系统首先根据波动率相关特征计算 signal_score。数值 80 并非直接"
        "由某一市场变量计算得到，而是应用于信号评分的开仓阈值。"
        "当 signal_score 大于或等于 80 时，策略认为当前信号强度已达到"
        "开仓条件。"
    )

    report.heading2(tr("CH5_3"))

    report.paragraph(
        "在正式的 Signal Engine 完成之前，signal_score 的具体计算公式仍需"
        "进一步依据源代码进行标准化记录。现阶段应将信号阈值视为研究参数，"
        "而不是已经完成充分统计检验的生产参数。"
    )

    report.page_break()


# ==========================================================
# Chapter 6
# ==========================================================

def build_strategy(report):
    report.heading1(tr("CHAPTER_6"))

    report.paragraph(
        "第一阶段的策略原型将波动率信号转化为具体期权持仓。初始实现主要"
        "采用基于信号的 ATM 跨式或宽跨式结构，以构建方向性较低、"
        "波动率敏感度较高的期权组合。"
    )

    report.heading2(tr("CH6_1"))

    report.paragraph(
        "当信号评分超过预设开仓阈值时，策略建立新的期权持仓。"
    )

    report.heading2(tr("CH6_2"))

    for item in [
        "买入 ATM 看涨期权",
        "买入 ATM 看跌期权",
        "建立多头波动率敞口",
        "相较于直接持有期货，降低组合的初始方向性偏差",
        "在标的资产出现较大幅度波动时获得正向收益潜力",
    ]:
        report.bullet(item)

    report.heading2(tr("CH6_3"))

    report.paragraph(
        "当信号强度减弱，或持仓达到预设的最大持有期限时，策略平仓。"
    )

    report.heading2(tr("CH6_4"))

    report.paragraph(
        "该策略原型成功建立了波动率分析结果与系统化期权持仓之间的连接，"
        "并为后续日历价差、波动率相对价值以及多因子期权投资组合等策略"
        "提供了基础框架。"
    )

    report.page_break()


# ==========================================================
# Chapter 7
# ==========================================================

def build_backtest(report):
    report.heading1(tr("CHAPTER_7"))

    report.paragraph(
        "本项目建立了规则驱动的回测引擎，用于评估波动率信号能否被转化为"
        "系统化期权交易。回测框架记录开仓日期、平仓日期、持有期限、"
        "入场信号评分、退出信号评分、持仓收益率、净值曲线及回撤等信息。"
    )

    # 当前继续复用英文版数据表；后续可增加中文字段映射
    report.dataframe(
        tables_cn.phase1_backtest_metrics()
    )

    report.heading2(tr("CH7_1"))

    items = [
        "策略原型在当前样本期内取得了正收益。",
        "最终净值达到 1.305，对应累计收益率为 30.5%。",
        "最大回撤为 -0.92%。",
        "策略共完成 4 笔交易，其中 3 笔盈利，1 笔亏损。",
        "当前结果应被视为框架有效性验证，而不是对策略 Alpha 的最终确认。",
    ]

    for item in items:
        report.bullet(item)

    report.heading2(tr("CH7_2"))

    report.paragraph(
        "由于当前仅包含 4 笔完整交易，统计置信度仍然有限。后续研究应扩大"
        "历史样本，并引入更现实的成交、滑点和交易成本假设。"
    )

    report.page_break()


# ==========================================================
# Chapter 8
# ==========================================================

def build_robustness(report):
    report.heading1(tr("CHAPTER_8"))

    report.paragraph(
        "量化策略不仅需要在基础回测中取得较好表现，还需要在不同参数和"
        "执行假设下保持一定稳定性。本章从交易成本、信号阈值、持有期限"
        "及整体投资组合表现等角度，对期权策略进行稳健性分析。"
    )

    report.heading2(tr("CH8_1"))

    tests = [
        "信号阈值敏感性分析",
        "交易成本敏感性分析",
        "持有期限敏感性分析",
        "不同参数组合下的策略表现比较",
        "综合稳健性分析仪表板",
    ]

    for item in tests:
        report.bullet(item)

    report.paragraph(
        "本研究并非仅依赖单一参数配置，而是比较策略在多组研究设定下的"
        "表现，以判断回测结果是否过度依赖某一特定参数组合。"
    )

    report.figure(
        image=phase1_figures.robustness_dashboard(),
        title=tr("FIG_8_1_TITLE"),
        caption=(
            "不同信号阈值、交易成本和持有期限设定下的敏感性分析结果。"
            "该仪表板用于集中比较不同研究参数对策略表现的影响。"
        ),
        width=6.5,
    )

    report.heading2(tr("CH8_2"))

    report.paragraph(
        "策略净值曲线反映全部已完成期权交易对累计投资组合价值的影响。"
        "虽然当前样本规模有限，但该曲线能够直观展示研究期内策略净值的"
        "变化过程。"
    )

    report.figure(
        image=phase1_figures.option_equity_curve(),
        title=tr("FIG_8_2_TITLE"),
        caption=(
            "当前研究样本中已完成期权交易形成的累计净值曲线。由于回测仅"
            "包含 4 笔完整交易，该结果应主要用于验证框架运行是否有效。"
        ),
        width=6.5,
    )

    report.paragraph(
        "单笔交易收益率图进一步展示各笔完整交易的净收益情况。4 笔交易中"
        "有 3 笔取得正收益，1 笔出现小幅亏损。由于样本量较小，该图应被"
        "视为交易层面的透明展示，而不是收益率统计分布的可靠估计。"
    )

    report.figure(
        image=phase1_figures.option_return_distribution(),
        title=tr("FIG_8_3_TITLE"),
        caption=(
            "各笔完整期权交易的净收益率。当前共有 3 笔盈利交易和 1 笔"
            "亏损交易，样本规模不足以支持强统计结论。"
        ),
        width=6.5,
    )

    report.heading2(tr("CH8_3"))

    report.paragraph(
        "期权策略对交易成本较为敏感，原因在于不同合约之间的买卖价差和"
        "市场流动性存在显著差异。交易成本敏感性分析用于判断，在引入合理"
        "执行成本后，策略表现是否仍具有经济意义。"
    )

    report.paragraph(
        "当前实现采用了简化的交易成本假设，但整体架构允许后续加入更现实的"
        "佣金标准、滑点模型、买卖价差和成交概率，而无需重新设计回测框架。"
    )

    report.heading2(tr("CH8_4"))

    report.paragraph(
        "信号质量通过比较入场信号评分与后续策略收益进行评估。如果更高的"
        "信号评分与更好的交易结果之间存在稳定关系，则说明信号生成框架"
        "可能捕捉到了具有经济意义的信息。"
    )

    report.figure(
        image=phase1_figures.option_signal_score_vs_return(),
        title=tr("FIG_8_4_TITLE"),
        caption=(
            "入场信号评分与后续净收益率之间的关系。该图用于初步判断"
            "信号是否具有信息含量，但较小的交易样本限制了统计结论。"
        ),
        width=6.5,
    )

    report.paragraph(
        "因此，信号有效性检验为 signal_score 并非完全任意的排序指标提供了"
        "初步证据，但仍需要在更长历史区间和更多交易样本中进一步验证。"
    )

    report.heading2(tr("CH8_5"))

    report.paragraph(
        "稳健性分析框架已经成功接入量化期权研究平台。虽然当前数据仅覆盖"
        "有限研究区间，但该测试基础设施具有较强复用性，可直接应用于后续"
        "扩展后的历史数据。"
    )

    findings = [
        "在已测试参数范围内，策略表现未出现完全失效，但样本规模仍不足以支持强统计结论。",
        "交易成本分析表明，执行假设会对期权策略结果产生实质性影响。",
        "信号有效性检验初步支持信号评分具有一定信息含量。",
        "稳健性分析仪表板提供了策略稳定性的统一观察界面。",
        "当前框架为未来更大样本的策略验证建立了可扩展基础。",
    ]

    for item in findings:
        report.bullet(item)

    report.page_break()