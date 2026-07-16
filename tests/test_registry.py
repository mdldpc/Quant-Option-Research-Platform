from framework.registry import (
    get_backtester,
)


from framework.strategy.backtesters.butterfly import (
    ButterflyBacktester,
)



def test_strategy_backtester_mapping():

    cls = get_backtester(
        "long_call_butterfly"
    )


    assert cls == ButterflyBacktester