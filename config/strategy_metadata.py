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

}