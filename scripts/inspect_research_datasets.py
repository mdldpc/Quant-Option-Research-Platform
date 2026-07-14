import pandas as pd

files = [
    "research/exports/atm_iv_dataset_preview.csv",
    "research/exports/smile_dataset_near_preview.csv",
    "research/exports/surface_dataset_near_preview.csv",
    "research/exports/term_structure_preview.csv",
    "research/exports/option_trade_dataset.csv",
]

for f in files:
    print("\n" + "=" * 80)
    print(f)

    try:
        df = pd.read_csv(f, nrows=5)
        print("\nColumns:")
        print(df.columns.tolist())

        print("\nHead:")
        print(df.head())

    except Exception as e:
        print("ERROR:", e)