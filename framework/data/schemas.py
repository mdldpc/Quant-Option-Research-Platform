from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class OptionMarketSchema:
    """
    Standardized option market dataframe schema.

    Independent from exchange source.
    """


    required_columns: List[str] = None


    def columns(self):

        if self.required_columns is not None:
            return self.required_columns


        return [

            "symbol",

            "timestamp",

            "bid_price",

            "ask_price",

            "last_price",

            "volume",

            "open_interest",

        ]



@dataclass(frozen=True)
class FuturesMarketSchema:
    """
    Standardized futures dataframe schema.
    """


    required_columns: List[str] = None


    def columns(self):

        if self.required_columns is not None:
            return self.required_columns


        return [

            "symbol",

            "timestamp",

            "last_price",

            "volume",

            "open_interest",

        ]
    
    def validate_schema(
        df,
        schema
    ):
        """
        Validate dataframe against schema.
        """

        missing = [
            c
            for c in schema.columns()
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        return True