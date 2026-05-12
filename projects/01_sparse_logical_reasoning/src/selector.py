"""Sparse rule selection for the logical reasoning prototype.

The selector is deliberately simple: it activates only rules whose conditions are
fully satisfied by the task facts. This creates a clear contrast with the dense
baseline, which evaluates every rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .rules import Rule


@dataclass(frozen=True)
class SelectionResult:
    """Result of sparse rule selection."""

    active_rules: List[Rule]
    total_rules: int
    task_facts: List[str]

    @property
    def active_rule_count(self) -> int:
        return len(self.active_rules)

    @property
    def sparsity_ratio(self) -> float:
        if self.total_rules == 0:
            return 0.0
        return self.active_rule_count / self.total_rules

    @property
    def active_rule_ids(self) -> List[str]:
        return [rule.rule_id for rule in self.active_rules]


class SparseRuleSelector:
    """Select rules that are relevant to the current task facts."""

    def __init__(self, rules: Sequence[Rule]):
        self.rules = list(rules)

    def select(self, facts: Iterable[str]) -> SelectionResult:
        """Return only rules whose conditions match the supplied facts."""

        fact_list = list(facts)
        active_rules = [rule for rule in self.rules if rule.matches(fact_list)]

        return SelectionResult(
            active_rules=active_rules,
            total_rules=len(self.rules),
            task_facts=fact_list,
        )


class DenseRuleSelector:
    """Dense baseline that selects every available rule.

    This is not meant to be intelligent. It exists as a comparison baseline for
    sparse activation.
    """

    def __init__(self, rules: Sequence[Rule]):
        self.rules = list(rules)

    def select(self, facts: Iterable[str]) -> SelectionResult:
        """Return all rules regardless of relevance."""

        fact_list = list(facts)

        return SelectionResult(
            active_rules=list(self.rules),
            total_rules=len(self.rules),
            task_facts=fact_list,
        )
