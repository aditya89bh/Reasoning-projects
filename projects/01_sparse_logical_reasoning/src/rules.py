"""Rule definitions for the sparse logical reasoning prototype.

The prototype keeps rules explicit and inspectable. Each rule contains a set of
required conditions and an effect. A rule is considered active when all required
conditions are present in the task state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Iterable, List


@dataclass(frozen=True)
class Rule:
    """A minimal symbolic rule.

    Attributes:
        rule_id: Stable identifier for the rule.
        name: Human-readable rule name.
        conditions: Conditions required for activation.
        effect: Output or inferred fact produced by the rule.
        description: Short explanation of why the rule exists.
    """

    rule_id: str
    name: str
    conditions: FrozenSet[str]
    effect: str
    description: str

    def matches(self, facts: Iterable[str]) -> bool:
        """Return True when all rule conditions are present in the task facts."""

        fact_set = frozenset(facts)
        return self.conditions.issubset(fact_set)


def default_rules() -> List[Rule]:
    """Return the default rule set used by the first prototype.

    The rule set intentionally contains both relevant and irrelevant rules so the
    dense and sparse paths can be compared.
    """

    return [
        Rule(
            rule_id="rule_fragile_high_force_unsafe",
            name="Fragile object high-force safety rule",
            conditions=frozenset({"object_fragile", "grip_force_high"}),
            effect="action_unsafe",
            description="Fragile objects should not be handled with high grip force.",
        ),
        Rule(
            rule_id="rule_fragile_low_force_safe",
            name="Fragile object low-force handling rule",
            conditions=frozenset({"object_fragile", "grip_force_low"}),
            effect="action_safe",
            description="Fragile objects can be handled safely with low grip force.",
        ),
        Rule(
            rule_id="rule_blocked_path_replan",
            name="Blocked path replanning rule",
            conditions=frozenset({"path_blocked"}),
            effect="needs_replan",
            description="A blocked path requires an alternate strategy.",
        ),
        Rule(
            rule_id="rule_clear_path_continue",
            name="Clear path continuation rule",
            conditions=frozenset({"path_clear"}),
            effect="continue_plan",
            description="A clear path allows the current plan to continue.",
        ),
        Rule(
            rule_id="rule_heavy_object_slow_speed",
            name="Heavy object slow-speed rule",
            conditions=frozenset({"object_heavy"}),
            effect="use_slow_speed",
            description="Heavy objects should be moved with slower motion.",
        ),
        Rule(
            rule_id="rule_slippery_surface_caution",
            name="Slippery surface caution rule",
            conditions=frozenset({"surface_slippery"}),
            effect="increase_stability_check",
            description="Slippery surfaces require additional stability checks.",
        ),
        Rule(
            rule_id="rule_operator_prefers_manual_review",
            name="Operator manual review preference rule",
            conditions=frozenset({"operator_prefers_review"}),
            effect="request_manual_review",
            description="Operator preference requires review before execution.",
        ),
        Rule(
            rule_id="rule_unknown_object_needs_inspection",
            name="Unknown object inspection rule",
            conditions=frozenset({"object_unknown"}),
            effect="inspect_object",
            description="Unknown objects should be inspected before action.",
        ),
    ]
