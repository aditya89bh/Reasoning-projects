# Integrated Reasoning Demo

This folder connects the four reasoning projects into one end-to-end scaffold.

The purpose is to show how symbolic state, concept memory, sparse rules, and rule induction can work together as one reasoning loop.

## Integrated loop

```text
Structured Scene
→ Symbolic State
→ Concept Retrieval
→ Sparse Rule Reasoning
→ Rule Induction
→ Evaluation Trace
```

## Project connections

| Project | Role in integrated loop |
|---|---|
| Project 03: Visual-to-Symbolic State | Converts scene input into objects, attributes, relations, and predicates |
| Project 02: Memory-Backed Concepts | Retrieves reusable concepts from symbolic facts |
| Project 01: Sparse Logical Reasoning | Applies relevant explicit rules to task facts |
| Project 04: Rule Induction | Learns new rules from repeated episodes and applies them to future tasks |

## What the integrated demo should prove

The integrated demo should prove a small but important claim:

```text
A reasoning system becomes stronger when state, memory, rules, learning, and evaluation are connected through explicit interfaces.
```

It does not need to be a full AGI system. It needs to show a clean traceable loop.

## Minimum integrated scenario

Use a structured scene containing a fragile glass object.

Expected chain:

1. Project 03 extracts predicates such as:

```text
object(cup_glass)
material(cup_glass, glass)
fragile(cup_glass, true)
```

2. Project 02 retrieves:

```text
concept_fragile_object
```

3. Project 01 applies sparse rules for safe action selection:

```text
object_fragile + grip_force_high → action_unsafe
```

4. Project 04 uses repeated episodes to induce a rule:

```text
If object_fragile then avoid_high_force_grasp
```

5. The final trace explains:

```text
scene state → retrieved concept → active rule → induced rule → recommendation
```

## Current status

```text
Integration scaffold
```

The four individual projects are runnable first prototypes. This folder defines the integrated direction and will contain the first cross-project demo.

## Next files

```text
integrated_demo/run_integrated_demo.py
integrated_demo/results/integrated_trace.md
```

## Target

This integrated scaffold is the main step that moves the repository from four isolated prototypes toward a coherent reasoning architecture.
