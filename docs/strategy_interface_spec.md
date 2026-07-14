# Strategy Interface Specification

## Objective

This document defines the standard interface that every strategy implementation must follow.

All strategies should use the same workflow and output format.

---

## Standard Pipeline

Signal
↓

Entry
↓

Position Construction
↓

Greeks Monitoring
↓

Risk Monitoring
↓

Exit
↓

Performance Evaluation

---

## Required Inputs

- Option dataset
- Greeks dataset
- Signal dataset
- Risk engine

---

## Required Outputs

- Trade dataset
- Portfolio Greeks
- Portfolio risk
- Backtest summary

---

## Required Functions

Every strategy should implement:

- generate_signal()
- construct_position()
- monitor_greeks()
- evaluate_risk()
- generate_exit()
- compute_performance()

---

## Required Metrics

Performance

- Total Return
- Net Return
- Holding Days
- Win Rate
- Max Drawdown

Greeks

- Delta
- Gamma
- Vega
- Theta
- Vanna
- Vomma

Risk

- Warning Count
- Risk Level

---

## Strategy Metadata

Each strategy should specify

- Strategy Name
- Version
- Market View
- Data Requirement
- Current Status