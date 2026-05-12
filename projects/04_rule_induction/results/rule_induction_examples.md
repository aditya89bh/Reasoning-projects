# Rule Induction Examples

This document summarizes the expected behavior of the rule induction prototype.

The prototype demonstrates a minimal learning loop:

```text
Episodes → Pattern detection → Candidate rules → Rule scoring → Rule memory → Future task application
```

The goal is not full automated scientific discovery. The goal is to show how repeated experience can become explicit, inspectable rules that affect future behavior.

## Input episodes

The demo uses structured episodes from `examples/episodes.json`.

Each episode contains:

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
```

## Expected repeated patterns

The pattern detector should find repeated fact/action/outcome patterns such as:

| Fact | Action | Outcome | Meaning |
|---|---|---|---|
| `object_fragile` | `high_force_grasp` | `failure` | Fragile objects fail under high-force grasp |
| `grip_force_high` | `high_force_grasp` | `failure` | High grip force creates failure pattern |
| `grip_force_low` | `low_force_grasp` | `success` | Low-force grasp succeeds in relevant cases |
| `path_blocked` | `direct_path_plan` | `failure` | Direct path fails when path is blocked |
| `operator_prefers_review` | `manual_review` | `success` | Manual review succeeds when operator prefers review |

## Expected candidate rules

Candidate rules are generated from repeated patterns.

Examples:

```text
If object_fragile then avoid_high_force_grasp
```

```text
If grip_force_low then prefer_low_force_grasp
```

```text
If path_blocked then avoid_direct_path_plan
```

```text
If operator_prefers_review then prefer_manual_review
```

## Rule scoring

Rules are scored using:

| Metric | Meaning |
|---|---|
| Coverage | How many episodes match the rule condition? |
| Precision | How often the rule effect matches observed outcomes? |
| Confidence | Combined score from precision, coverage, and evidence count |
| Failure cases | Matching episodes where the rule did not explain the outcome |
| Status | `candidate` or `accepted` |

A rule becomes accepted when it has enough confidence and precision.

## Expected rule memory behavior

Rule memory stores both candidate and accepted rules.

Expected behavior:

```text
candidate rules are retained for inspection
accepted rules can be applied to future tasks
matching is explicit through rule conditions
```

## Future task application

The demo applies stored rules to future task facts.

| Future task | Facts | Expected recommendation |
|---|---|---|
| `future_fragile_high_force` | `object_fragile`, `grip_force_high` | `avoid_high_force_grasp` |
| `future_blocked_path` | `path_blocked`, `target_visible` | `avoid_direct_path_plan` |
| `future_operator_review` | `operator_prefers_review`, `task_sensitive` | `prefer_manual_review` |
| `future_no_match` | `object_standard`, `path_clear` | `no_rule_recommendation` |

## Example rule application trace

Expected trace shape:

```text
Task: future_fragile_high_force
Facts: object_fragile, grip_force_high
Matched rule_...: conditions [object_fragile] -> effect [avoid_high_force_grasp], confidence=<score>
Effects: avoid_high_force_grasp
Recommendation: avoid_high_force_grasp
```

## Example no-match trace

```text
Task: future_no_match
Facts: object_standard, path_clear
No induced rules matched.
Recommendation: no_rule_recommendation
```

## Evaluation dimensions

| Metric | Meaning |
|---|---|
| Pattern detection | Were repeated patterns detected correctly? |
| Rule generation | Were candidate rules created from patterns? |
| Rule scoring | Were rules scored using coverage and precision? |
| Rule memory | Were rules stored and retrievable? |
| Future application | Did induced rules influence future recommendations? |
| Trace clarity | Can rule origin and use be inspected? |

## What this prototype proves

This project proves a minimal experience-to-rule loop:

```text
repeated episodes → explicit rule → scored rule → stored rule → future recommendation
```

That loop is the learning layer of the reasoning stack.

## Run command

From the repository root:

```bash
python projects/04_rule_induction/run_demo.py
```

## Test command

From the repository root:

```bash
python -m pytest projects/04_rule_induction/tests
```

## Current limitations

- Pattern detection is simple fact/action/outcome grouping.
- Rule generation uses deterministic templates.
- No natural language rule explanation yet.
- No conflict resolution between induced rules yet.
- No persistent `induced_rules.json` output yet.
- No integration with Project 01 or Project 02 yet.
- No probabilistic or causal rule learning yet.

## Next improvement

The next useful improvement is to persist induced rules into:

```text
examples/induced_rules.json
```

Then connect induced rules to Project 01 sparse rule selection and Project 02 concept memory.
