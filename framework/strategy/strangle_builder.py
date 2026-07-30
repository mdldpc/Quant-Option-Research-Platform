from pathlib import Path
import pandas as pd


from config.data_version import (
    ALL_GREEKS_FILE,
    STRANGLE_DATASET,
)


from framework.strategy.dataset_base import (
    StrategyDatasetBuilder,
)


from framework.strategy.dataset_contracts import (
    StrategyDatasetResult,
)


PREVIEW_PATH = Path(
    "research/exports/option_strangle_dataset_2026H1_v1_1_preview.csv"
)


REPORT_PATH = Path(
    "research/reports/option_strangle_dataset_2026H1_v1_1_report.txt"
)



class StrangleBuilder(StrategyDatasetBuilder):

    dataset_name = "option_strangle"


    def build(self) -> StrategyDatasetResult:

        self.validate()


        print(
            "Reading all Greeks v1.1..."
        )


        df = pd.read_parquet(
            ALL_GREEKS_FILE
        )


        print(
            "Source shape:"
        )

        print(
            df.shape
        )


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


            calls = group[
                group["option_type"] == "C"
            ].copy()


            puts = group[
                group["option_type"] == "P"
            ].copy()


            if calls.empty or puts.empty:
                continue



            calls["abs_moneyness"] = (
                calls["strike"]
                -
                future_price
            ).abs()


            puts["abs_moneyness"] = (
                puts["strike"]
                -
                future_price
            ).abs()



            call_row = (
                calls
                .sort_values(
                    "abs_moneyness"
                )
                .iloc[0]
            )


            put_row = (
                puts
                .sort_values(
                    "abs_moneyness"
                )
                .iloc[0]
            )



            call_price = self.mid_price(
                call_row
            )


            put_price = self.mid_price(
                put_row
            )


            if (
                call_price is None
                or
                put_price is None
            ):
                strangle_price = None

            else:

                strangle_price = (
                    call_price
                    +
                    put_price
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



                    "call_symbol":
                        call_row["symbol"],


                    "put_symbol":
                        put_row["symbol"],



                    "call_strike":
                        call_row["strike"],


                    "put_strike":
                        put_row["strike"],



                    "call_moneyness":
                        call_row["strike"]
                        /
                        future_price,


                    "put_moneyness":
                        put_row["strike"]
                        /
                        future_price,



                    "call_iv":
                        call_row["smoothed_iv"],


                    "put_iv":
                        put_row["smoothed_iv"],



                    "call_raw_iv":
                        call_row["implied_vol"],


                    "put_raw_iv":
                        put_row["implied_vol"],



                    "call_delta":
                        call_row["delta"],


                    "put_delta":
                        put_row["delta"],



                    "call_gamma":
                        call_row["gamma"],


                    "put_gamma":
                        put_row["gamma"],



                    "call_vega":
                        call_row["vega"],


                    "put_vega":
                        put_row["vega"],



                    "call_theta":
                        call_row["theta"],


                    "put_theta":
                        put_row["theta"],



                    "call_vanna":
                        call_row["vanna"],


                    "put_vanna":
                        put_row["vanna"],



                    "call_vomma":
                        call_row["vomma"],


                    "put_vomma":
                        put_row["vomma"],



                    "call_speed":
                        call_row["speed"],


                    "put_speed":
                        put_row["speed"],



                    "call_price":
                        call_price,


                    "put_price":
                        put_price,


                    "strangle_price":
                        strangle_price,



                    "has_call":
                        True,


                    "has_put":
                        True,


                    "has_both":
                        True,

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



        STRANGLE_DATASET.parent.mkdir(
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
            STRANGLE_DATASET,
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

            "Option Strangle Dataset v1.1 Report",

            "=" * 80,

            "",

            f"Input file: {ALL_GREEKS_FILE}",

            f"Output dataset: {STRANGLE_DATASET}",

            "",

            f"Rows: {len(out)}",

            f"Trade dates: {out['trade_date'].nunique()}",

            "",

            "Strangle price summary:",

            str(
                out["strangle_price"]
                .describe()
            ),

        ]



        REPORT_PATH.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )



        return StrategyDatasetResult(

            dataset_name=self.dataset_name,

            dataset_path=STRANGLE_DATASET,

            preview_path=PREVIEW_PATH,

            report_path=REPORT_PATH,

            rows=len(out),

            status="success",

            message=
            "Option strangle dataset built successfully.",

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

        if not ALL_GREEKS_FILE.exists():

            raise FileNotFoundError(
                ALL_GREEKS_FILE
            )



def main():

    result = StrangleBuilder().build()

    print(result)



if __name__ == "__main__":

    main()