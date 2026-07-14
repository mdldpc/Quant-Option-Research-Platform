from pathlib import Path

import matplotlib.pyplot as plt


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FIGURE_DIR = PROJECT_ROOT / "docs" / "figures"

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# Helper
# ==========================================================

def create_box(ax, text, y):
    ax.text(
        0.5,
        y,
        text,
        ha="center",
        va="center",
        fontsize=13,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            edgecolor="black",
        ),
    )


def create_arrow(ax, y1, y2):
    ax.annotate(
        "",
        xy=(0.5, y2),
        xytext=(0.5, y1),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.5,
        ),
    )


# ==========================================================
# Figure 1
# System Architecture
# ==========================================================

def build_system_architecture():

    fig, ax = plt.subplots(
        figsize=(10, 12)
    )

    ax.axis("off")

    fig.suptitle(
        "Quant Option Research Platform\nSystem Architecture",
        fontsize=18,
        fontweight="bold",
    )

    layers = [
        "Market Data",
        "Data Processing Layer",
        "Volatility Research Engine\nIV | Smile | Surface | Greeks",
        "Strategy Research Framework",
        "Portfolio Engine\nPositionBook | NAV | Exposure",
        "Risk Management Engine\nDelta | Gamma | Vega | Monitoring",
        "Automated Documentation System\nReports | White Papers | Analytics",
    ]

    ys = [
        0.88,
        0.75,
        0.62,
        0.49,
        0.36,
        0.23,
        0.10,
    ]

    for text, y in zip(layers, ys):
        create_box(
            ax,
            text,
            y,
        )

    for i in range(len(ys)-1):
        create_arrow(
            ax,
            ys[i]-0.04,
            ys[i+1]+0.04,
        )


    output = (
        FIGURE_DIR /
        "system_architecture.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Saved: {output}"
    )


# ==========================================================
# Figure 2
# Strategy Pipeline
# ==========================================================

def build_strategy_pipeline():

    fig, ax = plt.subplots(
        figsize=(10, 12)
    )

    ax.axis("off")

    fig.suptitle(
        "Quantitative Option Research Workflow",
        fontsize=18,
        fontweight="bold",
    )

    steps = [
        "Market Data",
        "Data Preparation",
        "Volatility Feature Engineering",
        "Signal Generation",
        "Strategy Construction",
        "Backtesting",
        "Portfolio Evaluation",
        "Risk Analysis",
        "Research Documentation",
    ]

    ys = [
        0.90,
        0.79,
        0.68,
        0.57,
        0.46,
        0.35,
        0.24,
        0.13,
        0.02,
    ]


    for text, y in zip(steps, ys):

        create_box(
            ax,
            text,
            y,
        )


    for i in range(len(ys)-1):

        create_arrow(
            ax,
            ys[i]-0.03,
            ys[i+1]+0.03,
        )


    output = (
        FIGURE_DIR /
        "strategy_pipeline.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Saved: {output}"
    )


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    build_system_architecture()

    build_strategy_pipeline()

    print(
        "Project figures generated."
    )