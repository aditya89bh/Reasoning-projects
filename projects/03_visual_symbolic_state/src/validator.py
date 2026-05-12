"""Validation utilities for symbolic states.

The validator checks whether a generated SymbolicState is usable for downstream
reasoning. It is intentionally simple for the first prototype.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .symbolic_state import SymbolicState


@dataclass(frozen=True)
class ValidationResult:
    """Validation result for a symbolic state."""

    state_id: str
    valid: bool
    errors: List[str]
    warnings: List[str]
    predicate_count: int

    def as_dict(self) -> Dict:
        """Return a compact serializable representation."""

        return {
            "state_id": self.state_id,
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "predicate_count": self.predicate_count,
        }


class SymbolicStateValidator:
    """Validate symbolic state completeness and consistency."""

    def validate(self, state: SymbolicState) -> ValidationResult:
        """Validate a SymbolicState."""

        errors: List[str] = []
        warnings: List[str] = []
        predicates = state.predicates

        if not state.state_id:
            errors.append("missing_state_id")
        if not state.episode_id:
            errors.append("missing_episode_id")
        if not state.objects:
            errors.append("no_objects")
        if not predicates:
            errors.append("no_predicates")

        object_ids = [item.object_id for item in state.objects]
        if len(object_ids) != len(set(object_ids)):
            errors.append("duplicate_object_ids")

        if len(predicates) != len(set(predicates)):
            warnings.append("duplicate_predicates")

        for scene_object in state.objects:
            if not scene_object.object_id:
                errors.append("object_missing_id")
            if not scene_object.object_type:
                warnings.append(f"object_missing_type:{scene_object.object_id}")
            if "x" not in scene_object.position or "y" not in scene_object.position:
                warnings.append(f"object_missing_xy_position:{scene_object.object_id}")
            if scene_object.confidence < 0 or scene_object.confidence > 1:
                errors.append(f"object_confidence_out_of_range:{scene_object.object_id}")

        for relation in state.relations:
            if relation.subject_id not in object_ids:
                errors.append(f"relation_subject_missing:{relation.subject_id}")
            if relation.object_id not in object_ids:
                errors.append(f"relation_object_missing:{relation.object_id}")
            if relation.confidence < 0 or relation.confidence > 1:
                errors.append(
                    f"relation_confidence_out_of_range:{relation.relation_type}:{relation.subject_id}:{relation.object_id}"
                )

        return ValidationResult(
            state_id=state.state_id,
            valid=not errors,
            errors=errors,
            warnings=warnings,
            predicate_count=len(predicates),
        )
