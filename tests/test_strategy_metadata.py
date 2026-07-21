from config.strategy_metadata import STRATEGY_METADATA



def test_strategy_metadata():

    meta = STRATEGY_METADATA[
        "long_call_butterfly"
    ]


    assert (
        meta["display_name"]
        ==
        "Long Call Butterfly"
    )


    assert (
        len(meta["description"]) > 0
    )