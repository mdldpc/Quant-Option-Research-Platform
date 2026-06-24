import pandas as pd


def run_parameter_sweep(
    base_data,
    param_name: str,
    values: list,
    run_func,
):
    """
    Generic parameter sweep engine.

    Parameters
    ----------
    base_data : DataFrame
        Input dataset (signals or trades)

    param_name : str
        Name of parameter (e.g. "threshold")

    values : list
        Values to test

    run_func : function
        Function that takes (data, param_value) and returns metrics dict

    Returns
    -------
    DataFrame
    """

    results = []

    print("\n============================")
    print(f"Running parameter sweep: {param_name}")
    print("============================\n")

    for v in values:

        print(f"Running {param_name} = {v}")

        metrics = run_func(base_data, v)

        metrics[param_name] = v

        results.append(metrics)

    df = pd.DataFrame(results)

    print("\nSweep Result:")
    print(df)

    return df