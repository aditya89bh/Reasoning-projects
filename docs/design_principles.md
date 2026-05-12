# Design Principles

This document defines the technical principles for the Reasoning Projects repository.

The goal is not to build reasoning systems that look impressive in isolated demos. The goal is to define reasoning systems that are inspectable, sparse, memory-backed, and eventually useful for embodied agents.

## 1. Sparsity-first

Reasoning should activate only what is relevant.

Dense systems often process every input through large hidden representations, even when only a small subset of knowledge, rules, or concepts is needed. For reasoning, this is inefficient and hard to inspect.

A sparsity-first reasoning system should:

- activate only relevant rules
- retrieve only relevant concepts
- avoid unnecessary computation
- expose which reasoning paths were used
- measure active components during inference

The target is not sparsity for its own sake. The target is controlled reasoning.

## 2. Memory over parameters

Knowledge should not always be buried inside model weights.

For deployed agents, especially robots, knowledge often changes after deployment. A system may learn from failures, operator corrections, new environments, new objects, or repeated workflows.

A memory-backed reasoning system should store reusable knowledge externally where it can be inspected, updated, retrieved, and forgotten.

Examples of external knowledge:

- object concepts
- task patterns
- failure cases
- rules learned from experience
- operator preferences
- environment-specific constraints

Memory gives the system continuity without requiring constant retraining.

## 3. Explicit structure

Reasoning should operate over explicit structures whenever possible.

Useful structures include:

- objects
- attributes
- relations
- predicates
- concepts
- rules
- plans
- traces

Explicit structure improves debugging, evaluation, and human trust. It also makes the system easier to connect to robotics pipelines, where state, actions, constraints, and failures need clear representation.

The goal is not to replace neural systems with rigid symbolic systems. The goal is to make the reasoning layer structured enough to inspect.

## 4. Traceability

Every reasoning result should produce a trace.

A reasoning trace should show:

- what state was used
- what concepts were retrieved
- what rules were activated
- what plan was selected
- what action was taken
- what result was produced
- what evaluation was made

Traceability is not a UI feature. It is a core debugging and evaluation primitive.

Without traces, failures become guesses. With traces, failures become inspectable events.

## 5. Few-shot adaptation

A reasoning system should improve from limited examples.

Real-world agents often cannot rely on massive retraining cycles. They need to adapt from a small number of demonstrations, corrections, or failures.

Few-shot adaptation can happen through:

- storing new concepts in memory
- updating rule confidence
- adding new constraints
- changing strategy selection
- recording failure patterns
- reusing previous solutions

The system should learn behaviorally useful structure from small amounts of experience.

## 6. Deployment realism

Reasoning systems should be designed with real constraints in view.

For robotics and embodied agents, reasoning cannot be evaluated only by benchmark accuracy. The system must also consider latency, reliability, interpretability, safety, and integration cost.

Deployment realism means asking:

- Can this run fast enough?
- Can the reasoning path be inspected?
- Can failures be diagnosed?
- Can the system recover from mistakes?
- Can it work with noisy state?
- Can it connect to real action systems?

A reasoning architecture that cannot survive deployment constraints is only a lab artifact.

## 7. Modular composition

Reasoning should be built from modules that can be tested independently.

Each layer should have a clear role:

- symbolic state representation
- concept memory
- rule activation
- planning
- action
- evaluation

Modularity allows individual components to be replaced without rewriting the whole system. It also makes the architecture easier to test, debug, and extend.

## 8. Evaluation before scale

The system should be measurable before it is scaled.

Before adding larger models, more rules, or more complex environments, each project should define what success means.

Useful evaluation dimensions:

- correctness
- sparsity
- trace clarity
- generalization
- latency
- recovery behavior

Scaling unclear systems only creates larger unclear systems.

## 9. Middle path between neural and symbolic systems

Pure neural systems are flexible but often opaque.

Pure symbolic systems are inspectable but often brittle.

This repository explores the middle path:

```text
structured enough to inspect, flexible enough to adapt
```

The goal is not symbolic purity. The goal is useful reasoning.

## 10. Robotics relevance

Reasoning matters most when actions have consequences.

In robotics, a system must operate under physical constraints. It needs to understand state, choose actions, recover from failures, and explain what happened.

A reasoning system for robotics should support:

- state awareness
- constraint handling
- memory of past attempts
- failure recovery
- safe action selection
- operator-understandable traces

This is why the repository treats reasoning as a deployment problem, not only a cognitive benchmark problem.

## Summary

The guiding principles are:

| Principle | Meaning |
|---|---|
| Sparsity-first | Activate only what matters |
| Memory over parameters | Store reusable knowledge externally |
| Explicit structure | Represent state, concepts, rules, and plans clearly |
| Traceability | Make every reasoning path inspectable |
| Few-shot adaptation | Learn from limited examples |
| Deployment realism | Design for real constraints |
| Modular composition | Keep components separable and testable |
| Evaluation before scale | Measure before expanding |
| Neural-symbolic middle path | Combine flexibility with inspectability |
| Robotics relevance | Ground reasoning in action and consequence |
