from pathlib import Path

import pandas as pd

from framework.risk.exposure import compute_exposure
from framework.risk.hedge_rules import (
    HedgeRuleConfig,
    generate_hedge_recommendations,
)
from framework.risk.hedge_translator import translate_recommendations


def build_risk_report(
    positions: pd.DataFrame,
    report_path: Path,
    config: HedgeRuleConfig | None = None,
    trade_date: int | None = None,
):
    """
    Build portfolio risk report.

    Parameters
    ----------
    positions
        Portfolio positions (snapshot rows).

    report_path
        Output txt report.

    config
        Hedge rule configuration.

    trade_date
        Optional YYYYMMDD.
        None means latest snapshot.
    """

    if config is None:
        config = HedgeRuleConfig()

    exposure = compute_exposure(positions)

    recommendations = generate_hedge_recommendations(
        exposure,
        config,
    )

    execution_plans = translate_recommendations(
        recommendations
    )

    rec_rows = []

    for r in recommendations:

        rec_rows.append(
            {
                "risk_type": r.risk_type,
                "risk_level": r.risk_level,
                "action": r.action,
                "hedge_instrument": r.hedge_instrument,
                "hedge_size": r.hedge_size,
                "residual_target": r.residual_target,
                "reason": r.reason,
            }
        )

    plan_rows = []

    for p in execution_plans:

        plan_rows.append(
            {
                "risk_type": p.risk_type,
                "risk_level": p.risk_level,
                "action": p.action,
                "hedge_instrument": p.hedge_instrument,
                "trade_direction": p.trade_direction,
                "trade_units": p.trade_units,
                "requested_hedge_size": p.requested_hedge_size,
                "exposure_per_unit": p.exposure_per_unit,
                "estimated_hedged_exposure": p.estimated_hedged_exposure,
                "estimated_residual_exposure": p.estimated_residual_exposure,
                "reason": p.reason,
                "notes": p.notes,
            }
        )

    rec_df = pd.DataFrame(rec_rows)

    plan_df = pd.DataFrame(plan_rows)

    report = []

    report.append("Portfolio Risk & Hedge Report")
    report.append("=" * 80)

    if trade_date is None:
        report.append("Trade Date : latest snapshot")
    else:
        report.append(f"Trade Date : {trade_date}")

    report.append("")

    report.append("Exposure Summary")
    report.append("-" * 80)

    report.append(f"Positions   : {exposure.positions}")
    report.append(f"Net Delta   : {exposure.net_delta:.6f}")
    report.append(f"Net Gamma   : {exposure.net_gamma:.6f}")
    report.append(f"Net Vega    : {exposure.net_vega:.6f}")
    report.append(f"Net Theta   : {exposure.net_theta:.6f}")

    report.append(f"Gross Delta : {exposure.gross_delta:.6f}")
    report.append(f"Gross Vega  : {exposure.gross_vega:.6f}")

    report.append("")
    report.append("Hedge Recommendations")
    report.append("-" * 80)
    report.append(rec_df.to_string(index=False))

    report.append("")
    report.append("Executable Hedge Plan")
    report.append("-" * 80)
    report.append(plan_df.to_string(index=False))

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    return (
        exposure,
        rec_df,
        plan_df,
    )