"""Shared fact normalization utilities.

The reasoning projects use simple fact labels such as `object_fragile` and
`material_glass`, while symbolic state uses predicate strings such as
`fragile(cup_glass, true)` and `material(cup_glass, glass)`.

This module provides a shared normalization layer so integrated demos do not need
to duplicate predicate-to-fact mapping logic.
"""

from __future__ import annotations

from typing import Iterable, List, Set


class FactNormalizer:
    """Normalize symbolic predicates into project-level fact labels."""

    def __init__(self):
        self.predicate_map = {
            "material(cup_glass, glass)": "material_glass",
            "fragile(cup_glass, true)": "object_fragile",
            "type(cup_glass, cup)": "object_cup",
            "shape(cup_glass, cylinder)": "shape_cylinder",
            "object(cup_glass)": "object_detected",
        }

    def normalize_predicates(
        self,
        predicates: Iterable[str],
        extra_facts: Iterable[str] | None = None,
    ) -> List[str]:
        """Convert symbolic predicates into sorted fact labels.

        Args:
            predicates: Symbolic predicates from Project 03.
            extra_facts: Optional task assumptions or externally supplied facts.
        """

        facts: Set[str] = set()
        for predicate in predicates:
            mapped_fact = self.predicate_map.get(predicate)
            if mapped_fact:
                facts.add(mapped_fact)

        if extra_facts:
            facts.update(extra_facts)

        return sorted(facts)

    def add_mapping(self, predicate: str, fact: str) -> None:
        """Add or replace a predicate-to-fact mapping."""

        self.predicate_map[predicate] = fact
