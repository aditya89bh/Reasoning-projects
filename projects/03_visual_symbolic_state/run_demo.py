"""Run the visual-to-symbolic state demo.

Usage:
    python projects/03_visual_symbolic_state/run_demo.py

The demo loads a structured scene, extracts spatial relations, builds a
SymbolicState, validates it, and prints predicates plus an inspectable trace.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from src.predicate_builder import PredicateBuilder
from src.relation_extractor import RelationExtractor
from src.scene_loader import SceneLoader
from src.validator import SymbolicStateValidator


PROJECT_DIR = Path(__file__).resolve().parent
SCENE_PATH = PROJECT_DIR / "examples" / "sample_scene.json"


def build_trace(objects, relations, state, validation) -> List[str]:
    """Build a compact trace for state construction."""

    return [
        f"Loaded objects: {len(objects)}",
        f"Extracted relations: {len(relations)}",
        f"Built predicates: {len(state.predicates)}",
        f"State confidence: {state.confidence}",
        f"Validation passed: {validation.valid}",
        f"Validation errors: {validation.errors if validation.errors else 'none'}",
        f"Validation warnings: {validation.warnings if validation.warnings else 'none'}",
    ]


def main() -> None:
    """Run structured scene to symbolic state conversion."""

    loader = SceneLoader()
    raw_scene = loader.load_json(SCENE_PATH)
    objects = loader.objects_from_scene(raw_scene)

    relations = RelationExtractor().extract(objects)
    state = PredicateBuilder().build(
        state_id=loader.state_id_from_scene(raw_scene),
        episode_id=loader.episode_id_from_scene(raw_scene),
        objects=objects,
        relations=relations,
        source=raw_scene.get("source", "structured_scene"),
    )
    validation = SymbolicStateValidator().validate(state)
    trace = build_trace(objects, relations, state, validation)

    print("=" * 72)
    print("Visual-to-Symbolic State Demo")
    print("=" * 72)
    print(f"State ID: {state.state_id}")
    print(f"Episode ID: {state.episode_id}")
    print(f"Source: {state.source}")
    print(f"Confidence: {state.confidence}")

    print("\nObjects:")
    for scene_object in state.objects:
        print(
            f" - {scene_object.object_id}: type={scene_object.object_type}, "
            f"attributes={scene_object.attributes}, position={scene_object.position}"
        )

    print("\nRelations:")
    for relation in state.relations:
        print(f" - {relation.predicate()}")

    print("\nPredicates:")
    for predicate in state.predicates:
        print(f" - {predicate}")

    print("\nValidation:")
    print(validation.as_dict())

    print("\nTrace:")
    for step in trace:
        print(f" - {step}")


if __name__ == "__main__":
    main()
