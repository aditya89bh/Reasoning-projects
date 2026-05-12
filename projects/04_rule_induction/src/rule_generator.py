"""Candidate rule generation for the rule induction prototype.

The generator converts repeated patterns into explicit candidate rules. The first
version uses deterministic templates so generated rules remain inspectable.
"""

from __future__ import annotations

from typing import List

from .pattern_detector import DetectedPattern
from .rule import InducedRule


class RuleGenerator:
    """Generate candidate rules from detected patterns."""

    def generate(self, patterns: List[DetectedPattern]) -> List[InducedRule]:
        """Generate one candidate rule per detected pattern."""

        rules: List[InducedRule] = []
        for index, pattern in enumerate(patterns):
            effect = self._effect_from_pattern(pattern)
            rule = InducedRule(
                rule_id=f"rule_{index:03d}_{pattern.fact}_{effect}",
                name=self._name_from_pattern(pattern, effect),
                conditions=[pattern.fact],
                effect=effect,
                source_episodes=list(pattern.episode_ids),
                confidence=0.5,
                coverage=0.0,
                precision=0.0,
                status="candidate",
            )
            rules.append(rule)
        return rules

    def _effect_from_pattern(self, pattern: DetectedPattern) -> str:
        """Map a repeated outcome pattern to a rule effect."""

        if pattern.outcome in {"failure", "unsafe", "incorrect"}:
            return f"avoid_{pattern.action}"
        if pattern.outcome in {"success", "safe", "correct"}:
            return f"prefer_{pattern.action}"
        return f"review_{pattern.action}"

    def _name_from_pattern(self, pattern: DetectedPattern, effect: str) -> str:
        """Create a readable rule name."""

        return f"If {pattern.fact} then {effect}"
