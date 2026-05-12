# Project 04: Rule Induction

This project explores how reasoning systems can learn explicit rules from examples, feedback, or repeated experience.

The goal is to move beyond fixed hand-written rules and build a small system that can propose, score, store, and reuse human-readable rules.

## Core question

```text
Can the system learn rules instead of only learning policies?
```

## Why this matters

Many intelligent behaviors depend on rules that are not always available upfront.

A deployed agent may discover patterns such as:

- a certain object type fails under high force
- a specific path is blocked in one workcell
- an operator prefers one sequence over another
- a task succeeds only when a constraint is respected
- a repeated failure can be avoided with a new condition

If these patterns stay hidden inside logs or model weights, they are hard to inspect and reuse.

Rule induction makes experience operational.

## Project goal

Build a minimal rule induction system that can:

1. Receive examples or episodes.
2. Detect repeated patterns.
3. Generate candidate rules.
4. Score candidate rules.
5. Store useful rules in memory.
6. Reuse learned rules in future reasoning.
7. Produce a trace explaining where a rule came from.

## Example induced rules

```text
If object is fragile and grip force is high, then action is unsafe.
```

```text
If path is blocked, then select alternate approach direction.
```

```text
If the same failure occurs twice for a part family, then lower confidence in the current strategy.
```

```text
If an operator correction is repeated, then store it as a process preference.
```

## Minimal architecture

```text
Episodes → Pattern Detection → Candidate Rule Generation → Rule Scoring → Rule Memory → Future Use → Evaluation
```

## Components

| Component | Role |
|---|---|
| Episode store | Holds examples, successes, failures, and corrections |
| Pattern detector | Finds repeated conditions and outcomes |
| Rule generator | Converts patterns into candidate rules |
| Rule scorer | Scores usefulness, confidence, and coverage |
| Rule memory | Stores accepted rules |
| Rule applier | Uses learned rules in future reasoning |
| Trace generator | Explains the origin and use of a rule |

## Episode schema

A minimal episode should include:

```text
episode_id
state
action
outcome
feedback
constraints
notes
```

Example:

```text
episode_id: ep_001
state:
  object: glass_cup
  material: glass
  grip_force: high
action:
  pick_object
outcome:
  failure
feedback:
  object slipped and cracked
constraints:
  fragile object
notes:
  high force was unsafe
```

## Candidate rule format

A candidate rule should include:

```text
rule_id
condition
action_or_inference
source_episodes
confidence
coverage
failure_cases
status
```

Example:

```text
rule_id: rule_fragile_low_force
condition: object.material == glass OR object.tag == fragile
action_or_inference: reduce_grip_force
source_episodes: ep_001, ep_004, ep_009
confidence: 0.78
coverage: 3/4
failure_cases: ep_006
status: candidate
```

## Rule scoring

Rules should not be accepted only because they appear once.

Useful scoring dimensions:

| Score | Meaning |
|---|---|
| Confidence | How reliable is the rule? |
| Coverage | How many examples does it explain? |
| Specificity | Is the rule too broad or too narrow? |
| Utility | Does it improve future decisions? |
| Conflict | Does it contradict existing rules? |
| Recency | Is the rule based on recent relevant experience? |

## Rule lifecycle

A learned rule should move through stages.

```text
candidate → accepted → active → revised → deprecated
```

| Stage | Meaning |
|---|---|
| Candidate | Proposed from examples, not trusted yet |
| Accepted | Good enough to store and inspect |
| Active | Used during reasoning |
| Revised | Modified after new evidence |
| Deprecated | Retained for history but no longer used |

## Reasoning trace

The system should explain both rule creation and rule use.

Example creation trace:

```text
Episodes analyzed: ep_001, ep_004, ep_009
Repeated pattern: fragile material + high grip force → failure
Generated rule: reduce grip force for fragile objects
Confidence: 0.78
Status: candidate
```

Example use trace:

```text
Task: pick glass_cup_12
Matched rule: rule_fragile_low_force
Reasoning effect: reduce grip force
Action selected: low-force grasp
Evaluation: success
Rule confidence updated: 0.81
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Rule correctness | Does the rule match real outcomes? |
| Coverage | How many cases does the rule explain? |
| Precision | How often is the rule useful when activated? |
| Generalization | Does the rule work on unseen but related cases? |
| Conflict rate | Does the rule contradict other rules? |
| Trace clarity | Can a human inspect where the rule came from? |
| Decision impact | Did the learned rule improve future behavior? |

## Minimum viable demo

The first demo should use structured example episodes and induce one or more simple rules.

Example target behavior:

```text
Input episodes:
3 failures with glass objects and high grip force
1 success with glass object and low grip force

Generated candidate rule:
if material == glass then reduce_grip_force

Score:
confidence=0.75
coverage=4 episodes
status=candidate

Future task:
pick new glass object

Applied rule:
reduce_grip_force

Evaluation:
success=true
confidence updated
```

## Planned file structure

```text
projects/04_rule_induction/
├── README.md
├── src/
│   ├── episode.py
│   ├── pattern_detector.py
│   ├── rule_generator.py
│   ├── rule_scorer.py
│   ├── rule_memory.py
│   └── rule_applier.py
├── examples/
│   ├── episodes.json
│   └── induced_rules.json
├── tests/
│   └── test_rule_induction.py
└── results/
    └── rule_induction_examples.md
```

## Current status

```text
Design phase
```

This project does not yet have the runnable implementation. The immediate goal is to define the episode schema, candidate rule format, scoring logic, and rule lifecycle.

## Next steps

1. Define the episode schema.
2. Create example episodes.
3. Implement pattern detection.
4. Generate candidate rules.
5. Score candidate rules.
6. Store accepted rules.
7. Apply rules to future tasks.
8. Add trace generation.
9. Add tests and rule examples.

## Completion target

This project reaches a useful first milestone when it has:

- structured episode examples
- candidate rule generation
- rule scoring
- rule memory
- future task application
- trace output
- basic tests

At that point, Project 04 becomes the learning layer of the reasoning stack.
