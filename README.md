# Reasoning Projects

Sparse, memory-backed reasoning systems for AGI, robotics, and embodied AI.

## What this repository is

This repository is a structured research and implementation roadmap for reasoning systems. It focuses on how artificial agents can move beyond pattern matching toward explicit, inspectable, and deployable reasoning.

The repository is organized as a reasoning stack, not as a random collection of experiments. Each project studies one layer of the stack and is designed to connect with the others over time.

## Core thesis

Reasoning systems should not rely only on dense neural activation or hidden latent representations. For real-world deployment, especially in robotics, reasoning should be sparse, memory-backed, structured, and traceable.

The working assumption is simple:

```text
If perception and memory can be made sparse and efficient, reasoning should also be sparse, modular, and inspectable.
```

## Why reasoning matters

Modern AI systems are strong at perception and generation, but they remain weak at multi-step reasoning, abstraction, rule learning, and reliable decision-making under constraints.

This repository explores reasoning architectures that can support:

- explicit symbolic state
- concept reuse through memory
- sparse rule activation
- interpretable reasoning traces
- planning under real-world constraints
- adaptation from limited examples

The target is not academic symbolic reasoning in isolation. The target is reasoning that can eventually support embodied systems, robotics workflows, and real-world agent behavior.

## Reasoning stack

The intended stack is:

```text
Perception → Symbolic State → Concept Memory → Rule System → Planner → Action → Evaluation
```

Each project in this repository studies one layer of that stack.

| Layer | Role |
|---|---|
| Perception | Receives raw sensory or structured input |
| Symbolic State | Converts the world into objects, attributes, relations, and predicates |
| Concept Memory | Stores reusable concepts outside model weights |
| Rule System | Applies explicit rules and constraints |
| Planner | Selects reasoning steps and action sequences |
| Action | Executes or simulates decisions |
| Evaluation | Checks correctness, traceability, and recovery |

## Project map

| Project | Goal | Status | Output |
|---|---|---:|---|
| 01 Sparse Logical Reasoning | Discover minimal sparse circuits for logical reasoning | Planned / scaffold | Prototype + notes |
| 02 Memory-Backed Concepts | Store and reuse concepts through external memory | Planned | Architecture design |
| 03 Visual-to-Symbolic State | Convert perception into structured symbolic states | Planned | State extraction spec |
| 04 Rule Induction | Learn explicit rules from examples | Planned | Future prototype |

## Current status

This repository is in the early architecture phase.

Current focus:

1. Define the reasoning stack.
2. Create project-level specifications.
3. Establish shared interfaces.
4. Build the first runnable sparse logical reasoning prototype.

This repo is not yet a finished implementation. It is a structured build path toward a sparse, memory-backed reasoning system.

## Repository structure

Target structure:

```text
Reasoning-projects/
├── README.md
├── docs/
│   ├── reasoning_stack.md
│   ├── design_principles.md
│   ├── roadmap.md
│   └── open_questions.md
├── projects/
│   ├── 01_sparse_logical_reasoning/
│   │   └── README.md
│   ├── 02_memory_backed_concepts/
│   │   └── README.md
│   ├── 03_visual_symbolic_state/
│   │   └── README.md
│   └── 04_rule_induction/
│       └── README.md
├── shared/
│   ├── interfaces.md
│   └── evaluation.md
└── references/
    └── reading_list.md
```

## How to use this repository

Start with:

1. `docs/reasoning_stack.md`
2. `docs/design_principles.md`
3. `docs/roadmap.md`
4. `projects/01_sparse_logical_reasoning/README.md`

The repo should be read as a staged reasoning-system roadmap. The first priority is architectural clarity. Implementation follows the stack.

## Evaluation criteria

Each project will be evaluated using both technical and practical criteria.

| Metric | Meaning |
|---|---|
| Accuracy | Does the system produce the correct reasoning result? |
| Sparsity | How little of the system needs to activate? |
| Traceability | Can the reasoning path be inspected? |
| Generalization | Does it work on unseen combinations? |
| Latency | Can it work under real-time constraints? |
| Recovery | Can it detect and correct failed reasoning? |

## Related direction

This repo connects to broader work on:

- neuro-symbolic AI
- memory systems
- planning agents
- embodied AI
- robotics reasoning
- interpretable AGI systems

## Roadmap

The next milestone is to complete Project 01: Sparse Logical Reasoning.

The minimum target is a runnable prototype that compares dense and sparse reasoning behavior on simple logical tasks, with accuracy, sparsity, and traceability as evaluation criteria.

Longer term, the goal is to connect sparse reasoning, memory-backed concepts, symbolic state extraction, and rule induction into a coherent reasoning architecture for embodied agents.
