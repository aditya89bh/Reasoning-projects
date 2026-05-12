# Evaluation

This document defines the evaluation approach for the Reasoning Projects repository.

The goal is to avoid vague claims about reasoning ability. Each project should define what success means, how it is measured, and what failure looks like.

## Core evaluation principle

A reasoning system should be evaluated on more than final answer correctness.

Useful reasoning should be:

- correct
- sparse
- traceable
- robust
- fast enough for deployment constraints
- able to recover from failure

A system that gives the right answer but cannot show how it reached that answer is incomplete for this repository.

## Evaluation dimensions

| Dimension | Question |
|---|---|
| Correctness | Did the system produce the expected result? |
| Sparsity | How little of the reasoning structure was activated? |
| Traceability | Can the reasoning path be inspected? |
| Generalization | Does the system work on unseen combinations? |
| Latency | Can it run under useful time constraints? |
| Robustness | Does it handle noisy, missing, or contradictory input? |
| Recovery | Can it revise behavior after failure? |
| Human inspectability | Can a human understand the result and failure mode? |

## Correctness

Correctness measures whether the system produced the expected answer, plan, state, rule, or action.

Examples:

- logical task answer matches expected output
- symbolic state contains the correct predicates
- retrieved concept is relevant to the task
- induced rule matches observed examples
- planner selects a valid sequence of steps

Basic format:

```text
correct=true|false
expected=<expected output>
actual=<actual output>
```

Correctness is necessary, but not sufficient.

## Sparsity

Sparsity measures how much of the reasoning system was activated.

This matters because the repository is focused on sparse, controlled reasoning rather than dense activation.

Possible measures:

```text
active_rules / total_rules
retrieved_concepts / total_concepts
active_predicates / available_predicates
selected_steps / candidate_steps
```

Example:

```text
active_rules=2
total_rules=8
sparsity_ratio=0.25
```

A lower sparsity ratio is not always better. The goal is minimal sufficient activation, not blind compression.

## Traceability

Traceability measures whether the reasoning path can be inspected.

A useful trace should show:

- input state
- retrieved concepts
- activated rules
- selected plan
- action or output
- evaluation result
- failure or recovery notes

Trace quality levels:

| Level | Meaning |
|---|---|
| None | No reasoning path is visible |
| Low | Trace exists but is vague or incomplete |
| Medium | Trace shows major steps but lacks detail |
| High | Trace clearly shows state, rules, decisions, and result |

Example:

```text
trace_clarity=high
trace_steps=5
missing_trace_fields=[]
```

## Generalization

Generalization measures whether the system works on unseen but related cases.

Examples:

- a rule learned from glass cups also applies to glass bowls
- a relation extractor works on new object positions
- sparse reasoning handles new logical combinations
- concept retrieval works for related but non-identical tasks

Possible measures:

```text
seen_accuracy
unseen_accuracy
generalization_gap
```

Example:

```text
seen_accuracy=0.95
unseen_accuracy=0.82
generalization_gap=0.13
```

## Latency

Latency measures whether the reasoning system can run within practical constraints.

This matters for embodied agents and robotics. Reasoning that is too slow may be unusable even if it is correct.

Possible measures:

```text
parse_time_ms
retrieval_time_ms
rule_activation_time_ms
planning_time_ms
total_time_ms
```

Example:

```text
total_time_ms=14
```

Early prototypes do not need hard real-time performance, but they should measure latency from the beginning.

## Robustness

Robustness measures how the system behaves under imperfect inputs.

Test cases should include:

- missing attributes
- noisy confidence values
- contradictory predicates
- irrelevant concepts
- incomplete episodes
- ambiguous task descriptions

A robust system should degrade gracefully and expose uncertainty.

Example output:

```text
status=partial
reason=missing_attribute
missing_fields=[material]
confidence=0.62
```

## Recovery

Recovery measures whether the system can change behavior after failure.

Examples:

- failed rule activation triggers alternate rule
- failed plan triggers replanning
- failed action updates concept memory
- repeated failure produces a candidate rule

Possible statuses:

```text
not_needed
recovered
partial_recovery
failed_to_recover
```

Example:

```text
recovery_status=recovered
initial_strategy=high_force_grasp
revised_strategy=low_force_grasp
reason=fragile_object_failure
```

## Project-specific evaluation

## Project 01: Sparse Logical Reasoning

Primary metrics:

- answer correctness
- active rule count
- sparsity ratio
- trace clarity
- latency

Minimum result table:

| Task | Expected | Actual | Correct | Active rules | Total rules | Sparsity ratio |
|---|---|---|---:|---:|---:|---:|
| fragile object safety | unsafe | unsafe | true | 2 | 8 | 0.25 |

## Project 02: Memory-Backed Concepts

Primary metrics:

- retrieval relevance
- concept reuse
- reasoning impact
- update quality
- trace clarity

Minimum result table:

| Task | Retrieved concept | Relevant | Decision impact | Outcome | Memory updated |
|---|---|---:|---|---|---:|
| pick glass cup | fragile_object | true | reduce_grip_force | success | true |

## Project 03: Visual-to-Symbolic State

Primary metrics:

- object accuracy
- attribute accuracy
- relation accuracy
- predicate completeness
- state consistency
- trace clarity

Minimum result table:

| Scene | Objects correct | Attributes correct | Relations correct | Predicate completeness | Valid state |
|---|---:|---:|---:|---:|---:|
| scene_001 | 2/2 | 4/4 | 1/1 | 1.0 | true |

## Project 04: Rule Induction

Primary metrics:

- rule correctness
- coverage
- precision
- confidence calibration
- conflict rate
- future decision impact

Minimum result table:

| Rule | Source episodes | Coverage | Precision | Confidence | Status |
|---|---:|---:|---:|---:|---|
| fragile_low_force | 4 | 0.75 | 0.80 | 0.78 | candidate |

## EvaluationResult format

A minimal evaluation result should include:

```text
evaluation_id
target_id
project
correctness
sparsity
trace_clarity
latency_ms
robustness_status
recovery_status
notes
```

Example:

```text
evaluation_id: eval_001
target_id: task_001
project: sparse_logical_reasoning
correctness: true
sparsity:
  active_rules: 2
  total_rules: 8
  ratio: 0.25
trace_clarity: high
latency_ms: 14
robustness_status: not_tested
recovery_status: not_needed
notes: Correct result with minimal rule activation.
```

## Failure reporting

Failures should be treated as useful data.

A failure report should include:

```text
failure_id
task_id
expected
actual
failure_type
failed_layer
trace
possible_cause
next_action
```

Failure types:

```text
wrong_answer
missing_state
bad_retrieval
rule_conflict
invalid_plan
execution_failure
trace_missing
latency_exceeded
```

## Completion criteria

A project should not be called complete unless it has:

- runnable examples
- expected outputs
- evaluation metrics
- result table
- failure cases
- reasoning traces
- basic tests

## Summary

The repository evaluates reasoning as a full system behavior, not just answer generation.

The standard is:

```text
correct answer + sparse activation + inspectable trace + measurable behavior
```

That is the evaluation bar for every project in this repository.
