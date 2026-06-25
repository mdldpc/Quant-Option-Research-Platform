# Quant Option Research Platform

## Seven-Goal Project Report

### Version

Phase I Final Report

### Author

Jingzhe Yang

### Date

June 2026

---

# Executive Summary

This report summarizes the development of the Quant Option Research Platform and evaluates the completion status of the original seven project objectives. The project covers the full workflow from raw option data processing to implied volatility modelling, volatility surface construction, strategy development, backtesting, and robustness analysis.

---

# 1. Data Acquisition

## 1.1 Project Objective

Acquire and organize large-scale Chinese index option and futures market data for quantitative research. The objective is to build a research-ready dataset that supports implied volatility estimation, Greeks calculation, volatility surface construction, strategy development, and systematic backtesting.

## 1.2 Implementation

The project uses intraday Chinese index option market data stored in compressed CSV (.csv.xz) format. Each trading day contains option quotes, transaction information, and order book data for multiple option contracts across different strikes and maturities.

The original dataset consists of approximately 8 GB of compressed files and more than 300 GB after decompression. Due to the scale of the dataset, a local Python-based processing framework was developed to support efficient file inspection, batch processing, and intermediate data storage.

The project also utilizes corresponding index futures data as the underlying asset for option pricing and implied volatility estimation.

Key information extracted from the raw dataset includes:

* Trading date
* Option symbol
* Option type (Call / Put)
* Strike price
* Contract maturity
* Bid and ask quotes
* Trading volume
* Open interest
* Futures price

These variables form the foundation for all subsequent quantitative analyses.

## 1.3 Outputs

The data acquisition stage successfully produced a structured research dataset containing:

* Daily option market observations
* Contract-level metadata
* Futures market information
* Standardized identifiers for strike and maturity
* Intermediate datasets for implied volatility calculations

The resulting data pipeline supports downstream research tasks including volatility modelling, Greeks analysis, term structure construction, and strategy backtesting.

## 1.4 Assessment

The data acquisition objective was successfully completed.

A scalable workflow was established for processing large-scale option market data, transforming raw exchange-level observations into structured research datasets. While the current study focuses primarily on the available 2026 sample period, the framework can be extended to additional years without significant modifications.

---

# 2. Data Preprocessing and Cleaning

## 2.1 Project Objective

Prepare raw option and futures market data for implied volatility estimation and quantitative research. The objective is to transform raw exchange-level observations into standardized datasets suitable for volatility modelling, Greeks calculations, and strategy development.

## 2.2 Data Preprocessing

Several preprocessing procedures were implemented before implied volatility calculations.

First, option contract symbols were parsed to extract contract metadata, including:

* Option type (Call or Put)
* Contract maturity
* Strike price

Second, trading dates and contract identifiers were standardized to ensure consistency across different datasets.

Third, futures market data were aligned with option observations to provide the underlying price required for Black-76 option pricing.

The preprocessing stage produced a structured option dataset containing:

* Trade date
* Option contract
* Underlying futures price
* Strike price
* Time to maturity
* Market option price

These variables form the direct inputs for implied volatility and Greeks calculations.

## 2.3 Data Quality Control

A series of quality-control procedures were implemented throughout the project.

The following checks were performed:

### Contract Consistency Checks

* Verification of option symbol parsing
* Validation of strike extraction
* Validation of maturity extraction

### Missing Data Inspection

* Detection of missing option observations
* Inspection of incomplete trade records
* Identification of unavailable option prices

### Implied Volatility Diagnostics

* Investigation of IV calculation failures
* Review of extreme implied volatility values
* Verification of convergence behaviour

### Dataset Validation

Quality-control scripts were developed for:

* Term structure datasets
* Smile datasets
* Surface datasets
* Greeks summaries
* Trading datasets

These validation procedures ensured that downstream analyses were performed on internally consistent datasets.

## 2.4 Assessment

The data preprocessing and cleaning objective was successfully completed.

A reproducible preprocessing pipeline was established for transforming large-scale option market data into research-ready datasets. Multiple validation procedures were implemented to improve data consistency and reduce the likelihood of downstream modelling errors.

Although additional filtering rules could be introduced in future versions, the current framework provides a reliable foundation for implied volatility analysis, strategy development, and backtesting.

---

# 3. Implied Volatility Surface and Term Structure Construction

## 3.1 Project Objective

This section aims to construct and analyze the implied volatility (IV) surface, volatility smile, and term structure using the processed option dataset. The objective is to understand the cross-sectional and temporal structure of option-implied volatility and to establish a consistent empirical representation of the volatility surface.

