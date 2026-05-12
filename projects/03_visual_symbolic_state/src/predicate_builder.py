"""Predicate builder for the visual-to-symbolic state prototype.

This module converts scene objects and extracted relations into a complete
SymbolicState that downstream reasoning systems can consume.
"""

from __future__ import annotations

from typing import List

from .symbolic_state import Relation, SceneObject, SymbolicState


class PredicateBuilder:
    """Build reasoning-ready symbolic state from objects and relations."""

    def build(
        self,
        state_id: str,
        episode_id: str,
        objects: List[SceneObject],
        relations: List[Relation],
        source: str = "structured_scene",
    ) -> SymbolicState:
        """Create a SymbolicState from objects and relations."""

        confidence = self._state_confidence(objects, relations)
        return SymbolicState(
            state_id=state_id,
            episode_id=episode_id,
            objects=objects,
            relations=relations,
            source=source,
            confidence=confidence,
        )

    def _state_confidence(self, objects: List[SceneObject], relations: List[Relation]) -> float:
        """Compute a simple average confidence for the state."""

        confidence_values = [item.confidence for item in objects]
        confidence_values.extend(item.confidence for item in relations)

        if not confidence_values:
            return 0.0

        return round(sum(confidence_values) / len(confidence_values), 4)
