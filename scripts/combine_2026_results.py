from pathlib import Path
import pandas as pd

ROOT = Path(
    r"D:\Quant_Option_Project\data_parquet\batch_2026"
)

OUTPUT_FILE = (
    ROOT / "all_greeks_2026H1.parquet"
)

all_dfs = []

folders = sorted(
    [
        x for x in ROOT.iterdir()
        if x.is_dir()
    ]
)

print("Folders found:", len(folders))

for folder in folders:

    success_flag = folder / "SUCCESS.flag"
    greeks_file = folder / "greeks_spline.parquet"

    if not success_flag.exists():
        print("SKIP (no SUCCESS):", folder.name)
        continue

    if not greeks_file.exists():
        print("SKIP (no Greeks):", folder.name)
        continue

    print("Loading:", folder.name)

    df = pd.read_parquet(greeks_file)

    trade_date = (
        folder.name
        .replace("trade_date=", "")
    )

    df["trade_date"] = trade_date

    all_dfs.append(df)

print()
print("Valid days:", len(all_dfs))

combined = pd.concat(
    all_dfs,
    ignore_index=True
)

print()
print("Final Shape:")
print(combined.shape)

print()
print("Saving...")

combined.to_parquet(
    OUTPUT_FILE,
    index=False
)

print()
print("DONE")
print("Saved:")
print(OUTPUT_FILE)