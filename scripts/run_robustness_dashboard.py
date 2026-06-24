import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd

from config.paths import EXPORTS_DIR, FIGURES_DIR
from analysis.plotting import plot_robustness_dashboard


INPUT_FILE = EXPORTS_DIR / "robustness_suite_results.csv"

OUTPUT_FILE = FIGURES_DIR / "robustness_dashboard.png"


def main():
    print("Reading robustness results...")
    df = pd.read_csv(INPUT_FILE)

    print("Shape:")
    print(df.shape)

    plot_robustness_dashboard(
        df=df,
        output_path=OUTPUT_FILE,
    )

    print("\nDONE")
    print("Saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()