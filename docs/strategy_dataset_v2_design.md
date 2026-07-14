# Strategy Dataset v2.0 Design

## Background

The first prototype of the Long ATM Strangle strategy was built using:

research/datasets/smile_dataset_near_2026H1.parquet

Although this dataset is suitable for smile analysis, it is not designed as a universal strategy dataset.

During backtesting we observed missing execution snapshots for several expiry months because only near-term option observations were preserved.

Therefore, the strategy dataset architecture needs to be redesigned.

---

# New Architecture

Raw Greeks Dataset

↓

all_greeks_2026H1.parquet

↓

Strategy Dataset Builder

↓

Strategy Dataset

↓

Execution Snapshot Builder

↓

Backtest Engine

↓

Portfolio Greeks

↓

Exposure Risk

↓

Performance Report

---

# Design Principles

## 1. Strategy Dataset should be independent

Strategy datasets should not depend on research datasets
(e.g. Smile Dataset, Surface Dataset, Term Structure Dataset).

Instead, every strategy should be generated directly from
the complete option-level Greeks dataset.

---

## 2. One Builder per Strategy

Each strategy has its own builder.

Examples:

- ATM Straddle Builder
- ATM Strangle Builder
- Calendar Spread Builder
- Butterfly Builder
- Iron Condor Builder

All builders share the same raw data source.

---

## 3. Unified Execution Layer

Execution snapshots are generated after strategy datasets.

Execution Snapshot Builder is strategy-independent and reusable.

Responsibilities:

- Select representative execution quote
- Remove invalid quotes
- Provide one execution snapshot per day / expiry
- Support configurable execution rules

---

## 4. Shared Backtesting Framework

Every strategy should reuse the same modules.

Strategy Dataset

↓

Execution Snapshot

↓

Backtest

↓

Portfolio Greeks

↓

Risk Analysis

↓

Performance Evaluation

Only the strategy builder changes.

---

# Advantages

- Better modularity
- Easier maintenance
- Consistent execution logic
- Easier to add new strategies
- Better reproducibility
- Better research scalability

---

# Migration Plan

The current prototype implementation will remain for reference.

During the final v1.1 rebuild:

- Rebuild all strategy datasets directly from
  all_greeks_2026H1.parquet.

- Rebuild execution snapshots.

- Re-run all strategy backtests.

This architecture becomes the permanent framework for
future strategy development.