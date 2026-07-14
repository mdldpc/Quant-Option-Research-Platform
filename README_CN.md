# 量化期权研究平台

![系统架构](docs/figures/system_architecture.png)

一个模块化的量化期权研究平台，覆盖波动率建模、期权策略研究、投资组合分析、风险管理以及自动化研究文档生成。


---

# 项目概述

**量化期权研究平台（Quant Option Research Platform）** 是一个面向系统化期权研究的模块化量化框架。

项目目标是建立一个完整、可复现的期权研究流程，将市场数据处理、波动率分析、策略研究、组合管理、风险监控以及自动化报告生成整合为统一研究体系。


![研究流程](docs/figures/strategy_pipeline.png)


该平台主要覆盖：

- 波动率研究
- 期权策略开发
- 投资组合分析
- 风险监控
- 自动化技术文档生成


---

# 核心功能


## 1. 波动率研究引擎


波动率模块用于分析期权市场结构。

主要功能：

- 隐含波动率计算
- Volatility Smile 分析
- Volatility Surface 构建
- 到期期限结构分析
- ATM 波动率监控
- 基于 Moneyness 的波动率分析


研究输出包括：

- IV Surface 可视化
- Smile 演化分析
- Term Structure 监控
- 波动率信号生成


---

# 2. 策略研究框架


策略层采用模块化 Registry 架构。


每个策略包含：

- 策略研究动机
- 构建规则
- 入场与退出逻辑
- Greeks 特征
- 回测结果
- 性能分析
- 局限性
- 后续扩展方向


当前研究策略包括：

- 波动率策略
- Strangle
- Calendar Spread
- Butterfly


框架支持未来新增策略，而无需重新设计整体研究系统。


---

# 3. 投资组合管理引擎


投资组合模块提供：

- 持仓管理
- NAV 计算
- 风险暴露聚合
- Portfolio Greeks
- 风险状态快照


核心组件：

- PositionBook
- Portfolio Engine
- NAV Engine


---

# 4. 风险管理框架


风险模块通过期权 Greeks 分析组合风险。

监控指标：

- Delta
- Gamma
- Vega
- 综合风险状态


系统生成：

- 风险暴露报告
- Risk Dashboard
- 投资组合监控摘要


---

# 5. 自动化研究报告系统


项目的重要特点之一，是将研究流程与技术文档生成自动连接。


流程：

```
研究数据

      |

分析流程

      |

图表生成

      |

自动化报告构建

      |

技术白皮书
```


生成内容包括：

- 英文技术白皮书
- 中文技术白皮书
- 策略说明文档
- 研究总结报告


---

# 系统架构


项目采用模块化架构：

```
量化期权研究平台

|
├── 数据层
|      市场数据读取与处理
|
├── 分析层
|      研究分析模块
|
├── 波动率引擎
|      IV / Smile / Surface
|
├── 策略框架
|      策略注册与回测
|
├── 投资组合引擎
|      持仓与 NAV 管理
|
├── 风险引擎
|      Greeks 与风险暴露
|
├── 监控系统
|      风险状态监测
|
└── 报告系统
       自动化文档生成
```


---

# 研究成果展示


## 波动率曲面

![波动率曲面](docs/figures/volatility_surface.png)


## 投资组合表现

![NAV 曲线](docs/figures/portfolio_nav.png)


## 风险监控

![风险 Dashboard](docs/figures/risk_dashboard.png)


---

# 项目结构


```
Quant-Option-Research-Platform

|
├── analysis/
|      研究分析模块
|
├── config/
|      配置文件与研究参数
|
├── framework/
|      核心量化研究框架
|
├── scripts/
|      研究脚本与自动化流程
|
├── docs/
|      设计文档与展示图片
|
└── research/
       研究报告
```


---

# 技术文档


## 英文技术白皮书

```
research/reports/quant_option_technical_white_paper_v3_0.docx
```


## 中文技术白皮书

```
research/reports/quant_option_technical_white_paper_cn_v1_0.docx
```


文档覆盖：

- 研究方法
- 波动率分析
- 策略框架
- 投资组合管理
- 风险监控
- 系统架构


---

# 安装


克隆项目：

```bash
git clone https://github.com/mdldpc/Quant-Option-Research-Platform.git

cd Quant-Option-Research-Platform
```


创建虚拟环境：

```bash
python -m venv venv
```


Windows：

```bash
venv\Scripts\activate
```


Linux / macOS：

```bash
source venv/bin/activate
```


安装依赖：

```bash
pip install -r requirements.txt
```


---

# 使用方法


运行研究脚本：

```bash
python scripts/<script_name>.py
```


生成文档：

英文：

```bash
python -m scripts.rebuild.build_documentation_v3_1
```


中文：

```bash
python -m scripts.rebuild.build_documentation_cn_v1_0
```


---

# 后续规划


未来扩展方向：

- 更多波动率策略
- 更长历史数据集
- 高级投资组合优化
- 机器学习波动率预测
- 实时市场数据接入
- 云端研究部署


---

# License


本项目用于量化研究与金融工程学习目的。