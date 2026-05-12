"""Rule data model for the rule induction prototype.

A learned rule is an explicit condition-effect structure created from examples,
scored, stored, and reused in future reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InducedRule:
    """Human-readable rule proposed from examples or experience."""

    rule_id: str
    name: str
    conditions: List[str]
    effect: str
    source_episodes: List[str] = field(default_factory=list)
    confidence: float = 0.5
    coverage: float = 0.0
    precision: float = 0.0
    failure_cases: List[str] = field(default_factory=list)
    status: str = "candidate"

    def matches(self, facts: List[str]) -> bool:
        """Return True when all rule conditions are present in task facts."""

        fact_set = set(facts)
        return all(condition in fact_set for condition in self.conditions)

    def to_dict(self) -> Dict:
        """Serialize rule to dictionary."""

        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "conditions": list(self.conditions),
            "effect": self.effect,
            "source_episodes": list(self.source_episodes),
            "confidence": self.confidence,
            "coverage": self.coverage,
            "precision": self.precision,
            "failure_cases": list(self.failure_cases),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "InducedRule":
        """Create an induced rule from dictionary data."""

        return cls(
            rule_id=data["rule_id"],
            name=data.get("name", data["rule_id"]),
            conditions=list(data.get("conditions", [])),
            effect=data.get("effect", ""),
            source_episodes=list(data.get("source_episodes", [])),
            confidence=float(data.get("confidence", 0.5)),
            coverage=float(data.get("coverage", 0.0)),
            precision=float(data.get("precision", 0.0)),
            failure_cases=list(data.get("failure_cases", [])),
            status=data.get("status", "candidate"),
        )
