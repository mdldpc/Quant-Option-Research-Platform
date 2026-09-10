"""Small-sample machine-learning tools for option research."""

from .small_sample import (
    WalkForwardConfig,
    build_market_features,
    run_walk_forward,
    summarize_predictions,
)
from .adapters import add_path_labels, normalize_trades, parse_trading_date
from .evaluation import performance_metrics, stationary_block_bootstrap_ci

__all__ = [
    "WalkForwardConfig",
    "build_market_features",
    "run_walk_forward",
    "summarize_predictions",
    "add_path_labels",
    "normalize_trades",
    "parse_trading_date",
    "performance_metrics",
    "stationary_block_bootstrap_ci",
]
