import pandas as pd


from analysis.signal_backtest_sensitivity import (
    SignalBacktestSensitivity,
)



def test_import():

    assert SignalBacktestSensitivity is not None



def test_empty_threshold():

    config={

        "signal_input":
            None,

        "snapshot":
            None,

    }


    obj=SignalBacktestSensitivity(
        config
    )


    assert obj.config == config