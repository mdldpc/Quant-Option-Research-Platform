from pathlib import Path
import pandas as pd


from config.data_version import (
    ALL_GREEKS_FILE,
    CALENDAR_DATASET,
)


from framework.strategy.dataset_base import (
    StrategyDatasetBuilder,
)


from framework.strategy.dataset_contracts import (
    StrategyDatasetResult,
)



PREVIEW_PATH = Path(
    "research/exports/calendar_spread_dataset_v1_1_preview.csv"
)


REPORT_PATH = Path(
    "research/reports/calendar_spread_dataset_v1_1_report.txt"
)



KEEP_COLS = [
    "trade_date",
    "time_bucket",
    "symbol",
    "expiry_code",
    "option_type",
    "strike",
    "future_price",
    "T",
    "smoothed_iv",
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "BP1",
    "AP1",
]



class CalendarBuilder(StrategyDatasetBuilder):

    dataset_name = "calendar_spread"



    def build(self):

        self.validate()


        df = pd.read_parquet(
            ALL_GREEKS_FILE,
            columns=KEEP_COLS,
        )


        rows = []


        grouped = df.groupby(
            [
                "trade_date",
                "time_bucket",
            ],
            sort=False,
        )


        for _, group in grouped:


            expiries = []


            for _, expiry_group in group.groupby(
                "expiry_code",
                sort=False,
            ):

                item = self.build_atm_straddle(
                    expiry_group
                )


                if item is not None:

                    expiries.append(item)



            if len(expiries) < 2:
                continue



            expiries = sorted(
                expiries,
                key=lambda x:x["T"]
            )


            near = expiries[0]
            next_ = expiries[1]



            row = {


                "trade_date":
                    group["trade_date"].iloc[0],


                "time_bucket":
                    group["time_bucket"].iloc[0],



                "near_expiry":
                    near["expiry_code"],


                "next_expiry":
                    next_["expiry_code"],



                "near_T":
                    near["T"],


                "next_T":
                    next_["T"],



                "near_iv":
                    near["atm_iv"],


                "next_iv":
                    next_["atm_iv"],



                "iv_spread":
                    next_["atm_iv"]
                    -
                    near["atm_iv"],



                "near_straddle_price":
                    near["straddle_price"],


                "next_straddle_price":
                    next_["straddle_price"],



                "calendar_price":
                    near["straddle_price"]
                    -
                    next_["straddle_price"],



                "net_delta":
                    self.net_greek(
                        near,
                        next_,
                        "delta",
                    ),


                "net_gamma":
                    self.net_greek(
                        near,
                        next_,
                        "gamma",
                    ),


                "net_vega":
                    self.net_greek(
                        near,
                        next_,
                        "vega",
                    ),


                "net_theta":
                    self.net_greek(
                        near,
                        next_,
                        "theta",
                    ),


                "net_vanna":
                    self.net_greek(
                        near,
                        next_,
                        "vanna",
                    ),


                "net_vomma":
                    self.net_greek(
                        near,
                        next_,
                        "vomma",
                    ),


                "calendar_direction":
                    "long_near_short_next",

            }


            rows.append(row)



        out = pd.DataFrame(rows)


        CALENDAR_DATASET.parent.mkdir(
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
            CALENDAR_DATASET,
            index=False,
        )


        out.head(100000).to_csv(
            PREVIEW_PATH,
            index=False,
            encoding="utf-8-sig",
        )


        REPORT_PATH.write_text(
            "Calendar Spread Dataset v1.1",
            encoding="utf-8",
        )



        return StrategyDatasetResult(

            dataset_name=self.dataset_name,

            dataset_path=CALENDAR_DATASET,

            preview_path=PREVIEW_PATH,

            report_path=REPORT_PATH,

            rows=len(out),

            status="success",

            message=
            "Calendar spread dataset built successfully.",

        )



    @staticmethod
    def mid_price(row):

        if row["BP1"] > 0 and row["AP1"] > 0:

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



    def build_atm_straddle(self, group):

        future_price = (
            group["future_price"]
            .median()
        )


        calls = group[
            group["option_type"]=="C"
        ]


        puts = group[
            group["option_type"]=="P"
        ]


        if calls.empty or puts.empty:
            return None



        call = calls.loc[
            (
                calls["strike"]
                -
                future_price
            )
            .abs()
            .idxmin()
        ]


        put = puts.loc[
            (
                puts["strike"]
                -
                future_price
            )
            .abs()
            .idxmin()
        ]



        call_mid = self.mid_price(call)

        put_mid = self.mid_price(put)



        if call_mid is None or put_mid is None:

            return None



        return {

            "expiry_code":
                group["expiry_code"].iloc[0],


            "T":
                group["T"].median(),


            "atm_iv":
                (
                    call["smoothed_iv"]
                    +
                    put["smoothed_iv"]
                ) / 2,


            "straddle_price":
                call_mid + put_mid,


            "call_delta":
                call["delta"],

            "put_delta":
                put["delta"],

            "call_gamma":
                call["gamma"],

            "put_gamma":
                put["gamma"],

            "call_vega":
                call["vega"],

            "put_vega":
                put["vega"],

            "call_theta":
                call["theta"],

            "put_theta":
                put["theta"],

            "call_vanna":
                call["vanna"],

            "put_vanna":
                put["vanna"],

            "call_vomma":
                call["vomma"],

            "put_vomma":
                put["vomma"],

        }



    @staticmethod
    def net_greek(
        near,
        next_,
        greek,
    ):

        return (
            near[f"call_{greek}"]
            +
            near[f"put_{greek}"]
            -
            next_[f"call_{greek}"]
            -
            next_[f"put_{greek}"]
        )



    def validate(self):

        if not ALL_GREEKS_FILE.exists():

            raise FileNotFoundError(
                ALL_GREEKS_FILE
            )