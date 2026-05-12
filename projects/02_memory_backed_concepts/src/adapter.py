"""Reasoning adapter for memory-backed concepts.

The adapter converts retrieved concepts into a compact reasoning recommendation.
It is the bridge between concept retrieval and downstream decision-making.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .retriever import RetrievalResult


@dataclass(frozen=True)
class ConceptReasoningResult:
    """Reasoning result produced from retrieved concepts."""

    task_id: str
    retrieved_concept_ids: List[str]
    recommended_effects: List[str]
    recommendation: str
    trace: List[str]

    def as_dict(self) -> Dict:
        """Return a compact serializable representation."""

        return {
            "task_id": self.task_id,
            "retrieved_concept_ids": list(self.retrieved_concept_ids),
            "recommended_effects": list(self.recommended_effects),
            "recommendation": self.recommendation,
            "trace": list(self.trace),
        }


class ConceptReasoningAdapter:
    """Apply retrieved concepts to produce a reasoning recommendation."""

    def adapt(self, retrieval: RetrievalResult) -> ConceptReasoningResult:
        """Convert retrieved concepts into a recommendation."""

        effects = retrieval.recommended_effects
        recommendation = self._derive_recommendation(effects)
        trace = self._build_trace(retrieval, effects, recommendation)

        return ConceptReasoningResult(
            task_id=retrieval.task_id,
            retrieved_concept_ids=retrieval.concept_ids,
            recommended_effects=effects,
            recommendation=recommendation,
            trace=trace,
        )

    def _derive_recommendation(self, effects: List[str]) -> str:
        """Derive one compact recommendation from recommended effects."""

        if "request_manual_review" in effects:
            return "request_manual_review"
        if "avoid_high_force" in effects:
            return "use_low_force_strategy"
        if "select_alternate_path" in effects:
            return "replan_with_alternate_path"
        if "inspect_before_action" in effects:
            return "inspect_object_first"
        if "slow_motion" in effects:
            return "use_slow_motion"
        if "increase_stability_check" in effects:
            return "perform_stability_check"
        if effects:
            return effects[0]
        return "no_concept_recommendation"

    def _build_trace(
        self,
        retrieval: RetrievalResult,
        effects: List[str],
        recommendation: str,
    ) -> List[str]:
        """Build an inspectable trace for concept-guided reasoning."""

        trace = [
            f"Task: {retrieval.task_id}",
            f"Retrieved concepts: {', '.join(retrieval.concept_ids) if retrieval.concept_ids else 'none'}",
        ]

        if not retrieval.concept_ids:
            trace.append("No concept effects applied.")
            trace.append("Recommendation: no_concept_recommendation")
            return trace

        trace.append(f"Applied effects: {', '.join(effects) if effects else 'none'}")
        trace.append(f"Recommendation: {recommendation}")
        return trace
