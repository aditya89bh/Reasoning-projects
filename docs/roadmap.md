# Roadmap

This roadmap defines the staged build plan for the Reasoning Projects repository.

The repository is currently in the architecture and scaffolding phase. The goal is to move from conceptual clarity to runnable prototypes without turning the repo into scattered experiments.

## Current status

```text
Phase: Early architecture
Target: Structured reasoning-system roadmap
Current priority: Project 01, Sparse Logical Reasoning
```

The immediate goal is not to build every module at once. The immediate goal is to create a clean sequence of reasoning projects that can eventually connect into one coherent stack.

## Roadmap overview

| Phase | Focus | Output | Status |
|---|---|---|---:|
| Phase 0 | Repository structure | README, docs, project folders | In progress |
| Phase 1 | Sparse Logical Reasoning | Runnable sparse reasoning prototype | Planned |
| Phase 2 | Memory-Backed Concepts | External concept memory design + prototype | Planned |
| Phase 3 | Visual-to-Symbolic State | Structured state extraction spec + demo | Planned |
| Phase 4 | Rule Induction | Learn explicit rules from examples | Planned |
| Phase 5 | Integrated Reasoning Stack | Connect state, memory, rules, planning, and evaluation | Future |

## Phase 0: Repository structure

Goal:

Create a clean foundation for the repository.

Deliverables:

- updated `README.md`
- `docs/reasoning_stack.md`
- `docs/design_principles.md`
- `docs/roadmap.md`
- project-level README files
- shared interfaces document
- evaluation document
- reading list

Success criteria:

- A visitor can understand the repo in under five minutes.
- Each project has a clear goal, status, and output.
- The repository does not pretend unfinished work is complete.
- The reasoning stack is clearly defined.

Status:

```text
In progress
```

## Phase 1: Sparse Logical Reasoning

Goal:

Build a minimal reasoning prototype that compares dense and sparse reasoning behavior on logical tasks.

Core question:

```text
What is the smallest active reasoning structure that can still solve the task correctly?
```

Planned components:

- simple logical task dataset
- dense baseline model or rule evaluator
- sparse reasoning module
- activation tracking
- accuracy comparison
- reasoning trace output

Evaluation metrics:

- correctness
- sparsity ratio
- active rule/circuit count
- trace clarity
- latency

Minimum viable demo:

```text
Input logical task → Sparse reasoning path → Answer → Trace → Evaluation
```

Expected output:

- runnable demo
- example tasks
- result table
- short technical note

Status:

```text
Planned
```

## Phase 2: Memory-Backed Concepts

Goal:

Design a system where reusable concepts live in external memory rather than only in model parameters.

Core question:

```text
Can concepts be stored, retrieved, reused, and composed without retraining the whole model?
```

Planned components:

- concept representation format
- concept memory store
- retrieval mechanism
- concept composition examples
- update and forgetting rules

Example concepts:

- fragile object
- blocked path
- safe grasp
- tool affordance
- repeated failure pattern

Minimum viable demo:

```text
Task state → Retrieve relevant concept → Apply concept to reasoning → Produce trace
```

Expected output:

- architecture document
- concept memory schema
- small retrieval prototype
- example traces

Status:

```text
Planned
```

## Phase 3: Visual-to-Symbolic State

Goal:

Convert perceptual or structured scene input into symbolic state that reasoning systems can use.

Core question:

```text
Can perception produce clean symbolic states for downstream reasoning?
```

Planned components:

- object representation
- attribute extraction
- relation extraction
- predicate generation
- confidence scores
- symbolic state schema

Example symbolic state:

```text
object(block_1)
color(block_1, red)
shape(block_1, cube)
left_of(block_1, block_2)
clear(block_1)
```

Minimum viable demo:

```text
Scene input → Objects and relations → SymbolicState → Reasoning-ready output
```

Expected output:

- symbolic state specification
- scene examples
- parser or extraction prototype
- downstream reasoning example

Status:

```text
Planned
```

## Phase 4: Rule Induction

Goal:

Learn explicit rules from examples or experience.

Core question:

```text
Can the system learn rules instead of only learning policies?
```

Planned components:

- example episodes
- candidate rule generator
- rule scoring
- rule memory
- human-readable rule export
- confidence update mechanism

Example induced rule:

```text
If object is fragile and grasp attempt failed, reduce grip force on next attempt.
```

Minimum viable demo:

```text
Examples → Candidate rule → Rule score → Stored rule → Future use
```

Expected output:

- rule induction prototype
- example learned rules
- evaluation notes
- failure cases

Status:

```text
Planned
```

## Phase 5: Integrated Reasoning Stack

Goal:

Connect the individual projects into a unified reasoning loop.

Integrated loop:

```text
Perception → Symbolic State → Concept Memory → Rule System → Planner → Action → Evaluation → Memory Update
```

The integrated system should support:

- symbolic state construction
- concept retrieval
- sparse rule activation
- planning
- trace generation
- evaluation
- memory update

Expected output:

- integrated demo
- architecture diagram
- end-to-end trace
- evaluation table
- robotics-oriented use case

Status:

```text
Future
```

## Near-term priorities

The next concrete work should happen in this order:

1. Complete project-level README files.
2. Add shared interface definitions.
3. Add evaluation criteria.
4. Build Project 01 as a runnable sparse logical reasoning demo.
5. Add examples and result table for Project 01.

## Definition of repo completion

This repository should be considered structurally complete when:

- the reasoning stack is clearly documented
- every project folder has a clear README
- shared interfaces are defined
- evaluation metrics are documented
- Project 01 has a runnable prototype
- the README links to all major docs and projects

That would move the repo from a roadmap to a working research scaffold.

## Completion estimate

Current estimate:

```text
30% complete
```

After Phase 0:

```text
50% complete
```

After Project 01 runnable prototype:

```text
70% complete
```

After integrated stack prototype:

```text
85%+ complete
```
