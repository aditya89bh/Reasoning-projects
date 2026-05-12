"""Symbolic state data model for the visual-to-symbolic state prototype.

The goal of this project is to convert structured scene input into explicit
objects, attributes, relations, and predicates that downstream reasoning systems
can use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class SceneObject:
    """Object representation extracted from a scene."""

    object_id: str
    object_type: str
    attributes: Dict[str, str]
    position: Dict[str, float]
    confidence: float = 1.0

    def attribute_predicates(self) -> List[str]:
        """Return symbolic predicates for object attributes."""

        predicates = [f"object({self.object_id})", f"type({self.object_id}, {self.object_type})"]
        for key, value in sorted(self.attributes.items()):
            predicates.append(f"{key}({self.object_id}, {value})")
        return predicates


@dataclass(frozen=True)
class Relation:
    """Symbolic relation between two objects."""

    relation_type: str
    subject_id: str
    object_id: str
    confidence: float = 1.0

    def predicate(self) -> str:
        """Return predicate string for the relation."""

        return f"{self.relation_type}({self.subject_id}, {self.object_id})"


@dataclass
class SymbolicState:
    """Reasoning-ready symbolic state."""

    state_id: str
    episode_id: str
    objects: List[SceneObject]
    relations: List[Relation] = field(default_factory=list)
    source: str = "structured_scene"
    confidence: float = 1.0

    @property
    def predicates(self) -> List[str]:
        """Return all symbolic predicates in a stable order."""

        predicates: List[str] = []
        for scene_object in sorted(self.objects, key=lambda item: item.object_id):
            predicates.extend(scene_object.attribute_predicates())
        for relation in sorted(
            self.relations,
            key=lambda item: (item.relation_type, item.subject_id, item.object_id),
        ):
            predicates.append(relation.predicate())
        return predicates

    def to_dict(self) -> Dict:
        """Serialize symbolic state to a dictionary."""

        return {
            "state_id": self.state_id,
            "episode_id": self.episode_id,
            "source": self.source,
            "confidence": self.confidence,
            "objects": [
                {
                    "object_id": item.object_id,
                    "object_type": item.object_type,
                    "attributes": dict(item.attributes),
                    "position": dict(item.position),
                    "confidence": item.confidence,
                }
                for item in self.objects
            ],
            "relations": [
                {
                    "relation_type": item.relation_type,
                    "subject_id": item.subject_id,
                    "object_id": item.object_id,
                    "confidence": item.confidence,
                }
                for item in self.relations
            ],
            "predicates": self.predicates,
        }
