from pathlib import Path
import pandas as pd


import sys

sys.path.append(".")



from analysis.evaluation_report import (
    EvaluationReport,
)



EXPORT_DIR = Path(
    "research/exports"
)


REPORT_DIR = Path(
    "research/reports"
)



STRATEGIES = {


    "long_atm_strangle":

    "option_strategy_backtest_strangle_v1_1.csv",



    "long_call_butterfly":

    "option_strategy_backtest_butterfly_v1_1.csv",



    "calendar_spread":

    "option_strategy_backtest_calendar_v1_1.csv",

}





def run():


    results = []


    for strategy, file in STRATEGIES.items():


        print("\n" + "="*80)

        print(strategy)


        path = (
            EXPORT_DIR
            /
            file
        )


        trades = pd.read_csv(
            path
        )


        print(
            "Trades:",
            len(trades)
        )


        report = (
            EvaluationReport
            .generate(
                trades
            )
        )


        results.append(
            report
        )



    df = pd.DataFrame(
        results
    )


    output = (
        REPORT_DIR
        /
        "strategy_evaluation_report_v1_1.csv"
    )


    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )


    print("\n" + "="*80)

    print(
        "Final Evaluation Report"
    )

    print(df)


    print("\nSaved:")

    print(output)



if __name__ == "__main__":

    run()