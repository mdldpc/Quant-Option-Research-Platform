import pandas as pd

from framework.strategy.signals.butterfly_signal import (
    ButterflySignalGenerator,
)


def test_butterfly_signal():


    df = pd.DataFrame({

        "trade_date":[
            20260101+i
            for i in range(30)
        ],

        "butterfly_price":[
            10
        ]*20
        +
        [
            5
        ]*10,

    })


    generator = ButterflySignalGenerator(
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