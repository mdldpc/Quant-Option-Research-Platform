from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from framework.reporting.documentation.strategy_data import STRATEGIES
from framework.reporting.documentation.strategy_performance_loader import (
    load_strategy_evidence,
)


@dataclass
class StrategyRecord:
    key: str
    metadata: dict[str, Any]
    title: str
    snapshot: list[list[str]]
    overview: str
    motivation: list[str]
    research_questions: list[str]
    market_conditions: list[list[str]]
    construction: list[str]
    payoff: list[str]
    greek_profile: list[list[str]]
    entry_rules: list[str]
    exit_rules: list[str]
    performance: list[list[str]]
    evidence: list[list[str]]
    advantages: list[str]
    limitations: list[str]
    future_work: list[str]
    references: list[str]
    roadmap: list[list[str]]
    dynamic_performance: list[list[str]] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.metadata.get("name", self.title)

    @property
    def strategy_id(self) -> str:
        return self.metadata.get("strategy_id", self.key)

    @property
    def category(self) -> str:
        return self.metadata.get("category", "")

    @property
    def research_stage(self) -> str:
        return self.metadata.get("research_stage", "")

    @property
    def implementation_status(self) -> str:
        return self.metadata.get("implementation_status", "")


class StrategyRegistry:

    def __init__(self, load_dynamic: bool = True):
        self.records: dict[str, StrategyRecord] = {}

        for key, data in STRATEGIES.items():
            record = self._make_record(key, data)

            if load_dynamic:
                record.dynamic_performance = load_strategy_evidence(key)

            self.records[key] = record

    def _make_record(self, key: str, data: dict[str, Any]) -> StrategyRecord:
        return StrategyRecord(
            key=key,
            metadata=data.get("metadata", {}),
            title=data.get("title", key),
            snapshot=data.get("snapshot", []),
            overview=data.get("overview", ""),
            motivation=data.get("motivation", []),
            research_questions=data.get("research_questions", []),
            market_conditions=data.get("market_conditions", []),
            construction=data.get("construction", []),
            payoff=data.get("payoff", []),
            greek_profile=data.get("greek_profile", []),
            entry_rules=data.get("entry_rules", []),
            exit_rules=data.get("exit_rules", []),
            performance=data.get("performance", []),
            evidence=data.get("evidence", []),
            advantages=data.get("advantages", []),
            limitations=data.get("limitations", []),
            future_work=data.get("future_work", []),
            references=data.get("references", []),
            roadmap=data.get("roadmap", []),
        )

    def get(self, key: str) -> StrategyRecord:
        return self.records[key]

    def all(self) -> list[StrategyRecord]:
        return list(self.records.values())

    def summary_table(self) -> pd.DataFrame:
        rows = []

        for r in self.all():
            rows.append(
                {
                    "ID": r.strategy_id,
                    "Strategy": r.name,
                    "Category": r.category,
                    "Stage": r.research_stage,
                    "Impl.": r.implementation_status,
                    "Portfolio": "Yes" if r.metadata.get("portfolio_support") else "No",
                    "Risk": "Yes" if r.metadata.get("risk_support") else "No",
                    "Hedge": "Yes" if r.metadata.get("hedge_support") else "No",
                }
            )

        return pd.DataFrame(rows)

    def performance_for(self, record: StrategyRecord) -> list[list[str]]:
        if record.dynamic_performance:
            return record.dynamic_performance

        return record.performance


def get_registry() -> StrategyRegistry:
    return StrategyRegistry(load_dynamic=True)