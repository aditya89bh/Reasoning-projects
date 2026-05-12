# Integrated Trace

This document describes the expected behavior of the integrated reasoning demo.

The integrated demo connects all four runnable prototypes:

```text
Project 03: Visual-to-Symbolic State
→ Shared Fact Normalizer
→ Project 02: Memory-Backed Concepts
→ Project 01: Sparse Logical Reasoning
→ Project 04: Rule Induction
```

## Integrated scenario

The demo uses the Project 03 sample scene containing a fragile glass cup.

The intended reasoning flow is:

```text
structured scene
→ symbolic predicates
→ normalized task facts
→ concept retrieval
→ sparse rule reasoning
→ induced rule recommendation
→ final trace
```

## Step 1: Symbolic state

Project 03 loads:

```text
projects/03_visual_symbolic_state/examples/sample_scene.json
```

Expected extracted predicates include:

```text
object(cup_glass)
type(cup_glass, cup)
material(cup_glass, glass)
fragile(cup_glass, true)
```

## Step 2: Shared fact normalization

The shared normalizer converts symbolic predicates into simplified task facts.

Shared module:

```text
shared/fact_normalizer.py
```

Expected normalized facts:

```text
material_glass
object_fragile
object_cup
object_detected
shape_cylinder
grip_force_high
```

The `grip_force_high` fact is added as the task assumption for the integrated safety scenario.

## Step 3: Concept memory

Project 02 uses the task facts to retrieve relevant concepts from:

```text
projects/02_memory_backed_concepts/examples/concept_memory.json
```

Expected retrieved concept:

```text
concept_fragile_object
```

Expected concept recommendation:

```text
use_low_force_strategy
```

Reason:

```text
material_glass/object_fragile → fragile object concept → avoid high force
```

## Step 4: Sparse logical reasoning

Project 01 applies sparse rule selection to the integrated task facts.

Expected active rule:

```text
rule_fragile_high_force_unsafe
```

Expected answer:

```text
action_unsafe
```

Expected evaluation:

```text
correct=true
active_rules=1
total_rules=8
```

## Step 5: Rule induction

Project 04 loads prior episodes from:

```text
projects/04_rule_induction/examples/episodes.json
```

Expected induced pattern:

```text
object_fragile + high_force_grasp + failure
```

Expected induced recommendation for the integrated task:

```text
avoid_high_force_grasp
```

## Final expected trace

The final integrated trace should look like this:

```text
Built symbolic state: state_tabletop_001
Objects: 3
Relations: <count>
Predicates: <count>
Validation passed: True
Mapped symbolic predicates to task facts: ['grip_force_high', 'material_glass', 'object_cup', 'object_detected', 'object_fragile', 'shape_cylinder']
Retrieved concepts: ['concept_fragile_object']
Concept recommendation: use_low_force_strategy
Sparse reasoning answer: action_unsafe
Sparse reasoning correct: True
Induced rule recommendation: avoid_high_force_grasp
```

## What this proves

The integrated demo proves that the repository is no longer a set of disconnected prototypes.

It now has a coherent loop:

```text
state → normalized facts → memory → rules → learning → trace
```

This is the main step from project collection to reasoning architecture.

## Run command

From the repository root:

```bash
python integrated_demo/run_integrated_demo.py
```

## Current limitation

The fact normalizer is still simple and rule-based. It maps known predicate strings to known fact labels.

Future improvements should support:

- more general predicate parsing
- object-agnostic fact mapping
- confidence-aware facts
- temporal facts
- normalized facts shared across all project demos

## Next improvement

Add tests for the integrated demo and fact normalizer.