## 3.2 Implied Volatility Estimation

### 3.2.1 Black-76 Framework

Implied volatility is derived using the Black-76 option pricing framework, which is suitable for futures-style options. The model is used to invert market option prices into implied volatility values.

### 3.2.2 Implied Volatility Pipeline

The IV estimation pipeline includes:

* Option price extraction from tick-level data
* Alignment with underlying futures prices
* Strike and maturity standardization
* Numerical inversion to obtain implied volatility

### 3.2.3 Daily IV Summary Dataset

The resulting dataset aggregates daily implied volatility statistics across different maturities and strikes, forming the basis for volatility surface and term structure analysis.

## 3.3 Volatility Smile Analysis

### 3.3.1 Smile Construction Methodology

The volatility smile is constructed by grouping implied volatility observations across strikes for each maturity bucket.

### 3.3.2 Overall Smile Behaviour

**Figure 3.1. Overall Volatility Smile**

![Figure 3.1](../figures/smile_bucket_overall.png)

The implied volatility smile exhibits a clear U-shaped structure, indicating that deep in-the-money and out-of-the-money options are priced with higher implied volatility than at-the-money options.

### 3.3.3 Smile Skew Characteristics

A pronounced left-skew is observed in the volatility smile. The left tail, which represents downside protection demand, exhibits significantly higher implied volatility compared to the right tail. This reflects asymmetric market demand for downside risk hedging.

## 3.4 Volatility Surface Construction

### 3.4.1 Surface Construction Methodology

The volatility surface is constructed by mapping implied volatility across both strike and maturity dimensions.

### 3.4.2 Surface Visualization

**Figure 3.2. Volatility Surface Heatmap**

![Figure 3.2](../figures/surface_heatmap_near_h1.png)

The surface exhibits smooth structural behavior across maturities and strikes, with consistent shape persistence over time.

### 3.4.3 Surface Characteristics

The surface indicates that implied volatility is jointly influenced by both strike level and time to maturity, with stronger distortions observed in short-dated options.

## 3.5 Term Structure Analysis

### 3.5.1 Term Structure Construction

The term structure is derived by aggregating at-the-money implied volatility across different maturities.

### 3.5.2 Overall Term Structure Behaviour

**Figure 3.3. Overall ATM Implied Volatility Term Structure**

![Figure 3.3](../figures/atm_term_structure_overall.png)

The term structure is predominantly upward sloping, indicating that longer-dated options carry higher implied volatility than short-dated options.

### 3.5.3 Short-Term Distortions

Short-dated options exhibit a strong left-skewed structure, suggesting elevated demand for near-term downside protection. This effect is particularly pronounced in the nearest maturity bucket.

### 3.5.4 Stability of Term Structure

Despite short-term distortions, the overall shape of the term structure remains stable over time, indicating persistent structural pricing behavior in the market.

## 3.6 Assessment

The construction of the implied volatility surface and term structure successfully reveals key structural properties of the option market, including:

* A stable upward-sloping term structure
* A pronounced volatility smile with left-tail dominance
* Strong short-term asymmetry in implied volatility behavior

These findings provide the empirical foundation for subsequent strategy development and risk analysis.

---

# 4. Strategy Construction

## 4.1 Project Objective

Develop a prototype option trading strategy based on implied volatility signals and term structure information. The objective is to transform volatility analytics into a systematic trading framework suitable for backtesting and evaluation.

## 4.2 Signal Construction

Several signal variables were developed using the implied volatility datasets constructed in previous stages.

The primary inputs include:

* ATM implied volatility
* Implied volatility z-score
* Term structure slope
* Signal strength score

These indicators are designed to identify periods when implied volatility appears unusually low relative to recent observations.

The underlying hypothesis is that unusually depressed volatility levels may subsequently revert toward more normal market conditions.

## 4.3 Strategy Design

A signal-based ATM straddle strategy was implemented as the first trading prototype.

The strategy follows three core steps:

### Entry Rule

Open an ATM straddle position when the signal score exceeds a predefined threshold.

### Position Structure

The position consists of:

* Long ATM Call
* Long ATM Put

This structure provides exposure to future volatility changes while reducing directional market bias.

### Exit Rule

Positions are closed when the signal score falls below the exit threshold.

The resulting framework creates a systematic process for converting volatility signals into tradeable option positions.

## 4.4 Assessment

The strategy construction objective was successfully completed.

A prototype volatility-based trading framework was developed using implied volatility signals and ATM straddle positions.

