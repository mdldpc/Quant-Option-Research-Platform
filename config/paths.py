from pathlib import Path

PROJECT_ROOT = Path(r"D:\Quant_Option_Project")

DATA_PARQUET_DIR = PROJECT_ROOT / "data_parquet"
DATA_RAW_DIR = PROJECT_ROOT / "data_raw"

RESEARCH_DIR = PROJECT_ROOT / "research"
DATASETS_DIR = RESEARCH_DIR / "datasets"
SUMMARIES_DIR = RESEARCH_DIR / "summaries"
SIGNALS_DIR = RESEARCH_DIR / "signals"
BACKTEST_DIR = RESEARCH_DIR / "backtest"
EXPORTS_DIR = RESEARCH_DIR / "exports"
FIGURES_DIR = RESEARCH_DIR / "figures"
REPORTS_DIR = RESEARCH_DIR / "reports"

BATCH_2026_DIR = DATA_PARQUET_DIR / "batch_2026"

ALL_GREEKS_2026H1 = BATCH_2026_DIR / "all_greeks_2026H1.parquet"

DAILY_SIGNAL_FEATURES = SIGNALS_DIR / "daily_signal_features.parquet"
LONG_ONLY_TRADES = SIGNALS_DIR / "long_only_trades.parquet"
OPTION_TRADE_DATASET = BACKTEST_DIR / "option_trade_dataset.parquet"
OPTION_STRATEGY_BACKTEST = BACKTEST_DIR / "option_strategy_backtest.parquet"