"""Run the memory-backed concepts demo.

Usage:
    python projects/02_memory_backed_concepts/run_demo.py

The demo loads a small concept memory, retrieves relevant concepts for each task,
adapts retrieved concepts into a recommendation, updates concept confidence from
outcomes, and prints an inspectable trace.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.adapter import ConceptReasoningAdapter
from src.memory_store import ConceptMemoryStore
from src.retriever import ConceptRetriever
from src.updater import ConceptMemoryUpdater


PROJECT_DIR = Path(__file__).resolve().parent
CONCEPT_MEMORY_PATH = PROJECT_DIR / "examples" / "concept_memory.json"
TASKS_PATH = PROJECT_DIR / "examples" / "demo_tasks.json"


def load_tasks(path: Path = TASKS_PATH) -> List[Dict]:
    """Load demo tasks from JSON."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_task(
    task: Dict,
    retriever: ConceptRetriever,
    adapter: ConceptReasoningAdapter,
    updater: ConceptMemoryUpdater,
) -> Dict:
    """Run one task through retrieval, adaptation, and memory update."""

    retrieval = retriever.retrieve(task_id=task["task_id"], task_facts=task["facts"])
    reasoning = adapter.adapt(retrieval)
    update = updater.update(
        task_id=task["task_id"],
        concept_ids=reasoning.retrieved_concept_ids,
        outcome=task.get("outcome", "success"),
    )

    concept_match = reasoning.retrieved_concept_ids == task["expected_concepts"]
    recommendation_match = reasoning.recommendation == task["expected_recommendation"]

    print("\n" + "=" * 72)
    print(f"Task: {task['task_id']}")
    print(f"Description: {task['description']}")
    print(f"Facts: {', '.join(task['facts'])}")
    print(f"Expected concepts: {task['expected_concepts']}")
    print(f"Retrieved concepts: {reasoning.retrieved_concept_ids}")
    print(f"Expected recommendation: {task['expected_recommendation']}")
    print(f"Recommendation: {reasoning.recommendation}")
    print(f"Concept match: {concept_match}")
    print(f"Recommendation match: {recommendation_match}")

    print("\nRetrieval trace:")
    for step in retrieval.trace:
        print(f" - {step}")

    print("\nReasoning trace:")
    for step in reasoning.trace:
        print(f" - {step}")

    print("\nUpdate trace:")
    for step in update.trace:
        print(f" - {step}")

    return {
        "task_id": task["task_id"],
        "expected_concepts": task["expected_concepts"],
        "retrieved_concepts": reasoning.retrieved_concept_ids,
        "expected_recommendation": task["expected_recommendation"],
        "recommendation": reasoning.recommendation,
        "concept_match": concept_match,
        "recommendation_match": recommendation_match,
        "updated_concepts": update.updated_concept_ids,
    }


def print_summary(results: List[Dict]) -> None:
    """Print compact summary for all demo tasks."""

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)

    for result in results:
        print(
            f"{result['task_id']:<34} | "
            f"concepts={str(result['concept_match']):<5} | "
            f"recommendation={str(result['recommendation_match']):<5} | "
            f"retrieved={result['retrieved_concepts']}"
        )

    if results:
        concept_accuracy = sum(result["concept_match"] for result in results) / len(results)
        recommendation_accuracy = (
            sum(result["recommendation_match"] for result in results) / len(results)
        )
        print("\nAggregate:")
        print(f"concept_match_accuracy={concept_accuracy:.3f}")
        print(f"recommendation_match_accuracy={recommendation_accuracy:.3f}")


def main() -> None:
    """Run all memory-backed concept demo tasks."""

    memory_store = ConceptMemoryStore.from_json(CONCEPT_MEMORY_PATH)
    retriever = ConceptRetriever(memory_store)
    adapter = ConceptReasoningAdapter()
    updater = ConceptMemoryUpdater(memory_store)
    tasks = load_tasks()

    results = [run_task(task, retriever, adapter, updater) for task in tasks]
    print_summary(results)


if __name__ == "__main__":
    main()
