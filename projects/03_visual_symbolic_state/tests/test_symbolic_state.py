"""Tests for the visual-to-symbolic state prototype.

Run from the repository root with:
    python -m pytest projects/03_visual_symbolic_state/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.predicate_builder import PredicateBuilder
from src.relation_extractor import RelationExtractor
from src.scene_loader import SceneLoader
from src.symbolic_state import SceneObject, SymbolicState
from src.validator import SymbolicStateValidator


def sample_objects():
    return [
        SceneObject(
            object_id="block_red",
            object_type="block",
            attributes={"color": "red", "shape": "cube"},
            position={"x": 1.0, "y": 2.0},
            confidence=0.98,
        ),
        SceneObject(
            object_id="sphere_blue",
            object_type="sphere",
            attributes={"color": "blue", "shape": "sphere"},
            position={"x": 4.0, "y": 2.0},
            confidence=0.96,
        ),
        SceneObject(
            object_id="cup_glass",
            object_type="cup",
            attributes={"material": "glass", "fragile": "true"},
            position={"x": 2.0, "y": 5.0},
            confidence=0.92,
        ),
    ]


def test_scene_object_generates_attribute_predicates():
    scene_object = SceneObject(
        object_id="block_red",
        object_type="block",
        attributes={"color": "red", "shape": "cube"},
        position={"x": 1.0, "y": 2.0},
    )

    predicates = scene_object.attribute_predicates()

    assert "object(block_red)" in predicates
    assert "type(block_red, block)" in predicates
    assert "color(block_red, red)" in predicates
    assert "shape(block_red, cube)" in predicates


def test_scene_loader_converts_raw_scene_to_objects():
    raw_scene = {
        "episode_id": "episode_test",
        "state_id": "state_test",
        "objects": [
            {
                "object_id": "block_red",
                "object_type": "block",
                "attributes": {"color": "red"},
                "position": {"x": 1.0, "y": 2.0},
                "confidence": 0.9,
            }
        ],
    }

    loader = SceneLoader()
    objects = loader.objects_from_scene(raw_scene)

    assert loader.episode_id_from_scene(raw_scene) == "episode_test"
    assert loader.state_id_from_scene(raw_scene) == "state_test"
    assert len(objects) == 1
    assert objects[0].object_id == "block_red"
    assert objects[0].attributes["color"] == "red"


def test_relation_extractor_computes_spatial_relations():
    relations = RelationExtractor(near_threshold=3.1).extract(sample_objects())
    predicates = [relation.predicate() for relation in relations]

    assert "left_of(block_red, sphere_blue)" in predicates
    assert "right_of(sphere_blue, block_red)" in predicates
    assert "below(block_red, cup_glass)" in predicates
    assert "above(cup_glass, block_red)" in predicates
    assert "near(block_red, sphere_blue)" in predicates


def test_predicate_builder_creates_symbolic_state():
    objects = sample_objects()
    relations = RelationExtractor(near_threshold=3.1).extract(objects)
    state = PredicateBuilder().build(
        state_id="state_test",
        episode_id="episode_test",
        objects=objects,
        relations=relations,
    )

    assert isinstance(state, SymbolicState)
    assert state.state_id == "state_test"
    assert state.episode_id == "episode_test"
    assert "object(block_red)" in state.predicates
    assert "material(cup_glass, glass)" in state.predicates
    assert "left_of(block_red, sphere_blue)" in state.predicates
    assert state.confidence > 0.0


def test_validator_accepts_valid_symbolic_state():
    objects = sample_objects()
    relations = RelationExtractor().extract(objects)
    state = PredicateBuilder().build(
        state_id="state_valid",
        episode_id="episode_valid",
        objects=objects,
        relations=relations,
    )

    validation = SymbolicStateValidator().validate(state)

    assert validation.valid is True
    assert validation.errors == []
    assert validation.predicate_count == len(state.predicates)


def test_validator_rejects_empty_state():
    state = SymbolicState(
        state_id="state_empty",
        episode_id="episode_empty",
        objects=[],
        relations=[],
    )

    validation = SymbolicStateValidator().validate(state)

    assert validation.valid is False
    assert "no_objects" in validation.errors
    assert "no_predicates" in validation.errors


def test_validator_detects_duplicate_object_ids():
    duplicate_objects = [
        SceneObject("obj_1", "block", {"color": "red"}, {"x": 1, "y": 1}),
        SceneObject("obj_1", "block", {"color": "blue"}, {"x": 2, "y": 2}),
    ]
    state = SymbolicState(
        state_id="state_duplicate",
        episode_id="episode_duplicate",
        objects=duplicate_objects,
    )

    validation = SymbolicStateValidator().validate(state)

    assert validation.valid is False
    assert "duplicate_object_ids" in validation.errors
