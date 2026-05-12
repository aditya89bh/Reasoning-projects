# Reading List

This reading list supports the Reasoning Projects repository.

The goal is not to collect every paper in neuro-symbolic AI. The goal is to keep a compact research spine for sparse reasoning, concept memory, symbolic state, rule induction, and embodied reasoning.

## Neuro-symbolic AI

| Resource | Why it matters |
|---|---|
| Neural-Symbolic Learning and Reasoning: A Survey and Interpretation | Broad foundation for hybrid neural-symbolic systems |
| The Neuro-Symbolic Concept Learner | Useful reference for language-to-program reasoning over structured scenes |
| Neural Logic Machines | Connects neural models with relational and logical reasoning |
| Logic Tensor Networks | Shows one approach to combining logic with differentiable learning |

## Program induction and structured reasoning

| Resource | Why it matters |
|---|---|
| DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning | Useful for learning reusable programs and abstractions |
| Neural Programmer-Interpreters | Relevant for compositional execution and learned program-like behavior |
| Differentiable Neural Computer | Relevant to memory-augmented reasoning systems |
| Neural Turing Machines | Early foundation for differentiable memory and algorithmic behavior |

## Sparse networks and efficient reasoning

| Resource | Why it matters |
|---|---|
| The Lottery Ticket Hypothesis | Foundation for sparse subnetworks that retain capability |
| Scalable training of artificial neural networks with adaptive sparse connectivity inspired by network science | Useful for dynamic sparse training ideas |
| Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | Relevant to sparse activation and conditional computation |
| Switch Transformers | Useful reference for efficient sparse activation at scale |

## Memory systems

| Resource | Why it matters |
|---|---|
| Memory Networks | Foundation for external memory in neural systems |
| End-To-End Memory Networks | Relevant for differentiable memory retrieval and reasoning |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Useful for external retrieval as a model capability |
| Generative Agents: Interactive Simulacra of Human Behavior | Useful for memory, reflection, and behavior over time |

## Rule induction and logic learning

| Resource | Why it matters |
|---|---|
| Inductive Logic Programming: Theory and Methods | Classical foundation for learning rules from examples |
| Differentiable Inductive Logic Programming | Connects rule learning with differentiable systems |
| Neural Theorem Provers | Useful for differentiable logic and rule-like inference |
| DeepProbLog | Relevant for probabilistic logic with neural components |

## Symbolic state and embodied reasoning

| Resource | Why it matters |
|---|---|
| CLEVR: A Diagnostic Dataset for Compositional Language and Elementary Visual Reasoning | Useful for visual-to-symbolic reasoning examples |
| ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks | Relevant for grounded instruction following and state-action reasoning |
| SayCan: Do As I Can, Not As I Say | Useful for connecting language, affordances, and action selection |
| PaLM-E: An Embodied Multimodal Language Model | Relevant to embodied AI and multimodal grounding |

## Planning and agents

| Resource | Why it matters |
|---|---|
| ReAct: Synergizing Reasoning and Acting in Language Models | Useful for explicit reasoning-action traces |
| Tree of Thoughts | Relevant to search-based reasoning over candidate paths |
| Reflexion | Relevant to self-evaluation and behavioral improvement through memory |
| Voyager | Useful reference for lifelong learning agents with skill memory |

## Robotics and deployment relevance

| Resource | Why it matters |
|---|---|
| RT-1: Robotics Transformer for Real-World Control at Scale | Relevant to robot policy learning and data scale |
| RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control | Relevant to grounding web-scale knowledge in robotic action |
| Inner Monologue: Embodied Reasoning through Planning with Language Models | Useful for language-mediated robot planning and feedback |
| Code as Policies | Relevant to converting language reasoning into robot-executable structures |

## How to use this list

Use the list as a working reference, not as a reading marathon.

Recommended sequence for this repository:

1. Start with neuro-symbolic reasoning and structured scene reasoning.
2. Study sparse activation and conditional computation.
3. Study memory systems for concept reuse.
4. Study rule induction.
5. Study embodied reasoning and robotics planning.
6. Map ideas back into the four projects.

## Near-term reading priority

For Project 01, prioritize:

1. The Lottery Ticket Hypothesis
2. Neural Logic Machines
3. Neural-Symbolic Learning and Reasoning: A Survey and Interpretation
4. ReAct
5. Tree of Thoughts

For Project 02, prioritize:

1. Memory Networks
2. End-To-End Memory Networks
3. Differentiable Neural Computer
4. Generative Agents
5. Retrieval-Augmented Generation

For Project 03, prioritize:

1. CLEVR
2. The Neuro-Symbolic Concept Learner
3. ALFRED
4. Inner Monologue
5. Code as Policies

For Project 04, prioritize:

1. Inductive Logic Programming
2. Differentiable Inductive Logic Programming
3. Neural Theorem Provers
4. DeepProbLog
5. DreamCoder

## Rule for adding references

A reference should only be added if it supports at least one of these:

- sparse reasoning
- symbolic state
- concept memory
- rule induction
- planning traces
- embodied reasoning
- robotics deployment
- evaluation of reasoning systems

Do not turn this into a generic AGI paper dump.
