# Research Question 1

# Daily ATM Implied Volatility Distribution

**Research ID:** RQ1  
**Version:** 1.0  
**Status:** Frozen  
**Last Updated:** June 2026  
**Author:** Jingzhe Yang  
**Project:** Quant Option Research Platform  

---

## Executive Summary

This study establishes the first empirical benchmark for daily at-the-money (ATM) implied volatility using the 2026 Chinese index option dataset. Through descriptive statistics and exploratory data analysis, the research characterizes the central tendency, symmetry, tail behaviour, and extreme volatility observations of the empirical distribution.

The results indicate that daily ATM implied volatility exhibits a stable central distribution with approximate symmetry and moderate excess kurtosis, suggesting that extreme volatility observations occur more frequently than predicted by a Gaussian distribution. Rather than representing statistical anomalies, these observations reflect economically meaningful market regimes that warrant further investigation.

The statistical benchmark established in this study provides the empirical foundation for subsequent research on implied volatility term structures, smile dynamics, option Greeks, volatility forecasting, and systematic option trading strategies. As the first research question within this project, this study defines the baseline statistical characteristics against which future analyses will be evaluated.

## 1. Introduction： Why does this question matter?

Implied volatility is one of the most important state variables in option markets because it summarizes the market's expectation of future uncertainty. Among all implied volatility measures, at-the-money (ATM) implied volatility occupies a central position, serving as the benchmark level from which volatility smiles, skews, and term structures are constructed. Consequently, understanding the statistical behavior of ATM implied volatility is a prerequisite for any systematic study of option market dynamics.

While volatility smiles and volatility surfaces describe cross-sectional differences across strikes and maturities, these structures are fundamentally anchored by the ATM volatility level. Without first establishing the empirical characteristics of ATM implied volatility, it becomes difficult to distinguish ordinary market fluctuations from genuinely abnormal volatility regimes. A quantitative understanding of the baseline distribution therefore provides essential context for interpreting more complex volatility structures.

From a practical perspective, the empirical distribution of ATM implied volatility also provides valuable information for quantitative research and risk management. Distributional properties such as central tendency, dispersion, skewness, tail behavior, and the frequency of extreme observations influence volatility forecasting, stochastic volatility model calibration, strategy design, and portfolio risk assessment. These statistical characteristics represent the stylized facts that any realistic quantitative model should be able to capture.

Accordingly, this study investigates the empirical distribution of daily ATM implied volatility using the 2026 Chinese index option dataset. Through descriptive statistics and exploratory data analysis, this research establishes a statistical benchmark for subsequent studies on volatility term structures, smile dynamics, option Greeks, and volatility-based trading strategies.

## 2. Research Question

The objective of this study is to establish a statistical benchmark for daily at-the-money (ATM) implied volatility using the 2026 Chinese index option dataset. Rather than focusing on option pricing models or trading strategies, this study aims to characterize the empirical statistical properties of the ATM implied volatility distribution.

The primary research question is:

> **Can the empirical distribution of daily ATM implied volatility be characterized by stable statistical properties that establish a reliable benchmark for subsequent volatility research?**

To answer this question, the following sub-questions are investigated:

1. Is the empirical distribution approximately symmetric?

2. Does the distribution exhibit excess kurtosis or fat-tail behavior?

3. How frequently do extreme volatility observations occur?

4. Can these statistical characteristics serve as a reference benchmark for future studies on volatility smiles, term structures, Greeks, and volatility-based trading strategies?

These questions provide the foundation for the remaining analyses presented in this study.

## 3. Dataset

This study uses the daily summary dataset constructed from the 2026 Chinese index option market. The dataset was generated through the data processing pipeline developed in Version 1 of this project, which includes implied volatility estimation, data quality control, and daily aggregation.

Rather than analyzing individual option transactions, this study focuses on daily aggregated at-the-money (ATM) implied volatility. For each trading day, the ATM implied volatility is summarized across the available option contracts, producing a stable daily measure that represents the overall market's implied volatility level.

