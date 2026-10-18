# Experiment design: feature constraints and valid configurations

## Objective

Main research question:

> How can a feature model be used to describe variants of a Task Manager and
> determine which combinations of features are valid?

The experiment addresses a narrower question: how does adding dependency
constraints change the set of valid configurations of the same feature model?

The Task Manager is the example domain. We evaluate feature selections, rather
than the behaviour of a running Task Manager application.

## Model and configuration space

The product root is Task Manager. Core is mandatory. Priority, Categories,
Deadlines, Statistics and Export are optional.

Core remains selected in every experimental configuration. Each of the five
optional features can be selected or unselected, producing 2^5 = 32 candidates.
All 32 candidates are evaluated in every scenario; none are sampled.

The model defines two dependencies:

- C1: Statistics requires Categories.
- C2: Export requires Statistics.

A requires rule A -> B is satisfied when A is unselected or B is selected.
It is violated only when A is selected and B is unselected. Validity requires
all applicable rules to hold. The validator does not automatically select
dependencies or repair a configuration.

## Scenarios

| Scenario | Active dependencies | Purpose |
| --- | --- | --- |
| S0 | None | Baseline with independent optional features |
| S1 | C1 | Measure the effect of the first dependency |
| S2 | C1 and C2 | Evaluate the complete project model |

Only the active dependency set changes. Feature declarations, candidates,
mandatory selections and validator remain identical. S0 and S1 are experimental
variants; S2 remains the intended Task Manager model and matches the diagram.
The canonical `feature-model/model.json` must remain unchanged during comparison.

## Measurements

For each scenario, record:

- Total candidate configurations N.
- Number of valid configurations V.
- Number of invalid configurations I = N - V.
- Rejection percentage R = 100 × I / N.
- Number of candidates violating each active dependency.
- Every candidate's feature values, validity and directly violated rules.

A candidate can violate several rules in a general model. Count it once in I,
but once per violated rule in the reason breakdown. Reason counts therefore
must not generally be summed to calculate I.

## Procedure

1. Load `feature-model/model.json`.
2. Enumerate the 32 unique selections of optional features with Core selected.
3. For S0, S1 and S2, use a copy of the model with the scenario's active rules.
4. Pass every candidate to the existing `validate` function.
5. Save each scenario's measurements and individual validation results.
6. Compare measured results with the independent manual derivation below.
7. Check that adding constraints never makes a previously invalid candidate
   valid: valid(S2) is a subset of valid(S1), which is a subset of valid(S0).

This is a deterministic enumeration, so repeated runs with identical inputs
should produce identical results. Repeated timing trials and significance tests
are unnecessary for these configuration counts.

## Expected results and independent verification

These are manually derived expectations. All three scenarios have now been
measured by the analysis script and agree with these expectations. See
[results and interpretation](results/README.md).

| Scenario | Total | Valid | Invalid | Rejected |
| --- | ---: | ---: | ---: | ---: |
| S0 | 32 | 32 | 0 | 0% |
| S1 | 32 | 24 | 8 | 25% |
| S2 | 32 | 16 | 16 | 50% |

In S0, all optional selections are allowed, so all 32 candidates are valid.

In S1, Statistics selected with Categories unselected violates C1. The other
three optional features have 2^3 = 8 selections, so eight candidates are rejected.

In S2, consider the triple (Categories, Statistics, Export). Its valid values
are (0,0,0), (1,0,0), (1,1,0) and (1,1,1). Priority and Deadlines each have two
independent choices, giving 4 × 2 × 2 = 16 valid configurations.

C1 and C2 each reject eight candidates in S2. Their violation sets are disjoint
here: violating C1 requires Statistics selected, while violating C2 requires
Statistics unselected. The second rule therefore rejects eight additional
candidates, or one third of the 24 that were valid in S1.

Example: Core + Export is valid in S0 and S1, but invalid in S2 because Export
requires Statistics. Core + Statistics is valid in S0 and invalid in S1 and S2
because Statistics requires Categories.

## Interpretation and limitations

The comparison demonstrates how explicit dependencies restrict product choices
and how the validator identifies selections that contradict those dependencies.
The chain Export -> Statistics -> Categories explains why Export indirectly
requires Categories. Direct-rule validation detects invalid selections without
needing a separate transitive rule in the model.

A higher rejection percentage describes a more restricted configuration space;
it does not by itself indicate better software quality or a better model.

The conclusions apply to this small model and these rules. Enumeration grows
as 2^n with n optional features; this experiment provides no performance evidence
for large models. It does not evaluate alternative groups, excludes constraints,
configuration repair, user experience or runtime application behaviour. Dependency
semantics are assumed to reflect the intended domain; the experiment cannot
establish that those domain choices are correct.

Missing mandatory features, unknown names and non-boolean values are tested
separately in the validator tests. They are outside this experiment's deliberately
well-formed candidate space.

## Deliverables and verification

The analysis script runs all three scenarios. It preserves S2 outputs in
`results/summary.json` and `results/configurations.json`, saves the comparison
in `results/comparison.json`, and records complete per-scenario evidence in
`results/scenarios/`. `results/README.md` explains the measured comparison.
Tests check expected counts, identical candidate spaces, the subset relation,
preservation of the canonical model and reproducible output.

The [literature review](literature-review.md) connects these findings to published
feature-model validation approaches, comparing supported rule types, validation
method, diagnostic output and scalability assumptions. It provides a starting
point for the essay. The current validator has not been benchmarked against
another tool, and the project does not claim a novel validation method.
