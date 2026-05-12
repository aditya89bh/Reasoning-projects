"""Tests for the memory-backed concepts prototype.

Run from the repository root with:
    python -m pytest projects/02_memory_backed_concepts/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.adapter import ConceptReasoningAdapter
from src.concept import Concept
from src.memory_store import ConceptMemoryStore
from src.retriever import ConceptRetriever
from src.updater import ConceptMemoryUpdater


def build_store():
    return ConceptMemoryStore(
        [
            Concept(
                concept_id="concept_fragile_object",
                name="fragile_object",
                description="Fragile objects should avoid high force.",
                trigger_conditions=["object_fragile", "material_glass"],
                recommended_effects=["avoid_high_force", "slow_motion"],
                confidence=0.85,
            ),
            Concept(
                concept_id="concept_blocked_path",
                name="blocked_path",
                description="Blocked paths require alternate route planning.",
                trigger_conditions=["path_blocked", "obstacle_detected"],
                recommended_effects=["select_alternate_path"],
                confidence=0.8,
            ),
            Concept(
                concept_id="concept_operator_review_preference",
                name="operator_review_preference",
                description="Manual review is needed when operator preference says so.",
                trigger_conditions=["operator_prefers_review"],
                recommended_effects=["request_manual_review"],
                confidence=0.82,
            ),
        ]
    )


def test_concept_matches_task_facts():
    concept = Concept(
        concept_id="concept_fragile_object",
        name="fragile_object",
        description="Fragile objects should avoid high force.",
        trigger_conditions=["object_fragile", "material_glass"],
        recommended_effects=["avoid_high_force"],
        confidence=0.8,
    )

    assert concept.matches(["material_glass", "object_light"]) is True
    assert concept.matches(["path_clear"]) is False
    assert concept.match_score(["material_glass"]) == 0.4


def test_memory_store_search_returns_relevant_concept():
    store = build_store()
    results = store.search(["material_glass", "object_light"])

    assert len(results) == 1
    assert results[0].concept_id == "concept_fragile_object"


def test_retriever_returns_trace_and_concept_ids():
    store = build_store()
    retrieval = ConceptRetriever(store).retrieve(
        task_id="task_pick_glass_object",
        task_facts=["material_glass", "object_light"],
    )

    assert retrieval.concept_ids == ["concept_fragile_object"]
    assert retrieval.recommended_effects == ["avoid_high_force", "slow_motion"]
    assert any("Retrieved concept_fragile_object" in step for step in retrieval.trace)


def test_adapter_converts_concept_effects_to_recommendation():
    store = build_store()
    retrieval = ConceptRetriever(store).retrieve(
        task_id="task_pick_glass_object",
        task_facts=["material_glass"],
    )
    reasoning = ConceptReasoningAdapter().adapt(retrieval)

    assert reasoning.retrieved_concept_ids == ["concept_fragile_object"]
    assert reasoning.recommendation == "use_low_force_strategy"
    assert "avoid_high_force" in reasoning.recommended_effects


def test_manual_review_takes_priority_over_low_force_strategy():
    store = build_store()
    retrieval = ConceptRetriever(store).retrieve(
        task_id="task_operator_review",
        task_facts=["operator_prefers_review", "object_fragile"],
    )
    reasoning = ConceptReasoningAdapter().adapt(retrieval)

    assert "concept_operator_review_preference" in reasoning.retrieved_concept_ids
    assert "concept_fragile_object" in reasoning.retrieved_concept_ids
    assert reasoning.recommendation == "request_manual_review"


def test_no_concept_match_returns_no_recommendation():
    store = build_store()
    retrieval = ConceptRetriever(store).retrieve(
        task_id="task_no_match",
        task_facts=["object_standard", "path_clear"],
    )
    reasoning = ConceptReasoningAdapter().adapt(retrieval)

    assert retrieval.concept_ids == []
    assert reasoning.recommendation == "no_concept_recommendation"
    assert any("No concepts retrieved" in step for step in retrieval.trace)


def test_memory_update_after_success_increases_confidence_and_adds_evidence():
    store = build_store()
    before = store.get("concept_fragile_object").confidence

    update = ConceptMemoryUpdater(store).update(
        task_id="task_pick_glass_object",
        concept_ids=["concept_fragile_object"],
        outcome="success",
    )

    concept = store.get("concept_fragile_object")
    assert concept.confidence > before
    assert "task_pick_glass_object" in concept.evidence
    assert update.updated_concept_ids == ["concept_fragile_object"]


def test_memory_update_after_failure_decreases_confidence_and_adds_note():
    store = build_store()
    before = store.get("concept_blocked_path").confidence

    update = ConceptMemoryUpdater(store).update(
        task_id="task_blocked_path_replan",
        concept_ids=["concept_blocked_path"],
        outcome="failure",
        note="Alternate path was also blocked.",
    )

    concept = store.get("concept_blocked_path")
    assert concept.confidence < before
    assert "Alternate path was also blocked." in concept.failure_notes
    assert update.updated_concept_ids == ["concept_blocked_path"]