Although the current implementation represents an initial research prototype rather than a fully developed trading system, it establishes a practical link between volatility analytics and systematic trading decisions.

The framework provides a foundation for future extensions including calendar spreads, volatility arbitrage, and multi-factor option strategies.

---

# 5. Backtesting Framework

## 5.1 Project Objective

Evaluate the performance of the proposed option trading strategy using a systematic backtesting framework. The objective is to assess whether implied volatility signals can be converted into profitable trading opportunities under realistic trading rules.

## 5.2 Backtesting Engine

A rule-based backtesting engine was developed to simulate the trading process.

The framework records:

* Entry date
* Exit date
* Holding period
* Entry signal score
* Exit signal score
* Position returns
* Equity curve
* Drawdown

Each trade is evaluated independently and aggregated into portfolio-level performance statistics.

The backtesting framework is designed to support future extensions including transaction costs, robustness analysis, and alternative trading strategies.

## 5.3 Performance Metrics

**Figure 5.1. Option Strategy Equity Curve**

![Figure 5.1](../figures/option_equity_curve.png)

The following performance metrics were calculated:

### Trade Statistics

* Total Trades: 4
* Winning Trades: 3
* Losing Trades: 1
* Win Rate: 75%

### Return Statistics

* Final Equity: 1.305
* Cumulative Return: 30.5%

### Risk Statistics

**Figure 5.2. Option Strategy Drawdown Curve**

![Figure 5.2](../figures/option_drawdown_curve.png)

* Maximum Drawdown: -0.92%

### Holding Period Statistics

* Average Holding Period: Approximately 4 trading days

These metrics provide a preliminary assessment of strategy behavior during the sample period.

## 5.4 Assessment

The backtesting objective was successfully completed.

The strategy prototype generated positive performance within the available sample period and demonstrated the ability to convert volatility signals into systematic trading decisions.

However, the current results should be interpreted cautiously due to the limited number of trades available in the sample. The primary contribution of this stage is the successful construction of a reusable backtesting framework rather than the validation of a fully mature trading strategy.

Future research will focus on expanding the trade sample, introducing alternative strategy structures, and evaluating performance across different market environments.

---

# 6. Risk and Robustness Analysis

## 6.1 Project Objective

Evaluate the sensitivity of strategy performance to transaction costs and parameter choices. The objective is to determine whether the observed strategy performance is highly dependent on specific assumptions or remains reasonably stable under alternative configurations.

## 6.2 Transaction Cost Analysis

Transaction costs are an important consideration in option trading strategies because option markets often exhibit wider bid-ask spreads and lower liquidity than underlying futures markets.

To evaluate the impact of trading frictions, a transaction cost analysis framework was implemented.

The analysis examines how strategy performance changes when different levels of trading costs are applied to each transaction.

This procedure helps assess whether strategy profitability is driven solely by idealized assumptions or remains economically meaningful after accounting for realistic execution costs.

## 6.3 Robustness Tests

Several robustness procedures were implemented within the project framework.

The robustness suite includes:

* Signal threshold sensitivity analysis
* Transaction cost sensitivity analysis
* Performance comparison across parameter configurations
* Robustness dashboard generation

**Figure 6.1. Robustness Analysis Dashboard**

![Figure 6.1](../figures/robustness_dashboard.png)

These tests are designed to identify whether strategy outcomes are highly dependent on a specific parameter setting.

The results indicate that the framework can systematically evaluate alternative assumptions and parameter choices, providing a foundation for future strategy validation.

### Limitations of Current Robustness Results

The current sample contains a relatively small number of completed trades.

As a result, robustness conclusions should be interpreted as preliminary evidence rather than definitive validation of strategy effectiveness.

Future research with larger datasets and longer sample periods will provide a more reliable assessment of parameter stability and risk characteristics.

## 6.4 Assessment

The risk and robustness analysis objective was successfully completed.

A reusable framework was established for evaluating transaction costs, parameter sensitivity, and strategy stability.

Although the current empirical sample remains limited, the project successfully demonstrates the infrastructure required for systematic robustness analysis.

This framework represents an important step toward developing institution-grade option research and strategy evaluation capabilities.

---

# 7. Project Summary

## 7.1 Completion Status

The project was originally designed around seven major objectives:

1. Data Acquisition
2. Data Preprocessing
3. Data Cleaning
4. Implied Volatility Surface and Term Structure Construction
5. Strategy Construction
6. Backtesting Framework
7. Risk and Robustness Analysis

All seven objectives were successfully completed during Phase I of the project.

The resulting platform provides an end-to-end workflow covering the entire quantitative research process from raw market data processing to strategy evaluation.

