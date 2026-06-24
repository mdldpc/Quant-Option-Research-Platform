import pandas as pd


def describe_distribution(series: pd.Series) -> pd.DataFrame:
    """
    Return descriptive statistics for a numeric series.
    """

    s = series.dropna()

    summary = {
        "count": s.count(),
        "mean": s.mean(),
        "median": s.median(),
        "std": s.std(),
        "min": s.min(),
        "5%": s.quantile(0.05),
        "25%": s.quantile(0.25),
        "75%": s.quantile(0.75),
        "95%": s.quantile(0.95),
        "max": s.max(),
        "skewness": s.skew(),
        "kurtosis": s.kurt(),
    }

    return pd.DataFrame(summary, index=[0])

from scipy.stats import jarque_bera


def normality_test(series: pd.Series) -> pd.DataFrame:
    """
    Perform Jarque-Bera normality test.
    """

    s = series.dropna()

    jb_stat, p_value = jarque_bera(s)

    result = {
        "jb_statistic": jb_stat,
        "p_value": p_value,
        "is_normal_5pct": p_value > 0.05,
    }

    return pd.DataFrame(result, index=[0])


def detect_iqr_outliers(series: pd.Series) -> pd.DataFrame:
    """
    Detect outliers using the IQR rule.
    """

    s = series.dropna()

    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = s[(s < lower) | (s > upper)]

    result = {
        "lower_bound": lower,
        "upper_bound": upper,
        "outlier_count": len(outliers),
        "outlier_ratio": len(outliers) / len(s),
    }

    return pd.DataFrame(result, index=[0])