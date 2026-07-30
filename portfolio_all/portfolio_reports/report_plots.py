"""
Report Plot Generator v1.0

Generate figures for portfolio research report.

Figures:

1. Portfolio equity curves
2. Maximum Sharpe allocation
3. Portfolio drawdown

"""


import os

import pandas as pd

import matplotlib.pyplot as plt



# =====================================================
# Paths
# =====================================================


RESULT_DIR = (

    "research/portfolio/results"

)


FIGURE_DIR = (

    "research/reports/figures"

)



os.makedirs(

    FIGURE_DIR,

    exist_ok=True

)



# =====================================================
# Plot Generator
# =====================================================


class ReportPlotGenerator:



    def __init__(

        self,

        result_dir=RESULT_DIR,

        figure_dir=FIGURE_DIR,

    ):


        self.result_dir = result_dir

        self.figure_dir = figure_dir



    # =================================================
    # 1. Equity Curve
    # =================================================


    def plot_equity_curve(self):


        portfolios = {

            "equal_weight":
                "Equal Weight",

            "minimum_variance":
                "Minimum Variance",

            "maximum_sharpe":
                "Maximum Sharpe",

            "risk_parity":
                "Risk Parity",

        }



        plt.figure(

            figsize=(10,6)

        )



        for portfolio, label in portfolios.items():


            file = os.path.join(

                self.result_dir,

                f"{portfolio}_scaled_equity_v1_1.csv"

            )



            df = pd.read_csv(

                file,

                index_col=0

            )



            # equity column

            plt.plot(

                df.index,

                df["equity"],

                label=label,

            )



        plt.title(

            "Risk-Scaled Portfolio Equity Curve"

        )


        plt.xlabel(

            "Trading Day"

        )


        plt.ylabel(

            "Equity"

        )


        plt.legend()



        plt.grid(

            True

        )



        output = os.path.join(

            self.figure_dir,

            "portfolio_equity_curve.png"

        )



        plt.savefig(

            output,

            dpi=300,

            bbox_inches="tight"

        )


        plt.close()



        return output



    # =================================================
    # 2. Maximum Sharpe Allocation
    # =================================================


    def plot_max_sharpe_allocation(self):


        file = os.path.join(

            self.result_dir,

            "portfolio_weights_v1_1.csv"

        )


        df = pd.read_csv(

            file,

            index_col=0

        )



        weights = df[

            "maximum_sharpe"

        ]

        strategy_names = {

            "long_atm_strangle":
                "Long ATM Strangle",

            "long_call_butterfly":
                "Long Call Butterfly",

            "calendar_spread":
                "Calendar Spread",

        }


        weights.index = [

            strategy_names.get(

                x,

                x

            )

            for x in weights.index

        ]

        plt.figure(

            figsize=(7,7)

        )



        plt.pie(

            weights.values,

            labels=weights.index,

            autopct="%1.1f%%",

        )



        plt.title(

            "Maximum Sharpe Portfolio Allocation"

        )



        output = os.path.join(

            self.figure_dir,

            "maximum_sharpe_allocation.png"

        )



        plt.savefig(

            output,

            dpi=300,

            bbox_inches="tight"

        )


        plt.close()



        return output



    # =================================================
    # 3. Drawdown Curve
    # =================================================


    def plot_drawdown(self):


        portfolios = {

            "equal_weight":
                "Equal Weight",

            "minimum_variance":
                "Minimum Variance",

            "maximum_sharpe":
                "Maximum Sharpe",

            "risk_parity":
                "Risk Parity",

        }



        plt.figure(

            figsize=(10,6)

        )



        for portfolio, label in portfolios.items():


            file = os.path.join(

                self.result_dir,

                f"{portfolio}_scaled_equity_v1_1.csv"

            )



            df = pd.read_csv(

                file,

                index_col=0

            )


            equity = df[

                "equity"

            ]



            drawdown = (

                equity

                /

                equity.cummax()

                -

                1

            )



            plt.plot(

                drawdown.index,

                drawdown,

                label=label,

            )



        plt.title(

            "Portfolio Drawdown"

        )


        plt.xlabel(

            "Trading Day"

        )


        plt.ylabel(

            "Drawdown"

        )


        plt.legend()



        plt.grid(

            True

        )



        output = os.path.join(

            self.figure_dir,

            "portfolio_drawdown.png"

        )


        plt.savefig(

            output,

            dpi=300,

            bbox_inches="tight"

        )


        plt.close()



        return output



    # =================================================
    # Generate All
    # =================================================


    def generate_all(self):


        results = {}


        results["equity_curve"] = (

            self.plot_equity_curve()

        )


        results["allocation"] = (

            self.plot_max_sharpe_allocation()

        )


        results["drawdown"] = (

            self.plot_drawdown()

        )


        return results



# =====================================================
# Standalone Execution
# =====================================================


if __name__ == "__main__":


    generator = ReportPlotGenerator()



    outputs = (

        generator

        .generate_all()

    )



    print("=" * 80)

    print(

        "Generated Report Figures"

    )

    print("=" * 80)



    for name, path in outputs.items():

        print(

            f"{name}: {path}"

        )