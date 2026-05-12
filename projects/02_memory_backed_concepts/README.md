# Project 02: Memory-Backed Concepts

This project explores how reasoning systems can store, retrieve, reuse, and update concepts through external memory instead of relying only on model parameters.

The current prototype implements a small deterministic concept memory loop. It loads seed concepts, retrieves relevant concepts from task facts, converts them into recommendations, updates concept confidence after outcomes, and prints inspectable traces.

## Core question

```text
Can concepts be learned, stored, retrieved, reused, and composed without retraining the whole model?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- explicit concept data model
- JSON-backed concept memory
- deterministic concept retrieval
- reasoning adapter
- memory confidence updater
- seed concept memory
- demo tasks
- command-line demo
- tests
- retrieval example documentation

Estimated project status:

```text
65-70% complete
```

## Why this matters

Reasoning depends on reusable concepts.

A deployed agent should not treat every task as isolated. It should remember useful abstractions from previous tasks and apply them when the context is relevant.

For robotics and embodied agents, concept memory can help with:

- object affordances
- task patterns
- safety constraints
- repeated failure cases
- operator preferences
- environment-specific knowledge

Memory-backed concepts give agents continuity without requiring constant retraining.

## Architecture

```text
Task Facts → Concept Memory → Retrieval → Reasoning Adapter → Recommendation → Memory Update
```

The first prototype uses structured task facts and deterministic trigger matching. This keeps the system easy to inspect before adding semantic retrieval or learned representations.

## Components

| File | Role |
|---|---|
| `src/concept.py` | Defines the reusable concept data model |
| `src/memory_store.py` | Loads, saves, searches, and updates concepts |
| `src/retriever.py` | Retrieves relevant concepts and produces retrieval traces |
| `src/adapter.py` | Converts retrieved concept effects into recommendations |
| `src/updater.py` | Updates concept confidence after success or failure |
| `examples/concept_memory.json` | Seed concept memory |
| `examples/demo_tasks.json` | Structured demo tasks with expected outputs |
| `run_demo.py` | Runs retrieval, recommendation, and update loop |
| `tests/test_concept_memory.py` | Regression tests for retrieval and updates |
| `results/retrieval_examples.md` | Documents expected retrieval behavior |

## Seed concepts

The demo starts with five concepts:

| Concept | Trigger examples | Recommended effects |
|---|---|---|
| `concept_fragile_object` | `object_fragile`, `material_glass` | `avoid_high_force`, `slow_motion` |
| `concept_blocked_path` | `path_blocked`, `obstacle_detected` | `select_alternate_path` |
| `concept_unknown_object` | `object_unknown`, `low_object_confidence` | `inspect_before_action` |
| `concept_slippery_surface` | `surface_slippery`, `low_friction_surface` | `increase_stability_check`, `slow_motion` |
| `concept_operator_review_preference` | `operator_prefers_review`, `requires_manual_approval` | `request_manual_review` |

## Demo tasks

| Task | Expected concept behavior | Expected recommendation |
|---|---|---|
| `task_pick_glass_object` | Retrieve fragile object concept | `use_low_force_strategy` |
| `task_blocked_path_replan` | Retrieve blocked path concept | `replan_with_alternate_path` |
| `task_unknown_object_inspection` | Retrieve unknown object concept | `inspect_object_first` |
| `task_slippery_surface` | Retrieve slippery surface and fragile object concepts | `use_low_force_strategy` |
| `task_operator_review` | Retrieve operator review and fragile object concepts | `request_manual_review` |
| `task_no_concept_match` | Retrieve no concepts | `no_concept_recommendation` |

## Concept schema

A minimal concept includes:

```text
concept_id
name
description
trigger_conditions
recommended_effects
confidence
evidence
failure_notes
status
```

Example:

```text
concept_id: concept_fragile_object
name: fragile_object
description: Objects marked fragile or made of glass should be handled with reduced force and slower motion.
trigger_conditions:
  - object_fragile
  - material_glass
recommended_effects:
  - avoid_high_force
  - slow_motion
confidence: 0.85
evidence:
  - seed_manual_rule
failure_notes: []
status: active
```

## Retrieval behavior

The first version uses trigger-condition overlap.

A concept is retrieved when one or more trigger conditions match the task facts. Concepts are ranked by a simple score:

```text
overlap_score × confidence
```

This is deliberately simple. It gives a deterministic baseline before adding embeddings, hybrid retrieval, or learned concept matching.

## Reasoning behavior

Retrieved concepts are converted into recommendations through the reasoning adapter.

Examples:

| Retrieved effect | Recommendation |
|---|---|
| `avoid_high_force` | `use_low_force_strategy` |
| `select_alternate_path` | `replan_with_alternate_path` |
| `inspect_before_action` | `inspect_object_first` |
| `request_manual_review` | `request_manual_review` |

Manual review has priority over other recommendations because it represents a process constraint.

## Memory update behavior

The updater modifies concept confidence after outcomes.

| Outcome | Behavior |
|---|---|
| `success` | Adds evidence and increases confidence |
| `safe` | Adds evidence and increases confidence |
| `correct` | Adds evidence and increases confidence |
| `failure` | Adds failure note and decreases confidence |
| `unsafe` | Adds failure note and decreases confidence |
| `incorrect` | Adds failure note and decreases confidence |

## Run the demo

From the repository root:

```bash
python projects/02_memory_backed_concepts/run_demo.py
```

The demo prints:

- task facts
- expected concepts
- retrieved concepts
- expected recommendation
- actual recommendation
- retrieval trace
- reasoning trace
- update trace
- aggregate match summary

## Run tests

From the repository root:

```bash
python -m pytest projects/02_memory_backed_concepts/tests
```

## Example trace

```text
Task: task_pick_glass_object
Task facts: material_glass, object_light
Retrieved concept_fragile_object: matched [material_glass], score=0.425, confidence=0.85
Recommended effects: avoid_high_force, slow_motion
Recommendation: use_low_force_strategy
Updated concept_fragile_object: success evidence added, confidence=0.88
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Concept match | Did the system retrieve the expected concepts? |
| Recommendation match | Did the system produce the expected recommendation? |
| Trace clarity | Can retrieval and recommendation be inspected? |
| Memory update | Did concept confidence change after outcome? |
| No-match handling | Does the system handle missing concepts explicitly? |

## What this prototype proves

This project does not claim full memory-based reasoning yet.

It proves a smaller operational loop:

```text
retrieved concept → reasoning effect → recommendation → outcome → confidence update
```

That loop is the first working memory-backed abstraction layer for the reasoning stack.

## Current limitations

- Retrieval is deterministic trigger matching.
- No semantic embedding retrieval yet.
- No natural language input yet.
- No persistent write-back to the seed JSON after demo runs.
- No advanced conflict resolution between concepts.
- No connection to Project 01 rule execution yet.
- No robotics integration yet.

## Next steps

1. Run the demo locally and capture actual output.
2. Add persistent memory write-back after updates.
3. Add semantic or hybrid retrieval.
4. Add concept conflict handling.
5. Add more task examples.
6. Connect retrieved concepts to Project 01 rule selection.
7. Add richer result tables.

## Completion target

This project reaches a stronger milestone when it has:

- persistent update behavior
- actual demo output captured in results
- hybrid symbolic + semantic retrieval
- conflict handling
- richer concept examples
- integration with sparse logical reasoning

At that point, Project 02 will move from first prototype to a more serious memory-backed reasoning module.
