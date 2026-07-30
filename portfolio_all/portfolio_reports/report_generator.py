"""
Portfolio Research Report Generator v1.1

Generate final research PDF report.

Upgrade from v1.0:

- Executive Summary
- Data Description
- Research Limitations
- Improved presentation wording


Output:

research/reports/

portfolio_research_report_v1_1.pdf

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


from reportlab.lib.styles import getSampleStyleSheet


from reportlab.lib.pagesizes import letter



# =====================================================
# Paths
# =====================================================


REPORT_DIR = "research/reports"

TABLE_DIR = "research/reports/tables"

FIGURE_DIR = "research/reports/figures"



OUTPUT_FILE = os.path.join(

    REPORT_DIR,

    "portfolio_research_report_v1_1_final.pdf"

)



# =====================================================
# Helper
# =====================================================


def dataframe_to_table(df):


    data = [

        list(df.columns)

    ] + df.values.tolist()



    table = Table(

        data,

        repeatRows=1

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

            ]

        )

    )


    return table



# =====================================================
# Generator
# =====================================================


class PortfolioReportGenerator:



    def __init__(

        self,

        output_file=OUTPUT_FILE,

    ):


        self.output_file = output_file


        self.styles = getSampleStyleSheet()



    # =================================================
    # Generate
    # =================================================


    def generate(self):


        doc = SimpleDocTemplate(

            self.output_file,

            pagesize=letter

        )


        story = []



        # =================================================
        # Title
        # =================================================


        story.append(

            Paragraph(

                "Multi-Strategy Option Portfolio Construction<br/>"
                "and Risk Management Framework",

                self.styles["Title"]

            )

        )


        story.append(

            Spacer(

                1,

                20

            )

        )


        story.append(

            Paragraph(

                "Research Report v1.1<br/>"
                "2026",

                self.styles["Heading2"]

            )

        )



        story.append(

            Spacer(

                1,

                30

            )

        )



        # =================================================
        # Executive Summary
        # =================================================


        story.append(

            Paragraph(

                "Executive Summary",

                self.styles["Heading1"]

            )

        )


        summary = """

        This research develops an end-to-end quantitative framework
        for multi-strategy option portfolio construction.

        The framework integrates option strategy design, historical
        backtesting, portfolio optimization, and volatility-targeted
        risk management.

        Among evaluated portfolio methods, the Maximum Sharpe portfolio
        achieved the strongest risk-adjusted performance after volatility
        scaling, reaching an annualized return of 37.98% and a Sharpe ratio
        of 2.53.

        Risk Parity produced comparable performance with slightly improved
        drawdown characteristics.

        """


        story.append(

            Paragraph(

                summary,

                self.styles["BodyText"]

            )

        )


        story.append(

            PageBreak()

        )



        # =================================================
        # Overview
        # =================================================


        story.append(

            Paragraph(

                "1. Project Overview",

                self.styles["Heading1"]

            )

        )


        overview = """

        This project develops an end-to-end quantitative research framework
        for option strategy analysis.

        The framework covers:

        <br/><br/>

        - Option strategy construction<br/>
        - Historical backtesting<br/>
        - Strategy performance analysis<br/>
        - Portfolio optimization<br/>
        - Volatility-targeted risk management<br/>

        """


        story.append(

            Paragraph(

                overview,

                self.styles["BodyText"]

            )

        )



        story.append(

            Spacer(

                1,

                20

            )

        )



        # =================================================
        # Data Description
        # =================================================


        story.append(

            Paragraph(

                "2. Data Description",

                self.styles["Heading1"]

            )

        )


        data_text = """

        The research evaluates index option strategies using historical
        market data.

        <br/><br/>

        Dataset characteristics:

        <br/><br/>

        Underlying: Index Options<br/>

        Evaluation Period: 2026 H1<br/>

        Strategy Frequency: Trade-based evaluation<br/>

        Strategies: Long ATM Strangle, Long Call Butterfly,
        Calendar Spread

        """


        story.append(

            Paragraph(

                data_text,

                self.styles["BodyText"]

            )

        )



        story.append(

            PageBreak()

        )



        # =================================================
        # Strategy
        # =================================================


        story.append(

            Paragraph(

                "3. Strategy Overview",

                self.styles["Heading1"]

            )

        )


        strategy_text = """

        <b>Long ATM Strangle</b><br/>

        A long volatility strategy using simultaneous call and put positions.

        <br/><br/>


        <b>Long Call Butterfly</b><br/>

        A limited-risk directional volatility strategy with defined payoff.

        <br/><br/>


        <b>Calendar Spread</b><br/>

        A maturity spread strategy capturing differences in option term
        structure.

        """


        story.append(

            Paragraph(

                strategy_text,

                self.styles["BodyText"]

            )

        )



        story.append(

            PageBreak()

        )



        # =================================================
        # Methodology
        # =================================================


        story.append(

            Paragraph(

                "4. Portfolio Construction Methodology",

                self.styles["Heading1"]

            )

        )


        methodology = """

        Four portfolio construction approaches are evaluated:

        <br/><br/>

        <b>Equal Weight</b><br/>
        Equal capital allocation across strategies.

        <br/><br/>

        <b>Minimum Variance</b><br/>
        Portfolio variance minimization.

        <br/><br/>

        <b>Maximum Sharpe</b><br/>
        Optimization of risk-adjusted return.

        <br/><br/>

        <b>Risk Parity</b><br/>
        Equal contribution of portfolio risk.

        """


        story.append(

            Paragraph(

                methodology,

                self.styles["BodyText"]

            )

        )



        # =================================================
        # Allocation
        # =================================================


        story.append(

            Spacer(

                1,

                20

            )

        )


        story.append(

            Paragraph(

                "5. Portfolio Allocation Results",

                self.styles["Heading1"]

            )

        )


        weight_file = os.path.join(

            TABLE_DIR,

            "portfolio_weights_table.csv"

        )


        weights = pd.read_csv(

            weight_file,

            index_col=0

        )


        story.append(

            dataframe_to_table(

                weights.reset_index()

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

                    "maximum_sharpe_allocation.png"

                ),

                width=350,

                height=350

            )

        )



        story.append(

            PageBreak()

        )



        # =================================================
        # Performance
        # =================================================


        story.append(

            Paragraph(

                "6. Portfolio Performance",

                self.styles["Heading1"]

            )

        )


        performance = pd.read_csv(

            os.path.join(

                TABLE_DIR,

                "portfolio_performance_table.csv"

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

                    "portfolio_equity_curve.png"

                ),

                width=450,

                height=280

            )

        )



        story.append(

            PageBreak()

        )



        # =================================================
        # Risk
        # =================================================


        story.append(

            Paragraph(

                "7. Risk Analysis",

                self.styles["Heading1"]

            )

        )


        story.append(

            Paragraph(

                """

                All portfolios are scaled to a target annualized volatility
                of 15%, allowing comparison across different portfolio
                construction methods.

                """,

                self.styles["BodyText"]

            )

        )


        story.append(

            Image(

                os.path.join(

                    FIGURE_DIR,

                    "portfolio_drawdown.png"

                ),

                width=450,

                height=280

            )

        )



        story.append(

            PageBreak()

        )



        # =================================================
        # Limitations
        # =================================================


        story.append(

            Paragraph(

                "8. Research Limitations",

                self.styles["Heading1"]

            )

        )


        limitations = """

        The current framework represents a research prototype.

        <br/><br/>

        Key limitations:

        <br/><br/>

        - Transaction costs and execution slippage are not explicitly modeled.<br/>

        - Results are based on historical backtesting and may not represent
          future performance.<br/>

        - Market regime changes may affect strategy effectiveness.

        """


        story.append(

            Paragraph(

                limitations,

                self.styles["BodyText"]

            )

        )



        # =================================================
        # Conclusion
        # =================================================


        story.append(

            Paragraph(

                "9. Conclusion",

                self.styles["Heading1"]

            )

        )


        conclusion = """

        The Maximum Sharpe portfolio achieved the strongest risk-adjusted
        performance among evaluated approaches.

        Risk Parity provided comparable returns with slightly improved
        downside characteristics.

        The results demonstrate the effectiveness of combining multiple
        option strategies with portfolio optimization and volatility
        targeting.

        """


        story.append(

            Paragraph(

                conclusion,

                self.styles["BodyText"]

            )

        )



        doc.build(

            story

        )


        return self.output_file



# =====================================================
# Main
# =====================================================


if __name__ == "__main__":


    generator = PortfolioReportGenerator()


    output = generator.generate()



    print("="*80)

    print(

        "Generated Portfolio Research Report v1.1 final"

    )

    print("="*80)

    print(output)