"""Tests for the rule induction prototype.

Run from the repository root with:
    python -m pytest projects/04_rule_induction/tests
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.episode import Episode
from src.pattern_detector import PatternDetector
from src.rule_applier import RuleApplier
from src.rule_generator import RuleGenerator
from src.rule_memory import RuleMemory
from src.rule_scorer import RuleScorer


def sample_episodes():
    return [
        Episode(
            episode_id="ep_001",
            facts=["object_fragile", "grip_force_high"],
            action="high_force_grasp",
            outcome="failure",
        ),
        Episode(
            episode_id="ep_002",
            facts=["object_fragile", "material_glass", "grip_force_high"],
            action="high_force_grasp",
            outcome="failure",
        ),
        Episode(
            episode_id="ep_003",
            facts=["object_fragile", "grip_force_low"],
            action="low_force_grasp",
            outcome="success",
        ),
        Episode(
            episode_id="ep_004",
            facts=["material_glass", "grip_force_low"],
            action="low_force_grasp",
            outcome="success",
        ),
        Episode(
            episode_id="ep_005",
            facts=["path_blocked", "target_visible"],
            action="direct_path_plan",
            outcome="failure",
        ),
        Episode(
            episode_id="ep_006",
            facts=["path_blocked", "obstacle_detected"],
            action="direct_path_plan",
            outcome="failure",
        ),
    ]


def test_episode_success_and_failure_flags():
    success = Episode("ep_success", ["object_fragile"], "low_force_grasp", "success")
    failure = Episode("ep_failure", ["object_fragile"], "high_force_grasp", "failure")

    assert success.is_success is True
    assert success.is_failure is False
    assert failure.is_failure is True
    assert failure.is_success is False
    assert failure.contains_fact("object_fragile") is True


def test_pattern_detector_finds_repeated_patterns():
    patterns = PatternDetector(min_count=2).detect(sample_episodes())
    pattern_keys = {(pattern.fact, pattern.action, pattern.outcome) for pattern in patterns}

    assert ("object_fragile", "high_force_grasp", "failure") in pattern_keys
    assert ("grip_force_high", "high_force_grasp", "failure") in pattern_keys
    assert ("path_blocked", "direct_path_plan", "failure") in pattern_keys


def test_rule_generator_creates_candidate_rules_from_patterns():
    patterns = PatternDetector(min_count=2).detect(sample_episodes())
    rules = RuleGenerator().generate(patterns)

    assert rules
    assert all(rule.status == "candidate" for rule in rules)
    assert any(rule.effect == "avoid_high_force_grasp" for rule in rules)
    assert any(rule.effect == "avoid_direct_path_plan" for rule in rules)


def test_rule_scorer_scores_and_accepts_useful_rules():
    episodes = sample_episodes()
    patterns = PatternDetector(min_count=2).detect(episodes)
    candidate_rules = RuleGenerator().generate(patterns)
    scored_rules = RuleScorer().score(candidate_rules, episodes)

    fragile_rules = [
        rule
        for rule in scored_rules
        if rule.conditions == ["object_fragile"] and rule.effect == "avoid_high_force_grasp"
    ]

    assert fragile_rules
    assert fragile_rules[0].confidence > 0
    assert fragile_rules[0].precision >= 0.5
    assert fragile_rules[0].coverage > 0


def test_rule_memory_stores_and_finds_matching_rules():
    episodes = sample_episodes()
    patterns = PatternDetector(min_count=2).detect(episodes)
    rules = RuleScorer().score(RuleGenerator().generate(patterns), episodes)

    memory = RuleMemory()
    memory.add_many(rules)

    assert len(memory) == len(rules)
    assert memory.list_rules()

    matches = memory.find_matching(["object_fragile", "grip_force_high"], accepted_only=False)
    assert matches
    assert any(rule.effect == "avoid_high_force_grasp" for rule in matches)


def test_rule_applier_returns_recommendation_for_future_task():
    episodes = sample_episodes()
    patterns = PatternDetector(min_count=2).detect(episodes)
    rules = RuleScorer().score(RuleGenerator().generate(patterns), episodes)

    memory = RuleMemory()
    memory.add_many(rules)

    result = RuleApplier(memory).apply(
        task_id="future_fragile_high_force",
        facts=["object_fragile", "grip_force_high"],
        accepted_only=False,
    )

    assert "avoid_high_force_grasp" in result.effects
    assert result.recommendation == "avoid_high_force_grasp"
    assert any("Matched" in step for step in result.trace)


def test_rule_applier_handles_no_match():
    memory = RuleMemory()
    result = RuleApplier(memory).apply(
        task_id="future_no_match",
        facts=["object_standard", "path_clear"],
    )

    assert result.matched_rule_ids == []
    assert result.recommendation == "no_rule_recommendation"
    assert any("No induced rules matched" in step for step in result.trace)
