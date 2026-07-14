from pathlib import Path
import time

from scripts.rebuild.build_utils import (
    banner,
    check_python_packages,
    run_script,
    verify_files,
    print_summary,
)

# ==========================================================
# Project Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PYTHON_PACKAGES = [
    "pandas",
    "numpy",
    "matplotlib",
    "pyarrow",
    "docx",
]

BUILD_SCRIPTS = [

    # -------------------------
    # Volatility Analytics
    # -------------------------
    "scripts/plot_daily_iv_summary.py",
    "scripts/plot_smile_bucket.py",
    "scripts/plot_surface_heatmap.py",
    "scripts/plot_atm_term_structure.py",

    # -------------------------
    # Greeks
    # -------------------------
    "scripts/plot_delta_heatmap.py",
    "scripts/plot_gamma_heatmap.py",
    "scripts/plot_vega_heatmap.py",

    # -------------------------
    # Signals
    # -------------------------
    "scripts/plot_signal_features.py",

    # -------------------------
    # Backtest
    # -------------------------
    "scripts/plot_option_backtest.py",

    # -------------------------
    # Dashboard
    # -------------------------
    "scripts/run_robustness_dashboard.py",
]

EXPECTED_OUTPUTS = [

    # White Paper
    "research/reports/quant_option_technical_white_paper_v3_0.docx",

    # Phase I Figures
    "research/figures/smile_bucket_overall.png",
    "research/figures/surface_heatmap_near_h1.png",
    "research/figures/atm_term_structure_overall.png",
    "research/figures/option_equity_curve.png",
    "research/figures/option_drawdown_curve.png",
    "research/figures/option_trade_returns.png",
    "research/figures/robustness_dashboard.png",
]

# ==========================================================
# Main Build
# ==========================================================


def main():

    banner(
        "Quant Option Research Platform\n"
        "Documentation Build Pipeline v3.1"
    )

    start = time.perf_counter()

    check_python_packages(PYTHON_PACKAGES)

    for script in BUILD_SCRIPTS:
        run_script(
            PROJECT_ROOT,
            script,
        )

    run_script(
        PROJECT_ROOT,
        "scripts.rebuild.build_documentation_v3_0",
        as_module=True,
    )

    missing = verify_files(
        PROJECT_ROOT,
        EXPECTED_OUTPUTS,
    )

    elapsed = time.perf_counter() - start

    print_summary(
        title="Documentation Build Completed",
        scripts_executed=len(BUILD_SCRIPTS) + 1,
        elapsed=elapsed,
        missing_files=missing,
    )

if __name__ == "__main__":
    main()