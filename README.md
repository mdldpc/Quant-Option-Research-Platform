# Quant Option Research Platform

A quantitative research platform for option volatility modeling, feature engineering, systematic strategy development, and backtesting based on high-frequency Chinese index option data.

---

## Project Overview

This project is a complete quantitative research framework designed for volatility-based option trading strategies.

Starting from raw high-frequency option and futures market data, the platform automatically performs:

* Data engineering
* Implied volatility estimation (Black-76)
* Greeks calculation
* Volatility surface construction
* ATM term structure extraction
* Feature engineering
* Signal generation
* Strategy backtesting
* Transaction cost analysis
* Robustness evaluation
* Research visualization

The goal is not only to implement pricing models, but also to provide a reusable research framework for quantitative option strategy development.

---

## Key Features

### Market Data Engineering

* High-frequency option and futures data processing
* Efficient parquet-based storage
* Tick-level data pipeline
* Automatic preprocessing and cleaning

### Volatility Modeling

* Black-76 implied volatility solver
* ATM implied volatility extraction
* Volatility smile construction
* Volatility surface generation
* ATM term structure analysis

### Greeks Engine

Automatic calculation of

* Delta
* Gamma
* Vega
* Theta
* Vanna
* Vomma
* Speed

for every option observation.

### Feature Engineering

Generate research features including

* ATM IV
* IV Z-score
* Term structure slope
* Rolling statistics
* Signal score

### Trading Strategy

Current Version (V1.0)

* Long-only volatility strategy
* ATM straddle selection
* Signal-driven entry
* Rule-based exit
* Real option price backtest

### Backtesting Framework

Performance metrics include

* Win Rate
* Average Return
* Sharpe Ratio
* Profit Factor
* Maximum Drawdown
* Holding Days
* Equity Curve

### Robustness Framework

Automatic evaluation under different parameters

* Signal Threshold
* Holding Period
* Transaction Cost

Future versions will support

* Walk-forward validation
* Rolling window testing
* Multi-year backtesting
* Strategy comparison

---

## Research Pipeline

```
Raw Tick Data
        │
        ▼
Data Engineering
        │
        ▼
Black-76 Implied Volatility
        │
        ▼
Greeks Calculation
        │
        ▼
Volatility Surface
        │
        ▼
ATM Term Structure
        │
        ▼
Feature Engineering
        │
        ▼
Signal Generation
        │
        ▼
Option Strategy
        │
        ▼
Backtesting
        │
        ▼
Robustness Analysis
        │
        ▼
Research Dashboard
```

---

## Project Structure

```
Quant_Option_Project/

analysis/
backtest/
config/
core/
docs/
experiments/
research/
scripts/
strategy/
utils/

data_raw/
data_parquet/
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd Quant_Option_Project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the complete research pipeline

```bash
python run_all.py
```

### 4. Or run individual modules

```bash
python scripts/run_option_backtest_v2.py

python scripts/run_transaction_cost_analysis.py

python scripts/run_robustness_suite.py

python scripts/run_robustness_dashboard.py
```

---

## Current Research Status

| Module                    | Status |
| ------------------------- | ------ |
| Data Engineering          | ✅      |
| Black-76 IV               | ✅      |
| Greeks Engine             | ✅      |
| Volatility Surface        | ✅      |
| ATM Term Structure        | ✅      |
| Feature Engineering       | ✅      |
| Signal Engine             | ✅      |
| Strategy Engine           | ✅      |
| Option Backtest           | ✅      |
| Transaction Cost Analysis | ✅      |
| Robustness Framework      | ✅      |
| Dashboard                 | ✅      |

Current Version

**Version 1.0**

---

## Current Results

Current implementation includes

* Long-only ATM straddle strategy
* Rule-based signal engine
* Transaction cost sensitivity analysis
* Robustness dashboard

The platform has been successfully validated on real option market data.

---

## Future Development

Version 2.0

* Rolling window validation
* Walk-forward testing
* Multi-period backtesting
* Strategy optimization
* Portfolio construction
* Delta-neutral strategies
* Vega-neutral strategies
* Machine learning signal generation

---

## Technologies

Python

Main libraries

* pandas
* numpy
* scipy
* matplotlib
* pyarrow

Pricing model

* Black-76

---

## Author

Developed as an independent quantitative research project focusing on systematic option trading and volatility modeling.

This project is continuously evolving toward a production-level quantitative research platform.
