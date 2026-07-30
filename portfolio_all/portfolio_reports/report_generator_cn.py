"""
Chinese Portfolio Research Report Generator v1.0

Generate Chinese PDF research report.

Input:

research/reports/tables_cn/

    portfolio_weights_table_cn.csv

    portfolio_performance_table_cn.csv


research/reports/figures_cn/

    maximum_sharpe_allocation_cn.png

    portfolio_equity_curve_cn.png

    portfolio_drawdown_cn.png


Output:

research/reports/

    portfolio_research_report_cn_v1_0.pdf

"""


import os


import pandas as pd



from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Image,

    Table,

    TableStyle,

    PageBreak,

)


from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


from reportlab.lib.pagesizes import letter



# ================================
# Chinese Font
# ================================


from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.cidfonts import UnicodeCIDFont



pdfmetrics.registerFont(

    UnicodeCIDFont(

        "STSong-Light"

    )

)



# ================================
# Paths
# ================================


REPORT_DIR = (

    "research/reports"

)


TABLE_DIR = (

    "research/reports/tables_cn"

)


FIGURE_DIR = (

    "research/reports/figures_cn"

)



OUTPUT_FILE = os.path.join(

    REPORT_DIR,

    "portfolio_research_report_cn_v1_0.pdf"

)



# ================================
# Table Helper
# ================================


def dataframe_to_table(df):


    data = [

        list(df.columns)

    ] + df.values.tolist()



    table = Table(

        data,

        repeatRows=1,

        colWidths=[

            120,

            75,

            75,

            75,

            75,

        ]

    )


    table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    None,

                ),


                (

                    "ALIGN",

                    (0,0),

                    (-1,-1),

                    "CENTER",

                ),


                (

                    "VALIGN",

                    (0,0),

                    (-1,-1),

                    "MIDDLE",

                ),


                (

                    "FONT",

                    (0,0),

                    (-1,-1),

                    "STSong-Light",

                ),


                (

                    "FONTSIZE",

                    (0,0),

                    (-1,-1),

                    8,

                ),


                (

                    "LEADING",

                    (0,0),

                    (-1,-1),

                    10,

                ),

            ]

        )

    )


    return table


# ================================
# Generator
# ================================


