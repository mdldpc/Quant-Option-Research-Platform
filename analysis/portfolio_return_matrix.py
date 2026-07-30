"""
Portfolio Return Matrix Builder

Convert multiple strategy return series
into unified daily return matrix.

Output format:

trade_date | strategy_1 | strategy_2 | ...

Example:

20260119 | 0.01 | 0.00 | 0.00

"""

import pandas as pd


from analysis.strategy_return_series import (
    StrategyReturnBuilder,
)



class PortfolioReturnMatrix:


    def __init__(
        self,
        strategy_configs,
        start_date="20260102",
        end_date="20260610",
    ):

        self.strategy_configs = strategy_configs

        self.start_date = start_date

        self.end_date = end_date



    # ==================================================
    # Build matrix
    # ==================================================

    def build(self):


        series_list = []



        # ----------------------------------------------
        # Generate each strategy return series
        # ----------------------------------------------

        for strategy, config in self.strategy_configs.items():


            print(
                f"\nBuilding strategy return: {strategy}"
            )


            trades = pd.read_csv(

                config["trade_file"]

            )


            snapshot = pd.read_parquet(

                config["snapshot"]

            )



            builder = StrategyReturnBuilder(

                trades,

                snapshot,

            )


            result = builder.build()



            if result.empty:

                continue



            result = result[

                [
                    "trade_date",
                    "return",
                ]

            ]



            result = result.rename(

                columns={

                    "return":
                    strategy

                }

            )



            series_list.append(

                result

            )



        if not series_list:


            return pd.DataFrame()



        # ----------------------------------------------
        # Merge strategies
        # ----------------------------------------------

        matrix = series_list[0]



        for series in series_list[1:]:


            matrix = matrix.merge(

                series,

                on="trade_date",

                how="outer",

            )



        # ----------------------------------------------
        # Trading calendar alignment
        # ----------------------------------------------

        calendar = pd.DataFrame(

            {

                "trade_date":

                pd.date_range(

                    start=

                    pd.to_datetime(
                        self.start_date
                    ),

                    end=

                    pd.to_datetime(
                        self.end_date
                    ),

                    freq="B"

                )

                .strftime("%Y%m%d")

            }

        )



        matrix = calendar.merge(

            matrix,

            on="trade_date",

            how="left",

        )



        # ----------------------------------------------
        # No position = zero return
        # ----------------------------------------------

        strategy_columns = [

            c

            for c in matrix.columns

            if c != "trade_date"

        ]



        matrix[

            strategy_columns

        ] = matrix[

            strategy_columns

        ].fillna(0)



        # ----------------------------------------------
        # Sort
        # ----------------------------------------------

        matrix = matrix.sort_values(

            "trade_date"

        ).reset_index(

            drop=True

        )



        return matrix