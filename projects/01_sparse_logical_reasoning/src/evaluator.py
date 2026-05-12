"""Evaluation utilities for the sparse logical reasoning prototype.

The evaluator checks more than correctness. It also records sparse activation,
trace availability, and basic execution metadata so the prototype aligns with
the repository's evaluation philosophy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .executor import ExecutionResult
from .selector import SelectionResult


@dataclass(frozen=True)
class EvaluationResult:
    """Evaluation result for a single reasoning task."""

    task_id: str
    expected_answer: str
    actual_answer: str
    correct: bool
    active_rules: int
    total_rules: int
    sparsity_ratio: float
    trace_clarity: str
    notes: str

    def as_row(self) -> dict:
        """Return a compact dictionary for result tables."""

        return {
            "task_id": self.task_id,
            "expected_answer": self.expected_answer,
            "actual_answer": self.actual_answer,
            "correct": self.correct,
            "active_rules": self.active_rules,
            "total_rules": self.total_rules,
            "sparsity_ratio": round(self.sparsity_ratio, 3),
            "trace_clarity": self.trace_clarity,
            "notes": self.notes,
        }


class ReasoningEvaluator:
    """Evaluate correctness, sparsity, and trace quality."""

    def evaluate(
        self,
        expected_answer: str,
        execution: ExecutionResult,
        selection: SelectionResult,
    ) -> EvaluationResult:
        """Evaluate one task execution."""

        correct = execution.answer == expected_answer
        trace_clarity = self._score_trace(execution.trace)
        notes = self._build_notes(correct, execution, selection)

        return EvaluationResult(
            task_id=execution.task_id,
            expected_answer=expected_answer,
            actual_answer=execution.answer,
            correct=correct,
            active_rules=selection.active_rule_count,
            total_rules=selection.total_rules,
            sparsity_ratio=selection.sparsity_ratio,
            trace_clarity=trace_clarity,
            notes=notes,
        )

    def _score_trace(self, trace: List[str]) -> str:
        """Score trace clarity with a simple rubric."""

        if not trace:
            return "none"

        has_task = any(step.startswith("Task:") for step in trace)
        has_facts = any(step.startswith("Input facts:") for step in trace)
        has_answer = any(step.startswith("Answer:") for step in trace)
        has_activation = any(step.startswith("Activated") for step in trace)
        has_no_match = any("No rules matched" in step for step in trace)

        if has_task and has_facts and has_answer and (has_activation or has_no_match):
            return "high"
        if has_answer and (has_activation or has_no_match):
            return "medium"
        return "low"

    def _build_notes(
        self,
        correct: bool,
        execution: ExecutionResult,
        selection: SelectionResult,
    ) -> str:
        """Create a compact evaluation note."""

        correctness_note = "correct" if correct else "incorrect"
        return (
            f"{correctness_note}; "
            f"matched_rules={execution.matched_rule_count}; "
            f"selected_rules={selection.active_rule_count}/{selection.total_rules}; "
            f"answer={execution.answer}"
        )
