"""Relation extraction for the visual-to-symbolic state prototype.

The first version computes simple spatial relations from structured object
positions. This gives downstream reasoning a predicate-level world state.
"""

from __future__ import annotations

import math
from typing import List

from .symbolic_state import Relation, SceneObject


class RelationExtractor:
    """Extract spatial relations between scene objects."""

    def __init__(self, near_threshold: float = 2.5):
        self.near_threshold = near_threshold

    def extract(self, objects: List[SceneObject]) -> List[Relation]:
        """Extract spatial relations between all object pairs."""

        relations: List[Relation] = []

        for subject in objects:
            for target in objects:
                if subject.object_id == target.object_id:
                    continue

                relations.extend(self._pairwise_relations(subject, target))

        return self._dedupe(relations)

    def _pairwise_relations(self, subject: SceneObject, target: SceneObject) -> List[Relation]:
        """Return spatial relations from subject to target."""

        relations: List[Relation] = []
        subject_x = float(subject.position.get("x", 0.0))
        subject_y = float(subject.position.get("y", 0.0))
        target_x = float(target.position.get("x", 0.0))
        target_y = float(target.position.get("y", 0.0))

        if subject_x < target_x:
            relations.append(Relation("left_of", subject.object_id, target.object_id))
        elif subject_x > target_x:
            relations.append(Relation("right_of", subject.object_id, target.object_id))

        if subject_y > target_y:
            relations.append(Relation("above", subject.object_id, target.object_id))
        elif subject_y < target_y:
            relations.append(Relation("below", subject.object_id, target.object_id))

        distance = math.dist([subject_x, subject_y], [target_x, target_y])
        if distance <= self.near_threshold:
            relations.append(Relation("near", subject.object_id, target.object_id))

        return relations

    def _dedupe(self, relations: List[Relation]) -> List[Relation]:
        """Remove duplicate relations while preserving stable ordering."""

        seen = set()
        unique: List[Relation] = []
        for relation in relations:
            key = (relation.relation_type, relation.subject_id, relation.object_id)
            if key not in seen:
                seen.add(key)
                unique.append(relation)
        return unique
