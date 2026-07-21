from pathlib import Path
import sys
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.append(
    str(PROJECT_ROOT)
)


from framework.runner import run_strategy_report



def main():


    trades = pd.DataFrame(

        {

            "trade_id":
            [
                1,
                2,
                3,
                4,
            ],


            "status":
            [
                "constructed",
                "constructed",
                "constructed",
                "constructed",
            ],


            "entry_butterfly_price":
            [
                10,
                12,
                8,
                15,
            ],


            "exit_butterfly_price":
            [
                13,
                9,
                11,
                18,
            ],

        }

    )


    output_dir = Path(
        "research/reports/long_call_butterfly"
    )


    result = run_strategy_report(

        strategy_name=
        "long_call_butterfly",


        trades=
        trades,


        report_path=
        output_dir
        /
        "report.docx",


        trades_path=
        output_dir
        /
        "trades.csv",

    )


    print(
        "Publication completed"
    )

    print(result)



if __name__ == "__main__":

    main()