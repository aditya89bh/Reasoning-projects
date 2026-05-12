# Project 03: Visual-to-Symbolic State

This project explores how perceptual or scene-level input can be converted into symbolic state for downstream reasoning.

The goal is to create a clean bridge between perception and reasoning. Reasoning systems need structured state. Raw input alone is not enough.

## Core question

```text
Can perception produce clean symbolic states for downstream reasoning?
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

## Project goal

Build a minimal state extraction system that can:

1. Receive structured scene input or simple perception output.
2. Identify objects, attributes, and relations.
3. Convert them into symbolic predicates.
4. Attach confidence where needed.
5. Produce a reasoning-ready `SymbolicState`.
6. Generate a trace of how the state was built.

## Example symbolic state

```text
object(block_1)
shape(block_1, cube)
color(block_1, red)
size(block_1, small)
left_of(block_1, block_2)
clear(block_1)
gripper_empty(robot_1)
```

## Minimal architecture

```text
Scene Input → Object Extraction → Attribute Extraction → Relation Extraction → Predicate Builder → SymbolicState → Trace
```

## Components

| Component | Role |
|---|---|
| Scene input | Raw or structured representation of the environment |
| Object extractor | Identifies objects in the scene |
| Attribute extractor | Assigns properties such as color, shape, size, material, pose |
| Relation extractor | Computes relations between objects |
| Predicate builder | Converts objects and relations into symbolic predicates |
| State validator | Checks consistency and missing fields |
| Trace generator | Shows how the symbolic state was created |

## Input types

Early versions can use structured input instead of full computer vision.

Possible input types:

| Input type | Example |
|---|---|
| JSON scene | List of objects with attributes and positions |
| Detection output | Object labels, bounding boxes, confidence |
| Robot state | Gripper state, joint state, tool pose |
| Simulated world state | Objects and relations from a simulator |
| Future visual input | Image or video frame with detections |

## SymbolicState schema

A minimal symbolic state should include:

```text
episode_id
timestamp
objects
attributes
relations
predicates
confidence
source
```

Example structured form:

```text
episode_id: scene_001
objects:
  - id: block_1
    type: block
    attributes:
      color: red
      shape: cube
      size: small
    position:
      x: 1
      y: 2
relations:
  - left_of(block_1, block_2)
predicates:
  - object(block_1)
  - color(block_1, red)
  - shape(block_1, cube)
  - left_of(block_1, block_2)
```

## Relation extraction

The first prototype should support simple spatial relations.

| Relation | Meaning |
|---|---|
| left_of(a, b) | Object `a` is left of object `b` |
| right_of(a, b) | Object `a` is right of object `b` |
| above(a, b) | Object `a` is above object `b` |
| below(a, b) | Object `a` is below object `b` |
| near(a, b) | Object `a` is within a distance threshold of object `b` |
| touching(a, b) | Object `a` is in contact with object `b` |

## Reasoning trace

The system should explain how symbolic state was generated.

Example trace:

```text
Input: scene_001
Detected objects: block_1, block_2
Extracted attributes: color(block_1, red), shape(block_1, cube)
Computed relation: left_of(block_1, block_2)
Built predicates: 6
Validation: passed
Output: SymbolicState(scene_001)
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Object accuracy | Were objects identified correctly? |
| Attribute accuracy | Were attributes assigned correctly? |
| Relation accuracy | Were spatial or logical relations correct? |
| Predicate completeness | Did the state include all required predicates? |
| State consistency | Are there contradictions or missing fields? |
| Trace clarity | Can the symbolic conversion be inspected? |
| Downstream usefulness | Can the state support reasoning tasks? |

## Minimum viable demo

The first demo should use a simple JSON scene and convert it into predicates.

Example target behavior:

```text
Input scene:
block_1: red cube at x=1, y=2
block_2: blue sphere at x=4, y=2

Generated predicates:
object(block_1)
object(block_2)
color(block_1, red)
shape(block_1, cube)
left_of(block_1, block_2)

Trace:
1. Loaded scene
2. Extracted 2 objects
3. Generated 4 attribute predicates
4. Generated 1 relation predicate
5. Validated symbolic state
```

## Planned file structure

```text
projects/03_visual_symbolic_state/
├── README.md
├── src/
│   ├── scene_loader.py
│   ├── object_extractor.py
│   ├── relation_extractor.py
│   ├── predicate_builder.py
│   └── validator.py
├── examples/
│   ├── sample_scene.json
│   └── expected_state.txt
├── tests/
│   └── test_symbolic_state.py
└── results/
    └── state_conversion_examples.md
```

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define the state schema, predicate format, relation extraction rules, and evaluation criteria.

## Next steps

1. Define the `SymbolicState` schema.
2. Create sample scene input files.
3. Implement object and attribute extraction from structured input.
4. Implement relation extraction.
5. Build predicate output.
6. Add validation rules.
7. Add trace generation.
8. Add downstream reasoning example.

## Completion target

This project reaches a useful first milestone when it has:

- symbolic state schema
- at least 5 sample scenes
- object and relation extraction
- predicate generation
- trace output
- validation checks
- basic tests

At that point, Project 03 becomes the perception-to-reasoning bridge for the stack.
