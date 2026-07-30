from framework.data.adapters.symbol import (
    OptionSymbolParser,
)


def test_parse_call_option():

    result = (
        OptionSymbolParser
        .parse(
            "IO2502-C-3850"
        )
    )


    assert result["underlying"] == "IO"

    assert result["expiry"] == "2502"

    assert result["option_type"] == "C"

    assert result["strike"] == 3850



def test_parse_put_option():

    result = (
        OptionSymbolParser
        .parse(
            "IO2506-P-4200"
        )
    )


    assert result["underlying"] == "IO"

    assert result["option_type"] == "P"

    assert result["strike"] == 4200