### Completion Assessment

| Objective                   | Status    |
| --------------------------- | --------- |
| Data Acquisition            | Completed |
| Data Preprocessing          | Completed |
| Data Cleaning               | Completed |
| IV Surface & Term Structure | Completed |
| Strategy Construction       | Completed |
| Backtesting Framework       | Completed |
| Risk & Robustness Analysis  | Completed |

Overall Project Status:

**Phase I Complete**

---

## 7.2 Key Findings

Several important findings emerged from the project.

### Volatility Structure

The implied volatility term structure is generally upward sloping, indicating higher implied volatility for longer-dated options.

### Volatility Smile

The volatility smile exhibits a pronounced U-shape with significant left-tail dominance, reflecting stronger market demand for downside protection.

### Surface Stability

The overall volatility surface remains structurally stable throughout the sample period despite short-term fluctuations.

### Strategy Prototype

The signal-based ATM straddle strategy generated positive returns within the available sample period and successfully demonstrated the practical application of volatility-based trading signals.

### Research Infrastructure

The project successfully established a reusable framework for implied volatility analysis, strategy research, backtesting, and robustness evaluation.

---

## 7.3 Limitations

Several limitations should be acknowledged.

### Limited Historical Coverage

The current analysis is based primarily on the available 2026 dataset.

As a result, conclusions regarding long-term stability should be interpreted cautiously.

### Limited Trade Sample

The strategy prototype generated a relatively small number of completed trades.

Additional data will be required before drawing strong conclusions regarding long-term strategy performance.

### Prototype-Level Strategies

The current implementation focuses on an initial volatility-based strategy prototype.

More sophisticated strategies such as calendar spreads, volatility arbitrage structures, and multi-factor option portfolios remain subjects for future development.

---

## 7.4 Future Work

The project establishes a strong foundation for future research and development.

Potential extensions include:

### Data Expansion

* Additional historical years
* Larger sample periods
* More market environments

### Research Expansion

* ATM Term Structure Research
* Volatility Smile Dynamics
* Greeks Distribution Analysis
* Regime Classification
* Volatility Forecasting

### Strategy Expansion

* Calendar Spread Strategies
* Volatility Arbitrage Strategies
* Multi-Factor Signal Models
* Portfolio-Level Option Strategies

### Platform Expansion

* Enhanced reporting automation
* Additional robustness tests
* Advanced visualization tools

The completion of Phase I marks the transition from infrastructure development to deeper quantitative research and strategy innovation.

---

# Appendices

---

# Appendix A. Project Architecture

## A.1 Overview

The Quant Option Research Platform was developed as a modular quantitative research framework. Rather than consisting of a single analysis script, the project is organized into multiple independent components that together support the complete research workflow, from raw market data processing to strategy evaluation and report generation.

The modular architecture improves code reusability, reproducibility, and maintainability, allowing each research component to be developed and tested independently while remaining compatible with the overall platform.

---

## A.2 Overall Workflow

The overall research workflow consists of seven major stages:

```text
Raw Option Market Data
            │
            ▼
Data Acquisition
            │
            ▼
Data Preprocessing & Cleaning
            │
            ▼
Implied Volatility Estimation
            │
            ▼
Smile / Surface / Term Structure Construction
            │
            ▼
Signal Generation
            │
            ▼
Strategy Construction
            │
            ▼
Backtesting
            │
            ▼
Risk & Robustness Analysis
            │
            ▼
Research Reports
```

Each stage produces standardized intermediate datasets that are subsequently consumed by downstream modules.

---

## A.3 Modular Design

The platform follows a modular design philosophy.

Major functional modules include:

| Module                | Responsibility                                              |
| --------------------- | ----------------------------------------------------------- |
| Data Processing       | Read, preprocess and clean raw market data                  |
| IV Engine             | Estimate implied volatility using Black-76                  |
| Greeks Engine         | Compute option Greeks                                       |
| Smile Module          | Construct volatility smile                                  |
| Surface Module        | Build volatility surfaces                                   |
| Term Structure Module | Construct ATM term structures                               |
| Signal Module         | Generate quantitative trading signals                       |
| Strategy Module       | Implement trading strategies                                |
| Backtest Module       | Evaluate historical performance                             |
| Robustness Module     | Perform parameter sensitivity and transaction cost analysis |
| Reporting Module      | Generate research reports and visualizations                |

Each module can be developed, tested, and extended independently.

---

## A.4 Platform Characteristics

The project architecture exhibits several important characteristics.

### Reproducibility

