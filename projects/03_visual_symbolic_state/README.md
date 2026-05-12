# Project 03: Visual-to-Symbolic State

This project explores how structured scene input can be converted into symbolic state for downstream reasoning.

The current prototype uses structured JSON scenes instead of raw images. This keeps the first milestone focused on the core bridge: converting objects, attributes, and spatial relations into reasoning-ready predicates.

## Core question

```text
Can perception or scene-level input produce clean symbolic states for downstream reasoning?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- symbolic state data model
- structured scene loader
- spatial relation extractor
- predicate builder
- symbolic state validator
- sample scene
- command-line demo
- tests
- state conversion result documentation

Estimated project status:

```text
65-70% complete
```

## Why this matters

Reasoning systems need a representation of the world before they can reason about it.

For robotics and embodied agents, the system must understand:

- what objects exist
- what attributes they have
- how objects relate to each other
- what constraints apply
- what state changed over time
- which parts of the state are uncertain

Visual-to-symbolic state extraction gives the reasoning layer a structured world model to operate on.

## Architecture

```text
Structured Scene → Scene Objects → Spatial Relations → Symbolic Predicates → SymbolicState → Validation → Trace
```

The first prototype does not use computer vision. It uses controlled structured input so the symbolic conversion path can be tested clearly.

## Components

| File | Role |
|---|---|
| `src/symbolic_state.py` | Defines `SceneObject`, `Relation`, and `SymbolicState` |
| `src/scene_loader.py` | Loads structured scene JSON into scene objects |
| `src/relation_extractor.py` | Computes spatial relations between objects |
| `src/predicate_builder.py` | Builds the final symbolic state |
| `src/validator.py` | Validates state completeness and consistency |
| `examples/sample_scene.json` | Sample structured tabletop scene |
| `run_demo.py` | Runs scene-to-symbolic-state conversion |
| `tests/test_symbolic_state.py` | Regression tests for state construction |
| `results/state_conversion_examples.md` | Documents expected conversion behavior |

## Symbolic state schema

A minimal symbolic state includes:

```text
state_id
episode_id
source
objects
relations
predicates
confidence
```

Example predicates:

```text
object(block_red)
type(block_red, block)
color(block_red, red)
shape(block_red, cube)
left_of(block_red, sphere_blue)
below(block_red, cup_glass)
```

## Sample scene

The demo scene contains three objects:

| Object ID | Type | Key attributes | Position |
|---|---|---|---|
| `block_red` | block | red, cube, small, plastic | x=1.0, y=2.0 |
| `sphere_blue` | sphere | blue, sphere, large, rubber | x=4.0, y=2.0 |
| `cup_glass` | cup | clear, cylinder, medium, glass, fragile | x=2.0, y=5.0 |

## Relation extraction

The prototype currently supports:

| Relation | Meaning |
|---|---|
| `left_of(a, b)` | Object `a` is left of object `b` |
| `right_of(a, b)` | Object `a` is right of object `b` |
| `above(a, b)` | Object `a` is above object `b` |
| `below(a, b)` | Object `a` is below object `b` |
| `near(a, b)` | Object `a` is within a distance threshold of object `b` |

## Run the demo

From the repository root:

```bash
python projects/03_visual_symbolic_state/run_demo.py
```

The demo prints:

- state id
- episode id
- objects
- extracted relations
- generated predicates
- validation result
- conversion trace

## Run tests

From the repository root:

```bash
python -m pytest projects/03_visual_symbolic_state/tests
```

## Example trace

```text
Loaded objects: 3
Extracted relations: <relation_count>
Built predicates: <predicate_count>
State confidence: <average_confidence>
Validation passed: True
Validation errors: none
Validation warnings: none
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Object extraction | Were scene objects loaded correctly? |
| Attribute predicates | Were attributes converted into predicates? |
| Relation extraction | Were spatial relations computed correctly? |
| Predicate completeness | Did the state include object, type, attribute, and relation predicates? |
| Validation | Did the symbolic state pass consistency checks? |
| Trace clarity | Can the conversion process be inspected? |

## What this prototype proves

This project does not yet prove visual perception.

It proves the required bridge:

```text
structured scene → symbolic state → reasoning-ready predicates
```

That bridge is needed before connecting perception to sparse rules, concept memory, and rule induction.

## Current limitations

- Uses structured JSON input, not raw images.
- No object detector yet.
- No segmentation or pose estimation yet.
- No temporal state tracking yet.
- No uncertainty-aware perception model yet.
- No direct integration with Project 01 or Project 02 yet.

## Next steps

1. Add more sample scenes.
2. Add expected output fixtures.
3. Capture actual demo output in results.
4. Connect generated predicates to Project 01 sparse rule selection.
5. Connect generated attributes to Project 02 concept retrieval.
6. Add temporal scene updates.
7. Later, replace structured JSON input with detection output.

## Completion target

This project reaches a stronger milestone when it has:

- multiple scenes
- expected state fixtures
- actual demo output captured in results
- integration with Project 01 and Project 02
- temporal state update examples

At that point, Project 03 becomes the active perception-to-reasoning bridge for the repository.
