"""
Expired Trade Valuation v1.1

Support:

- Long ATM Strangle
- Long Call Butterfly
"""


from analysis.terminal_price_loader import TerminalPriceLoader




class ExpiredTradeValuator:


    def __init__(
        self,
        data_dir
    ):

        self.loader = TerminalPriceLoader(
            data_dir
        )



    # --------------------------------------------------
    # Strangle
    # --------------------------------------------------

    def value_strangle(
        self,
        trade
    ):


        expiry = str(
            int(trade["expiry_code"])
        )


        expiry = expiry.zfill(4)



        call_symbol = (
            f"IO{expiry}-C-"
            f"{int(trade['entry_call_strike'])}"
        )


        put_symbol = (
            f"IO{expiry}-P-"
            f"{int(trade['entry_put_strike'])}"
        )



        valuation_date = (
            int(trade["exit_date"])
        )



        call_value = (
            self.loader
            .get_terminal_price(
                call_symbol,
                valuation_date
            )
        )


        put_value = (
            self.loader
            .get_terminal_price(
                put_symbol,
                valuation_date
            )
        )



        terminal_price = (

            call_value["terminal_price"]

            +

            put_value["terminal_price"]

        )



        realized_return = (

            terminal_price

            -

            trade["entry_strangle_price"]

        ) / trade["entry_strangle_price"]



        return {

            "terminal_call":
                call_value,


            "terminal_put":
                put_value,


            "terminal_strangle_price":
                terminal_price,


            "realized_return":
                realized_return,

        }



    # --------------------------------------------------
    # Butterfly
    # --------------------------------------------------

    def value_butterfly(
        self,
        trade
    ):


        expiry = str(
            int(trade["expiry_code"])
        )


        expiry = expiry.zfill(4)



        lower_symbol = (
            f"IO{expiry}-C-"
            f"{int(trade['entry_lower_strike'])}"
        )


        middle_symbol = (
            f"IO{expiry}-C-"
            f"{int(trade['entry_middle_strike'])}"
        )


        upper_symbol = (
            f"IO{expiry}-C-"
            f"{int(trade['entry_upper_strike'])}"
        )



        valuation_date = (
            int(trade["exit_date"])
        )



        lower_value = (
            self.loader
            .get_terminal_price(
                lower_symbol,
                valuation_date
            )
        )


        middle_value = (
            self.loader
            .get_terminal_price(
                middle_symbol,
                valuation_date
            )
        )


        upper_value = (
            self.loader
            .get_terminal_price(
                upper_symbol,
                valuation_date
            )
        )



        terminal_price = (

            lower_value["terminal_price"]

            -

            2
            *
            middle_value["terminal_price"]

            +

            upper_value["terminal_price"]

        )



        realized_return = (

            terminal_price

            -

            trade["entry_butterfly_price"]

        ) / trade["entry_butterfly_price"]



        return {


            "terminal_lower":

                lower_value,


            "terminal_middle":

                middle_value,


            "terminal_upper":

                upper_value,


            "terminal_butterfly_price":

                terminal_price,


            "realized_return":

                realized_return,


        }

    # --------------------------------------------------
    # Calendar Spread
    # --------------------------------------------------

    def value_calendar(
        self,
        trade
    ):


        near_expiry = str(
            int(trade["near_expiry"])
        ).zfill(4)


        next_expiry = str(
            int(trade["next_expiry"])
        ).zfill(4)



        near_strike = int(
            trade["near_strike"]
        )


        next_strike = int(
            trade["next_strike"]
        )



        valuation_date = int(
            trade["exit_date"]
        )



        # ------------------------------------------
        # Near expiry short straddle
        # ------------------------------------------

        near_call_symbol = (
            f"IO{near_expiry}-C-{near_strike}"
        )

        near_put_symbol = (
            f"IO{near_expiry}-P-{near_strike}"
        )


        near_call = (
            self.loader
            .get_terminal_price(
                near_call_symbol,
                valuation_date
            )
        )


        near_put = (
            self.loader
            .get_terminal_price(
                near_put_symbol,
                valuation_date
            )
        )



        near_value = (

            near_call["terminal_price"]

            +

            near_put["terminal_price"]

        )



        # ------------------------------------------
        # Next expiry long straddle
        # ------------------------------------------

        next_call_symbol = (
            f"IO{next_expiry}-C-{next_strike}"
        )

        next_put_symbol = (
            f"IO{next_expiry}-P-{next_strike}"
        )



        next_call = (
            self.loader
            .get_terminal_price(
                next_call_symbol,
                valuation_date
            )
        )


        next_put = (
            self.loader
            .get_terminal_price(
                next_put_symbol,
                valuation_date
            )
        )



        next_value = (

            next_call["terminal_price"]

            +

            next_put["terminal_price"]

        )



        # Calendar:
        #
        # Long next
        # Short near
        #

        terminal_price = (

            near_value

            -

            next_value

        )



        realized_return = (

            terminal_price

            -
            trade["entry_calendar_price"]

        ) / trade["entry_calendar_price"]



        return {

            "terminal_near":

                {
                    "call": near_call,
                    "put": near_put,
                    "value": near_value,
                },


            "terminal_next":

                {
                    "call": next_call,
                    "put": next_put,
                    "value": next_value,
                },


            "terminal_calendar_price":

                terminal_price,


            "realized_return":

                realized_return,

        }