import pandas as pd

path = r"D:\Quant_Option_Project\data_parquet\option_table_sample.parquet"

df = pd.read_parquet(path)

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nSymbols:")
print(df["symbol"].nunique())

print("\nFuture symbols:")
print(df["fut_symbol"].value_counts())

print("\nOption type:")
print(df["option_type"].value_counts())

print("\nPrice summary:")
print(df[["option_price", "future_price", "strike"]].describe())

print("\nHead:")
print(df.head(20))