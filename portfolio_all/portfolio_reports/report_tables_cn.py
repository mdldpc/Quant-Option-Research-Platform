"""
Chinese Report Tables Generator v1.0

Generate Chinese formatted tables
for Chinese PDF research report.

Input:

research/portfolio/results/

    portfolio_weights_v1_1.csv

    portfolio_comparison_v1_1.csv


Output:

research/reports/tables_cn/

    portfolio_weights_table_cn.csv

    portfolio_performance_table_cn.csv

"""


import os

import pandas as pd



# =====================================================
# Paths
# =====================================================


INPUT_DIR = (

    "research/portfolio/results"

)


OUTPUT_DIR = (

    "research/reports/tables_cn"

)


os.makedirs(

    OUTPUT_DIR,

    exist_ok=True

)



# =====================================================
# Translation Dictionary
# =====================================================


STRATEGY_NAMES = {


    "long_atm_strangle":

        "平值跨式策略",


    "long_call_butterfly":

        "看涨蝶式价差策略",


    "calendar_spread":

        "日历价差策略",

}



PORTFOLIO_NAMES = {


    "equal_weight":

        "等权重组合",


    "minimum_variance":

        "最小方差组合",


    "maximum_sharpe":

        "最大夏普组合",


    "risk_parity":

        "风险平价组合",

}



# =====================================================
# Generator
# =====================================================


class ChineseReportTableGenerator:



    def __init__(

        self,

        input_dir=INPUT_DIR,

        output_dir=OUTPUT_DIR,

    ):


        self.input_dir = input_dir

        self.output_dir = output_dir



    # =================================================
    # Weight Table
    # =================================================


    def generate_weight_table(self):


        file = os.path.join(

            self.input_dir,

            "portfolio_weights_v1_1.csv"

        )


        df = pd.read_csv(

            file,

            index_col=0

        )


        table = (

            df * 100

        ).round(2)



        table.index = [

            STRATEGY_NAMES.get(

                x,

                x

            )

            for x in table.index

        ]



        table.index.name = (

            "策略"

        )



        table.columns = [

            "等权重组合",

            "最小方差组合",

            "最大夏普组合",

            "风险平价组合",

        ]



        output = os.path.join(

            self.output_dir,

            "portfolio_weights_table_cn.csv"

        )


        table.to_csv(

            output,

            encoding="utf-8-sig"

        )


        return table



    # =================================================
    # Performance Table
    # =================================================


    def generate_performance_table(self):


        file = os.path.join(

            self.input_dir,

            "portfolio_comparison_v1_1.csv"

        )


        df = pd.read_csv(

            file

        )



        scaled = df[

            df["type"]

            ==

            "scaled"

        ].copy()



        table = scaled[

            [

                "portfolio",

                "total_return",

                "annual_return",

                "volatility",

                "sharpe_ratio",

                "max_drawdown",

            ]

        ].copy()



        table["portfolio"] = (

            table["portfolio"]

            .map(

                PORTFOLIO_NAMES

            )

        )



        # Percentage conversion


        for col in [

            "total_return",

            "annual_return",

            "volatility",

            "max_drawdown",

        ]:


            table[col] = (

                table[col]

                *

                100

            ).round(2)



        table["sharpe_ratio"] = (

            table["sharpe_ratio"]

            .round(2)

        )



        table.columns = [

            "组合",

            "总收益率(%)",

            "年化收益率(%)",

            "年化波动率(%)",

            "夏普比率",

            "最大回撤(%)",

        ]



        output = os.path.join(

            self.output_dir,

            "portfolio_performance_table_cn.csv"

        )


        table.to_csv(

            output,

            index=False,

            encoding="utf-8-sig"

        )


        return table



    # =================================================
    # Generate All
    # =================================================


    def generate_all(self):


        results = {}


        results["weights"] = (

            self.generate_weight_table()

        )


        results["performance"] = (

            self.generate_performance_table()

        )


        return results



# =====================================================
# Main
# =====================================================


if __name__ == "__main__":


    generator = ChineseReportTableGenerator()



    tables = generator.generate_all()



    print("=" * 80)

    print(

        "中文报告表格生成完成"

    )

    print("=" * 80)



    print("\n组合权重表:")

    print(

        tables["weights"]

    )



    print("\n组合表现表:")

    print(

        tables["performance"]

    )