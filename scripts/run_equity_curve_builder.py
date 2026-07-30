from pathlib import Path
import sys

sys.path.append(".")


import pandas as pd


from analysis.equity_curve_builder import (
    EquityCurveBuilder,
)



def main():


    strategies = {


        "long_atm_strangle":

        "research/exports/"
        "option_strategy_backtest_strangle_v1_1.csv",



        "long_call_butterfly":

        "research/exports/"
        "option_strategy_backtest_butterfly_v1_1.csv",



        "calendar_spread":

        "research/exports/"
        "option_strategy_backtest_calendar_v1_1.csv",

    }



    output_dir = Path(
        "research/portfolio/equity_curves"
    )


    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )



    for strategy, file in strategies.items():


        print("="*80)

        print(strategy)

        print("="*80)



        trades = pd.read_csv(file)



        builder = EquityCurveBuilder(

            trades,

            strategy,

        )


        curve = builder.build()



        output = (

            output_dir

            /

            f"{strategy}_equity_v1_0.csv"

        )


        curve.to_csv(

            output,

            index=False,

            encoding="utf-8-sig"

        )


        print(curve.head())

        print()

        print("Saved:")

        print(output)



if __name__ == "__main__":

    main()