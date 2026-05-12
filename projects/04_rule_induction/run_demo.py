"""Run the rule induction demo.

Usage:
    python projects/04_rule_induction/run_demo.py

The demo loads structured episodes, detects repeated patterns, generates
candidate rules, scores them, stores them in rule memory, and applies accepted
rules to future task facts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.episode import Episode
from src.pattern_detector import PatternDetector
from src.rule_applier import RuleApplier
from src.rule_generator import RuleGenerator
from src.rule_memory import RuleMemory
from src.rule_scorer import RuleScorer


PROJECT_DIR = Path(__file__).resolve().parent
EPISODES_PATH = PROJECT_DIR / "examples" / "episodes.json"


def load_episodes(path: Path = EPISODES_PATH) -> List[Episode]:
    """Load structured episodes from JSON."""

    with path.open("r", encoding="utf-8") as file:
        raw_episodes = json.load(file)
    return [Episode.from_dict(item) for item in raw_episodes]


def future_tasks() -> List[Dict]:
    """Return future tasks used to test induced rules."""

    return [
        {
            "task_id": "future_fragile_high_force",
            "facts": ["object_fragile", "grip_force_high"],
            "expected_recommendation": "avoid_high_force_grasp",
        },
        {
            "task_id": "future_blocked_path",
            "facts": ["path_blocked", "target_visible"],
            "expected_recommendation": "avoid_direct_path_plan",
        },
        {
            "task_id": "future_operator_review",
            "facts": ["operator_prefers_review", "task_sensitive"],
            "expected_recommendation": "prefer_manual_review",
        },
        {
            "task_id": "future_no_match",
            "facts": ["object_standard", "path_clear"],
            "expected_recommendation": "no_rule_recommendation",
        },
    ]


def print_patterns(patterns) -> None:
    """Print detected patterns."""

    print("\n" + "=" * 72)
    print("Detected patterns")
    print("=" * 72)
    for pattern in patterns:
        print(
            f"{pattern.pattern_id}: fact={pattern.fact}, action={pattern.action}, "
            f"outcome={pattern.outcome}, count={pattern.count}, episodes={pattern.episode_ids}"
        )


def print_rules(rules) -> None:
    """Print scored induced rules."""

    print("\n" + "=" * 72)
    print("Scored rules")
    print("=" * 72)
    for rule in rules:
        print(
            f"{rule.rule_id}: {rule.name} | effect={rule.effect} | "
            f"confidence={rule.confidence} | coverage={rule.coverage} | "
            f"precision={rule.precision} | status={rule.status}"
        )


def run_future_tasks(rule_memory: RuleMemory) -> List[Dict]:
    """Apply accepted rules to future tasks."""

    applier = RuleApplier(rule_memory)
    results: List[Dict] = []

    print("\n" + "=" * 72)
    print("Future task application")
    print("=" * 72)

    for task in future_tasks():
        result = applier.apply(task_id=task["task_id"], facts=task["facts"])
        matched = result.recommendation == task["expected_recommendation"]

        print(f"\nTask: {task['task_id']}")
        print(f"Facts: {task['facts']}")
        print(f"Expected: {task['expected_recommendation']}")
        print(f"Recommendation: {result.recommendation}")
        print(f"Matched expected: {matched}")
        print("Trace:")
        for step in result.trace:
            print(f" - {step}")

        row = result.as_dict()
        row["expected_recommendation"] = task["expected_recommendation"]
        row["matched_expected"] = matched
        results.append(row)

    return results


def print_summary(results: List[Dict]) -> None:
    """Print compact future-task summary."""

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)

    for result in results:
        print(
            f"{result['task_id']:<28} | "
            f"recommendation={result['recommendation']:<28} | "
            f"matched={result['matched_expected']}"
        )

    if results:
        accuracy = sum(result["matched_expected"] for result in results) / len(results)
        print(f"\nfuture_task_recommendation_accuracy={accuracy:.3f}")


def main() -> None:
    """Run the full rule induction demo."""

    episodes = load_episodes()
    patterns = PatternDetector(min_count=2).detect(episodes)
    candidate_rules = RuleGenerator().generate(patterns)
    scored_rules = RuleScorer().score(candidate_rules, episodes)

    rule_memory = RuleMemory()
    rule_memory.add_many(scored_rules)

    print(f"Loaded episodes: {len(episodes)}")
    print_patterns(patterns)
    print_rules(scored_rules)
    print(f"\nAccepted rules: {len(rule_memory.accepted_rules())}")
    print(f"Candidate rules: {len(rule_memory.candidate_rules())}")

    results = run_future_tasks(rule_memory)
    print_summary(results)


if __name__ == "__main__":
    main()
