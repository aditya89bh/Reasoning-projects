"""Rule memory for the rule induction prototype.

Rule memory stores induced rules so they can be inspected, filtered, and reused
on future tasks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Optional

from .rule import InducedRule


class RuleMemory:
    """In-memory rule store with optional JSON persistence."""

    def __init__(self, rules: Optional[Iterable[InducedRule]] = None):
        self._rules = {rule.rule_id: rule for rule in rules or []}

    @classmethod
    def from_json(cls, path: str | Path) -> "RuleMemory":
        """Load rules from a JSON file."""

        json_path = Path(path)
        with json_path.open("r", encoding="utf-8") as file:
            raw_rules = json.load(file)

        return cls(InducedRule.from_dict(item) for item in raw_rules)

    def to_json(self, path: str | Path) -> None:
        """Save rules to a JSON file."""

        json_path = Path(path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open("w", encoding="utf-8") as file:
            json.dump([rule.to_dict() for rule in self.list_rules(include_all=True)], file, indent=2)

    def add(self, rule: InducedRule) -> None:
        """Add or replace one induced rule."""

        self._rules[rule.rule_id] = rule

    def add_many(self, rules: Iterable[InducedRule]) -> None:
        """Add multiple induced rules."""

        for rule in rules:
            self.add(rule)

    def get(self, rule_id: str) -> InducedRule:
        """Return rule by id."""

        return self._rules[rule_id]

    def list_rules(self, include_all: bool = False) -> List[InducedRule]:
        """Return stored rules sorted by id.

        Args:
            include_all: If False, hide deprecated rules.
        """

        rules = list(self._rules.values())
        if not include_all:
            rules = [rule for rule in rules if rule.status != "deprecated"]
        return sorted(rules, key=lambda rule: rule.rule_id)

    def accepted_rules(self) -> List[InducedRule]:
        """Return rules with accepted status."""

        return [rule for rule in self.list_rules() if rule.status == "accepted"]

    def candidate_rules(self) -> List[InducedRule]:
        """Return rules with candidate status."""

        return [rule for rule in self.list_rules() if rule.status == "candidate"]

    def find_matching(self, facts: List[str], accepted_only: bool = True) -> List[InducedRule]:
        """Return rules whose conditions match the supplied facts."""

        rules = self.accepted_rules() if accepted_only else self.list_rules()
        return [rule for rule in rules if rule.matches(facts)]

    def __len__(self) -> int:
        return len(self._rules)
