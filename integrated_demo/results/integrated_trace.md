# Integrated Trace

This document describes the expected behavior of the integrated reasoning demo.

The integrated demo connects all four runnable prototypes:

```text
Project 03: Visual-to-Symbolic State
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
→ task facts
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

The integration mapper converts these predicates into simplified task facts:

```text
material_glass
object_fragile
grip_force_high
```

The `grip_force_high` fact is added as the task assumption for the integrated safety scenario.

## Step 2: Concept memory

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

## Step 3: Sparse logical reasoning

Project 01 applies sparse rule selection to the integrated task facts:

```text
material_glass
object_fragile
grip_force_high
```

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

## Step 4: Rule induction

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
Mapped symbolic predicates to task facts: ['grip_force_high', 'material_glass', 'object_fragile']
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
state → memory → rules → learning → trace
```

This is the main step from project collection to reasoning architecture.

## Run command

From the repository root:

```bash
python integrated_demo/run_integrated_demo.py
```

## Current limitation

The integration mapper is intentionally simple. It maps selected symbolic predicates to the fact labels expected by the other projects.

Future improvements should replace this with a shared fact normalization layer.

## Next improvement

Add:

```text
shared/fact_normalizer.py
```

This would let all projects share a common fact format instead of relying on manual predicate-to-fact mapping inside the integrated demo.