The dataset contains **351 daily observations** and includes the following variables:

| Variable            | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| trade_date          | Trading date                                                 |
| term_rank           | Relative maturity ranking                                    |
| atm_iv_mean         | Mean daily ATM implied volatility                            |
| atm_iv_median       | Median daily ATM implied volatility                          |
| atm_iv_std          | Cross-sectional standard deviation of ATM implied volatility |
| T_mean              | Average time to maturity                                     |
| days_to_expiry_mean | Average remaining days to expiration                         |
| row_count           | Number of option observations included in the daily summary  |
| expiry_count        | Number of distinct expiration months represented             |

For this study, **atm_iv_mean** is selected as the primary variable of interest because it provides a representative measure of the market's daily implied volatility level while reducing idiosyncratic noise from individual option contracts.

Although the current dataset covers only the 2026 sample period, it is sufficient for establishing an initial statistical benchmark of daily ATM implied volatility. Multi-year datasets will be incorporated in future studies to evaluate the temporal stability of the observed statistical characteristics.

| Item                   |                             Value |
| ---------------------- | --------------------------------: |
| Sample Period          |                           2026 H1 |
| Frequency              |                             Daily |
| Number of Trading Days |                               351 |
| Primary Variable       |                       atm_iv_mean |
| Data Source            | Project-generated summary dataset |
| Observation Level      |                  Daily aggregated |

## 4. Methodology

The objective of this study is to characterize the empirical distribution of daily ATM implied volatility. Since the research focuses on understanding the statistical properties of the observed data rather than testing a pricing model, the methodology emphasizes descriptive statistics and exploratory data analysis (EDA). Each analytical component is designed to answer one of the research questions defined in Chapter 2.

### 4.1 Descriptive Statistics

The first step is to summarize the central tendency and dispersion of the daily ATM implied volatility series. The following statistics are computed:

* Mean
* Median
* Standard deviation
* Minimum and maximum
* Selected empirical quantiles (5%, 25%, 75%, and 95%)
* Skewness
* Excess kurtosis

These statistics provide an overall description of the location, variability, symmetry, and tail characteristics of the empirical distribution.

### 4.2 Distribution Visualization

To visualize the empirical distribution, a histogram and a box plot are constructed.

The histogram illustrates the overall shape of the distribution, allowing visual inspection of concentration regions, asymmetry, and tail behavior. The box plot summarizes the median, interquartile range (IQR), and potential extreme observations.

These visualizations complement the numerical statistics and provide intuitive evidence for subsequent interpretation.

### 4.3 Distribution Shape Analysis

Distribution shape is evaluated using skewness and excess kurtosis.

Skewness measures the degree of asymmetry around the center of the distribution, while excess kurtosis quantifies the heaviness of the tails relative to a Gaussian distribution.

Together, these measures help determine whether the observed ATM implied volatility can be reasonably approximated by a symmetric distribution and whether extreme volatility regimes occur more frequently than expected under normality.

### 4.4 Outlier Detection

Potential extreme observations are identified using the Interquartile Range (IQR) rule.

Observations located outside

Q1 − 1.5 × IQR

or

Q3 + 1.5 × IQR

are classified as statistical outliers.

Rather than treating outliers as data errors, this study interprets them as possible indicators of abnormal market volatility regimes.

### 4.5 Research Framework

The overall analytical workflow is summarized below:

Daily ATM IV Dataset

↓

Descriptive Statistics

↓

Distribution Visualization

↓

Distribution Shape Analysis

↓

Outlier Detection

↓

Interpretation

↓

Research Conclusion

This workflow provides a systematic framework for establishing a statistical benchmark of daily ATM implied volatility, which serves as the foundation for subsequent studies on volatility term structures, smile dynamics, Greeks, and quantitative trading strategies.

