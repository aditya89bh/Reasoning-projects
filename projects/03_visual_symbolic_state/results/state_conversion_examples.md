# State Conversion Examples

This document summarizes the expected behavior of the visual-to-symbolic state prototype.

The prototype demonstrates a minimal state conversion loop:

```text
Structured scene → Scene objects → Spatial relations → Symbolic predicates → Validation → Trace
```

The goal is not full computer vision yet. The goal is to create a clean bridge between scene input and reasoning-ready symbolic state.

## Sample scene

The demo uses `examples/sample_scene.json`.

Objects:

| Object ID | Type | Key attributes | Position |
|---|---|---|---|
| `block_red` | block | red, cube, small, plastic | x=1.0, y=2.0 |
| `sphere_blue` | sphere | blue, sphere, large, rubber | x=4.0, y=2.0 |
| `cup_glass` | cup | clear, cylinder, medium, glass, fragile | x=2.0, y=5.0 |

## Expected object predicates

The system should generate object and attribute predicates such as:

```text
object(block_red)
type(block_red, block)
color(block_red, red)
shape(block_red, cube)
size(block_red, small)
material(block_red, plastic)

object(sphere_blue)
type(sphere_blue, sphere)
color(sphere_blue, blue)
shape(sphere_blue, sphere)
size(sphere_blue, large)
material(sphere_blue, rubber)

object(cup_glass)
type(cup_glass, cup)
color(cup_glass, clear)
shape(cup_glass, cylinder)
size(cup_glass, medium)
material(cup_glass, glass)
fragile(cup_glass, true)
```

## Expected spatial relations

Based on object positions, the relation extractor should generate relations such as:

```text
left_of(block_red, sphere_blue)
right_of(sphere_blue, block_red)
below(block_red, cup_glass)
above(cup_glass, block_red)
left_of(block_red, cup_glass)
right_of(cup_glass, block_red)
left_of(cup_glass, sphere_blue)
right_of(sphere_blue, cup_glass)
below(sphere_blue, cup_glass)
above(cup_glass, sphere_blue)
```

Near relations depend on the configured distance threshold.

## Expected symbolic state

The final symbolic state should include:

```text
state_id: state_tabletop_001
episode_id: episode_tabletop_001
source: structured_scene
objects: 3
relations: computed from object positions
predicates: object predicates + relation predicates
validation: passed
```

## Example trace

Expected trace shape:

```text
Loaded objects: 3
Extracted relations: <relation_count>
Built predicates: <predicate_count>
State confidence: <average_confidence>
Validation passed: True
Validation errors: none
Validation warnings: none
```

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Object extraction | Were scene objects loaded correctly? |
| Attribute predicates | Were attributes converted into predicates? |
| Relation extraction | Were spatial relations computed correctly? |
| Predicate completeness | Did the state include object, type, attribute, and relation predicates? |
| Validation | Did the symbolic state pass basic consistency checks? |
| Trace clarity | Can the conversion process be inspected? |

## What this prototype proves

This project does not yet prove visual perception. It proves the first required bridge:

```text
structured scene → symbolic state → reasoning-ready predicates
```

That bridge is required before connecting perception to sparse rules, concept memory, and rule induction.

## Run command

From the repository root:

```bash
python projects/03_visual_symbolic_state/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/03_visual_symbolic_state/tests
```

## Current limitation

The demo uses structured JSON scenes. It does not yet support raw images, object detection, segmentation, pose estimation, temporal state tracking, or uncertainty-aware visual perception.

The current value is controlled symbolic state construction.

## Next improvement

The next useful improvement is to connect this output to Project 01 and Project 02:

```text
SymbolicState predicates → Sparse rule selection
SymbolicState attributes → Concept retrieval
```

That would make Project 03 part of the larger reasoning loop instead of a standalone converter.
