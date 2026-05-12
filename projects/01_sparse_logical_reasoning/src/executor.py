"""Rule execution for the sparse logical reasoning prototype.

The executor applies selected rules to a task state and returns both inferred
effects and a human-readable trace. It does not hide reasoning behind model
outputs. Every activated rule is visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .rules import Rule
from .selector import SelectionResult


@dataclass(frozen=True)
class ExecutionResult:
    """Result produced by executing selected rules."""

    task_id: str
    facts: List[str]
    selected_rule_ids: List[str]
    effects: List[str]
    answer: str
    trace: List[str]

    @property
    def matched_rule_count(self) -> int:
        return len(self.selected_rule_ids)


class RuleExecutor:
    """Execute selected rules against task facts."""

    def execute(self, task_id: str, selection: SelectionResult) -> ExecutionResult:
        """Apply selected rules and produce an answer plus trace."""

        matching_rules = [
            rule for rule in selection.active_rules if rule.matches(selection.task_facts)
        ]
        effects = self._unique_effects(rule.effect for rule in matching_rules)
        answer = self._derive_answer(effects)
        trace = self._build_trace(task_id, selection.task_facts, matching_rules, effects, answer)

        return ExecutionResult(
            task_id=task_id,
            facts=selection.task_facts,
            selected_rule_ids=[rule.rule_id for rule in matching_rules],
            effects=effects,
            answer=answer,
            trace=trace,
        )

    def _unique_effects(self, effects: Iterable[str]) -> List[str]:
        """Return effects in first-seen order without duplicates."""

        seen = set()
        ordered_effects: List[str] = []
        for effect in effects:
            if effect not in seen:
                seen.add(effect)
                ordered_effects.append(effect)
        return ordered_effects

    def _derive_answer(self, effects: Sequence[str]) -> str:
        """Derive a compact answer from inferred effects.

        Safety-related effects are prioritized because the first prototype is
        framed around deployable reasoning constraints.
        """

        if "action_unsafe" in effects:
            return "action_unsafe"
        if "needs_replan" in effects:
            return "needs_replan"
        if "request_manual_review" in effects:
            return "request_manual_review"
        if "inspect_object" in effects:
            return "inspect_object"
        if "action_safe" in effects:
            return "action_safe"
        if effects:
            return effects[0]
        return "no_rule_matched"

    def _build_trace(
        self,
        task_id: str,
        facts: Sequence[str],
        rules: Sequence[Rule],
        effects: Sequence[str],
        answer: str,
    ) -> List[str]:
        """Build an inspectable reasoning trace."""

        trace = [
            f"Task: {task_id}",
            f"Input facts: {', '.join(facts) if facts else 'none'}",
        ]

        if not rules:
            trace.append("No rules matched the input facts.")
            trace.append("Answer: no_rule_matched")
            return trace

        for rule in rules:
            conditions = ", ".join(sorted(rule.conditions))
            trace.append(
                f"Activated {rule.rule_id}: conditions [{conditions}] -> effect [{rule.effect}]"
            )

        trace.append(f"Inferred effects: {', '.join(effects)}")
        trace.append(f"Answer: {answer}")
        return trace
