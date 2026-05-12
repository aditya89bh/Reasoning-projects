# Project 02: Memory-Backed Concepts

This project explores how reasoning systems can store, retrieve, and reuse concepts through external memory instead of relying only on model parameters.

The goal is to design a concept memory layer that supports abstraction, reuse, composition, and adaptation from limited examples.

## Core question

```text
Can concepts be learned, stored, retrieved, reused, and composed without retraining the whole model?
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

## Project goal

Build a minimal concept memory system that can:

1. Store concepts in an explicit format.
2. Retrieve relevant concepts for a task.
3. Apply retrieved concepts during reasoning.
4. Update concept confidence from outcomes.
5. Produce a trace showing which concepts were used.

## Example concepts

| Concept | Meaning | Possible use |
|---|---|---|
| fragile_object | Object should be handled with reduced force | Grasp planning |
| blocked_path | Direct path is obstructed | Replanning |
| safe_grasp | Previously successful grasp configuration | Skill reuse |
| slippery_surface | Object or support surface has low friction | Motion constraint |
| operator_preference | User prefers a specific process or action | Personalization |
| repeated_failure | Similar attempt has failed before | Strategy change |

## Minimal architecture

```text
Task State → Concept Query → Concept Memory → Retrieved Concepts → Reasoning Use → Trace → Memory Update
```

## Components

| Component | Role |
|---|---|
| Concept schema | Defines what a concept contains |
| Memory store | Holds reusable concepts |
| Retriever | Finds relevant concepts for the current task |
| Reasoning adapter | Applies retrieved concepts to reasoning |
| Update mechanism | Adjusts confidence or records outcomes |
| Trace generator | Shows which concepts influenced the result |

## Concept schema

A minimal concept should include:

```text
id
name
description
trigger_conditions
recommended_action
confidence
evidence
last_used
failure_notes
```

Example:

```text
id: concept_fragile_object
name: fragile_object
description: Object may break under high force.
trigger_conditions:
  - object.material == glass
  - object.label includes fragile
recommended_action:
  - reduce grip force
  - slow approach speed
confidence: 0.85
evidence:
  - previous successful low-force grasp
failure_notes:
  - high-force grasp caused damage in prior attempt
```

## Retrieval behavior

The retriever should support more than generic similarity search.

Useful retrieval modes:

| Retrieval mode | Purpose |
|---|---|
| Attribute match | Retrieve concepts linked to object properties |
| Task match | Retrieve concepts linked to similar goals |
| Failure match | Retrieve concepts from past failed attempts |
| Constraint match | Retrieve relevant safety or process rules |
| Hybrid match | Combine semantic and symbolic retrieval |

## Reasoning trace

The system should expose concept use clearly.

Example trace:

```text
Task: pick object_12
State: object_12 material=glass, weight=low
Retrieved concept: fragile_object
Reasoning effect: reduce grip force and approach speed
Action recommendation: low-force grasp
Evaluation: successful grasp
Memory update: confidence +0.03
```

This makes memory operational rather than decorative.

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Retrieval relevance | Did the system retrieve the right concept? |
| Concept reuse | Was prior knowledge applied correctly? |
| Reasoning impact | Did the concept change the decision? |
| Outcome improvement | Did memory improve success or safety? |
| Trace clarity | Can a human see why the concept was used? |
| Update quality | Did the system update memory after feedback? |

## Minimum viable demo

The first demo should use structured task states and a small hand-written concept memory.

Example target behavior:

```text
Input task:
pick object_12

Task state:
material=glass
weight=low
surface=smooth

Retrieved concept:
fragile_object

Reasoning adjustment:
reduce_grip_force=true
slow_approach=true

Output:
recommended_action=low_force_grasp

Trace:
1. Detected glass material
2. Retrieved fragile_object concept
3. Applied low-force handling constraint
4. Recommended low-force grasp
5. Stored successful outcome
```

## Planned file structure

```text
projects/02_memory_backed_concepts/
├── README.md
├── src/
│   ├── concept.py
│   ├── memory_store.py
│   ├── retriever.py
│   ├── adapter.py
│   └── updater.py
├── examples/
│   ├── concept_memory.json
│   └── demo_tasks.json
├── tests/
│   └── test_concept_memory.py
└── results/
    └── retrieval_examples.md
```

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define concept schema, retrieval modes, and trace format before implementing the memory prototype.

## Next steps

1. Define the concept schema.
2. Create a small hand-written concept memory.
3. Define structured task input format.
4. Implement retrieval logic.
5. Apply retrieved concepts to reasoning outputs.
6. Add trace generation.
7. Add update behavior after success or failure.
8. Add tests and retrieval examples.

## Completion target

This project reaches a useful first milestone when it has:

- explicit concept schema
- concept memory file
- retrieval prototype
- at least 5 task examples
- reasoning trace output
- memory update example
- basic tests

At that point, Project 02 becomes the first working memory-backed abstraction layer for the reasoning stack.
