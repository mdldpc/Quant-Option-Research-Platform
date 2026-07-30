"""
Report Tables Generator v1.0

Convert portfolio research outputs
into formatted report tables.


Input:

research/portfolio/results/

    portfolio_weights_v1_1.csv

    portfolio_comparison_v1_1.csv


Output:

research/reports/tables/

    portfolio_weights_table.csv

    portfolio_performance_table.csv

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

    "research/reports/tables"

)



os.makedirs(

    OUTPUT_DIR,

    exist_ok=True

)



# =====================================================
# Table Generator
# =====================================================


class ReportTableGenerator:



    def __init__(

        self,

        input_dir=INPUT_DIR,

        output_dir=OUTPUT_DIR,

    ):


        self.input_dir = input_dir

        self.output_dir = output_dir



    # =================================================
    # Portfolio Weight Table
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



        # Convert decimals to percentage


        table = (

            df

            *

            100

        ).round(2)



        table.index.name = (

            "Strategy"

        )

        strategy_names = {

            "long_atm_strangle":
                "Long ATM Strangle",

            "long_call_butterfly":
                "Long Call Butterfly",

            "calendar_spread":
                "Calendar Spread",

        }


        table.index = [

            strategy_names.get(

                x,

                x

            )

            for x in table.index

        ]


        table.columns = [

            "Equal Weight",

            "Minimum Variance",

            "Maximum Sharpe",

            "Risk Parity",

        ]



        output = os.path.join(

            self.output_dir,

            "portfolio_weights_table.csv"

        )


        table.to_csv(

            output

        )



        return table



    # =================================================
    # Portfolio Performance Table
    # =================================================


    def generate_performance_table(self):


        file = os.path.join(

            self.input_dir,

            "portfolio_comparison_v1_1.csv"

        )


        df = pd.read_csv(

            file

        )



        # Keep scaled portfolio only

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

        ]

        portfolio_names = {

            "equal_weight":
                "Equal Weight",

            "minimum_variance":
                "Minimum Variance",

            "maximum_sharpe":
                "Maximum Sharpe",

            "risk_parity":
                "Risk Parity",

        }


        table["portfolio"] = (

            table["portfolio"]

            .map(

                portfolio_names

            )

        )

        # Convert ratios to %

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

            "Portfolio",

            "Total Return (%)",

            "Annual Return (%)",

            "Volatility (%)",

            "Sharpe Ratio",

            "Max Drawdown (%)",

        ]



        output = os.path.join(

            self.output_dir,

            "portfolio_performance_table.csv"

        )


        table.to_csv(

            output,

            index=False

        )



        return table



    # =================================================
    # Run All
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
# Standalone Execution
# =====================================================


if __name__ == "__main__":


    generator = ReportTableGenerator()



    tables = (

        generator

        .generate_all()

    )



    print("=" * 80)

    print(
        "Generated Report Tables"
    )

    print("=" * 80)



    print("\nPortfolio Weights:")

    print(

        tables["weights"]

    )



    print("\nPortfolio Performance:")

    print(

        tables["performance"]

    )