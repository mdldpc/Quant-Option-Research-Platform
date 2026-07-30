from framework.strategy.strategy_registry import (
    list_strategies,
    get_strategy,
)


def test_list_strategies():

    strategies = list_strategies()

    assert "long_atm_strangle" in strategies
    assert "long_call_butterfly" in strategies
    assert "calendar_spread" in strategies



def test_get_strategy():

    config = get_strategy(
        "long_atm_strangle"
    )

    assert "constructor" in config
    assert "backtester" in config


def test_butterfly_has_signal():

    config = get_strategy(
        "long_call_butterfly"
    )

    assert (
        config["signal_generator"]
        is not None
    )