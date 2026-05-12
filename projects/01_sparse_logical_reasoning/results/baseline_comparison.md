# Baseline Comparison

This document summarizes the expected behavior of the sparse logical reasoning prototype compared with the dense baseline.

The prototype compares two paths:

| Path | Behavior |
|---|---|
| Sparse | Selects only rules whose conditions match the input facts |
| Dense baseline | Selects all rules, then lets the executor filter matching rules |

The dense baseline exists to make sparse activation measurable. It is not meant to be an optimized reasoning system.

## Demo tasks

The demo uses seven structured logical tasks.

| Task | Facts | Expected answer |
|---|---|---|
| `task_fragile_high_force` | `object_fragile`, `grip_force_high` | `action_unsafe` |
| `task_fragile_low_force` | `object_fragile`, `grip_force_low` | `action_safe` |
| `task_blocked_path` | `path_blocked` | `needs_replan` |
| `task_unknown_object` | `object_unknown` | `inspect_object` |
| `task_manual_review` | `operator_prefers_review` | `request_manual_review` |
| `task_heavy_object` | `object_heavy` | `use_slow_speed` |
| `task_no_match` | `object_light`, `grip_force_medium` | `no_rule_matched` |

## Expected comparison

The default rule set contains 8 rules.

For most tasks, the sparse path should activate only 1 matching rule. The dense baseline selects all 8 rules before execution filters down to matches.

| Task | Sparse active rules | Dense selected rules | Expected correctness |
|---|---:|---:|---:|
| `task_fragile_high_force` | 1/8 | 8/8 | true |
| `task_fragile_low_force` | 1/8 | 8/8 | true |
| `task_blocked_path` | 1/8 | 8/8 | true |
| `task_unknown_object` | 1/8 | 8/8 | true |
| `task_manual_review` | 1/8 | 8/8 | true |
| `task_heavy_object` | 1/8 | 8/8 | true |
| `task_no_match` | 0/8 | 8/8 | true |

## Expected summary

| Path | Expected accuracy | Expected average sparsity ratio |
|---|---:|---:|
| Sparse | 1.0 | ~0.107 |
| Dense baseline | 1.0 | 1.0 |

The sparse path should preserve correctness while activating far fewer rules.

## Why this matters

The point is not that this toy prototype is intelligent. The point is that it creates a measurable reasoning loop:

```text
input facts → rule selection → execution → answer → trace → evaluation
```

That loop can later be expanded into richer reasoning tasks.

## Example sparse trace

```text
Task: task_fragile_high_force
Input facts: object_fragile, grip_force_high
Activated rule_fragile_high_force_unsafe: conditions [grip_force_high, object_fragile] -> effect [action_unsafe]
Inferred effects: action_unsafe
Answer: action_unsafe
```

## Example dense trace

The dense baseline selects all rules, but the executor only applies rules whose conditions match.

```text
Task: task_fragile_high_force
Input facts: object_fragile, grip_force_high
Activated rule_fragile_high_force_unsafe: conditions [grip_force_high, object_fragile] -> effect [action_unsafe]
Inferred effects: action_unsafe
Answer: action_unsafe
```

The final answer can be the same, but the selected rule count is different.

## Evaluation meaning

A successful first milestone means:

- all demo tasks return the expected answer
- sparse path activates fewer rules than dense baseline
- traces are generated for every task
- no-match behavior is explicit
- tests cover the main reasoning paths

## Next result artifact

After running the demo locally, this file can be updated with actual measured output from:

```bash
python projects/01_sparse_logical_reasoning/run_demo.py
```

For now, this document records the expected baseline comparison for the initial prototype.
