"""
Chinese Report Plot Generator v1.0

Generate Chinese figures
for Chinese PDF research report.


Output:

research/reports/figures_cn/

    maximum_sharpe_allocation_cn.png

    portfolio_equity_curve_cn.png

    portfolio_drawdown_cn.png

"""


import os


import pandas as pd


import matplotlib.pyplot as plt


from matplotlib import font_manager



# =====================================================
# Font Configuration
# =====================================================


def configure_chinese_font():


    possible_fonts = [

        r"C:\Windows\Fonts\msyh.ttc",

        r"C:\Windows\Fonts\simhei.ttf",

        r"C:\Windows\Fonts\simsun.ttc",

    ]


    for font in possible_fonts:


        if os.path.exists(font):


            font_manager.fontManager.addfont(

                font

            )


            font_name = (

                font_manager.FontProperties(

                    fname=font

                )

                .get_name()

            )


            plt.rcParams["font.sans-serif"] = [

                font_name

            ]


            plt.rcParams["axes.unicode_minus"] = False


            print(

                f"Using Chinese font: {font_name}"

            )


            return



    print(

        "Warning: Chinese font not found."

    )



configure_chinese_font()



# =====================================================
# Paths
# =====================================================


RESULT_DIR = (

    "research/portfolio/results"

)


OUTPUT_DIR = (

    "research/reports/figures_cn"

)


os.makedirs(

    OUTPUT_DIR,

    exist_ok=True

)



# =====================================================
# Names
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
# 1. Allocation Pie Chart
# =====================================================


def plot_allocation():



    file = os.path.join(

        RESULT_DIR,

        "portfolio_weights_v1_1.csv"

    )


    df = pd.read_csv(

        file,

        index_col=0

    )


    weights = (

        df["maximum_sharpe"]

        *

        100

    )


    weights.index = [

        STRATEGY_NAMES.get(

            x,

            x

        )

        for x in weights.index

    ]



    plt.figure(

        figsize=(8,8)

    )


    plt.pie(

        weights,

        labels=weights.index,

        autopct="%1.1f%%",

    )


    plt.title(

        "最大夏普组合资产配置",

        fontsize=16

    )


    output = os.path.join(

        OUTPUT_DIR,

        "maximum_sharpe_allocation_cn.png"

    )


    plt.savefig(

        output,

        dpi=300,

        bbox_inches="tight"

    )


    plt.close()



    return output



# =====================================================
# 2. Equity Curve
# =====================================================


def plot_equity_curve():



    portfolios = {


        "equal_weight":

            "等权重组合",


        "minimum_variance":

            "最小方差组合",


        "maximum_sharpe":

            "最大夏普组合",


        "risk_parity":

            "风险平价组合",

    }



    plt.figure(

        figsize=(10,6)

    )



    for key, label in portfolios.items():


        file = os.path.join(

            RESULT_DIR,

            f"{key}_scaled_equity_v1_1.csv"

        )


        df = pd.read_csv(

            file

        )


        plt.plot(

            df.index,

            df["equity"],

            label=label,

        )



    plt.title(

        "风险调整后组合净值曲线",

        fontsize=16

    )


    plt.xlabel(

        "交易日"

    )


    plt.ylabel(

        "组合净值"

    )


    plt.legend()



    plt.grid(

        True

    )


    output = os.path.join(

        OUTPUT_DIR,

        "portfolio_equity_curve_cn.png"

    )


    plt.savefig(

        output,

        dpi=300,

        bbox_inches="tight"

    )


    plt.close()



    return output



# =====================================================
# 3. Drawdown
# =====================================================


def plot_drawdown():



    portfolios = {


        "equal_weight":

            "等权重组合",


        "minimum_variance":

            "最小方差组合",


        "maximum_sharpe":

            "最大夏普组合",


        "risk_parity":

            "风险平价组合",

    }



    plt.figure(

        figsize=(10,6)

    )



    for key, label in portfolios.items():


        file = os.path.join(

            RESULT_DIR,

            f"{key}_scaled_equity_v1_1.csv"

        )


        df = pd.read_csv(

            file

        )


        equity = df["equity"]


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

        "组合最大回撤分析",

        fontsize=16

    )


    plt.xlabel(

        "交易日"

    )


    plt.ylabel(

        "回撤"

    )
    plt.tight_layout()

    plt.legend()



    plt.grid(

        True

    )



    output = os.path.join(

        OUTPUT_DIR,

        "portfolio_drawdown_cn.png"

    )


    plt.savefig(

        output,

        dpi=300,

        bbox_inches="tight",

        pad_inches = 0.2
    )


    plt.close()



    return output



# =====================================================
# Main
# =====================================================


if __name__ == "__main__":



    print("="*80)

    print(

        "中文报告图表生成完成"

    )

    print("="*80)



    print(

        "Allocation:",

        plot_allocation()

    )


    print(

        "Equity Curve:",

        plot_equity_curve()

    )


    print(

        "Drawdown:",

        plot_drawdown()

    )