## 5. Empirical Result

### 5.1 Overall Distribution

The empirical distribution of daily ATM implied volatility exhibits a stable and well-defined central tendency throughout the sample period. Across the 351 daily observations, the average ATM implied volatility is **18.85%**, while the median is **18.71%**, indicating that the majority of observations are concentrated around a consistent volatility level.

The histogram shown in **Figure 5.1** confirms that most observations fall within a relatively narrow interval between approximately **18% and 20%**, suggesting that the option market remained in a relatively stable volatility regime during most trading days within the sample period.

**Figure 5.1. Distribution of Daily ATM Implied Volatility**

![Figure 5.1](../figures/iv_distribution_histogram.png)

*Figure 5.1 illustrates the empirical distribution of daily ATM implied volatility during the 2026 sample period. Most observations are concentrated around the central volatility regime, while only a limited number of observations appear in the tails.*

Although observations outside this range are present, they occur relatively infrequently and therefore do not dominate the overall distribution. This finding suggests that the ATM implied volatility series possesses a stable statistical structure, making it suitable as a benchmark variable for subsequent empirical analyses.

Overall, the empirical evidence indicates that daily ATM implied volatility can be summarized by a stable baseline distribution, which provides the statistical foundation for the remaining research questions investigated in this study.

### 5.2 Distribution Symmetry

The symmetry of the empirical distribution is evaluated using three complementary statistics: the mean, the median, and the sample skewness.

The estimated mean of daily ATM implied volatility is **18.85%**, while the median is **18.71%**. The close agreement between these two measures suggests that the center of the distribution is not materially affected by extreme observations.

This conclusion is further supported by the estimated sample skewness of **−0.035**, which is very close to zero. The negative sign indicates a marginally longer left tail; however, the magnitude is sufficiently small that no meaningful asymmetry is observed in the empirical distribution.

The box plot presented in **Figure 5.2** visually supports this conclusion. The median is positioned near the center of the interquartile range, and the overall distribution appears well balanced around its central tendency.

**Figure 5.2. Box Plot of Daily ATM Implied Volatility**

![Figure 5.2](../figures/iv_distribution_boxplot.png)

*Figure 5.2 summarizes the median, interquartile range (IQR), and extreme volatility observations. Only a limited number of observations lie outside the whiskers, indicating that extreme volatility regimes are relatively infrequent.*

Overall, the statistical evidence suggests that the empirical distribution of daily ATM implied volatility can be reasonably regarded as approximately symmetric over the sample period.

The approximate symmetry of the empirical distribution provides a stable statistical baseline for subsequent analyses. However, symmetry alone does not imply normality, and the behaviour of the distribution tails must therefore be examined separately.

### 5.3 Tail Behaviour

Tail behaviour is evaluated using the sample excess kurtosis together with the empirical distribution illustrated in Figure 5.1.

The estimated excess kurtosis of the daily ATM implied volatility series is **1.026**, which is substantially greater than zero. Under the convention adopted by pandas, a Gaussian distribution has an excess kurtosis of zero. Therefore, the observed value indicates that the empirical distribution is more peaked and possesses heavier tails than a normal distribution.

This result suggests that extremely high or low implied volatility levels occur more frequently than would be expected under a Gaussian assumption. Although such observations remain relatively infrequent, they contribute disproportionately to the overall distributional characteristics and therefore cannot be ignored in quantitative modelling.

From a financial perspective, heavy-tail behaviour is a well-documented stylized fact of financial markets. The presence of excess kurtosis implies that volatility regimes occasionally experience abrupt changes that are inconsistent with simple normal-distribution assumptions. Consequently, quantitative models relying solely on Gaussian distributions may underestimate the probability of extreme market conditions.

Based on the available evidence, the empirical distribution is consistent with moderate heavy-tail behaviour. Additional statistical tests, including normality tests and QQ plots, will be incorporated in future revisions to further validate this conclusion.

