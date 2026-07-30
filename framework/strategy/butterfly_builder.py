from pathlib import Path
import pandas as pd


from config.data_version import (
    SMILE_DATASET,
    BUTTERFLY_DATASET,
)


from framework.strategy.dataset_base import (
    StrategyDatasetBuilder,
)


from framework.strategy.dataset_contracts import (
    StrategyDatasetResult,
)



PREVIEW_PATH = Path(
    "research/exports/butterfly_dataset_v1_1_preview.csv"
)


REPORT_PATH = Path(
    "research/reports/butterfly_dataset_v1_1_report.txt"
)



class ButterflyBuilder(StrategyDatasetBuilder):

    dataset_name = "long_call_butterfly"



    def build(self) -> StrategyDatasetResult:

        self.validate()


        print(
            "Reading near smile dataset v1.1..."
        )


        df = pd.read_parquet(
            SMILE_DATASET
        )


        print(
            "Source shape:"
        )

        print(
            df.shape
        )


        df = df[
            df["option_type"] == "C"
        ].copy()



        rows = []


        grouped = df.groupby(
            [
                "trade_date",
                "time_bucket",
                "expiry_code",
            ],
            sort=False,
        )


        total = grouped.ngroups



        for i, (_, group) in enumerate(
            grouped,
            start=1,
        ):


            future_price = (
                group["future_price"]
                .median()
            )


            strikes = sorted(
                group["strike"]
                .dropna()
                .unique()
            )


            if len(strikes) < 3:
                continue



            middle = min(
                strikes,
                key=lambda x:
                abs(x - future_price)
            )


            middle_idx = strikes.index(
                middle
            )


            if (
                middle_idx == 0
                or
                middle_idx == len(strikes)-1
            ):
                continue



            lower = strikes[
                middle_idx-1
            ]


            upper = strikes[
                middle_idx+1
            ]



            lower_row = (
                group[
                    group["strike"] == lower
                ]
                .iloc[-1]
            )


            middle_row = (
                group[
                    group["strike"] == middle
                ]
                .iloc[-1]
            )


            upper_row = (
                group[
                    group["strike"] == upper
                ]
                .iloc[-1]
            )



            lower_price = self.mid_price(
                lower_row
            )

            middle_price = self.mid_price(
                middle_row
            )

            upper_price = self.mid_price(
                upper_row
            )



            butterfly_price = None


            if (
                lower_price is not None
                and middle_price is not None
                and upper_price is not None
            ):

                butterfly_price = (
                    lower_price
                    -
                    2 * middle_price
                    +
                    upper_price
                )



            rows.append(

                {

                    "trade_date":
                        group["trade_date"].iloc[0],

                    "time_bucket":
                        group["time_bucket"].iloc[0],


                    "expiry_code":
                        group["expiry_code"].iloc[0],


                    "future_price":
                        future_price,


                    "T":
                        group["T"].median(),



                    "lower_symbol":
                        lower_row["symbol"],


                    "middle_symbol":
                        middle_row["symbol"],


                    "upper_symbol":
                        upper_row["symbol"],



                    "lower_strike":
                        lower,


                    "middle_strike":
                        middle,


                    "upper_strike":
                        upper,



                    "strike_width_low":
                        middle - lower,


                    "strike_width_high":
                        upper - middle,


                    "is_symmetric":
                        (middle-lower)
                        ==
                        (upper-middle),



                    "lower_price":
                        lower_price,


                    "middle_price":
                        middle_price,


                    "upper_price":
                        upper_price,


                    "butterfly_price":
                        butterfly_price,



                    "net_delta":
                        lower_row["delta"]
                        -
                        2 * middle_row["delta"]
                        +
                        upper_row["delta"],


                    "net_gamma":
                        lower_row["gamma"]
                        -
                        2 * middle_row["gamma"]
                        +
                        upper_row["gamma"],


                    "net_vega":
                        lower_row["vega"]
                        -
                        2 * middle_row["vega"]
                        +
                        upper_row["vega"],


                    "net_theta":
                        lower_row["theta"]
                        -
                        2 * middle_row["theta"]
                        +
                        upper_row["theta"],


                    "net_vanna":
                        lower_row["vanna"]
                        -
                        2 * middle_row["vanna"]
                        +
                        upper_row["vanna"],


                    "net_vomma":
                        lower_row["vomma"]
                        -
                        2 * middle_row["vomma"]
                        +
                        upper_row["vomma"],

                }

            )


            if i % 50000 == 0:

                print(
                    f"Processed groups: {i}/{total}"
                )



        out = pd.DataFrame(
            rows
        )


        out = out.sort_values(
            [
                "trade_date",
                "time_bucket",
                "expiry_code",
            ]
        ).reset_index(
            drop=True
        )



        BUTTERFLY_DATASET.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        PREVIEW_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        REPORT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )



        out.to_parquet(
            BUTTERFLY_DATASET,
            index=False,
        )


        out.head(
            100000
        ).to_csv(
            PREVIEW_PATH,
            index=False,
            encoding="utf-8-sig",
        )



        lines = [

            "Long Call Butterfly Dataset v1.1 Report",

            "=" * 80,

            "",

            f"Input file: {SMILE_DATASET}",

            f"Output dataset: {BUTTERFLY_DATASET}",

            "",

            f"Rows: {len(out)}",

            "",

            "Butterfly price summary:",

            str(
                out["butterfly_price"]
                .describe()
            ),

        ]



        REPORT_PATH.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )



        return StrategyDatasetResult(

            dataset_name=self.dataset_name,

            dataset_path=BUTTERFLY_DATASET,

            preview_path=PREVIEW_PATH,

            report_path=REPORT_PATH,

            rows=len(out),

            status="success",

            message=
            "Long call butterfly dataset built successfully.",

        )



    @staticmethod
    def mid_price(row):

        if (
            row["BP1"] > 0
            and
            row["AP1"] > 0
        ):

            return (
                row["BP1"]
                +
                row["AP1"]
            ) / 2


        if row["BP1"] > 0:

            return row["BP1"]


        if row["AP1"] > 0:

            return row["AP1"]


        return None



    def validate(self):

        if not SMILE_DATASET.exists():

            raise FileNotFoundError(
                SMILE_DATASET
            )



def main():

    result = ButterflyBuilder().build()

    print(result)



if __name__ == "__main__":

    main()