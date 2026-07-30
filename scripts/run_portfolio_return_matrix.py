from pathlib import Path
import sys


sys.path.append(".")


from analysis.portfolio_return_matrix import (
    PortfolioReturnMatrix,
)



def main():


    configs = {


        "long_atm_strangle":

        {

            "trade_file":

            "research/exports/option_strategy_backtest_strangle_v1_1.csv",


            "snapshot":

            "research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet"

        },



        "long_call_butterfly":

        {

            "trade_file":

            "research/exports/option_strategy_backtest_butterfly_v1_1.csv",


            "snapshot":

            "research/datasets/butterfly_daily_snapshot_2026H1_v1_1.parquet"

        },



        "calendar_spread":

        {

            "trade_file":

            "research/exports/option_strategy_backtest_calendar_v1_1.csv",


            "snapshot":

            "research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet"

        },

    }



    print("="*80)

    print(
        "Building strategy return matrix"
    )

    print("="*80)



    builder = PortfolioReturnMatrix(
        configs
    )


    matrix = builder.build()



    output = Path(
        "research/portfolio/"
        "strategy_return_matrix_v1_0.csv"
    )


    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )



    matrix.to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )



    print("\nResult")

    print("-"*80)

    print(matrix.head())


    print("\nShape:")

    print(
        matrix.shape
    )


    print("\nSaved:")

    print(
        output
    )



if __name__ == "__main__":

    main()