# ATM IV Dataset Specification v1.0

## Dataset Name

atm_iv_dataset_2026H1

## Purpose

Construct a research-ready ATM implied volatility dataset from contract-level option Greeks data.

This dataset will be used for:

- Volatility term structure analysis
- Calendar spread research
- ATM IV time series analysis
- Future strategy backtesting

## Source Dataset

D:\Quant_Option_Project\data_parquet\batch_2026\all_greeks_2026H1.parquet

## Output Dataset

D:\Quant_Option_Project\research\datasets\atm_iv_dataset_2026H1.parquet

## Primary Key

- trade_date
- time_bucket
- expiry_code

Each row represents one ATM IV observation for one expiry at one time bucket.

## ATM Definition

For each:

- trade_date
- time_bucket
- expiry_code

ATM strike is defined as:

abs(strike - future_price) minimum

## Call / Put Treatment

If both ATM Call and ATM Put exist:

atm_iv = average(call_iv, put_iv)

If only one side exists:

atm_iv = available side IV

## IV Source

Use:

smoothed_iv

as the main IV input.

Raw implied_vol is kept for QC only.

## Output Fields

- trade_date
- time_bucket
- expiry_code
- atm_strike
- future_price
- T
- call_symbol
- put_symbol
- call_iv
- put_iv
- atm_iv
- call_delta
- put_delta
- call_gamma
- put_gamma
- call_vega
- put_vega
- call_theta
- put_theta
- call_vanna
- put_vanna
- call_vomma
- put_vomma
- call_speed
- put_speed

## Notes

This is a research dataset, not a trading signal dataset.

Strategy construction and backtesting will be built on top of this dataset later.