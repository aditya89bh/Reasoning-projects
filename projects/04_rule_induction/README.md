# Project 04: Rule Induction

This project explores how reasoning systems can learn explicit rules from examples, feedback, or repeated experience.

The current prototype implements a small experience-to-rule loop. It loads structured episodes, detects repeated patterns, generates candidate rules, scores them, stores them in rule memory, and applies accepted rules to future task facts.

## Core question

```text
Can the system learn rules instead of only learning policies?
```

## Current status

```text
Runnable first prototype
```

This project now includes:

- episode data model
- induced rule data model
- pattern detector
- candidate rule generator
- rule scorer
- rule memory store
- rule applier
- example episodes
- command-line demo
- tests
- rule induction result documentation

Estimated project status:

```text
65-70% complete
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

## Architecture

```text
Episodes → Pattern Detection → Candidate Rule Generation → Rule Scoring → Rule Memory → Future Task Application
```

The first prototype uses deterministic pattern detection and templated rule generation. This keeps the rule-learning loop inspectable before adding probabilistic, causal, or neural rule learning.

## Components

| File | Role |
|---|---|
| `src/episode.py` | Defines structured task episodes |
| `src/rule.py` | Defines induced rule objects |
| `src/pattern_detector.py` | Finds repeated fact/action/outcome patterns |
| `src/rule_generator.py` | Converts patterns into candidate rules |
| `src/rule_scorer.py` | Scores candidate rules using coverage, precision, and confidence |
| `src/rule_memory.py` | Stores candidate and accepted rules |
| `src/rule_applier.py` | Applies induced rules to future task facts |
| `examples/episodes.json` | Seed episodes used for induction |
| `run_demo.py` | Runs the full induction and application loop |
| `tests/test_rule_induction.py` | Regression tests for rule induction behavior |
| `results/rule_induction_examples.md` | Documents expected rule induction behavior |

## Episode schema

A minimal episode includes:

```text
episode_id
facts
action
outcome
feedback
constraints
notes
```

Example:

```text
episode_id: ep_001
facts: object_fragile, grip_force_high
action: high_force_grasp
outcome: failure
feedback: Fragile object slipped and cracked under high force.
constraints: fragile_object
notes: High force was unsafe for fragile object.
```

## Rule format

An induced rule includes:

```text
rule_id
name
conditions
effect
source_episodes
confidence
coverage
precision
failure_cases
status
```

Example:

```text
rule_id: rule_000_object_fragile_avoid_high_force_grasp
name: If object_fragile then avoid_high_force_grasp
conditions:
  - object_fragile
effect: avoid_high_force_grasp
source_episodes:
  - ep_001
  - ep_002
confidence: <computed>
coverage: <computed>
precision: <computed>
status: candidate or accepted
```

## Rule scoring

Candidate rules are scored with:

| Score | Meaning |
|---|---|
| Coverage | How many episodes match the rule condition? |
| Precision | How often the rule effect matches observed outcomes? |
| Confidence | Combined score from precision, coverage, and evidence count |
| Failure cases | Episodes where the condition matched but the effect did not explain the outcome |
| Status | `candidate` or `accepted` |

A rule becomes accepted when confidence and precision cross the prototype thresholds.

## Demo behavior

The demo performs this loop:

1. Load episodes from `examples/episodes.json`.
2. Detect repeated fact/action/outcome patterns.
3. Generate candidate rules from patterns.
4. Score candidate rules.
5. Store rules in rule memory.
6. Apply accepted rules to future tasks.
7. Print rule traces and recommendation summary.

## Future task examples

| Future task | Facts | Expected recommendation |
|---|---|---|
| `future_fragile_high_force` | `object_fragile`, `grip_force_high` | `avoid_high_force_grasp` |
| `future_blocked_path` | `path_blocked`, `target_visible` | `avoid_direct_path_plan` |
| `future_operator_review` | `operator_prefers_review`, `task_sensitive` | `prefer_manual_review` |
| `future_no_match` | `object_standard`, `path_clear` | `no_rule_recommendation` |

## Run the demo

From the repository root:

```bash
python projects/04_rule_induction/run_demo.py
```

The demo prints:

- loaded episode count
- detected patterns
- scored candidate rules
- accepted/candidate rule counts
- future task recommendations
- application traces
- aggregate recommendation accuracy

## Run tests

From the repository root:

```bash
python -m pytest projects/04_rule_induction/tests
```

## Example trace

```text
Task: future_fragile_high_force
Facts: object_fragile, grip_force_high
Matched rule_...: conditions [object_fragile] -> effect [avoid_high_force_grasp], confidence=<score>
Effects: avoid_high_force_grasp
Recommendation: avoid_high_force_grasp
```

## Evaluation metrics

| Metric | Meaning |
|---|---|
| Pattern detection | Were repeated patterns detected correctly? |
| Rule generation | Were candidate rules created from patterns? |
| Rule scoring | Were rules scored with coverage and precision? |
| Rule memory | Were rules stored and retrievable? |
| Future application | Did induced rules influence future recommendations? |
| Trace clarity | Can rule origin and use be inspected? |

## What this prototype proves

This project does not claim full rule learning yet.

It proves the smaller operational loop:

```text
repeated episodes → explicit rule → scored rule → stored rule → future recommendation
```

That loop is the learning layer of the reasoning stack.

## Current limitations

- Pattern detection is simple fact/action/outcome grouping.
- Rule generation uses deterministic templates.
- No natural language rule explanation yet.
- No conflict resolution between induced rules yet.
- No persistent `induced_rules.json` output yet.
- No integration with Project 01 or Project 02 yet.
- No probabilistic or causal rule learning yet.

## Next steps

1. Persist generated rules to `examples/induced_rules.json`.
2. Add conflict handling between induced rules.
3. Add richer multi-condition rule generation.
4. Capture actual demo output in results.
5. Connect induced rules to Project 01 sparse rule selection.
6. Connect repeated failures to Project 02 concept memory.
7. Add natural-language summaries for induced rules.

## Completion target

This project reaches a stronger milestone when it has:

- persistent induced rule output
- multi-condition rules
- conflict resolution
- actual demo output captured in results
- integration with sparse reasoning and concept memory

At that point, Project 04 becomes a more serious learning layer for the repository.
