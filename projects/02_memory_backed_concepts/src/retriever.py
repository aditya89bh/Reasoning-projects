"""Concept retrieval for the memory-backed concepts prototype.

The retriever turns a task state into relevant concepts and an inspectable trace.
It is intentionally deterministic and simple for the first prototype.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .concept import Concept
from .memory_store import ConceptMemoryStore


@dataclass(frozen=True)
class RetrievalResult:
    """Concept retrieval result for one task."""

    task_id: str
    task_facts: List[str]
    retrieved_concepts: List[Concept]
    trace: List[str]

    @property
    def concept_ids(self) -> List[str]:
        return [concept.concept_id for concept in self.retrieved_concepts]

    @property
    def recommended_effects(self) -> List[str]:
        effects: List[str] = []
        seen = set()
        for concept in self.retrieved_concepts:
            for effect in concept.recommended_effects:
                if effect not in seen:
                    seen.add(effect)
                    effects.append(effect)
        return effects

    def as_dict(self) -> Dict:
        """Return a compact serializable representation."""

        return {
            "task_id": self.task_id,
            "task_facts": list(self.task_facts),
            "retrieved_concepts": [concept.to_dict() for concept in self.retrieved_concepts],
            "recommended_effects": self.recommended_effects,
            "trace": list(self.trace),
        }


class ConceptRetriever:
    """Retrieve relevant concepts from a concept memory store."""

    def __init__(self, memory_store: ConceptMemoryStore):
        self.memory_store = memory_store

    def retrieve(self, task_id: str, task_facts: List[str], limit: int = 5) -> RetrievalResult:
        """Retrieve concepts relevant to the supplied task facts."""

        concepts = self.memory_store.search(task_facts=task_facts, limit=limit)
        trace = self._build_trace(task_id, task_facts, concepts)

        return RetrievalResult(
            task_id=task_id,
            task_facts=list(task_facts),
            retrieved_concepts=concepts,
            trace=trace,
        )

    def _build_trace(
        self,
        task_id: str,
        task_facts: List[str],
        concepts: List[Concept],
    ) -> List[str]:
        """Build a human-readable retrieval trace."""

        trace = [
            f"Task: {task_id}",
            f"Task facts: {', '.join(task_facts) if task_facts else 'none'}",
        ]

        if not concepts:
            trace.append("No concepts retrieved.")
            return trace

        for concept in concepts:
            score = concept.match_score(task_facts)
            matched_conditions = [
                condition for condition in concept.trigger_conditions if condition in set(task_facts)
            ]
            trace.append(
                f"Retrieved {concept.concept_id}: matched [{', '.join(matched_conditions)}], "
                f"score={score}, confidence={concept.confidence}"
            )

        effects = []
        seen = set()
        for concept in concepts:
            for effect in concept.recommended_effects:
                if effect not in seen:
                    seen.add(effect)
                    effects.append(effect)

        trace.append(f"Recommended effects: {', '.join(effects) if effects else 'none'}")
        return trace