The existence of moderately heavy tails naturally motivates the investigation of individual extreme volatility observations, which is presented in the following section.

### 5.4 Extreme Volatility Observations

Potential extreme volatility observations are identified using the Interquartile Range (IQR) criterion. Rather than interpreting these observations as data errors, this study regards them as statistically unusual market states that may correspond to periods of elevated uncertainty or exceptionally calm market conditions.

As illustrated in **Figure 5.2**, only a limited number of observations fall outside the whisker boundaries, indicating that extreme implied volatility levels occur relatively infrequently during the sample period. This result is consistent with the histogram presented in Figure 5.1, where most observations remain concentrated around the central volatility regime.

Although the proportion of extreme observations is relatively small, these periods are of particular importance for quantitative finance. Episodes of unusually high implied volatility are frequently associated with market stress, increased uncertainty, and rapid repricing of option contracts, while unusually low implied volatility may reflect periods of exceptionally stable market expectations.

Consequently, these extreme volatility observations should not be regarded as statistical anomalies to be discarded. Instead, they represent economically meaningful market regimes that warrant separate investigation in subsequent studies. Their occurrence may provide valuable information for volatility forecasting, regime identification, option portfolio risk management, and the design of volatility-based trading strategies.

Overall, the empirical evidence suggests that the daily ATM implied volatility series is characterized by a stable central distribution accompanied by a relatively small number of economically significant extreme volatility observations.

### 5.5 Statistical Benchmark

The empirical analyses presented in the previous sections collectively establish a statistical benchmark for daily ATM implied volatility during the 2026 sample period.

First, the distribution exhibits a stable central tendency, with most observations concentrated within a relatively narrow volatility range. Second, the empirical distribution is approximately symmetric, as evidenced by the close agreement between the mean and median together with the near-zero sample skewness. Third, the positive excess kurtosis indicates that the distribution exhibits moderately heavier tails than a Gaussian distribution, suggesting that extreme volatility observations occur more frequently than would be expected under normality. Finally, the box plot and IQR analysis demonstrate that these extreme observations remain relatively infrequent and should be interpreted as economically meaningful market regimes rather than statistical anomalies.

Taken together, these findings suggest that daily ATM implied volatility possesses sufficiently stable statistical characteristics to serve as a reference benchmark for subsequent empirical studies. Future analyses of volatility term structures, smile dynamics, option Greeks, and volatility-based trading strategies can therefore interpret their findings relative to this baseline statistical behaviour.

Consequently, this study provides the first building block of the research framework developed in this project. Rather than representing an isolated descriptive analysis, the statistical benchmark established here serves as the empirical foundation upon which the remaining research questions are constructed.

## 6. Discussion and Implications

### 6.1 Implications for Volatility Research

The statistical benchmark established in this study provides a quantitative reference point for subsequent research on option market dynamics. Rather than analysing volatility smiles, term structures, or option Greeks in isolation, future studies can evaluate these phenomena relative to the baseline behaviour of daily ATM implied volatility.

The empirical evidence suggests that the option market is characterised by a relatively stable central volatility regime accompanied by occasional but economically meaningful deviations. Consequently, subsequent research should distinguish between ordinary market fluctuations and genuine regime shifts rather than treating all observations equally.

Establishing this benchmark also improves the interpretability of future empirical analyses. Changes observed in volatility smiles or term structures can now be evaluated relative to the statistical properties documented in this study, allowing subsequent findings to be interpreted within a consistent empirical framework.

### 6.2 Implications for Quantitative Modelling

The observed statistical properties also provide useful guidance for quantitative model development. The approximate symmetry of the empirical distribution suggests that simple descriptive statistics remain informative for characterising the central volatility regime. However, the presence of moderate excess kurtosis indicates that Gaussian assumptions may underestimate the likelihood of extreme market conditions.

