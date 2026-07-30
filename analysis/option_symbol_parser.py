"""
Option Symbol Parser

Parse CFFEX IO option symbols.

Example:
IO2601-C-4000 
"""


class OptionSymbolParser:


    @staticmethod
    def parse(symbol):

        if symbol is None:
            raise ValueError(
                "symbol is None"
            )


        symbol = str(symbol).strip()


        parts = symbol.split("-")


        if len(parts) != 3:
            raise ValueError(
                f"Invalid option symbol: {symbol}"
            )


        contract, option_type, strike = parts


        if not contract.startswith("IO"):

            raise ValueError(
                f"Unsupported underlying: {contract}"
            )


        return {

            "underlying":
                contract[:2],


            "expiry":
                contract[2:],


            "option_type":
                option_type,


            "strike":
                float(strike),

        }