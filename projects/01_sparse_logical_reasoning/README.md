# Project 01: Sparse Logical Reasoning

This project explores whether logical reasoning can be performed with minimal active structure instead of dense, opaque activation.

The goal is to build a small runnable prototype that compares dense reasoning behavior with sparse reasoning behavior on simple logical tasks.

## Core question

```text
What is the smallest active reasoning structure that can still solve the task correctly?
```

## Why this matters

Reasoning systems should not activate every rule, feature, or representation for every problem.

For real-world deployment, especially in robotics and embodied agents, reasoning needs to be:

- efficient
- inspectable
- modular
- traceable
- robust under constraints

Sparse logical reasoning is the first step toward that direction.

## Project goal

Build a minimal system that can:

1. Receive a logical task.
2. Select only the relevant reasoning path.
3. Produce an answer.
4. Show the active reasoning trace.
5. Compare sparse behavior against a dense baseline.

## Initial task types

The first prototype should use simple logical tasks before moving to richer reasoning.

Possible task types:

| Task type | Example |
|---|---|
| Boolean logic | `A AND B` |
| Rule matching | `if fragile then reduce_force` |
| Predicate reasoning | `red(block_1) and cube(block_1)` |
| Relation reasoning | `left_of(a, b)` and `left_of(b, c)` implies `left_of(a, c)` |
| Constraint checking | `action is unsafe if object is fragile and grip force is high` |

## Minimal architecture

```text
Task Input → Candidate Rules → Sparse Rule Selection → Execution → Answer → Trace → Evaluation
```

## Components

| Component | Role |
|---|---|
| Task input | Defines the logical problem to solve |
| Rule set | Contains available rules or logical operations |
| Sparse selector | Chooses only relevant rules |
| Executor | Applies selected rules |
| Trace generator | Records the reasoning path |
| Evaluator | Checks correctness, sparsity, and trace quality |

## Dense baseline

The dense baseline should apply all available rules or evaluate all possible reasoning paths.

Purpose:

```text
Show what happens when the system does not selectively activate reasoning structure.
```

Expected behavior:

- more active rules
- more unnecessary computation
- less clean trace
- same or similar answer on simple tasks

## Sparse reasoning prototype

The sparse version should activate only the rules relevant to the current task.

Expected behavior:

- fewer active rules
- clearer trace
- same correct answer
- better interpretability

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Accuracy | Did the system produce the correct answer? |
| Active rule count | How many rules were activated? |
| Sparsity ratio | Active rules divided by total available rules |
| Trace clarity | Can the reasoning path be understood? |
| Latency | How long did execution take? |

## Minimum viable demo

The first demo should run from the command line.

Example target behavior:

```text
Input task:
object is fragile and grip force is high

Selected rules:
- fragile_object_rule
- high_force_risk_rule

Answer:
action is unsafe

Trace:
1. Detected fragile object
2. Detected high grip force
3. Activated safety constraint
4. Classified action as unsafe

Evaluation:
correct=true
active_rules=2
total_rules=6
sparsity_ratio=0.33
```

## Planned file structure

```text
projects/01_sparse_logical_reasoning/
├── README.md
├── src/
│   ├── rules.py
│   ├── selector.py
│   ├── executor.py
│   └── evaluator.py
├── examples/
│   └── demo_tasks.json
├── tests/
│   └── test_sparse_reasoning.py
└── results/
    └── baseline_comparison.md
```

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define the interface, task format, and evaluation criteria before writing the prototype.

## Next steps

1. Define the task input schema.
2. Define the rule representation.
3. Create dense baseline evaluator.
4. Create sparse rule selector.
5. Add command-line demo.
6. Add tests.
7. Add result table comparing dense vs sparse reasoning.

## Completion target

This project reaches a useful first milestone when it has:

- runnable demo
- at least 5 logical tasks
- dense vs sparse comparison
- reasoning trace output
- basic tests
- result table

At that point, Project 01 becomes the first working technical proof for the repository.