Consequently, future stochastic volatility models and machine learning approaches should account for the empirical distribution rather than relying solely on theoretical assumptions. Model calibration should therefore prioritise empirical consistency over analytical convenience.

More generally, the statistical characteristics documented in this study represent empirical stylized facts that any realistic volatility model should aim to reproduce.

### 6.3 Implications for Trading and Risk Management

From a practical perspective, understanding the empirical behaviour of ATM implied volatility is essential for quantitative trading and portfolio risk management. The statistical benchmark established in this study enables future trading strategies to distinguish between normal volatility environments and statistically unusual market conditions.

Extreme volatility observations identified in this study should not be interpreted as data anomalies but rather as potential market regimes that may require different trading or hedging decisions. Strategies that explicitly recognise these regime changes may achieve greater robustness than approaches based solely on average market behaviour.

Furthermore, the statistical benchmark developed here provides a natural reference for future research on volatility forecasting, signal generation, and regime classification, all of which constitute important components of systematic option trading systems.

### 6.4 Summary

This chapter has discussed the broader implications of the empirical findings presented in Chapter 5. The statistical benchmark established for daily ATM implied volatility not only provides a reliable description of the observed data but also serves as the empirical foundation for subsequent research within this project. Future studies on volatility term structures, smile dynamics, option Greeks, and systematic trading strategies will therefore be developed upon the benchmark established here.

## 7. Limitations

Although this study establishes an initial statistical benchmark for daily ATM implied volatility, several limitations should be acknowledged.

First, the analysis is based exclusively on the 2026 Chinese index option dataset. Consequently, the statistical characteristics documented in this study should be interpreted as evidence for the observed sample period rather than universal properties of implied volatility across different market environments. Future multi-year datasets will be required to evaluate the temporal stability of these findings.

Second, this study focuses on descriptive statistical analysis rather than formal statistical inference. While empirical measures such as skewness, excess kurtosis, and the IQR criterion provide useful evidence regarding the distributional characteristics of ATM implied volatility, additional statistical procedures—including normality tests, goodness-of-fit analysis, and distributional comparisons—would provide stronger quantitative support for the conclusions.

Third, the current analysis treats all trading days as a single sample and does not distinguish between different market regimes, macroeconomic events, or volatility environments. Event-driven behaviour may exhibit statistical characteristics that differ substantially from those reported in this study.

Finally, this study is intentionally descriptive in nature. It does not investigate predictive relationships, causal mechanisms, or trading performance. These topics are addressed in subsequent research questions within this project.

## 8. Future Research

The statistical benchmark established in this study serves as the empirical foundation for the broader quantitative research framework developed in this project. Having characterized the overall behaviour of daily ATM implied volatility, subsequent studies will investigate progressively more complex aspects of option market dynamics.

The next stage of the research focuses on the cross-sectional structure of implied volatility. In particular, future studies will examine whether implied volatility distributions vary systematically across option maturities, leading to an empirical investigation of ATM term structures.

Subsequent research will investigate the stability and evolution of volatility smiles, followed by analyses of option Greeks, volatility forecasting signals, and regime classification. Ultimately, these empirical findings will be integrated into systematic option trading strategies and quantitative risk management frameworks.

Collectively, these studies aim to establish a comprehensive empirical understanding of implied volatility behaviour, providing a unified research platform that connects statistical analysis, quantitative modelling, and practical option trading.

---

# Version Record

**Current Version:** RQ1 v1.0  
**Status:** Frozen  
**Freeze Date:** June 2026  

## Included Analyses

- Daily ATM IV distribution analysis
- Descriptive statistics
- Histogram
- Box plot
- Skewness analysis
- Excess kurtosis analysis
- IQR-based extreme observation analysis
- Research discussion and implications
- Limitations
- Future research roadmap

## Planned Improvements for RQ1 v1.1

- Jarque–Bera normality test
- QQ plot
- Anderson–Darling test
- Multi-year comparison
- Market regime classification
- Formal statistical inference