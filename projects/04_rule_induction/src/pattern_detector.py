"""Pattern detection for the rule induction prototype.

The detector finds repeated fact/action/outcome patterns across episodes. These
patterns become the raw material for candidate rule generation.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .episode import Episode


@dataclass(frozen=True)
class DetectedPattern:
    """Repeated pattern found across episodes."""

    pattern_id: str
    fact: str
    action: str
    outcome: str
    episode_ids: List[str]
    count: int

    def to_dict(self) -> Dict:
        """Serialize pattern to dictionary."""

        return {
            "pattern_id": self.pattern_id,
            "fact": self.fact,
            "action": self.action,
            "outcome": self.outcome,
            "episode_ids": list(self.episode_ids),
            "count": self.count,
        }


class PatternDetector:
    """Detect repeated fact/action/outcome patterns."""

    def __init__(self, min_count: int = 2):
        self.min_count = min_count

    def detect(self, episodes: List[Episode]) -> List[DetectedPattern]:
        """Return patterns that appear at least min_count times."""

        grouped: Dict[Tuple[str, str, str], List[str]] = defaultdict(list)

        for episode in episodes:
            normalized_outcome = episode.outcome.strip().lower()
            for fact in episode.facts:
                key = (fact, episode.action, normalized_outcome)
                grouped[key].append(episode.episode_id)

        patterns: List[DetectedPattern] = []
        for index, ((fact, action, outcome), episode_ids) in enumerate(sorted(grouped.items())):
            if len(episode_ids) < self.min_count:
                continue

            patterns.append(
                DetectedPattern(
                    pattern_id=f"pattern_{index:03d}",
                    fact=fact,
                    action=action,
                    outcome=outcome,
                    episode_ids=episode_ids,
                    count=len(episode_ids),
                )
            )

        return patterns
