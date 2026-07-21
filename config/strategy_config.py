"""
===========================================================
Strategy Framework Configuration
===========================================================

Central configuration for:

- Signal thresholds
- Execution rules
- Risk thresholds
- Backtest defaults
- Strategy registry

Future strategy builders should ONLY read parameters
from this file instead of hard-coded values.
"""

# =========================================================
# Signal Configuration
# =========================================================

SIGNAL_CONFIG = {

    "entry_score": 80,

    "exit_score": 40,

    "calendar_entry_zscore": 1.0,

    "calendar_exit_zscore": 0.2,

    "rolling_window": 20,

}


# =========================================================
# Execution Configuration
# =========================================================

EXECUTION_CONFIG = {

    "target_time_bucket": None,

    "max_time_distance": None,

    "fallback_to_latest": True,

}


# =========================================================
# Risk Configuration
# =========================================================

RISK_CONFIG = {

    "delta_threshold": 0.30,

    "gamma_threshold": 0.004,

    "vega_threshold": 1500,

    "theta_threshold": 1200,

}


# =========================================================
# Backtest Configuration
# =========================================================

BACKTEST_CONFIG = {

    "initial_equity": 1.0,

    "transaction_cost": 0.0,

    "slippage": 0.0,

}


# =========================================================
# Strategy Registry
# =========================================================

STRATEGY_REGISTRY = {

    "long_atm_straddle": {

        "enabled": True,

        "status": "prototype",

    },

    "long_atm_strangle": {

        "enabled": True,

        "status": "prototype",

    },

    "calendar_spread": {

        "enabled": False,

        "status": "planned",

    },

    "long_call_butterfly": {

        "enabled": True,

        "status": "prototype",

    },

    "iron_condor": {

        "enabled": False,

        "status": "planned",

    },

    "bull_call_spread": {

        "enabled": False,

        "status": "planned",

    },

    "bear_put_spread": {

        "enabled": False,

        "status": "planned",

    },

}