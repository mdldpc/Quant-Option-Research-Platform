"""
===========================================================
Strategy Metadata Configuration
===========================================================

Contains human-readable information
for research reports.

This file should NOT contain
trading logic.

Only documentation metadata.
"""


STRATEGY_METADATA = {


    "long_call_butterfly":

    {

        "display_name":
        "Long Call Butterfly",


        "version":
        "v1.2",


        "category":
        "Volatility Strategy",


        "description":
        """
Long Call Butterfly is a limited-risk
options volatility strategy constructed
using three strike levels.

The strategy is designed to benefit when
the underlying price converges near the
middle strike price at expiration.

Maximum loss is limited to the initial
premium paid, while maximum profit occurs
when the underlying finishes near the
central strike.
""",

    },
    "long_atm_straddle":

    {

        "display_name":
        "Long ATM Straddle",


        "version":
        "v1.0",


        "category":
        "Volatility Strategy",


        "description":
        """
Long ATM Straddle is a long volatility
options strategy constructed by buying
an at-the-money call and put option.

The strategy benefits from large price
movements in either direction while the
maximum loss is limited to the initial
premium paid.
""",

    },
}