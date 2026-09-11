"""Print a reproducible synthetic convergence study: python -m api.valuation_example."""

from api.valuation import black_scholes_price, crr_price


def main():
    parameters = dict(spot=100, strike=100, maturity=1, rate=0.05, volatility=0.2)
    print("Synthetic European options: S=K=100, T=1 year, r=5%, sigma=20%, no dividends")
    print("| Type | Steps | Black-Scholes | CRR | Absolute error |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for kind in ("call", "put"):
        benchmark = black_scholes_price(**parameters, option_type=kind)
        for steps in (25, 50, 100, 250, 500, 1000):
            tree = crr_price(**parameters, option_type=kind, steps=steps)
            print(f"| {kind} | {steps} | {benchmark:.8f} | {tree:.8f} | {abs(tree - benchmark):.8f} |")


if __name__ == "__main__":
    main()
