"""Rule scoring for the rule induction prototype.

The scorer evaluates candidate rules against episodes using simple coverage and
precision metrics. This keeps the first prototype measurable and inspectable.
"""

from __future__ import annotations

from typing import List

from .episode import Episode
from .rule import InducedRule


class RuleScorer:
    """Score candidate rules against observed episodes."""

    def score(self, rules: List[InducedRule], episodes: List[Episode]) -> List[InducedRule]:
        """Return scored candidate rules."""

        scored_rules: List[InducedRule] = []
        total_episodes = len(episodes)

        for rule in rules:
            matching_episodes = [episode for episode in episodes if rule.matches(episode.facts)]
            positive_matches = [
                episode
                for episode in matching_episodes
                if self._effect_matches_episode(rule.effect, episode)
            ]
            failure_cases = [
                episode.episode_id
                for episode in matching_episodes
                if not self._effect_matches_episode(rule.effect, episode)
            ]

            coverage = len(matching_episodes) / total_episodes if total_episodes else 0.0
            precision = len(positive_matches) / len(matching_episodes) if matching_episodes else 0.0
            confidence = self._confidence_from_scores(coverage, precision, len(positive_matches))
            status = "accepted" if confidence >= 0.65 and precision >= 0.7 else "candidate"

            scored_rules.append(
                InducedRule(
                    rule_id=rule.rule_id,
                    name=rule.name,
                    conditions=list(rule.conditions),
                    effect=rule.effect,
                    source_episodes=list(rule.source_episodes),
                    confidence=confidence,
                    coverage=round(coverage, 4),
                    precision=round(precision, 4),
                    failure_cases=failure_cases,
                    status=status,
                )
            )

        return scored_rules

    def _effect_matches_episode(self, effect: str, episode: Episode) -> bool:
        """Return True if rule effect is consistent with episode outcome."""

        if effect.startswith("avoid_"):
            avoided_action = effect.replace("avoid_", "", 1)
            return episode.action == avoided_action and episode.is_failure

        if effect.startswith("prefer_"):
            preferred_action = effect.replace("prefer_", "", 1)
            return episode.action == preferred_action and episode.is_success

        if effect.startswith("review_"):
            reviewed_action = effect.replace("review_", "", 1)
            return episode.action == reviewed_action

        return False

    def _confidence_from_scores(self, coverage: float, precision: float, positive_count: int) -> float:
        """Compute confidence from coverage, precision, and evidence count."""

        evidence_bonus = min(0.2, positive_count * 0.05)
        confidence = (0.65 * precision) + (0.25 * coverage) + evidence_bonus
        return round(min(1.0, confidence), 4)
