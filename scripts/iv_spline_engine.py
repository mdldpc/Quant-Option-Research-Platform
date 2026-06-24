import pandas as pd
from scipy.interpolate import UnivariateSpline


def build_spline_surface(iv_df, smoothing=0.0005):
    """
    Input:
        iv_df with columns:
        expiry_code, option_type, strike, implied_vol, future_price

    Output:
        spline surface table with:
        expiry_code, option_type, strike, implied_vol, smoothed_iv
    """

    df = iv_df[iv_df["implied_vol"].notna()].copy()

    results = []

    for (expiry_code, option_type), group in df.groupby(
        ["expiry_code", "option_type"]
    ):

        smile = (
            group.groupby("strike", as_index=False)
            .agg(
                implied_vol=("implied_vol", "median"),
                future_price=("future_price", "median"),
                n_obs=("implied_vol", "count"),
            )
            .sort_values("strike")
        )

        if len(smile) < 4:
            continue

        x = smile["strike"].to_numpy()
        y = smile["implied_vol"].to_numpy()

        spline = UnivariateSpline(
            x,
            y,
            k=3,
            s=smoothing,
        )

        smile["smoothed_iv"] = spline(x)
        smile["expiry_code"] = expiry_code
        smile["option_type"] = option_type

        results.append(smile)

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)