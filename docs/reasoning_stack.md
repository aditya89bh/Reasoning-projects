# Reasoning Stack

This document defines the working architecture behind the Reasoning Projects repository.

The goal is to describe a reasoning system that is sparse, memory-backed, structured, and useful for embodied agents. The system is not designed as a single monolithic model. It is designed as a stack of interacting layers.

## Core stack

```text
Perception → Symbolic State → Concept Memory → Rule System → Planner → Action → Evaluation
```

Each layer has a specific responsibility. The system becomes useful when the layers communicate through explicit interfaces rather than hidden latent behavior alone.

## Why a stack is needed

Most modern AI systems are strong at pattern recognition and generation. They are weaker at durable reasoning because many internal steps remain implicit.

A reasoning system for real-world agents needs to answer questions like:

- What is the current state of the world?
- Which objects, concepts, or rules matter right now?
- What constraints apply?
- What action should be selected?
- Why was that action selected?
- What should change after success or failure?

The stack exists to make these steps explicit.

## Layer 1: Perception

Perception receives raw or structured input from the environment.

Possible inputs:

- images
- sensor data
- text
- robot state
- object detections
- structured scene data

In early projects, this layer may use simple structured inputs rather than real perception models. That is acceptable. The first goal is not visual complexity. The first goal is reasoning clarity.

Output:

```text
observations
```

## Layer 2: Symbolic State

The symbolic state layer converts observations into explicit objects, attributes, relations, and predicates.

Example:

```text
object(block_1)
color(block_1, red)
shape(block_1, cube)
left_of(block_1, block_2)
clear(block_1)
```

This layer gives the reasoning system something structured to operate on.

Output:

```text
SymbolicState
```

A minimal symbolic state should include:

- objects
- attributes
- relations
- predicates
- confidence values where needed
- timestamp or episode identifier

## Layer 3: Concept Memory

Concept memory stores reusable concepts outside model weights.

The purpose is to avoid relearning every concept from scratch. Concepts should be retrievable, composable, and inspectable.

Examples:

- fragile object
- blocked path
- successful grasp pattern
- unsafe motion region
- reusable tool affordance

Concept memory should support:

- retrieval by similarity
- retrieval by symbolic constraints
- concept composition
- updating from new experience
- forgetting or compression over time

Output:

```text
RelevantConcepts
```

## Layer 4: Rule System

The rule system applies explicit rules, constraints, and logical relations.

Rules can be hand-written at first. Later, they can be induced from examples or experience.

Example rules:

```text
if object_is_fragile(x) then reduce_grip_force(x)
if target_is_blocked(x) then search_alternate_path(x)
if relation(left_of(a, b)) and relation(left_of(b, c)) then infer(left_of(a, c))
```

The rule system should not activate everything at once. It should use sparse activation: only relevant rules should fire for the current state.

Output:

```text
RuleActivations
```

## Layer 5: Planner

The planner converts the current symbolic state, retrieved concepts, and active rules into a sequence of reasoning or action steps.

A planner should answer:

- What is the goal?
- What steps are needed?
- Which constraints apply?
- Which strategy should be used?
- What can fail?
- What should be checked after each step?

Output:

```text
Plan
```

A minimal plan should include:

- goal
- steps
- selected strategy
- assumptions
- constraints
- success criteria
- failure conditions

## Layer 6: Action

The action layer executes or simulates the plan.

In early prototypes, action can be simulated. In robotics, action may connect to motion planning, robot control, or a task-level API.

Examples:

- answer a reasoning question
- execute a symbolic operation
- move an object
- call a robot skill
- run a planning step

Output:

```text
ActionResult
```

## Layer 7: Evaluation

Evaluation checks whether the reasoning or action worked.

It should measure:

- correctness
- traceability
- sparsity
- latency
- robustness
- failure recovery

The evaluation layer should also produce feedback that can update memory, rules, or planning strategy.

Output:

```text
EvaluationResult
```

## Reasoning trace

A reasoning system should expose its reasoning path.

A useful trace should include:

- selected input state
- retrieved concepts
- activated rules
- planner decision
- action result
- evaluation result

Example:

```text
Goal: identify safe object to pick
State: block_1 is fragile, block_2 is metal
Retrieved concept: fragile_object_handling
Activated rule: fragile objects require reduced grip force
Plan: pick block_1 using low-force grasp
Evaluation: safe grasp selected
```

This trace is not decoration. It is the debugging surface of the reasoning system.

## Robotics relevance

Robots need reasoning because physical tasks are constrained, sequential, and failure-prone.

A robot should not only execute a command. It should understand:

- what state it is in
- what changed from the previous attempt
- which constraints matter
- which action is safe
- why a plan failed
- what to try next

This makes reasoning relevant to physical AI and embodied agents.

## Relationship to projects

The repository projects map onto the stack as follows:

| Project | Stack layer focus |
|---|---|
| 01 Sparse Logical Reasoning | Rule System + Evaluation |
| 02 Memory-Backed Concepts | Concept Memory |
| 03 Visual-to-Symbolic State | Perception + Symbolic State |
| 04 Rule Induction | Rule System + Concept Memory |

The long-term goal is to connect these projects into one coherent reasoning loop.

## Minimum viable reasoning loop

The first useful loop does not need advanced perception or robotics.

A minimal version can be:

```text
Structured input → Symbolic state → Sparse rules → Answer → Trace → Evaluation
```

This is enough to test the central claim: reasoning should be explicit, sparse, and inspectable.

## Open design challenge

The hard problem is not adding more modules. The hard problem is controlling how much structure is enough.

Too little structure creates opaque behavior.
Too much structure creates brittle symbolic systems.

The target is the middle path:

```text
structured enough to inspect, flexible enough to adapt
```
