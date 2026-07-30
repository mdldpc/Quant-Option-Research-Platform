from pathlib import Path


def test_strategy_files_exist():


    files = [

        "research/exports/option_strategy_backtest_strangle_v1_1.csv",

        "research/exports/option_strategy_backtest_butterfly_v1_1.csv",

        "research/exports/option_strategy_backtest_calendar_v1_1.csv",

    ]


    for f in files:

        assert Path(f).exists()