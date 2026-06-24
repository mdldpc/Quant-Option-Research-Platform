import os
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline

IV_PATH = r"D:\Quant_Option_Project\data_parquet\iv_sample.parquet"
OUT_PATH = r"D:\Quant_Option_Project\data_parquet\iv_spline_sample.parquet"


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print("Reading IV sample...")
    df = pd.read_parquet(IV_PATH)

    df = df[df["implied_vol"].notna()].copy()

    # 先只做 2501 样本
    df["expiry_code"] = df["symbol"].str.extract(r"IO(\d{4})")[0]

    results = []

    for (expiry_code, option_type), group in df.groupby(["expiry_code", "option_type"]):

        print(f"\nProcessing expiry={expiry_code}, type={option_type}")

        # 同一个 strike 可能有多条 tick，先聚合成一个 strike 一个 IV
        smile = (
            group.groupby("strike", as_index=False)
            .agg(
                implied_vol=("implied_vol", "median"),
                future_price=("future_price", "median"),
                n_obs=("implied_vol", "count"),
            )
            .sort_values("strike")
        )

        print("Unique strikes:", len(smile))

        if len(smile) < 4:
            print("Not enough strikes for spline, skipped.")
            continue

        x = smile["strike"].to_numpy()
        y = smile["implied_vol"].to_numpy()

        # 平滑参数：先用轻微平滑
        # 后续可调 s
        spline = UnivariateSpline(
            x,
            y,
            k=3,
            s=0.0005
        )

        smile["smoothed_iv"] = spline(x)

        smile["expiry_code"] = expiry_code
        smile["option_type"] = option_type

        results.append(smile)

    surface = pd.concat(results, ignore_index=True)

    print("\nSpline Surface Summary:")
    print(surface[["implied_vol", "smoothed_iv"]].describe())

    print("\nSample:")
    print(surface.head(30))

    surface.to_parquet(OUT_PATH, index=False)

    print("\nSaved to:")
    print(OUT_PATH)


if __name__ == "__main__":
    main()