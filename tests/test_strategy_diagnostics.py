import pandas as pd

from analysis.strategy_diagnostics import (
    StrategyDiagnostics,
)



def test_signal_statistics():

    df = pd.DataFrame(
        {
            "signal_score":[
                10,
                50,
                70,
                20,
            ],

            "long_signal":[
                0,
                1,
                1,
                0,
            ]
        }
    )


    diag = StrategyDiagnostics(
        df
    )


    result = diag.signal_statistics()


    assert result["total_days"] == 4

    assert result["signal_days"] == 2

    assert result["signal_frequency"] == 0.5



def test_threshold_analysis():

    df = pd.DataFrame(
        {
            "signal_score":[
                10,
                30,
                50,
                70,
            ],

            "long_signal":[
                0,
                0,
                1,
                1,
            ]
        }
    )


    diag = StrategyDiagnostics(
        df
    )


    result = diag.threshold_analysis(
        thresholds=[20,50]
    )


    assert len(result)==2

    assert result.iloc[0]["signal_days"] == 3

    assert result.iloc[1]["signal_days"] == 2