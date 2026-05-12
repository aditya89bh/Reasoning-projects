"""Tests for the sparse logical reasoning prototype.

Run from the repository root with:
    python -m pytest projects/01_sparse_logical_reasoning/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.evaluator import ReasoningEvaluator
from src.executor import RuleExecutor
from src.rules import default_rules
from src.selector import DenseRuleSelector, SparseRuleSelector


def run_sparse_task(task_id, facts, expected_answer):
    rules = default_rules()
    selector = SparseRuleSelector(rules)
    executor = RuleExecutor()
    evaluator = ReasoningEvaluator()

    selection = selector.select(facts)
    execution = executor.execute(task_id, selection)
    evaluation = evaluator.evaluate(expected_answer, execution, selection)

    return selection, execution, evaluation


def test_fragile_high_force_is_unsafe():
    selection, execution, evaluation = run_sparse_task(
        task_id="task_fragile_high_force",
        facts=["object_fragile", "grip_force_high"],
        expected_answer="action_unsafe",
    )

    assert execution.answer == "action_unsafe"
    assert evaluation.correct is True
    assert selection.active_rule_count == 1
    assert selection.total_rules == 8
    assert evaluation.trace_clarity == "high"


def test_fragile_low_force_is_safe():
    selection, execution, evaluation = run_sparse_task(
        task_id="task_fragile_low_force",
        facts=["object_fragile", "grip_force_low"],
        expected_answer="action_safe",
    )

    assert execution.answer == "action_safe"
    assert evaluation.correct is True
    assert selection.active_rule_count == 1
    assert evaluation.sparsity_ratio == 1 / 8


def test_blocked_path_requires_replan():
    selection, execution, evaluation = run_sparse_task(
        task_id="task_blocked_path",
        facts=["path_blocked"],
        expected_answer="needs_replan",
    )

    assert execution.answer == "needs_replan"
    assert evaluation.correct is True
    assert "rule_blocked_path_replan" in execution.selected_rule_ids


def test_unknown_object_requires_inspection():
    selection, execution, evaluation = run_sparse_task(
        task_id="task_unknown_object",
        facts=["object_unknown"],
        expected_answer="inspect_object",
    )

    assert execution.answer == "inspect_object"
    assert evaluation.correct is True
    assert selection.active_rule_count == 1


def test_no_matching_rule_returns_no_rule_matched():
    selection, execution, evaluation = run_sparse_task(
        task_id="task_no_match",
        facts=["object_light", "grip_force_medium"],
        expected_answer="no_rule_matched",
    )

    assert execution.answer == "no_rule_matched"
    assert evaluation.correct is True
    assert selection.active_rule_count == 0
    assert execution.selected_rule_ids == []
    assert any("No rules matched" in step for step in execution.trace)


def test_sparse_selector_activates_fewer_rules_than_dense_selector():
    rules = default_rules()
    facts = ["object_fragile", "grip_force_high"]

    sparse_selection = SparseRuleSelector(rules).select(facts)
    dense_selection = DenseRuleSelector(rules).select(facts)

    assert sparse_selection.active_rule_count == 1
    assert dense_selection.active_rule_count == len(rules)
    assert sparse_selection.sparsity_ratio < dense_selection.sparsity_ratio


def test_dense_baseline_still_produces_correct_answer_after_executor_filtering():
    rules = default_rules()
    facts = ["object_fragile", "grip_force_high"]
    selection = DenseRuleSelector(rules).select(facts)
    execution = RuleExecutor().execute("task_dense_baseline", selection)

    assert execution.answer == "action_unsafe"
    assert execution.selected_rule_ids == ["rule_fragile_high_force_unsafe"]
