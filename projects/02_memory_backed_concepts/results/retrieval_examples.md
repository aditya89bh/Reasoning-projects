# Retrieval Examples

This document summarizes the expected behavior of the memory-backed concepts prototype.

The prototype demonstrates a small concept memory loop:

```text
Task facts → Concept retrieval → Reasoning recommendation → Outcome update → Concept memory change
```

The goal is not to build a full memory system yet. The goal is to make concept reuse explicit, inspectable, and testable.

## Seed concept memory

The demo starts with five seed concepts.

| Concept | Trigger examples | Recommended effects |
|---|---|---|
| `concept_fragile_object` | `object_fragile`, `material_glass` | `avoid_high_force`, `slow_motion` |
| `concept_blocked_path` | `path_blocked`, `obstacle_detected` | `select_alternate_path` |
| `concept_unknown_object` | `object_unknown`, `low_object_confidence` | `inspect_before_action` |
| `concept_slippery_surface` | `surface_slippery`, `low_friction_surface` | `increase_stability_check`, `slow_motion` |
| `concept_operator_review_preference` | `operator_prefers_review`, `requires_manual_approval` | `request_manual_review` |

## Demo tasks

| Task | Facts | Expected concepts | Expected recommendation |
|---|---|---|---|
| `task_pick_glass_object` | `material_glass`, `object_light` | `concept_fragile_object` | `use_low_force_strategy` |
| `task_blocked_path_replan` | `path_blocked`, `object_target_visible` | `concept_blocked_path` | `replan_with_alternate_path` |
| `task_unknown_object_inspection` | `object_unknown`, `workspace_clear` | `concept_unknown_object` | `inspect_object_first` |
| `task_slippery_surface` | `surface_slippery`, `object_fragile` | `concept_slippery_surface`, `concept_fragile_object` | `use_low_force_strategy` |
| `task_operator_review` | `operator_prefers_review`, `object_fragile` | `concept_operator_review_preference`, `concept_fragile_object` | `request_manual_review` |
| `task_no_concept_match` | `object_standard`, `path_clear` | none | `no_concept_recommendation` |

## Expected behavior

The system should:

1. Load seed concepts from `examples/concept_memory.json`.
2. Load demo tasks from `examples/demo_tasks.json`.
3. Retrieve concepts whose trigger conditions match task facts.
4. Convert retrieved concept effects into a recommendation.
5. Update concept confidence after the task outcome.
6. Print retrieval, reasoning, and update traces.

## Example 1: Glass object

Input task:

```text
task_pick_glass_object
facts: material_glass, object_light
```

Expected retrieval:

```text
concept_fragile_object
```

Expected recommendation:

```text
use_low_force_strategy
```

Expected trace:

```text
Task: task_pick_glass_object
Task facts: material_glass, object_light
Retrieved concept_fragile_object: matched [material_glass], score=0.425, confidence=0.85
Recommended effects: avoid_high_force, slow_motion
Recommendation: use_low_force_strategy
```

Expected update:

```text
Outcome: success
Updated concept_fragile_object: success evidence added
confidence increases
```

## Example 2: Blocked path

Input task:

```text
task_blocked_path_replan
facts: path_blocked, object_target_visible
```

Expected retrieval:

```text
concept_blocked_path
```

Expected recommendation:

```text
replan_with_alternate_path
```

Expected reasoning:

```text
path_blocked → retrieve blocked_path concept → select alternate path
```

## Example 3: Operator review

Input task:

```text
task_operator_review
facts: operator_prefers_review, object_fragile
```

Expected retrieval:

```text
concept_operator_review_preference
concept_fragile_object
```

Expected recommendation:

```text
request_manual_review
```

Reason:

Manual review has priority over low-force handling. The system should not only optimize the action. It should respect the process constraint.

## Example 4: No concept match

Input task:

```text
task_no_concept_match
facts: object_standard, path_clear
```

Expected retrieval:

```text
none
```

Expected recommendation:

```text
no_concept_recommendation
```

Expected trace:

```text
No concepts retrieved.
No concept effects applied.
Recommendation: no_concept_recommendation
```

This makes non-retrieval explicit rather than silently failing.

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Concept match | Did the system retrieve the expected concepts? |
| Recommendation match | Did the system produce the expected recommendation? |
| Trace clarity | Can retrieval and recommendation be inspected? |
| Memory update | Did concept confidence change after outcome? |
| No-match handling | Does the system handle missing concepts explicitly? |

## Expected aggregate result

| Metric | Expected value |
|---|---:|
| Concept match accuracy | high for seed demo tasks |
| Recommendation match accuracy | high for seed demo tasks |
| Retrieval trace coverage | 100% |
| Reasoning trace coverage | 100% |
| Update trace coverage | 100% |

## Why this matters

This prototype makes memory operational.

Instead of treating memory as passive storage, the loop shows how memory can influence behavior:

```text
retrieved concept → reasoning effect → recommendation → outcome → confidence update
```

That is the smallest useful memory-backed reasoning loop.

## Run command

From the repository root:

```bash
python projects/02_memory_backed_concepts/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/02_memory_backed_concepts/tests
```

## Current limitation

The demo uses deterministic trigger matching. It does not yet support embeddings, semantic retrieval, natural language input, advanced conflict resolution, or persistent updates back to the JSON file after the demo run.

Those are future improvements. The current value is clarity.
