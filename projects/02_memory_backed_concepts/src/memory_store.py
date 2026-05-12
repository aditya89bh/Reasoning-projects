"""Concept memory store for the memory-backed concepts prototype.

The memory store keeps reusable concepts outside model parameters. It supports
loading, saving, listing, lookup, relevance search, and confidence updates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Optional

from .concept import Concept


class ConceptMemoryStore:
    """In-memory concept store with optional JSON persistence."""

    def __init__(self, concepts: Optional[Iterable[Concept]] = None):
        self._concepts = {concept.concept_id: concept for concept in concepts or []}

    @classmethod
    def from_json(cls, path: str | Path) -> "ConceptMemoryStore":
        """Load concepts from a JSON file."""

        json_path = Path(path)
        with json_path.open("r", encoding="utf-8") as file:
            raw_concepts = json.load(file)

        concepts = [Concept.from_dict(item) for item in raw_concepts]
        return cls(concepts)

    def to_json(self, path: str | Path) -> None:
        """Save concepts to a JSON file."""

        json_path = Path(path)
        json_path.parent.mkdir(parents=True, exist_ok=True)

        with json_path.open("w", encoding="utf-8") as file:
            json.dump([concept.to_dict() for concept in self.list_concepts()], file, indent=2)

    def add(self, concept: Concept) -> None:
        """Add or replace a concept."""

        self._concepts[concept.concept_id] = concept

    def get(self, concept_id: str) -> Concept:
        """Return a concept by id.

        Raises:
            KeyError: If the concept id is not present.
        """

        return self._concepts[concept_id]

    def find_by_name(self, name: str) -> Optional[Concept]:
        """Return the first concept matching a concept name."""

        normalized = name.strip().lower()
        for concept in self._concepts.values():
            if concept.name.lower() == normalized:
                return concept
        return None

    def list_concepts(self, include_inactive: bool = False) -> List[Concept]:
        """Return concepts sorted by concept id."""

        concepts = list(self._concepts.values())
        if not include_inactive:
            concepts = [concept for concept in concepts if concept.status != "deprecated"]
        return sorted(concepts, key=lambda concept: concept.concept_id)

    def search(self, task_facts: List[str], limit: int = 5) -> List[Concept]:
        """Return concepts ranked by relevance to task facts."""

        scored = []
        for concept in self.list_concepts():
            score = concept.match_score(task_facts)
            if score > 0:
                scored.append((score, concept.confidence, concept.concept_id, concept))

        scored.sort(reverse=True, key=lambda item: (item[0], item[1], item[2]))
        return [concept for _, _, _, concept in scored[:limit]]

    def update_after_success(self, concept_id: str, evidence_id: str) -> None:
        """Increase confidence after a concept was useful."""

        self.get(concept_id).apply_success(evidence_id)

    def update_after_failure(self, concept_id: str, note: str) -> None:
        """Decrease confidence after a concept failed or was risky."""

        self.get(concept_id).apply_failure(note)

    def __len__(self) -> int:
        return len(self._concepts)
