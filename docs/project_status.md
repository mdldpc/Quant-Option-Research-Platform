# Quant Option Project Status
.\venv\Scripts\Activate.ps1

## Project Overview

Objective:

Build a production-grade China Index Option dataset from CFFEX tick data, including:

* Black-76 Implied Volatility
* Spline-Smoothed IV Surface
* Delta
* Gamma
* Vega
* Theta
* Vanna
* Vomma
* Speed

for quantitative research and volatility trading studies.

---

# Development Timeline

## Phase 0 – Environment Setup

Status: COMPLETE

Components:

* Python virtual environment
* Project directory structure
* Parquet storage framework

---

## Phase 1 – Raw Data Reader

Status: COMPLETE

Input:

* CFFEX IF / IO tick-level data

Output:

* Raw DataFrame

---

## Phase 2 – Option Table Builder

Status: COMPLETE

Generated fields:

* symbol
* option_type
* strike
* expiry_code
* future_price
* option_price
* openInterest
* volume

---

## Phase 3 – Time Resampling

Status: COMPLETE

Method:

* 10-second snapshot sampling

Result:

* Significant reduction in storage and compute cost
* Minimal information loss

---

## Phase 4 – Black76 IV Engine

Status: COMPLETE

Features:

* Vectorized IV calculation
* Unique IV cache
* Robust convergence checks

---

## Phase 5 – Spline IV Surface

Status: COMPLETE

Method:

* Cross-sectional spline smoothing

Output:

* smoothed_iv

---

## Phase 6 – Greeks Engine

Status: COMPLETE

Calculated Greeks:

* Delta
* Gamma
* Vega
* Theta
* Vanna
* Vomma
* Speed

---

## Phase 7 – Batch Production Pipeline

Status: COMPLETE

Pipeline:

Raw
→ Option Table
→ Resample
→ IV Cache
→ Spline Surface
→ Greeks
→ Save

---

# Production Dataset

Dataset:

all_greeks_2026H1.parquet

Location:

D:\Quant_Option_Project\data_parquet\batch_2026

Coverage:

2026-01-02
to
2026-06-10

Trading Days:

112

Excluded Days:

20260505

Reason:

Raw source file contains known data issue.

---

# Dataset Statistics

Rows:

19,259,752

Columns:

25

Total Storage:

2.14 GB

Average Rows per Day:

171,962

Maximum Daily Rows:

283,249

Minimum Daily Rows:

4,764

---

# Quality Control Results

## Missing Values

implied_vol:

344,441

Reason:

Black-76 inversion failure for illiquid or extreme contracts.

Accepted.

---

All Remaining Fields:

0 missing values.

Fields verified:

* smoothed_iv
* delta
* gamma
* vega
* theta
* vanna
* vomma
* speed

---

## Infinite Values

All fields:

0

Status:

PASS

---

## Trade Date Coverage

Range:

20260102
to
20260610

Unique Dates:

112

Status:

PASS

---

# Known Events

## 20260114–20260115

Valid IV Ratio:

93%–94%

Cause:

Near-expiry IO2601 contracts.

Status:

Expected behavior.

---

## 20260207

Valid IV Ratio:

84%

Cause:

Weekend data file.

Status:

Excluded from normal trading-day analysis.

---

## 20260306–20260319

Valid IV Ratio decline:

96% → 90%

Likely Cause:

March expiry cycle and market structure effects.

Status:

Monitor only.

No evidence of pipeline failure.

---

# Current Status

Engineering Layer:

COMPLETE

Production Dataset:

COMPLETE

Quality Control:

COMPLETE

Version:

Research Ready v1.0

Date:

2026-06-17

---

# Next Phase

Research Layer

Potential Topics:

1. IV Surface Dynamics

2. Term Structure Analysis

3. Gamma Exposure Studies

4. Vanna Exposure Studies

5. Volatility Risk Premium

6. Event-Driven Volatility Analysis

7. Dealer Position Proxy Models

8. Expiry Effect Studies

Status:

READY TO START
