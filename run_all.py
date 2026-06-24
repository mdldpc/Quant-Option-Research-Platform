import subprocess


def run(cmd):
    print(f"\n====================")
    print(f"Running: {cmd}")
    print(f"====================\n")
    subprocess.run(cmd, shell=True)


def main():

    # 1. Backtest
    run("python scripts/run_option_backtest_v2.py")

    # 2. Transaction cost
    run("python scripts/run_transaction_cost_analysis.py")

    # 3. Robustness suite
    run("python scripts/run_robustness_suite.py")

    # 4. Dashboard
    run("python scripts/run_robustness_dashboard.py")

    print("\nALL DONE")


if __name__ == "__main__":
    main()