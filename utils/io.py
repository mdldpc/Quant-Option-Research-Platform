from pathlib import Path
import pandas as pd


def ensure_parent(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_parquet(df, path, index=False):
    path = ensure_parent(path)
    df.to_parquet(path, index=index)
    print(f"Saved parquet: {path}")


def save_csv(df, path, index=False):
    path = ensure_parent(path)
    df.to_csv(path, index=index, encoding="utf-8-sig")
    print(f"Saved csv: {path}")


def save_text(text, path):
    path = ensure_parent(path)
    path.write_text(text, encoding="utf-8")
    print(f"Saved text: {path}")