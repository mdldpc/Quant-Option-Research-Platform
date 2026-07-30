"""
Terminal Price Loader v1.1

Load the last available valid option market price
before or on target date.

Priority:

1. lastPrice > 0

2. Mid quote:
       (BP1 + AP1) / 2

3. Otherwise search previous trading day
"""


from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd




class TerminalPriceLoader:



    def __init__(
        self,
        data_dir
    ):

        self.data_dir = Path(
            data_dir
        )



    # --------------------------------------------------
    # Build daily file path
    # --------------------------------------------------

    def _file_path(
        self,
        date
    ):

        return (
            self.data_dir
            /
            f"CFFEX.IF.{date}.csv.xz"
        )



    # --------------------------------------------------
    # Find price from one day
    # --------------------------------------------------

    def _find_price_on_date(
        self,
        symbol,
        date
    ):


        file = self._file_path(
            date
        )


        if not file.exists():

            return None



        df = pd.read_csv(

            file,

            compression="xz",

            usecols=[

                "symbol",

                "lastPrice",

                "BP1",

                "AP1",

            ]

        )



        target_symbol = (
            str(symbol)
            .strip()
        )


        df["symbol"] = (
            df["symbol"]
            .astype(str)
            .str.strip()
        )


        result = df[
            df["symbol"]
            ==
            target_symbol
        ]



        if result.empty:

            return None



        # ------------------------------------------
        # 1. Try last traded price
        # ------------------------------------------

        last_prices = (
            result["lastPrice"]
            .astype(float)
        )


        valid_last = last_prices[
            last_prices > 0
        ]


        if not valid_last.empty:


            return {

                "price":
                    float(
                        valid_last.iloc[-1]
                    ),

                "source":
                    "lastPrice"

            }



        # ------------------------------------------
        # 2. Try mid quote
        # ------------------------------------------

        bp = (
            result["BP1"]
            .astype(float)
        )


        ap = (
            result["AP1"]
            .astype(float)
        )



        mid = (
            (bp + ap)
            /
            2
        )



        valid_mid = mid[
            mid > 0
        ]



        if not valid_mid.empty:


            return {

                "price":
                    float(
                        valid_mid.iloc[-1]
                    ),

                "source":
                    "mid_quote"

            }



        # ------------------------------------------
        # No valid price
        # ------------------------------------------

        return None



    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def get_terminal_price(
        self,
        symbol,
        target_date,
        max_search_days=30
    ):


        """
        Search backward for terminal option price.

        Parameters
        ----------
        symbol:
            IO option symbol

        target_date:
            YYYYMMDD

        Returns
        -------

        {
            symbol,
            valuation_date,
            terminal_price,
            price_source
        }

        """



        dt = datetime.strptime(

            str(target_date),

            "%Y%m%d"

        )



        for i in range(
            max_search_days + 1
        ):



            current = (

                dt

                -

                timedelta(days=i)

            )



            date_str = (

                current

                .strftime("%Y%m%d")

            )



            result = (

                self
                ._find_price_on_date(

                    symbol,

                    date_str

                )

            )



            if result is not None:



                return {


                    "symbol":

                        str(symbol)
                        .strip(),



                    "valuation_date":

                        date_str,



                    "terminal_price":

                        result["price"],



                    "price_source":

                        result["source"],


                }



        raise ValueError(

            f"No valid terminal price found for {symbol}"

        )