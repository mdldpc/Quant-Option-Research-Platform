from pathlib import Path
import pandas as pd

INPUT_FILE = Path(
    "research/datasets/portfolio_exposure_risk_2026H1.parquet"
)


def main():

    print("=" * 80)
    print("Risk Management QC")
    print("=" * 80)

    df = pd.read_parquet(INPUT_FILE)

    print("\nDataset Shape")
    print(df.shape)

    print("\nRisk Level Counts")
    print(df["risk_level"].value_counts())

    print("\nRecommended Action Counts")
    print(df["recommended_action"].value_counts())

    print("\nMissing Recommended Actions")

    missing = df[
        df["recommended_action"].isna()
        | (df["recommended_action"].str.strip() == "")
    ]

    print(len(missing))

    print("\nRows with Warning but No Action")

    warning_cols = [
        "delta_warning",
        "gamma_warning",
        "vega_warning",
        "theta_warning",
    ]

    has_warning = df[warning_cols].any(axis=1)

    bad = df[
        has_warning
        &
        (
            df["recommended_action"].str.contains(
                "No immediate hedge",
                na=False
            )
        )
    ]

    print(len(bad))

    if len(bad):

        print("\nProblem Rows")

        print(
            bad[
                [
                    "trade_id",
                    "trade_date",
                    "net_delta",
                    "net_gamma",
                    "net_vega",
                    "net_theta",
                    "recommended_action",
                ]
            ]
        )

    print("\nQC PASSED")


if __name__ == "__main__":
    main()