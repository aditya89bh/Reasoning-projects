"""Episode data model for the rule induction prototype.

An episode captures a task attempt: state facts, action, outcome, feedback, and
notes. Rule induction operates over repeated episode patterns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Episode:
    """Structured task episode used for rule induction."""

    episode_id: str
    facts: List[str]
    action: str
    outcome: str
    feedback: str = ""
    constraints: List[str] = field(default_factory=list)
    notes: str = ""

    @property
    def is_success(self) -> bool:
        """Return True when the episode outcome is successful."""

        return self.outcome.lower() in {"success", "safe", "correct"}

    @property
    def is_failure(self) -> bool:
        """Return True when the episode outcome is a failure."""

        return self.outcome.lower() in {"failure", "unsafe", "incorrect"}

    def contains_fact(self, fact: str) -> bool:
        """Return True when a fact appears in the episode."""

        return fact in set(self.facts)

    def to_dict(self) -> Dict:
        """Serialize episode to dictionary."""

        return {
            "episode_id": self.episode_id,
            "facts": list(self.facts),
            "action": self.action,
            "outcome": self.outcome,
            "feedback": self.feedback,
            "constraints": list(self.constraints),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Episode":
        """Create an episode from dictionary data."""

        return cls(
            episode_id=data["episode_id"],
            facts=list(data.get("facts", [])),
            action=data.get("action", ""),
            outcome=data.get("outcome", ""),
            feedback=data.get("feedback", ""),
            constraints=list(data.get("constraints", [])),
            notes=data.get("notes", ""),
        )
