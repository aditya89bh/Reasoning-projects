"""Run the sparse logical reasoning demo.

Usage:
    python projects/01_sparse_logical_reasoning/run_demo.py

The demo compares sparse rule activation against a dense baseline. Sparse
selection activates only matching rules. Dense selection selects every rule and
then lets the executor filter matches during execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.evaluator import ReasoningEvaluator
from src.executor import RuleExecutor
from src.rules import default_rules
from src.selector import DenseRuleSelector, SparseRuleSelector


PROJECT_DIR = Path(__file__).resolve().parent
TASKS_PATH = PROJECT_DIR / "examples" / "demo_tasks.json"


def load_tasks(path: Path = TASKS_PATH) -> List[Dict]:
    """Load demo tasks from JSON."""

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_path(path_name: str, selector, executor, evaluator, task: Dict) -> Dict:
    """Run one task through a selector, executor, and evaluator."""

    selection = selector.select(task["facts"])
    execution = executor.execute(task["task_id"], selection)
    evaluation = evaluator.evaluate(task["expected_answer"], execution, selection)

    print("\n" + "=" * 72)
    print(f"Path: {path_name}")
    print(f"Task: {task['task_id']}")
    print(f"Description: {task['description']}")
    print(f"Expected: {task['expected_answer']}")
    print(f"Actual: {execution.answer}")
    print(f"Correct: {evaluation.correct}")
    print(
        f"Active rules: {evaluation.active_rules}/{evaluation.total_rules} "
        f"(sparsity={evaluation.sparsity_ratio:.3f})"
    )
    print("Trace:")
    for step in execution.trace:
        print(f" - {step}")

    result = evaluation.as_row()
    result["path"] = path_name
    return result


def print_summary(results: List[Dict]) -> None:
    """Print compact result summary."""

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)

    for result in results:
        print(
            f"{result['path']:>6} | "
            f"{result['task_id']:<28} | "
            f"correct={str(result['correct']):<5} | "
            f"active={result['active_rules']}/{result['total_rules']} | "
            f"sparsity={result['sparsity_ratio']}"
        )

    sparse_results = [result for result in results if result["path"] == "sparse"]
    dense_results = [result for result in results if result["path"] == "dense"]

    if sparse_results:
        sparse_accuracy = sum(result["correct"] for result in sparse_results) / len(sparse_results)
        sparse_avg_ratio = sum(result["sparsity_ratio"] for result in sparse_results) / len(sparse_results)
        print("\nSparse path:")
        print(f"accuracy={sparse_accuracy:.3f}")
        print(f"average_sparsity_ratio={sparse_avg_ratio:.3f}")

    if dense_results:
        dense_accuracy = sum(result["correct"] for result in dense_results) / len(dense_results)
        dense_avg_ratio = sum(result["sparsity_ratio"] for result in dense_results) / len(dense_results)
        print("\nDense baseline:")
        print(f"accuracy={dense_accuracy:.3f}")
        print(f"average_sparsity_ratio={dense_avg_ratio:.3f}")


def main() -> None:
    """Run demo tasks through sparse and dense reasoning paths."""

    rules = default_rules()
    sparse_selector = SparseRuleSelector(rules)
    dense_selector = DenseRuleSelector(rules)
    executor = RuleExecutor()
    evaluator = ReasoningEvaluator()
    tasks = load_tasks()

    results: List[Dict] = []
    for task in tasks:
        results.append(run_path("sparse", sparse_selector, executor, evaluator, task))
        results.append(run_path("dense", dense_selector, executor, evaluator, task))

    print_summary(results)


if __name__ == "__main__":
    main()
