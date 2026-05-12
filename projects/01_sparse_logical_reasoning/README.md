# Project 01: Sparse Logical Reasoning

This project explores whether logical reasoning can be performed with minimal active structure instead of dense, opaque activation.

The current prototype compares sparse rule activation against a dense baseline on simple logical tasks. The system is intentionally small, explicit, and inspectable.

## Core question

```text
What is the smallest active reasoning structure that can still solve the task correctly?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- explicit rule definitions
- sparse rule selector
- dense baseline selector
- rule executor
- evaluator
- demo tasks
- command-line demo
- tests
- baseline comparison notes

Estimated project status:

```text
70% complete
```

## Why this matters

Reasoning systems should not activate every rule, feature, or representation for every problem.

For real-world deployment, especially in robotics and embodied agents, reasoning needs to be:

- efficient
- inspectable
- modular
- traceable
- robust under constraints

Sparse logical reasoning is the first technical proof in this repository.

## Architecture

```text
Task Facts → Rule Selection → Rule Execution → Answer → Trace → Evaluation
```

The prototype has two reasoning paths:

| Path | Behavior |
|---|---|
| Sparse | Selects only rules whose conditions match the input facts |
| Dense baseline | Selects all rules, then lets the executor filter matching rules |

## Components

| File | Role |
|---|---|
| `src/rules.py` | Defines explicit symbolic rules and the default rule set |
| `src/selector.py` | Implements sparse and dense rule selection |
| `src/executor.py` | Applies selected rules and generates answers plus traces |
| `src/evaluator.py` | Checks correctness, sparsity ratio, and trace clarity |
| `examples/demo_tasks.json` | Contains structured demo tasks and expected answers |
| `run_demo.py` | Runs sparse vs dense comparison from the command line |
| `tests/test_sparse_reasoning.py` | Regression tests for core reasoning behavior |
| `results/baseline_comparison.md` | Documents expected sparse vs dense behavior |

## Rule set

The default prototype includes 8 rules:

| Rule | Effect |
|---|---|
| Fragile object + high force | `action_unsafe` |
| Fragile object + low force | `action_safe` |
| Blocked path | `needs_replan` |
| Clear path | `continue_plan` |
| Heavy object | `use_slow_speed` |
| Slippery surface | `increase_stability_check` |
| Operator prefers review | `request_manual_review` |
| Unknown object | `inspect_object` |

## Demo tasks

The demo currently includes 7 tasks:

| Task | Expected answer |
|---|---|
| `task_fragile_high_force` | `action_unsafe` |
| `task_fragile_low_force` | `action_safe` |
| `task_blocked_path` | `needs_replan` |
| `task_unknown_object` | `inspect_object` |
| `task_manual_review` | `request_manual_review` |
| `task_heavy_object` | `use_slow_speed` |
| `task_no_match` | `no_rule_matched` |

## Run the demo

From the repository root:

```bash
python projects/01_sparse_logical_reasoning/run_demo.py
```

The demo prints:

- sparse path result
- dense baseline result
- expected answer
- actual answer
- active rule count
- sparsity ratio
- reasoning trace
- summary comparison

## Run tests

From the repository root:

```bash
python -m pytest projects/01_sparse_logical_reasoning/tests
```

## Example trace

```text
Task: task_fragile_high_force
Input facts: object_fragile, grip_force_high
Activated rule_fragile_high_force_unsafe: conditions [grip_force_high, object_fragile] -> effect [action_unsafe]
Inferred effects: action_unsafe
Answer: action_unsafe
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Accuracy | Did the system produce the correct answer? |
| Active rule count | How many rules were activated? |
| Sparsity ratio | Active rules divided by total available rules |
| Trace clarity | Can the reasoning path be understood? |

Expected first comparison:

| Path | Expected accuracy | Expected average sparsity ratio |
|---|---:|---:|
| Sparse | 1.0 | ~0.107 |
| Dense baseline | 1.0 | 1.0 |

The sparse path should preserve correctness while activating far fewer rules.

## What this prototype proves

This project does not claim general reasoning ability yet.

It proves a smaller, useful loop:

```text
input facts → relevant rule selection → answer → trace → evaluation
```

That loop can be extended into richer symbolic state, memory-backed concepts, rule induction, and planning.

## Current limitations

- Rules are hand-written.
- Task facts are structured manually.
- No learned rule induction yet.
- No concept memory yet.
- No natural language interface yet.
- No robotics integration yet.
- Dense baseline is intentionally simple.

## Next steps

1. Run the demo locally and update `results/baseline_comparison.md` with actual output.
2. Add a small result table generated from the demo run.
3. Add more tasks involving multiple simultaneous facts.
4. Add conflict handling between rules.
5. Add simple latency measurement.
6. Connect this project to Project 02: Memory-Backed Concepts.

## Completion target

This project reaches a stronger milestone when it has:

- demo output captured in results
- more multi-rule tasks
- conflict tests
- latency measurement
- richer baseline comparison
- cleaner packaging for external readers

At that point, Project 01 will move from first runnable prototype to polished technical proof.
