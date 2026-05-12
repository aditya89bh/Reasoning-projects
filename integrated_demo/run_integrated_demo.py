"""Run the integrated reasoning demo.

Usage:
    python integrated_demo/run_integrated_demo.py

This script connects the four project prototypes:

1. Project 03 builds symbolic state from a structured scene.
2. Project 02 retrieves memory-backed concepts from extracted facts.
3. Project 01 applies sparse logical reasoning rules.
4. Project 04 induces and applies rules from prior episodes.

The demo is intentionally small. Its purpose is to prove the integration path,
not to claim general reasoning.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_01 = REPO_ROOT / "projects" / "01_sparse_logical_reasoning"
PROJECT_02 = REPO_ROOT / "projects" / "02_memory_backed_concepts"
PROJECT_03 = REPO_ROOT / "projects" / "03_visual_symbolic_state"
PROJECT_04 = REPO_ROOT / "projects" / "04_rule_induction"

for project_path in [PROJECT_01, PROJECT_02, PROJECT_03, PROJECT_04]:
    sys.path.insert(0, str(project_path))

# Project 03 imports
from src.scene_loader import SceneLoader  # type: ignore  # noqa: E402
from src.relation_extractor import RelationExtractor  # type: ignore  # noqa: E402
from src.predicate_builder import PredicateBuilder  # type: ignore  # noqa: E402
from src.validator import SymbolicStateValidator  # type: ignore  # noqa: E402

# Clear src namespace collision before importing Project 02 modules.
for module_name in list(sys.modules):
    if module_name == "src" or module_name.startswith("src."):
        del sys.modules[module_name]
sys.path.insert(0, str(PROJECT_02))

# Project 02 imports
from src.memory_store import ConceptMemoryStore  # type: ignore  # noqa: E402
from src.retriever import ConceptRetriever  # type: ignore  # noqa: E402
from src.adapter import ConceptReasoningAdapter  # type: ignore  # noqa: E402

for module_name in list(sys.modules):
    if module_name == "src" or module_name.startswith("src."):
        del sys.modules[module_name]
sys.path.insert(0, str(PROJECT_01))

# Project 01 imports
from src.rules import default_rules  # type: ignore  # noqa: E402
from src.selector import SparseRuleSelector  # type: ignore  # noqa: E402
from src.executor import RuleExecutor  # type: ignore  # noqa: E402
from src.evaluator import ReasoningEvaluator  # type: ignore  # noqa: E402

for module_name in list(sys.modules):
    if module_name == "src" or module_name.startswith("src."):
        del sys.modules[module_name]
sys.path.insert(0, str(PROJECT_04))

# Project 04 imports
from src.episode import Episode  # type: ignore  # noqa: E402
from src.pattern_detector import PatternDetector  # type: ignore  # noqa: E402
from src.rule_generator import RuleGenerator  # type: ignore  # noqa: E402
from src.rule_scorer import RuleScorer  # type: ignore  # noqa: E402
from src.rule_memory import RuleMemory  # type: ignore  # noqa: E402
from src.rule_applier import RuleApplier  # type: ignore  # noqa: E402


SCENE_PATH = PROJECT_03 / "examples" / "sample_scene.json"
CONCEPT_MEMORY_PATH = PROJECT_02 / "examples" / "concept_memory.json"
EPISODES_PATH = PROJECT_04 / "examples" / "episodes.json"


def load_episodes() -> List[Episode]:
    """Load Project 04 episodes."""

    with EPISODES_PATH.open("r", encoding="utf-8") as file:
        raw_episodes = json.load(file)
    return [Episode.from_dict(item) for item in raw_episodes]


def facts_from_symbolic_state(predicates: List[str]) -> List[str]:
    """Convert symbolic predicates into simplified task facts.

    This mapper is intentionally simple. It bridges Project 03 predicate strings
    to the fact labels expected by Projects 01 and 02.
    """

    facts = set()
    for predicate in predicates:
        if predicate == "material(cup_glass, glass)":
            facts.add("material_glass")
        if predicate == "fragile(cup_glass, true)":
            facts.add("object_fragile")

    # Add a task assumption for the integrated scenario.
    facts.add("grip_force_high")
    return sorted(facts)


def build_symbolic_state() -> Dict:
    """Run Project 03 scene-to-symbolic-state conversion."""

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

    return {
        "state": state,
        "validation": validation,
        "facts": facts_from_symbolic_state(state.predicates),
        "trace": [
            f"Built symbolic state: {state.state_id}",
            f"Objects: {len(state.objects)}",
            f"Relations: {len(state.relations)}",
            f"Predicates: {len(state.predicates)}",
            f"Validation passed: {validation.valid}",
        ],
    }


def run_concept_memory(task_facts: List[str]) -> Dict:
    """Run Project 02 concept retrieval and recommendation."""

    store = ConceptMemoryStore.from_json(CONCEPT_MEMORY_PATH)
    retrieval = ConceptRetriever(store).retrieve(
        task_id="integrated_fragile_object_task",
        task_facts=task_facts,
    )
    reasoning = ConceptReasoningAdapter().adapt(retrieval)

    return {
        "retrieval": retrieval,
        "reasoning": reasoning,
        "trace": retrieval.trace + reasoning.trace,
    }


def run_sparse_reasoning(task_facts: List[str]) -> Dict:
    """Run Project 01 sparse logical reasoning."""

    rules = default_rules()
    selection = SparseRuleSelector(rules).select(task_facts)
    execution = RuleExecutor().execute("integrated_fragile_object_task", selection)
    evaluation = ReasoningEvaluator().evaluate("action_unsafe", execution, selection)

    return {
        "selection": selection,
        "execution": execution,
        "evaluation": evaluation,
        "trace": execution.trace,
    }


def run_rule_induction(task_facts: List[str]) -> Dict:
    """Run Project 04 rule induction and future rule application."""

    episodes = load_episodes()
    patterns = PatternDetector(min_count=2).detect(episodes)
    candidate_rules = RuleGenerator().generate(patterns)
    scored_rules = RuleScorer().score(candidate_rules, episodes)
    memory = RuleMemory(scored_rules)
    application = RuleApplier(memory).apply(
        task_id="integrated_fragile_object_task",
        facts=task_facts,
        accepted_only=False,
    )

    return {
        "patterns": patterns,
        "rules": scored_rules,
        "application": application,
        "trace": application.trace,
    }


def main() -> None:
    """Run the integrated demo."""

    symbolic = build_symbolic_state()
    task_facts = symbolic["facts"]
    concept = run_concept_memory(task_facts)
    sparse = run_sparse_reasoning(task_facts)
    induced = run_rule_induction(task_facts)

    print("=" * 72)
    print("Integrated Reasoning Demo")
    print("=" * 72)

    print("\n[1] Symbolic state")
    for step in symbolic["trace"]:
        print(f" - {step}")
    print(f"Task facts: {task_facts}")

    print("\n[2] Concept memory")
    print(f"Retrieved concepts: {concept['reasoning'].retrieved_concept_ids}")
    print(f"Concept recommendation: {concept['reasoning'].recommendation}")

    print("\n[3] Sparse rule reasoning")
    print(f"Answer: {sparse['execution'].answer}")
    print(f"Correct: {sparse['evaluation'].correct}")
    print(
        f"Active rules: {sparse['selection'].active_rule_count}/{sparse['selection'].total_rules}"
    )

    print("\n[4] Rule induction")
    print(f"Detected patterns: {len(induced['patterns'])}")
    print(f"Generated rules: {len(induced['rules'])}")
    print(f"Applied induced rule recommendation: {induced['application'].recommendation}")

    print("\nFinal integrated trace")
    final_trace = []
    final_trace.extend(symbolic["trace"])
    final_trace.append(f"Mapped symbolic predicates to task facts: {task_facts}")
    final_trace.append(f"Retrieved concepts: {concept['reasoning'].retrieved_concept_ids}")
    final_trace.append(f"Concept recommendation: {concept['reasoning'].recommendation}")
    final_trace.append(f"Sparse reasoning answer: {sparse['execution'].answer}")
    final_trace.append(f"Sparse reasoning correct: {sparse['evaluation'].correct}")
    final_trace.append(f"Induced rule recommendation: {induced['application'].recommendation}")

    for step in final_trace:
        print(f" - {step}")


if __name__ == "__main__":
    main()
