# Quant Option Project V2 Refactor Plan

## 1. Goal

Freeze the current V1.0 research pipeline and prepare the project for V2 research experiments.

V1.0 includes:
- Data engineering
- Black-76 implied volatility
- Greeks
- Smile / surface / term structure
- Signal engine
- Long-only option strategy
- Real option price backtest
- Transaction cost analysis
- Robustness suite
- Robustness dashboard

## 2. Keep in scripts/

These scripts are V1.0 official entry points:

```text
run_option_backtest_v2.py
run_transaction_cost_analysis.py
run_cost_sweep_v2.py
run_robustness_suite.py
run_robustness_dashboard.py