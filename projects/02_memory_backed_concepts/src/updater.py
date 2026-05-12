"""Memory update utilities for the memory-backed concepts prototype.

The updater records whether a retrieved concept helped or failed. This keeps
concept memory operational rather than static documentation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .memory_store import ConceptMemoryStore


@dataclass(frozen=True)
class MemoryUpdateResult:
    """Result of applying memory updates after a task outcome."""

    task_id: str
    outcome: str
    updated_concept_ids: List[str]
    trace: List[str]

    def as_dict(self) -> Dict:
        """Return a compact serializable representation."""

        return {
            "task_id": self.task_id,
            "outcome": self.outcome,
            "updated_concept_ids": list(self.updated_concept_ids),
            "trace": list(self.trace),
        }


class ConceptMemoryUpdater:
    """Update concept confidence based on task outcomes."""

    SUCCESS_OUTCOMES = {"success", "safe", "correct"}
    FAILURE_OUTCOMES = {"failure", "unsafe", "incorrect"}

    def __init__(self, memory_store: ConceptMemoryStore):
        self.memory_store = memory_store

    def update(
        self,
        task_id: str,
        concept_ids: List[str],
        outcome: str,
        note: str = "",
    ) -> MemoryUpdateResult:
        """Update retrieved concepts after a task outcome.

        Args:
            task_id: Task or episode identifier.
            concept_ids: Concepts that influenced the reasoning result.
            outcome: Outcome label such as success, failure, safe, unsafe.
            note: Optional failure or update note.
        """

        normalized_outcome = outcome.strip().lower()
        updated: List[str] = []
        trace = [f"Task: {task_id}", f"Outcome: {normalized_outcome}"]

        if not concept_ids:
            trace.append("No concepts to update.")
            return MemoryUpdateResult(task_id, normalized_outcome, updated, trace)

        for concept_id in concept_ids:
            if normalized_outcome in self.SUCCESS_OUTCOMES:
                self.memory_store.update_after_success(concept_id, evidence_id=task_id)
                concept = self.memory_store.get(concept_id)
                updated.append(concept_id)
                trace.append(
                    f"Updated {concept_id}: success evidence added, confidence={concept.confidence}"
                )
            elif normalized_outcome in self.FAILURE_OUTCOMES:
                failure_note = note or f"Concept did not help on {task_id}."
                self.memory_store.update_after_failure(concept_id, failure_note)
                concept = self.memory_store.get(concept_id)
                updated.append(concept_id)
                trace.append(
                    f"Updated {concept_id}: failure noted, confidence={concept.confidence}"
                )
            else:
                trace.append(f"Skipped {concept_id}: unsupported outcome '{normalized_outcome}'")

        return MemoryUpdateResult(
            task_id=task_id,
            outcome=normalized_outcome,
            updated_concept_ids=updated,
            trace=trace,
        )
