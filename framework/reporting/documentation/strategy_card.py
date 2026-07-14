import pandas as pd

from framework.reporting.documentation.strategy_registry import StrategyRecord


def _table(report, rows, columns):
    if rows:
        report.dataframe(pd.DataFrame(rows, columns=columns))


def _bullets(report, items):
    for item in items:
        report.bullet(item)


def build_strategy_card(
    report,
    record: StrategyRecord,
    performance_rows: list[list[str]] | None = None,
):
    report.heading1(record.title)

    report.heading2("Strategy Snapshot")
    _table(
        report,
        record.snapshot,
        ["Item", "Value"],
    )

    report.heading2("Overview")
    report.paragraph(record.overview)

    report.heading2("Research Motivation")
    _bullets(report, record.motivation)

    report.heading2("Research Questions")
    _bullets(report, record.research_questions)

    report.heading2("Suitable Market Environment")
    _table(
        report,
        record.market_conditions,
        ["Market Condition", "Suitability"],
    )

    report.heading2("Position Construction")
    _bullets(report, record.construction)

    report.heading2("Payoff Characteristics")
    _bullets(report, record.payoff)

    report.heading2("Greeks Characteristics")
    _table(
        report,
        record.greek_profile,
        ["Greek", "Expected Exposure", "Interpretation"],
    )

    report.heading2("Signal and Entry Rules")
    _bullets(report, record.entry_rules)

    report.heading2("Exit Rules")
    _bullets(report, record.exit_rules)

    report.heading2("Current Evidence")
    _table(
        report,
        record.evidence,
        ["Evidence", "Status"],
    )

    report.heading2("Backtest / Portfolio Evaluation")
    _table(
        report,
        performance_rows or record.performance,
        ["Metric", "Value"],
    )

    report.paragraph(
        "The evaluation results above are generated from the currently available research "
        "exports. Because the dataset currently covers only the 2026 sample period, these "
        "results should be interpreted as preliminary research evidence rather than final "
        "production validation."
    )

    report.heading2("Advantages")
    _bullets(report, record.advantages)

    report.heading2("Limitations")
    _bullets(report, record.limitations)

    report.heading2("Future Improvements")
    _bullets(report, record.future_work)

    report.heading2("Research Roadmap")
    _table(
        report,
        record.roadmap,
        ["Version", "Milestone"],
    )

    report.heading2("References")
    _bullets(report, record.references)

    report.page_break()