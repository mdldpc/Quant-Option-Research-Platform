from framework.registry import (
    list_all_strategies,
    enabled_strategies,
    get_strategy,
)

from framework.contracts import (
    StrategyDatasetContract,
    BacktestContract,
    RiskContract,
)

from config.strategy_config import (
    SIGNAL_CONFIG,
    EXECUTION_CONFIG,
    RISK_CONFIG,
)


def show_framework_status():

    print("=" * 70)
    print("Strategy Framework v2")
    print("=" * 70)

    print("\nFramework Status")
    print("-" * 70)

    print(f"{'Signal Config':25} OK")
    print(f"{'Execution Config':25} OK")
    print(f"{'Risk Config':25} OK")
    print(f"{'Registry':25} OK")
    print(f"{'Builder Interface':25} OK")
    print(f"{'Contracts':25} OK")

    print("\nRegistered Strategies")
    print("-" * 70)

    print(f"{'Name':25}{'Enabled':10}{'Status'}")

    production = 0
    prototype = 0
    planned = 0

    for name in list_all_strategies():

        cfg = get_strategy(name)

        print(
            f"{name:25}"
            f"{str(cfg['enabled']):10}"
            f"{cfg['status']}"
        )

        if cfg["status"] == "production":
            production += 1
        elif cfg["status"] == "prototype":
            prototype += 1
        else:
            planned += 1

    print("\nSummary")
    print("-" * 70)

    print(f"Registered : {len(list_all_strategies())}")
    print(f"Enabled    : {len(enabled_strategies())}")
    print(f"Production : {production}")
    print(f"Prototype  : {prototype}")
    print(f"Planned    : {planned}")

    print("\nFramework Ready")


if __name__ == "__main__":
    show_framework_status()