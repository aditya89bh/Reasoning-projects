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
| 01 Sparse Logical Reasoning | Compare sparse rule activation against a dense baseline | Runnable first prototype | Demo, tests, traces, baseline comparison |
| 02 Memory-Backed Concepts | Store, retrieve, reuse, and update concepts through external memory | Runnable first prototype | Demo, tests, seed memory, retrieval examples |
| 03 Visual-to-Symbolic State | Convert structured scene input into symbolic predicates | Runnable first prototype | Demo, tests, sample scene, state conversion examples |
| 04 Rule Induction | Learn explicit rules from repeated examples | Runnable first prototype | Demo, tests, episodes, rule induction examples |

## Current status

This repository has moved from pure architecture into early runnable prototypes.

Current state:

1. Reasoning stack is documented.
2. Design principles are documented.
3. Shared interfaces are documented.
4. Evaluation criteria are documented.
5. Project 01 has a runnable sparse logical reasoning prototype.
6. Project 02 has a runnable memory-backed concepts prototype.
7. Project 03 has a runnable visual-to-symbolic state prototype.
8. Project 04 has a runnable rule induction prototype.

This repo is not yet a finished integrated reasoning system. It is now a working research scaffold with four runnable modules.

Estimated repository status:

```text
75-80% complete
```

## Repository structure

Current structure:

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
│   │   ├── README.md
│   │   ├── run_demo.py
│   │   ├── src/
│   │   ├── examples/
│   │   ├── tests/
│   │   └── results/
│   ├── 02_memory_backed_concepts/
│   │   ├── README.md
│   │   ├── run_demo.py
│   │   ├── src/
│   │   ├── examples/
│   │   ├── tests/
│   │   └── results/
│   ├── 03_visual_symbolic_state/
│   │   ├── README.md
│   │   ├── run_demo.py
│   │   ├── src/
│   │   ├── examples/
│   │   ├── tests/
│   │   └── results/
│   └── 04_rule_induction/
│       ├── README.md
│       ├── run_demo.py
│       ├── src/
│       ├── examples/
│       ├── tests/
│       └── results/
├── shared/
│   ├── interfaces.md
│   └── evaluation.md
└── references/
    └── reading_list.md
```

## Runnable prototypes

## Project 01: Sparse Logical Reasoning

Run from the repository root:

```bash
python projects/01_sparse_logical_reasoning/run_demo.py
```

Run tests:

```bash
python -m pytest projects/01_sparse_logical_reasoning/tests
```

What it demonstrates:

```text
input facts → sparse rule selection → execution → answer → trace → evaluation
```

## Project 02: Memory-Backed Concepts

Run from the repository root:

```bash
python projects/02_memory_backed_concepts/run_demo.py
```

Run tests:

```bash
python -m pytest projects/02_memory_backed_concepts/tests
```

What it demonstrates:

```text
task facts → concept retrieval → recommendation → outcome update → memory trace
```

## Project 03: Visual-to-Symbolic State

Run from the repository root:

```bash
python projects/03_visual_symbolic_state/run_demo.py
```

Run tests:

```bash
python -m pytest projects/03_visual_symbolic_state/tests
```

What it demonstrates:

```text
structured scene → objects → relations → predicates → symbolic state → validation trace
```

## Project 04: Rule Induction

Run from the repository root:

```bash
python projects/04_rule_induction/run_demo.py
```

Run tests:

```bash
python -m pytest projects/04_rule_induction/tests
```

What it demonstrates:

```text
episodes → repeated patterns → candidate rules → scored rules → rule memory → future recommendation
```

## How to use this repository

Start with:

1. `docs/reasoning_stack.md`
2. `docs/design_principles.md`
3. `shared/interfaces.md`
4. `shared/evaluation.md`
5. `projects/01_sparse_logical_reasoning/README.md`
6. `projects/02_memory_backed_concepts/README.md`
7. `projects/03_visual_symbolic_state/README.md`
8. `projects/04_rule_induction/README.md`

Then run the four working demos.

## Evaluation criteria

Each project is evaluated using both technical and practical criteria.

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

Near-term roadmap:

1. Run all four demos locally and capture actual output in result files.
2. Add persistent concept memory write-back for Project 02.
3. Persist induced rules to `examples/induced_rules.json` for Project 04.
4. Connect Project 03 symbolic predicates to Project 01 sparse rule selection.
5. Connect Project 03 symbolic attributes to Project 02 concept retrieval.
6. Connect Project 04 induced rules to Project 01 rule execution.
7. Build one integrated loop across symbolic state, concept memory, sparse rules, rule induction, and evaluation.

Longer term, the goal is to connect sparse reasoning, memory-backed concepts, symbolic state extraction, and rule induction into a coherent reasoning architecture for embodied agents.
