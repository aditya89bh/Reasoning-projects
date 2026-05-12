"""Rule application for the rule induction prototype.

The applier uses stored induced rules on future task facts and returns explicit
trace output so rule reuse is inspectable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .rule import InducedRule
from .rule_memory import RuleMemory


@dataclass(frozen=True)
class RuleApplicationResult:
    """Result of applying induced rules to a future task."""

    task_id: str
    facts: List[str]
    matched_rule_ids: List[str]
    effects: List[str]
    recommendation: str
    trace: List[str]

    def as_dict(self) -> Dict:
        """Return a compact serializable representation."""

        return {
            "task_id": self.task_id,
            "facts": list(self.facts),
            "matched_rule_ids": list(self.matched_rule_ids),
            "effects": list(self.effects),
            "recommendation": self.recommendation,
            "trace": list(self.trace),
        }


class RuleApplier:
    """Apply accepted induced rules to future task facts."""

    def __init__(self, rule_memory: RuleMemory):
        self.rule_memory = rule_memory

    def apply(self, task_id: str, facts: List[str], accepted_only: bool = True) -> RuleApplicationResult:
        """Apply matching rules and return a recommendation."""

        matched_rules = self.rule_memory.find_matching(facts, accepted_only=accepted_only)
        effects = self._unique_effects(matched_rules)
        recommendation = self._derive_recommendation(effects)
        trace = self._build_trace(task_id, facts, matched_rules, effects, recommendation)

        return RuleApplicationResult(
            task_id=task_id,
            facts=list(facts),
            matched_rule_ids=[rule.rule_id for rule in matched_rules],
            effects=effects,
            recommendation=recommendation,
            trace=trace,
        )

    def _unique_effects(self, rules: List[InducedRule]) -> List[str]:
        """Return rule effects without duplicates in first-seen order."""

        seen = set()
        effects: List[str] = []
        for rule in rules:
            if rule.effect not in seen:
                seen.add(rule.effect)
                effects.append(rule.effect)
        return effects

    def _derive_recommendation(self, effects: List[str]) -> str:
        """Derive a compact recommendation from rule effects."""

        avoid_effects = [effect for effect in effects if effect.startswith("avoid_")]
        if avoid_effects:
            return avoid_effects[0]

        prefer_effects = [effect for effect in effects if effect.startswith("prefer_")]
        if prefer_effects:
            return prefer_effects[0]

        review_effects = [effect for effect in effects if effect.startswith("review_")]
        if review_effects:
            return review_effects[0]

        if effects:
            return effects[0]
        return "no_rule_recommendation"

    def _build_trace(
        self,
        task_id: str,
        facts: List[str],
        matched_rules: List[InducedRule],
        effects: List[str],
        recommendation: str,
    ) -> List[str]:
        """Build an inspectable rule application trace."""

        trace = [
            f"Task: {task_id}",
            f"Facts: {', '.join(facts) if facts else 'none'}",
        ]

        if not matched_rules:
            trace.append("No induced rules matched.")
            trace.append("Recommendation: no_rule_recommendation")
            return trace

        for rule in matched_rules:
            conditions = ", ".join(rule.conditions)
            trace.append(
                f"Matched {rule.rule_id}: conditions [{conditions}] -> effect [{rule.effect}], confidence={rule.confidence}"
            )

        trace.append(f"Effects: {', '.join(effects) if effects else 'none'}")
        trace.append(f"Recommendation: {recommendation}")
        return trace
