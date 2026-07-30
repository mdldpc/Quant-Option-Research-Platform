import re


class OptionSymbolParser:
    """
    Parse CFFEX option symbols.

    Example:

    IO2502-C-3850

    """

    PATTERN = re.compile(
        r"([A-Z]+)(\d{4})-([CP])-(\d+)"
    )


    @staticmethod
    def parse(symbol: str):

        match = (
            OptionSymbolParser
            .PATTERN
            .match(symbol)
        )


        if not match:
            raise ValueError(
                f"Invalid option symbol: {symbol}"
            )


        underlying = match.group(1)

        expiry = match.group(2)

        option_type = match.group(3)

        strike = int(
            match.group(4)
        )


        return {

            "underlying":
                underlying,

            "expiry":
                expiry,

            "option_type":
                option_type,

            "strike":
                strike,

        }