All intermediate datasets are generated programmatically from raw market data, ensuring that research results can be reproduced.

### Scalability

The platform is designed to accommodate additional historical data, new option products, and more sophisticated trading strategies without requiring substantial architectural changes.

### Modularity

Independent research modules allow future work to extend individual components while preserving compatibility with the existing framework.

### Automation

Most analytical procedures—including implied volatility estimation, Greeks calculation, strategy evaluation, and report generation—can be executed automatically through Python scripts.

---

## A.5 Appendix Summary

The Quant Option Research Platform establishes a reusable infrastructure for quantitative option research.

Rather than representing a single empirical study, the platform provides a general framework capable of supporting future research on implied volatility, volatility surfaces, option strategies, and systematic backtesting.

# Appendix B. Research Pipeline

## B.1 Overview

The Quant Option Research Platform follows a standardized research pipeline that transforms raw option market data into quantitative research outputs through a sequence of reproducible analytical stages.

Rather than performing isolated analyses, each stage generates intermediate datasets that become the inputs of subsequent modules. This pipeline design improves reproducibility, scalability, and transparency throughout the research process.

---

## B.2 Research Pipeline

The complete research pipeline consists of the following stages:

```text
Raw Market Data
        │
        ▼
Data Inspection
        │
        ▼
Data Preprocessing
        │
        ▼
Data Cleaning
        │
        ▼
Implied Volatility Estimation
        │
        ▼
Greeks Calculation
        │
        ▼
Volatility Smile Construction
        │
        ▼
Volatility Surface Construction
        │
        ▼
ATM Term Structure Construction
        │
        ▼
Signal Generation
        │
        ▼
Strategy Construction
        │
        ▼
Backtesting
        │
        ▼
Risk & Robustness Analysis
        │
        ▼
Research Reports
```

Each stage is implemented independently and communicates through standardized datasets.

---

## B.3 Intermediate Outputs

The pipeline generates a series of reusable intermediate datasets, including:

* Daily implied volatility summaries
* Greeks summaries
* Smile datasets
* Surface datasets
* ATM term structure datasets
* Signal datasets
* Trade datasets
* Backtesting results
* Robustness analysis results

These outputs enable downstream research without requiring repeated processing of raw market data.

---

## B.4 Pipeline Characteristics

The research pipeline was designed with several engineering principles.

### Reproducibility

Every stage can be regenerated directly from raw market data.

### Independence

Each module operates independently while maintaining standardized interfaces.

### Scalability

Additional research modules can be incorporated without modifying the existing pipeline.

### Automation

The entire workflow can be executed automatically through Python scripts.

---

## B.5 Appendix Summary

The research pipeline provides a standardized workflow for transforming raw option market data into quantitative research results.

This pipeline serves as the core infrastructure supporting both the current project and future extensions of the Quant Option Research Platform.

# Appendix C. Generated Research Datasets

## C.1 Overview

Throughout the development of the Quant Option Research Platform, a series of standardized research datasets were generated. These datasets serve as reusable intermediate outputs that support subsequent analyses, strategy development, backtesting, and report generation.

Rather than operating directly on raw market data, downstream research modules consume these standardized datasets, improving reproducibility and computational efficiency.

---

## C.2 Implied Volatility Datasets

The implied volatility module produces the following research datasets.

| Dataset                    | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| daily_iv_summary.csv       | Daily summary statistics of implied volatility         |
| atm_iv_dataset_preview.csv | Preview dataset of ATM implied volatility observations |

These datasets provide the foundation for volatility analysis throughout the project.

---

## C.3 Greeks Datasets

The Greeks module generates daily summaries and diagnostic outputs.

| Dataset                       | Description                       |
| ----------------------------- | --------------------------------- |
| daily_greeks_summary.csv      | Daily summary of option Greeks    |
| daily_greeks_correlation.csv  | Correlation analysis among Greeks |
| daily_greeks_extreme_days.csv | Extreme Greeks observations       |

These datasets support both descriptive analysis and strategy construction.

---

## C.4 Volatility Structure Datasets

Several datasets describe different dimensions of the implied volatility structure.

### Smile

| Dataset                        | Description                                     |
| ------------------------------ | ----------------------------------------------- |
| daily_smile_bucket_iv.csv      | Average implied volatility across smile buckets |
| smile_dataset_near_preview.csv | Near-month smile dataset                        |
| smile_extreme_high_iv.csv      | Extreme smile observations                      |

### Surface

