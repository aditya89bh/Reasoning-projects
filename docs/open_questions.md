# Open Questions

This document collects unresolved research and design questions for the Reasoning Projects repository.

The goal is to make uncertainty explicit. A useful reasoning repository should not pretend that all architecture decisions are solved upfront.

## 1. Sparse reasoning

### How sparse can reasoning become before accuracy collapses?

The central question for Project 01 is not whether sparse reasoning is possible. The useful question is how much structure can be removed while preserving correctness and traceability.

Sub-questions:

- What is the minimum number of active rules needed for a task?
- Does sparsity improve interpretability or only reduce computation?
- When does sparse activation miss necessary context?
- How should the system recover from under-activation?

## 2. Dense baseline vs sparse reasoning

### What is the right dense baseline?

A sparse system only makes sense if it is compared to something.

Possible baselines:

- evaluate all rules
- retrieve all concepts
- activate all candidate reasoning paths
- use a simple dense neural model
- use a non-sparse symbolic executor

Sub-questions:

- Should the baseline optimize for accuracy, simplicity, or realism?
- Is the comparison computational, interpretability-based, or both?
- How should unnecessary activations be counted?

## 3. Symbolic state quality

### How much structure does a reasoning system need?

Too little symbolic structure creates opaque behavior. Too much structure creates brittle systems.

Sub-questions:

- Which predicates are necessary for useful reasoning?
- Should predicates include confidence values?
- How should contradictory predicates be handled?
- What happens when state is incomplete?
- How much should be inferred vs directly observed?

## 4. Concept memory

### What makes a concept reusable?

A concept is only useful if it can transfer across situations.

Sub-questions:

- What should a concept contain?
- How specific should a concept be?
- How should concepts be retrieved?
- When should a concept be updated?
- When should a concept be forgotten?
- How should conflicting concepts be handled?

## 5. Memory over parameters

### Which knowledge should live in memory, and which should live in model weights?

The repository assumes that some knowledge should be externalized into memory, but the boundary is not obvious.

Sub-questions:

- Should facts live in memory?
- Should skills live in memory?
- Should rules live in memory?
- Should failures live in memory?
- When is retraining better than memory update?

## 6. Rule induction

### Can useful rules be learned from small numbers of examples?

Rule induction is valuable only if learned rules improve future behavior.

Sub-questions:

- How many examples are needed before proposing a rule?
- How should candidate rules be scored?
- How should over-general rules be rejected?
- How should narrow but useful rules be preserved?
- How should rule confidence change over time?

## 7. Rule conflicts

### What happens when two rules disagree?

A real reasoning system will eventually contain conflicting rules.

Sub-questions:

- Should rules have priority?
- Should confidence decide conflicts?
- Should context decide conflicts?
- Should the system ask for human input?
- Should conflict itself become a trace event?

## 8. Planning and reasoning boundary

### Where does reasoning end and planning begin?

Reasoning and planning overlap. Reasoning may infer facts. Planning may select actions. But both use state, constraints, and goals.

Sub-questions:

- Is planning a separate layer or an extension of reasoning?
- Should plans be rule-generated, search-generated, or learned?
- How should plan failure update memory?
- Can planning remain traceable at longer horizons?

## 9. Trace quality

### What makes a reasoning trace useful?

A trace should not be a verbose log. It should expose the meaningful structure behind a decision.

Sub-questions:

- What fields are required in every trace?
- How much detail is too much?
- Should traces be optimized for developers, operators, or researchers?
- Can trace quality be evaluated automatically?
- Can trace compression preserve meaning?

## 10. Evaluation

### How should reasoning systems be evaluated beyond correctness?

Correct answers are not enough for this repository.

Sub-questions:

- How should sparsity be scored?
- How should trace clarity be scored?
- How should robustness be measured?
- How should recovery be evaluated?
- How should latency be weighed against interpretability?

## 11. Robotics relevance

### What reasoning capabilities matter most for physical AI?

Robotics introduces action, uncertainty, timing, and safety.

Sub-questions:

- Which symbolic states are useful for robot tasks?
- Which rules should be safety-critical?
- How should robot failures update reasoning memory?
- How should reasoning connect to robot skill APIs?
- What is the smallest robotics demo that proves value?

## 12. Integration risk

### How do the modules connect without becoming over-engineered?

The repository has multiple layers: symbolic state, concept memory, rules, planning, evaluation. The risk is building too much structure before there is a working demo.

Sub-questions:

- What is the minimum useful end-to-end loop?
- Which interfaces should be stable first?
- Which modules can remain mocked initially?
- When should integration happen?
- What should be deliberately left out?

## 13. Learning from failure

### How should the system convert failure into reusable knowledge?

Failures are useful only if they change future behavior.

Sub-questions:

- Should failures create concepts, rules, or plan constraints?
- How should repeated failure be detected?
- How should one-off noise be ignored?
- How should failure traces be stored?
- When should a failure trigger human review?

## 14. Human interpretability

### Who is the explanation for?

Different users need different explanations.

Possible audiences:

- developer
- robotics operator
- researcher
- customer
- evaluator

Sub-questions:

- Should the system produce different trace views?
- Should explanations include confidence?
- Should explanations include uncertainty?
- Should explanations include rejected alternatives?
- How much internal reasoning should be exposed?

## 15. Long-term architecture

### What is the final shape of the reasoning stack?

The current stack is:

```text
Perception → Symbolic State → Concept Memory → Rule System → Planner → Action → Evaluation
```

Open question:

```text
Is this the right architecture, or only a useful scaffold for discovery?
```

The answer should emerge through prototypes, not assumptions.

## Near-term research focus

The most important open questions for the next milestone are:

1. What is the minimum viable sparse reasoning demo?
2. What task format should Project 01 use?
3. What dense baseline should it compare against?
4. What should count as a reasoning trace?
5. Which evaluation table should appear first in the repo?

## Working rule

When in doubt, build the smallest testable loop:

```text
input → reasoning path → answer → trace → evaluation
```

The repo should grow from working loops, not abstract architecture alone.
