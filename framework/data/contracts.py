from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OptionQuote:

    """
    Standard option market quote.

    Independent from raw data source.
    """


    symbol: str

    timestamp: datetime


    bid_price: Optional[float]

    ask_price: Optional[float]

    last_price: Optional[float]


    volume: Optional[int]

    open_interest: Optional[int]


@dataclass
class FuturesQuote:

    """
    Standard futures quote.
    """


    symbol: str

    timestamp: datetime


    last_price: Optional[float]


    volume: Optional[int]

    open_interest: Optional[int]