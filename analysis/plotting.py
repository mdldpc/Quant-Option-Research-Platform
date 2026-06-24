from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from config.paths import FIGURES_DIR


def _prepare_experiment(df: pd.DataFrame, experiment_name: str) -> pd.DataFrame:
    out = df[df["experiment"] == experiment_name].copy()
    return out.reset_index(drop=True)


def plot_robustness_dashboard(
    df: pd.DataFrame,
    output_path: Path | None = None,
):
    """
    Plot robustness dashboard.

    Panels:
    1. Threshold vs average return
    2. Holding days vs average return
    3. Transaction cost vs average return
    4. Threshold vs trade count
    """

    if output_path is None:
        output_path = FIGURES_DIR / "robustness_dashboard.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    threshold_df = _prepare_experiment(df, "threshold")
    holding_df = _prepare_experiment(df, "holding")
    cost_df = _prepare_experiment(df, "cost")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # -----------------------------
    # 1. Threshold vs Avg Return
    # -----------------------------
    ax = axes[0, 0]

    if not threshold_df.empty:
        ax.plot(
            threshold_df["threshold"],
            threshold_df["avg_return"],
            marker="o",
            linewidth=2,
        )

    ax.set_title("Threshold vs Average Return")
    ax.set_xlabel("Signal Threshold")
    ax.set_ylabel("Average Return")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    # -----------------------------
    # 2. Holding Days vs Avg Return
    # -----------------------------
    ax = axes[0, 1]

    if not holding_df.empty:
        ax.plot(
            holding_df["holding_days"],
            holding_df["avg_return"],
            marker="o",
            linewidth=2,
        )

    ax.set_title("Holding Days vs Average Return")
    ax.set_xlabel("Max Holding Days")
    ax.set_ylabel("Average Return")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    # -----------------------------
    # 3. Transaction Cost vs Avg Return
    # -----------------------------
    ax = axes[1, 0]

    if not cost_df.empty:
        ax.plot(
            cost_df["cost"],
            cost_df["avg_return"],
            marker="o",
            linewidth=2,
        )

    ax.set_title("Transaction Cost vs Average Return")
    ax.set_xlabel("Transaction Cost")
    ax.set_ylabel("Average Return")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.3)

    # -----------------------------
    # 4. Threshold vs Trade Count
    # -----------------------------
    ax = axes[1, 1]

    if not threshold_df.empty:
        ax.bar(
            threshold_df["threshold"].astype(str),
            threshold_df["trade_count"],
        )

    ax.set_title("Threshold vs Trade Count")
    ax.set_xlabel("Signal Threshold")
    ax.set_ylabel("Trade Count")
    ax.grid(True, axis="y", alpha=0.3)

    fig.suptitle(
        "Robustness Dashboard",
        fontsize=16,
        fontweight="bold",
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(f"Saved robustness dashboard: {output_path}")

    return output_path

def plot_histogram(
    series,
    title,
    xlabel,
    save_path,
    bins=30,
):
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    data = series.dropna()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        data,
        bins=bins,
        edgecolor="black",
        alpha=0.8,
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Frequency")
    ax.grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved histogram: {save_path}")


def plot_boxplot(
    series,
    title,
    ylabel,
    save_path,
):
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    data = series.dropna()

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.boxplot(
        data,
        vert=True,
        showmeans=True,
    )

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved boxplot: {save_path}")