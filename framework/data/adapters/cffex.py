import pandas as pd


class CFFEXAdapter:
    """
    Adapter for CFFEX option/futures market data.

    Convert exchange-specific columns
    into standardized market schema.
    """

    OPTION_MAPPING = {

        "symbol": "symbol",

        "iRecvTime": "timestamp",

        "BP1": "bid_price",

        "AP1": "ask_price",

        "lastPrice": "last_price",

        "volume": "volume",

        "openInterest": "open_interest",

    }


    FUTURES_MAPPING = {

        "symbol": "symbol",

        "iRecvTime": "timestamp",

        "lastPrice": "last_price",

        "volume": "volume",

        "openInterest": "open_interest",

    }


    @staticmethod
    def normalize_option(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize CFFEX option dataframe.
        """

        result = (
            df[
                list(
                    CFFEXAdapter.OPTION_MAPPING.keys()
                )
            ]
            .rename(
                columns=
                CFFEXAdapter.OPTION_MAPPING
            )
            .copy()
        )


        return result

    @staticmethod
    def read_option_file(
        path,
    ) -> pd.DataFrame:
        """
        Read CFFEX option csv.xz file
        and normalize columns.

        Parameters
        ----------
        path:
            Raw CFFEX option file.

        Returns
        -------
        pd.DataFrame
            Standardized option market data.
        """


        df = pd.read_csv(
            path,
            compression="xz",
        )


        return CFFEXAdapter.normalize_option(
            df
        )

    @staticmethod
    def normalize_future(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize CFFEX futures dataframe.
        """

        result = (
            df[
                list(
                    CFFEXAdapter.FUTURES_MAPPING.keys()
                )
            ]
            .rename(
                columns=
                CFFEXAdapter.FUTURES_MAPPING
            )
            .copy()
        )


        return result