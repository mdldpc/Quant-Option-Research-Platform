from framework.registry import (
    get_backtester,
)


from framework.strategy.backtesters.butterfly import (
    ButterflyBacktester,
)


from framework.registry import get_backtester



def test_strategy_backtester_mapping():

    cls = get_backtester(
        "long_call_butterfly"
    )


    assert cls == ButterflyBacktester


def test_straddle_backtester_registered():

    cls = get_backtester(
        "long_atm_straddle"
    )


    assert cls.__name__ == "StraddleBacktester"