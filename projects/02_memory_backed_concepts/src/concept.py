"""Concept data model for the memory-backed concepts prototype.

A concept is reusable knowledge stored outside model parameters. The first
prototype keeps concepts explicit so they can be inspected, retrieved, applied,
and updated after outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Concept:
    """Reusable concept stored in external memory.

    Attributes:
        concept_id: Stable identifier for the concept.
        name: Human-readable concept name.
        description: Short explanation of what the concept means.
        trigger_conditions: Facts or attributes that make the concept relevant.
        recommended_effects: Reasoning effects or action adjustments.
        confidence: Current trust score between 0.0 and 1.0.
        evidence: Episode or task ids that support the concept.
        failure_notes: Notes about cases where the concept failed or was risky.
        status: Lifecycle state such as candidate, active, revised, deprecated.
    """

    concept_id: str
    name: str
    description: str
    trigger_conditions: List[str]
    recommended_effects: List[str]
    confidence: float = 0.5
    evidence: List[str] = field(default_factory=list)
    failure_notes: List[str] = field(default_factory=list)
    status: str = "active"

    def matches(self, task_facts: List[str]) -> bool:
        """Return True when at least one trigger condition appears in the task facts."""

        fact_set = set(task_facts)
        return any(condition in fact_set for condition in self.trigger_conditions)

    def match_score(self, task_facts: List[str]) -> float:
        """Return a simple relevance score based on trigger overlap and confidence."""

        if not self.trigger_conditions:
            return 0.0

        fact_set = set(task_facts)
        matched = sum(1 for condition in self.trigger_conditions if condition in fact_set)
        overlap_score = matched / len(self.trigger_conditions)
        return round(overlap_score * self.confidence, 4)

    def apply_success(self, evidence_id: str, confidence_delta: float = 0.03) -> None:
        """Update concept after successful use."""

        if evidence_id not in self.evidence:
            self.evidence.append(evidence_id)
        self.confidence = min(1.0, round(self.confidence + confidence_delta, 4))

    def apply_failure(self, note: str, confidence_delta: float = 0.05) -> None:
        """Update concept after failed or questionable use."""

        self.failure_notes.append(note)
        self.confidence = max(0.0, round(self.confidence - confidence_delta, 4))

    def to_dict(self) -> Dict:
        """Serialize concept to a plain dictionary."""

        return {
            "concept_id": self.concept_id,
            "name": self.name,
            "description": self.description,
            "trigger_conditions": list(self.trigger_conditions),
            "recommended_effects": list(self.recommended_effects),
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "failure_notes": list(self.failure_notes),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Concept":
        """Create a concept from a dictionary."""

        return cls(
            concept_id=data["concept_id"],
            name=data["name"],
            description=data.get("description", ""),
            trigger_conditions=list(data.get("trigger_conditions", [])),
            recommended_effects=list(data.get("recommended_effects", [])),
            confidence=float(data.get("confidence", 0.5)),
            evidence=list(data.get("evidence", [])),
            failure_notes=list(data.get("failure_notes", [])),
            status=data.get("status", "active"),
        )
