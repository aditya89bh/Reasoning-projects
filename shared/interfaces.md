# Shared Interfaces

This document defines the common interfaces used across the reasoning projects.

The goal is to keep the stack modular. Each project can evolve independently, but the outputs should remain compatible with the larger reasoning architecture.

## Core principle

Each layer should communicate through explicit structures rather than hidden assumptions.

```text
Perception → SymbolicState → ConceptMemory → RuleActivations → Plan → ActionResult → EvaluationResult
```

## Interface overview

| Interface | Used by | Purpose |
|---|---|---|
| `Observation` | Perception layer | Raw or structured input from the world |
| `SymbolicState` | Visual-to-symbolic state | Reasoning-ready world representation |
| `Concept` | Memory-backed concepts | Reusable abstraction stored outside weights |
| `ConceptQuery` | Memory retrieval | Query used to retrieve relevant concepts |
| `Rule` | Rule system | Explicit condition-action or inference structure |
| `RuleActivation` | Sparse reasoning | Record of which rules fired and why |
| `Plan` | Planner | Ordered reasoning or action steps |
| `ActionResult` | Action layer | Result of executing or simulating a step |
| `ReasoningTrace` | All layers | Inspectable path of reasoning |
| `EvaluationResult` | Evaluation layer | Measures correctness, sparsity, and recovery |

## Observation

An `Observation` is the input received from perception, a simulator, a structured file, or a robot state source.

Minimal fields:

```text
observation_id
timestamp
source
payload
confidence
metadata
```

Example:

```text
observation_id: obs_001
timestamp: 2026-05-12T10:30:00
source: structured_scene
payload:
  objects:
    - id: block_1
      color: red
      shape: cube
      x: 1
      y: 2
confidence: 1.0
metadata:
  episode_id: scene_001
```

## SymbolicState

A `SymbolicState` represents the world in reasoning-ready form.

Minimal fields:

```text
state_id
episode_id
timestamp
objects
attributes
relations
predicates
confidence
source_observation_ids
```

Example:

```text
state_id: state_001
episode_id: scene_001
objects:
  - block_1
  - block_2
attributes:
  - color(block_1, red)
  - shape(block_1, cube)
relations:
  - left_of(block_1, block_2)
predicates:
  - object(block_1)
  - color(block_1, red)
  - shape(block_1, cube)
  - left_of(block_1, block_2)
confidence: 0.95
```

## Concept

A `Concept` is reusable knowledge stored outside model parameters.

Minimal fields:

```text
concept_id
name
description
trigger_conditions
recommended_effect
confidence
evidence
last_used
failure_notes
status
```

Example:

```text
concept_id: concept_fragile_object
name: fragile_object
description: Object should be handled with reduced force.
trigger_conditions:
  - material == glass
  - tag == fragile
recommended_effect:
  - reduce_grip_force
  - slow_approach_speed
confidence: 0.85
evidence:
  - ep_001
  - ep_004
status: active
```

## ConceptQuery

A `ConceptQuery` is used to retrieve relevant concepts from memory.

Minimal fields:

```text
query_id
state_context
task_context
constraints
failure_context
retrieval_mode
limit
```

Retrieval modes:

```text
attribute_match
task_match
failure_match
constraint_match
hybrid_match
```

## Rule

A `Rule` is an explicit condition-action or condition-inference structure.

Minimal fields:

```text
rule_id
name
condition
effect
confidence
source
status
created_from
failure_cases
```

Example:

```text
rule_id: rule_fragile_low_force
name: fragile_low_force_rule
condition: object.material == glass OR object.tag == fragile
effect: reduce_grip_force
confidence: 0.78
source: induced_from_episodes
created_from:
  - ep_001
  - ep_004
status: candidate
```

## RuleActivation

A `RuleActivation` records which rule fired, under what condition, and with what effect.

Minimal fields:

```text
activation_id
rule_id
matched_conditions
input_state_id
effect
confidence
trace_note
```

Example:

```text
activation_id: act_001
rule_id: rule_fragile_low_force
matched_conditions:
  - material(glass_cup_12, glass)
effect: reduce_grip_force
confidence: 0.81
trace_note: Glass object matched fragile handling rule.
```

## Plan

A `Plan` is an ordered structure of reasoning or action steps.

Minimal fields:

```text
plan_id
goal
strategy
steps
assumptions
constraints
success_criteria
failure_conditions
```

Example:

```text
plan_id: plan_001
goal: pick glass_cup_12
strategy: low_force_pick
steps:
  - approach slowly
  - reduce grip force
  - close gripper
  - lift object
constraints:
  - object is fragile
success_criteria:
  - object lifted without slip
failure_conditions:
  - object slips
  - force threshold exceeded
```

## ActionResult

An `ActionResult` records the result of executing or simulating a step.

Minimal fields:

```text
action_id
plan_id
step_id
action_type
status
output
error
metadata
```

Possible statuses:

```text
success
failure
partial
skipped
not_run
```

## ReasoningTrace

A `ReasoningTrace` is the debugging surface of the reasoning system.

Minimal fields:

```text
trace_id
goal
input_state_id
retrieved_concepts
activated_rules
selected_plan
action_results
evaluation_result
notes
```

A useful trace should answer:

- What state was used?
- What concepts were retrieved?
- What rules were activated?
- What plan was selected?
- What happened during execution?
- What was evaluated?
- What should change next?

## EvaluationResult

An `EvaluationResult` measures the output of a reasoning step, plan, or project.

Minimal fields:

```text
evaluation_id
target_id
correctness
sparsity
trace_clarity
latency
recovery_status
notes
```

Example:

```text
evaluation_id: eval_001
target_id: plan_001
correctness: true
sparsity:
  active_rules: 2
  total_rules: 8
  ratio: 0.25
trace_clarity: high
latency_ms: 12
recovery_status: not_needed
notes: Correct answer with sparse rule activation.
```

## Versioning note

These interfaces are intentionally minimal. They should evolve as the projects become runnable.

The first priority is consistency, not completeness.

## Integration target

The long-term integrated loop should look like this:

```text
Observation
→ SymbolicState
→ ConceptQuery
→ Concept retrieval
→ Rule activation
→ Plan
→ ActionResult
→ EvaluationResult
→ Memory update
→ ReasoningTrace
```

This gives each project a defined role in the larger reasoning architecture.