class ChinesePortfolioReportGenerator:



    def __init__(self):


        self.output_file = OUTPUT_FILE


        self.styles = getSampleStyleSheet()



        # Chinese styles


        self.styles.add(

            ParagraphStyle(

                name="ChineseBody",

                parent=self.styles["BodyText"],

                fontName="STSong-Light",

                fontSize=11,

                leading=18,

            )

        )



        self.styles.add(

            ParagraphStyle(

                name="ChineseHeading",

                parent=self.styles["Heading1"],

                fontName="STSong-Light",

            )

        )



        self.styles.add(

            ParagraphStyle(

                name="ChineseTitle",

                parent=self.styles["Title"],

                fontName="STSong-Light",

            )

        )



    # ================================
    # Generate
    # ================================


    def generate(self):


        doc = SimpleDocTemplate(

            self.output_file,

            pagesize=letter

        )



        story = []



        # ----------------------------
        # Title
        # ----------------------------


        story.append(

            Paragraph(

                "多策略期权组合构建与风险管理框架",

                self.styles["ChineseTitle"]

            )

        )


        story.append(

            Spacer(

                1,

                25

            )

        )


        story.append(

            Paragraph(

                "量化研究报告 v1.0<br/>2026",

                self.styles["ChineseBody"]

            )

        )


        story.append(

            PageBreak()

        )



        # ----------------------------
        # Executive Summary
        # ----------------------------


        story.append(

            Paragraph(

                "摘要",

                self.styles["ChineseHeading"]

            )

        )


        summary = """

        本研究构建了一套端到端量化研究框架，用于多策略期权组合构建与风险管理。

        该框架覆盖期权策略设计、历史回测、组合优化以及波动率目标控制。

        在四种组合构建方法中，最大夏普组合表现出最优的风险调整收益，
        年化收益率达到37.98%，夏普比率达到2.53。

        风险平价组合取得了相近收益，同时具有略好的回撤控制能力。

        """


        story.append(

            Paragraph(

                summary,

                self.styles["ChineseBody"]

            )

        )



        story.append(

            PageBreak()

        )



        # ----------------------------
        # Overview
        # ----------------------------


        story.append(

            Paragraph(

                "1. 项目概述",

                self.styles["ChineseHeading"]

            )

        )


        text = """

        本项目开发了一套完整的期权量化研究框架。

        主要包括：

        <br/>

        - 期权策略构建<br/>

        - 历史回测分析<br/>

        - 策略收益评价<br/>

        - 投资组合优化<br/>

        - 波动率目标风险管理<br/>

        """


        story.append(

            Paragraph(

                text,

                self.styles["ChineseBody"]

            )

        )



        story.append(

            Spacer(

                1,

                20

            )

        )



        # ----------------------------
        # Data
        # ----------------------------


        story.append(

            Paragraph(

                "2. 数据说明",

                self.styles["ChineseHeading"]

            )

        )


        data_text = """

        数据基于指数期权历史交易结果。

        <br/>

        研究周期：2026年上半年

        <br/>

        策略频率：基于交易事件的策略评价

        <br/>

        策略包括：

        <br/>

        - 平值跨式策略

        <br/>

        - 看涨蝶式价差策略

        <br/>

        - 日历价差策略

        """


        story.append(

            Paragraph(

                data_text,

                self.styles["ChineseBody"]

            )

        )



        story.append(

            PageBreak()

        )



        # ----------------------------
        # Strategy
        # ----------------------------


        story.append(

            Paragraph(

                "3. 策略介绍",

                self.styles["ChineseHeading"]

            )

        )


        strategy = """

        <b>平值跨式策略</b><br/>

        通过同时买入看涨期权和看跌期权获得波动率收益。

        <br/><br/>

        <b>看涨蝶式价差策略</b><br/>

        具有有限风险和有限收益结构的方向性波动策略。

        <br/><br/>

        <b>日历价差策略</b><br/>

        利用不同到期期限期权之间的期限结构差异获取收益。

        """


        story.append(

            Paragraph(

                strategy,

                self.styles["ChineseBody"]

            )

        )



        story.append(

            PageBreak()

        )



        # ----------------------------
        # Allocation
        # ----------------------------


        story.append(

            Paragraph(

                "4. 组合配置结果",

                self.styles["ChineseHeading"]

            )

        )


        weights = pd.read_csv(

            os.path.join(

                TABLE_DIR,

                "portfolio_weights_table_cn.csv"

            )

        )


        story.append(

            dataframe_to_table(

                weights

            )

        )


        story.append(

            Spacer(

                1,

                20

            )

        )


        story.append(

            Image(

                os.path.join(

                    FIGURE_DIR,

                    "maximum_sharpe_allocation_cn.png"

                ),

                width=300,

                height=300

            )

        )



        story.append(

            PageBreak()

        )



        # ----------------------------
        # Performance
        # ----------------------------


        story.append(

            Paragraph(

                "5. 组合表现",

                self.styles["ChineseHeading"]

            )

        )


        performance = pd.read_csv(

            os.path.join(

                TABLE_DIR,

                "portfolio_performance_table_cn.csv"

            )

        )


        story.append(

            dataframe_to_table(

                performance

            )

        )



        story.append(

            Spacer(

                1,

                20

            )

        )


        story.append(

            Image(

                os.path.join(

                    FIGURE_DIR,

                    "portfolio_equity_curve_cn.png"

                ),

                width=400,

                height=250

            )

        )



        story.append(

            PageBreak()

        )



        # ----------------------------
        # Risk
        # ----------------------------


        story.append(

            Paragraph(

                "6. 风险分析",

                self.styles["ChineseHeading"]

            )

        )


        risk = """

        所有组合均经过波动率目标控制，使年化波动率调整至15%，

        从而保证不同组合构建方法之间具有可比性。

        """


        story.append(

            Paragraph(

                risk,

                self.styles["ChineseBody"]

            )

        )


        story.append(

            Image(

                os.path.join(

                    FIGURE_DIR,

                    "portfolio_drawdown_cn.png"

                ),

                width=400,

                height=250

            )

        )



        story.append(

            PageBreak()

        )



        # ----------------------------
        # Limitations
        # ----------------------------


        story.append(

            Paragraph(

                "7. 研究限制",

                self.styles["ChineseHeading"]

            )

        )


        limitations = """

        当前研究框架仍存在以下限制：

        <br/>

        - 未显式考虑交易成本和执行滑点；

        <br/>

        - 结果基于历史回测，不代表未来收益；

        <br/>

        - 市场环境变化可能影响策略有效性。

        """


        story.append(

            Paragraph(

                limitations,

                self.styles["ChineseBody"]

            )

        )



        # ----------------------------
        # Conclusion
        # ----------------------------


        story.append(

            Paragraph(

                "8. 结论",

                self.styles["ChineseHeading"]

            )

        )


        conclusion = """

        研究结果表明，最大夏普组合获得最高风险调整收益，

        风险平价组合在收益和风险控制之间实现了较好的平衡。

        多策略组合结合优化模型和波动率管理能够有效提升整体投资组合表现。

        """


        story.append(

            Paragraph(

                conclusion,

                self.styles["ChineseBody"]

            )

        )



        doc.build(

            story

        )


        return self.output_file



# ================================
# Main
# ================================


if __name__ == "__main__":


    generator = ChinesePortfolioReportGenerator()


    output = generator.generate()



    print("="*80)

    print(

        "中文研究报告生成完成"

    )

    print("="*80)


    print(output)