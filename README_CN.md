# 量化期权研究平台

一个模块化的量化期权研究平台，覆盖波动率建模、期权策略研究、投资组合分析、风险管理以及自动化研究文档生成。

---

# 项目概述

**量化期权研究平台（Quant Option Research Platform）** 是一个面向系统化期权研究的模块化量化框架。

该项目旨在建立一个完整、可复现的期权研究流程，将从市场数据处理到自动化研究报告生成的全过程进行系统化整合。

完整研究流程：

```
市场数据

      |

      v

数据清洗与标准化

      |

      v

波动率研究

(隐含波动率 / Smile / Surface / Term Structure)

      |

      v

策略构建

      |

      v

回测与绩效分析

      |

      v

投资组合管理

      |

      v

风险监控

      |

      v

自动化研究报告
```

项目目标：

> 将传统量化研究中的单次分析脚本，升级为具有模块化结构、可扩展能力和自动化文档生成能力的研究基础设施。

---

# 核心功能

## 1. 波动率研究引擎

波动率模块用于分析期权市场中的隐含波动率结构。

主要功能：

- 隐含波动率计算
- Volatility Smile 分析
- Volatility Surface 构建
- 到期期限结构分析
- ATM 波动率监控
- 基于 Moneyness 的波动率分桶分析


研究输出包括：

- IV Surface 可视化
- Smile 演化分析
- Term Structure 监控
- 波动率信号生成

---

# 2. 策略研究框架

策略层采用模块化 Registry 架构。

每个策略均由统一结构描述，包括：

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
- Strangle 结构
- Calendar Spread
- Butterfly 结构


该框架支持未来新增策略，而无需重新设计整体研究系统。

---

# 3. 投资组合管理引擎

投资组合模块提供系统化组合分析能力。

主要功能：

- 持仓管理
- NAV 计算
- 风险暴露聚合
- Portfolio Greeks 计算
- 风险状态快照


核心组件：

- PositionBook
- Portfolio Engine
- NAV Engine

---

# 4. 风险管理框架

风险模块通过期权 Greeks 对组合风险进行分析。

监控指标包括：

- Delta 暴露
- Gamma 暴露
- Vega 暴露
- 综合风险状态


系统能够生成：

- 风险暴露报告
- 风险 Dashboard
- 投资组合监控摘要

---

# 5. 自动化研究报告系统

本项目的重要特点之一，是将研究流程与技术文档生成自动连接。

报告系统能够将：

```
研究数据

      |

      v

分析流程

      |

      v

图表生成

      |

      v

自动化报告构建

      |

      v

技术白皮书
```

自动转换为结构化研究文档。


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
|      研究分析工具
|
├── 波动率引擎
|      IV / Smile / Surface / Term Structure
|
├── 策略框架
|      策略注册与回测
|
├── 投资组合引擎
|      持仓与 NAV 管理
|
├── 风险引擎
|      Greeks 与风险暴露分析
|
├── 监控系统
|      风险状态监测
|
└── 报告系统
       自动化研究文档生成
```

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
|      研究设计文档
|
└── research/
       研究报告与文档
```

---

# 技术文档

完整技术文档：

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

激活环境：

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

# 使用方法

## 运行研究脚本

单个研究模块：

```bash
python scripts/<script_name>.py
```

---

## 生成技术文档

英文版本：

```bash
python -m scripts.rebuild.build_documentation_v3_1
```

中文版：

```bash
python -m scripts.rebuild.build_documentation_cn_v1_0
```

自动生成：

- 研究图表
- 数据表格
- 技术文档

---

# 研究流程

典型工作流程：

```
1. 准备市场数据

        |

        v

2. 构建研究数据集

        |

        v

3. 分析波动率结构

        |

        v

4. 生成策略信号

        |

        v

5. 执行回测

        |

        v

6. 分析投资组合风险

        |

        v

7. 生成研究报告
```

---

# 后续规划

未来扩展方向：

- 更多波动率策略
- 更长历史数据集
- 高级投资组合优化
- 基于机器学习的波动率预测
- 实时市场数据接入
- 云端研究部署

---

# License

本项目用于量化研究与金融工程学习目的。