| Dataset                          | Description                      |
| -------------------------------- | -------------------------------- |
| daily_surface_bucket_iv.csv      | Daily volatility surface summary |
| surface_dataset_near_preview.csv | Near-month volatility surface    |
| surface_bucket_coverage.csv      | Surface coverage statistics      |
| surface_extreme_high_iv.csv      | Extreme surface observations     |

### Term Structure

| Dataset                         | Description                         |
| ------------------------------- | ----------------------------------- |
| daily_term_spread_summary.csv   | Daily term spread summary           |
| term_structure_preview.csv      | ATM term structure dataset          |
| term_structure_extreme_days.csv | Extreme term structure observations |
| atm_term_structure_preview.csv  | Daily ATM term structure preview    |

Together, these datasets describe the cross-sectional structure of implied volatility across strikes and maturities.

---

## C.5 Signal and Strategy Datasets

The strategy module produces several intermediate datasets for signal generation and trade execution.

| Dataset                   | Description                        |
| ------------------------- | ---------------------------------- |
| daily_signal_features.csv | Daily quantitative signal features |
| option_trade_dataset.csv  | Standardized option trade dataset  |
| long_only_trades.csv      | Executed prototype trades          |

These datasets bridge volatility analytics and systematic trading strategies.

---

## C.6 Backtesting Datasets

Backtesting outputs are stored separately from research datasets.

| Dataset                         | Description                |
| ------------------------------- | -------------------------- |
| option_strategy_backtest.csv    | Initial strategy backtest  |
| option_strategy_backtest_v2.csv | Updated strategy backtest  |
| backtest_summary.csv            | Trade-level summary        |
| backtest_long_only_v2.csv       | Long-only strategy results |

These datasets record historical trading performance and portfolio evolution.

---

## C.7 Robustness Datasets

Robustness analysis generates dedicated evaluation datasets.

| Dataset                       | Description                               |
| ----------------------------- | ----------------------------------------- |
| robustness_suite_results.csv  | Summary of robustness experiments         |
| transaction_cost_analysis.csv | Transaction cost analysis                 |
| cost_sweep_v2.csv             | Parameter sensitivity under varying costs |

These datasets support systematic evaluation of model stability and strategy robustness.

---

## C.8 Appendix Summary

The Quant Option Research Platform generates a comprehensive collection of standardized research datasets covering implied volatility, Greeks, volatility structures, trading signals, backtesting, and robustness analysis.

These datasets represent reusable research assets that enable future studies without repeating the entire data processing workflow.

# Appendix D. Generated Figures

## D.1 Overview

In addition to standardized research datasets, the Quant Option Research Platform automatically generates a collection of figures for exploratory analysis, strategy evaluation, and report generation.

These figures provide visual representations of implied volatility behaviour, Greeks, trading performance, and robustness analyses.

---

## D.2 Implied Volatility Figures

| Figure Category | Representative Figures                                     |
| --------------- | ---------------------------------------------------------- |
| IV Distribution | iv_distribution_histogram.png, iv_distribution_boxplot.png |
| ATM IV          | daily_near_iv_mean.png, daily_atm_iv_by_term.png           |

These figures summarize the statistical properties of implied volatility across the sample period.

---

## D.3 Volatility Smile Figures

| Figure Category | Representative Figures                |
| --------------- | ------------------------------------- |
| Smile Profile   | smile_bucket_overall.png              |
| Monthly Smile   | smile_bucket_monthly.png              |
| Smile Skew      | smile_skew_proxy_left_minus_right.png |
| ATM vs Wings    | daily_atm_vs_wings.png                |

These figures describe the cross-sectional structure of implied volatility across strike prices.

---

## D.4 Volatility Surface Figures

| Figure Category | Representative Figures          |
| --------------- | ------------------------------- |
| Surface Heatmap | surface_heatmap_near_h1.png     |
| Monthly Surface | surface_heatmap_near_202601.png |
| Monthly Surface | surface_heatmap_near_202603.png |

These figures visualize implied volatility jointly across strike and maturity dimensions.

---

## D.5 Term Structure Figures

| Figure Category        | Representative Figures                   |
| ---------------------- | ---------------------------------------- |
| Overall Term Structure | atm_term_structure_overall.png           |
| Monthly Term Structure | atm_term_structure_monthly.png           |
| Daily Term Rank        | daily_atm_iv_by_term_rank.png            |
| Term Slope             | daily_atm_term_slope_next_minus_near.png |

These figures summarize the evolution of implied volatility across different maturities.

---

## D.6 Greeks Figures

