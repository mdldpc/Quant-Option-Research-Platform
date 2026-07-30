import pandas as pd

from framework.strategy.signals.calendar_signal import (
    CalendarSignalGenerator,
)


def test_calendar_signal():


    df = pd.DataFrame({

        "trade_date":[
            20260101+i
            for i in range(30)
        ],

        "iv_spread":[
            0.10
        ]*20
        +
        [
            -0.10
        ]*10,

    })


    generator = CalendarSignalGenerator(
        max_holding_days=5
    )


    signals = generator.generate(df)


    assert isinstance(
        signals,
        pd.DataFrame
    )


    assert (
        "entry_date"
        in signals.columns
    )


    assert (
        "exit_date"
        in signals.columns
    )