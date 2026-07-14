from pathlib import Path


FIGURE_DIR = Path("research/figures")


def _figure(name: str) -> Path:
    path = FIGURE_DIR / name

    if not path.exists():
        raise FileNotFoundError(f"Figure not found: {path}")

    return path


def volatility_smile_overall() -> Path:
    return _figure("smile_bucket_overall.png")


def volatility_smile_monthly() -> Path:
    return _figure("smile_bucket_monthly.png")


def volatility_surface_h1() -> Path:
    return _figure("surface_heatmap_near_h1.png")


def atm_term_structure_overall() -> Path:
    return _figure("atm_term_structure_overall.png")


def atm_term_structure_monthly() -> Path:
    return _figure("atm_term_structure_monthly.png")


def iv_distribution_histogram() -> Path:
    return _figure("iv_distribution_histogram.png")


def iv_distribution_boxplot() -> Path:
    return _figure("iv_distribution_boxplot.png")


def option_equity_curve() -> Path:
    return _figure("option_equity_curve.png")


def option_drawdown_curve() -> Path:
    return _figure("option_drawdown_curve.png")


def option_equity_drawdown_dashboard() -> Path:
    return _figure("option_equity_drawdown_dashboard.png")


def option_return_distribution() -> Path:
    return _figure("option_return_distribution.png")


def option_signal_score_vs_return() -> Path:
    return _figure("option_signal_score_vs_return.png")


def robustness_dashboard() -> Path:
    return _figure("robustness_dashboard.png")