| Figure Category | Representative Figures                                                   |
| --------------- | ------------------------------------------------------------------------ |
| Delta           | delta_profile_overall.png, delta_profile_monthly.png                     |
| Gamma           | gamma_profile_overall.png, gamma_profile_monthly.png                     |
| Vega            | vega_profile_overall.png, vega_profile_monthly.png                       |
| Heatmaps        | delta_heatmap_daily.png, gamma_heatmap_daily.png, vega_heatmap_daily.png |

These figures illustrate the behaviour of option sensitivities over time.

---

## D.7 Strategy and Backtesting Figures

| Figure Category     | Representative Figures         |
| ------------------- | ------------------------------ |
| Equity Curve        | option_equity_curve.png        |
| Drawdown            | option_drawdown_curve.png      |
| Return Distribution | option_return_distribution.png |
| Trade Returns       | option_trade_returns.png       |
| Holding Period      | option_holding_days.png        |

These figures summarize the performance of the prototype trading strategy.

---

## D.8 Robustness Figures

| Figure Category      | Representative Figures           |
| -------------------- | -------------------------------- |
| Robustness Dashboard | robustness_dashboard.png         |
| Signal Strength      | signal_strength_distribution.png |
| Signal Through Time  | signal_score_through_time.png    |

These figures support robustness analysis and parameter evaluation.

---

## D.9 Appendix Summary

The platform automatically generates a comprehensive collection of figures covering volatility analysis, option Greeks, strategy evaluation, and robustness assessment.

These visual outputs support both research interpretation and automated report generation.

# Appendix E. Project Directory

## E.1 Overview

The Quant Option Research Platform is organized as a modular research project. Source code, datasets, reports, and research notebooks are separated into dedicated directories to improve maintainability and reproducibility.

---

## E.2 Project Structure

```text
Quant_Option_Project/

│
├── analysis/
│      Data analysis modules
│      IV engine
│      Greeks engine
│      Plotting utilities
│      Statistics
│
├── config/
│      Project configuration
│      Paths
│
├── docs/
│      Technical documentation
│      Research methodology
│      Project status
│      Changelog
│
├── research/
│      exports/
│      figures/
│      notebooks/
│      reports/
│      summaries/
│      studies/
│
├── scripts/
│      Data processing scripts
│      Report generation
│      Research utilities
│
├── tests/
│      Validation scripts
│      Quality-control tests
│
├── requirements.txt
│
└── README.md
```

---

## E.3 Directory Description

| Directory | Purpose                                                              |
| --------- | -------------------------------------------------------------------- |
| analysis  | Quantitative analysis modules and reusable research functions        |
| config    | Global configuration and project paths                               |
| docs      | Technical documentation and project records                          |
| research  | Research outputs including datasets, figures, reports, and notebooks |
| scripts   | Executable Python scripts for data processing and automation         |
| tests     | Validation and quality-control scripts                               |

---

## E.4 Research Output Organization

Research outputs are organized into dedicated folders.

| Folder    | Contents                                    |
| --------- | ------------------------------------------- |
| exports   | CSV datasets generated during research      |
| summaries | Parquet summary datasets                    |
| figures   | Automatically generated figures             |
| reports   | Text-based research reports                 |
| notebooks | Markdown research notes and project reports |
| studies   | Individual research scripts                 |

This separation enables downstream analyses to reuse standardized outputs without modifying the underlying research code.

---

## E.5 Design Philosophy

The project adopts several software engineering principles.

### Modular Design

Each component performs a clearly defined task.

### Separation of Concerns

Research logic, visualization, datasets, and documentation are stored independently.

### Reproducibility

All research outputs can be regenerated directly from raw market data.

### Extensibility

Additional research modules can be integrated without restructuring the existing project.

---

## E.6 Appendix Summary

The directory organization reflects the project's goal of building a reusable quantitative research platform rather than a collection of independent analysis scripts.

This modular architecture supports future development, collaboration, and automated report generation.

# Appendix F. Software Environment

## F.1 Overview

The Quant Option Research Platform was developed using an open-source Python environment. The software stack was selected to support efficient numerical computation, large-scale data processing, quantitative research, and reproducible report generation.

---

## F.2 Development Environment

| Component               | Version / Description |
| ----------------------- | --------------------- |
| Operating System        | Windows 11            |
| Programming Language    | Python 3.14           |
| Development Environment | Visual Studio Code    |
| Version Control         | Git                   |
| Repository Hosting      | GitHub                |

---

## F.3 Core Python Packages

The following packages constitute the primary software environment.

