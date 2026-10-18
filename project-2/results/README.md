# Configuration experiment results

## Method

The experiment evaluates how dependency constraints change the set of valid
Task Manager configurations. Core stays selected. All 32 combinations of the
five optional features are checked in each scenario using the same validator.
Only the active constraints change; no candidates are repaired or removed before
validation. The model file is unchanged. See [experiment design](../experiment-design.md).

## Measured comparison

| Scenario | Active constraints | Total | Valid | Invalid | Rejected |
| --- | --- | ---: | ---: | ---: | ---: |
| S0 | None | 32 | 32 | 0 | 0% |
| S1 | Statistics requires Categories | 32 | 24 | 8 | 25% |
| S2 | S1 plus Export requires Statistics | 32 | 16 | 16 | 50% |

These measured counts agree with the independent manual derivation in the design.
S0 and S1 are experimental variants. S2 is the complete intended Task Manager model.

## Interpretation

With no dependencies, each optional feature is independent and all 32 candidates
are valid. The first rule rejects selections with Statistics enabled and
Categories disabled. Three other optional features remain free, so this excludes
2^3 = 8 candidates.

The second rule excludes eight more candidates with Export enabled and Statistics
disabled. These cannot also violate the first rule, which needs Statistics enabled.
The valid set therefore shrinks from 32 to 24 to 16. Relative to S1, the second
rule removes one third of its 24 valid candidates; relative to all 32 candidates,
the rejection percentage rises by 25 percentage points.

An independent explanation considers (Categories, Statistics, Export). Only
(0,0,0), (1,0,0), (1,1,0) and (1,1,1) satisfy both dependencies. Priority and
Deadlines each have two independent choices, giving 4 × 2 × 2 = 16 valid products.

Core + Export illustrates the comparison: it is valid in S0 and S1 but invalid
in S2. In the intended model, selecting Export also needs Statistics and,
through that dependency, Categories. The validator reports directly violated
rules rather than automatically enabling missing features.

The results demonstrate that the feature model defines which selections are
allowed and that a model-driven validator can identify violations automatically.
A higher rejection percentage means a more restricted configuration space;
it does not establish better application quality.

## Evidence files

- `comparison.json`: active constraints and measurements for every scenario.
- `scenarios/S0.json`, `scenarios/S1.json`, `scenarios/S2.json`: active constraints,
  measurements and all 32 candidates with their validity and reasons.
- `summary.json` and `configurations.json`: the complete model's results,
  preserving the original output format.

Reason counts measure how many candidates violate each rule. They can overlap
in other models, so the invalid count is calculated per candidate. In S2 each
rule has eight violations and their violation sets happen to be disjoint.

## Reproduce and verify

From `project-2/`, use Python 3.12 (or your environment's Python command):

```text
python analyze_configurations.py
python -m pytest tests -q
```

On macOS without an activated virtual environment, `python3` can run the analysis.
The script uses only the standard library. Tests require pytest. Each run
overwrites the generated JSON files for the active scenarios, with deterministic
ordering. It leaves this README untouched.

Tests verify the manually expected counts, identical candidate spaces, shrinking
valid sets, unchanged input model and reproducible CLI output. Existing validator
tests separately cover missing mandatory features and malformed selections.

## Limitations

This is an exhaustive evaluation of one small model with requires constraints.
It does not establish scalability, performance, user benefits or application
correctness. Enumeration requires 2^n candidates for n optional features. The
validity of the domain dependencies themselves is assumed. A conceptual comparison
with published work is provided in the [literature review](../literature-review.md);
no comparison against an external tool has been measured.