| Package        | Purpose                                    |
| -------------- | ------------------------------------------ |
| NumPy          | Numerical computation                      |
| Pandas         | Data manipulation                          |
| SciPy          | Scientific computing and numerical methods |
| Matplotlib     | Data visualization                         |
| PyArrow        | Efficient Parquet data storage             |
| OpenPyXL       | Excel file processing                      |
| Jupyter        | Interactive research notebooks             |
| IPython Kernel | Notebook execution environment             |

Additional packages may be incorporated as the platform continues to evolve.

---

## F.4 Data Storage Formats

The platform employs multiple data formats depending on research requirements.

| Format   | Usage                                        |
| -------- | -------------------------------------------- |
| CSV      | Human-readable research datasets             |
| Parquet  | High-performance intermediate datasets       |
| PNG      | Figures and visualizations                   |
| Markdown | Research reports and technical documentation |

This combination balances readability, storage efficiency, and reproducibility.

---

## F.5 Reproducibility

The platform was designed to ensure that all major research outputs can be reproduced directly from raw market data.

Reproducibility is supported through:

* Standardized project directory structure
* Modular Python scripts
* Version-controlled source code
* Intermediate research datasets
* Automated figure generation
* Structured technical documentation

These design principles facilitate future maintenance, extension, and independent verification of research results.

---

## F.6 Appendix Summary

The software environment combines open-source scientific computing tools with a modular project architecture, providing a reproducible foundation for quantitative option research and future platform development.

# Appendix G. Version History

## G.1 Overview

The Quant Option Research Platform has evolved through multiple development stages. Each stage introduced new research capabilities while maintaining compatibility with previously completed modules.

---

## G.2 Development Timeline

| Version                | Major Milestones                                           |
| ---------------------- | ---------------------------------------------------------- |
| Initial Project        | Project initialization and repository setup                |
| Data Platform          | Raw data inspection, preprocessing, and cleaning framework |
| IV Engine              | Black-76 implied volatility estimation                     |
| Greeks Module          | Delta, Gamma, Vega and related analytical outputs          |
| Volatility Analysis    | Smile, surface, and term structure construction            |
| Strategy Prototype     | Signal generation and ATM straddle strategy                |
| Backtesting Framework  | Portfolio simulation and performance evaluation            |
| Robustness Framework   | Transaction cost and sensitivity analysis                  |
| RQ1 Research           | Daily ATM implied volatility distribution study            |
| Seven-Goal Report v1.0 | Comprehensive technical and research documentation         |

---

## G.3 Phase I Deliverables

Phase I successfully delivered the following components:

### Platform

* Quant Option Research Platform
* Modular research architecture
* Automated research pipeline

### Research

* RQ1: Daily ATM Implied Volatility Distribution
* Seven-Goal Project Report

### Analytics

* Implied volatility estimation
* Greeks analysis
* Volatility smile
* Volatility surface
* ATM term structure

### Trading

* Signal generation
* Prototype ATM straddle strategy
* Backtesting framework
* Robustness analysis

---

## G.4 Future Development

The completion of Phase I establishes a foundation for future research.

Potential Phase II objectives include:

* Expanded historical datasets
* Additional research questions (RQ2, RQ3, ...)
* Advanced volatility forecasting
* Multi-factor option strategies
* Calendar spread strategies
* Volatility arbitrage research
* Portfolio optimization
* Automated report generation

Future versions of the platform will extend these capabilities while preserving the modular architecture developed during Phase I.

---

## G.5 Final Statement

The completion of the Seven-Goal Project Report marks the conclusion of Phase I of the Quant Option Research Platform.

At this stage, the project has progressed from a collection of analytical scripts to a structured quantitative research platform integrating data engineering, volatility modelling, strategy development, backtesting, robustness evaluation, and technical documentation.

This report serves as the official technical documentation for Phase I and provides the foundation for future quantitative research and platform development.

---

# Closing Statement

The completion of this report marks the successful conclusion of **Phase I** of the Quant Option Research Platform.

Throughout this phase, a complete quantitative research framework was established, integrating data engineering, implied volatility modelling, volatility surface construction, quantitative strategy development, systematic backtesting, and robustness analysis into a unified research platform.

More importantly, the project has evolved from a collection of independent analytical scripts into a modular, reproducible, and extensible quantitative research platform.

The work presented in this report provides a solid foundation for future research, including expanded historical datasets, additional research questions, advanced volatility modelling, and more sophisticated option trading strategies.

This report serves as the official technical documentation for **Phase I** and marks the beginning of the next stage of platform development.

---

**Quant Option Research Platform**

**Seven-Goal Project Report v1.0**

**Phase I Complete**

**June 2026**

---

*End of Report*