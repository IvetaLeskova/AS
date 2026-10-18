# Task Manager feature model

Research question: How can a feature model describe variants of a Task Manager
and determine which combinations of features are valid?

`model.json` describes the product, mandatory and optional features, and
cross-tree constraints. The validator reads these declarations rather than
hard-coding Task Manager feature names.

- **Core** is mandatory: create, view, update and delete tasks, change their
  TODO / DONE status, and persist them. These capabilities are documented here;
  this project does not implement a Task Manager application.
- **Priority**, **Categories**, **Deadlines**, **Statistics**, and **Export** are optional.
- **Statistics requires Categories**.
- **Export requires Statistics**; consequently, selecting Export also needs Categories.

Configurations are JSON objects mapping feature names to booleans. Missing
features are treated as unselected. A missing or false mandatory feature,
an unknown feature, a non-boolean value, or a violated dependency makes a
configuration invalid. Validation reports all directly violated rules. For
example, Core + Export reports that Export requires Statistics; once Statistics
is selected, it also requires Categories. No features are automatically enabled.

## Examples

| File | Selected features | Expected result |
| --- | --- | --- |
| `configurations/basic.json` | Core | VALID |
| `configurations/student.json` | Core, Priority, Deadlines | VALID |
| `configurations/full.json` | All features | VALID |
| `configurations/invalid/statistics-without-categories.json` | Core, Statistics | INVALID |
| `configurations/invalid/export-without-statistics.json` | Core, Categories, Export | INVALID |

## Run validation and tests

Use Python 3.12. From `project-2/`, run the following commands on macOS or Windows
(use `python3.12` or `py -3.12` instead of `python` if needed):

```text
python -m validator.validator feature-model/configurations/basic.json
python -m validator.validator feature-model/configurations/invalid/statistics-without-categories.json
python -m pip install pytest
python -m pytest tests
```

The validator prints VALID or INVALID followed by reasons. Exit codes are 0 for
valid configurations, 1 for invalid configurations, and 2 for input errors.
Use `--model path/to/model.json` to select another model. The model is expected
to follow the structure of `model.json`; only `requires` constraints are supported.

The validator uses only the Python standard library; pytest is needed for tests.
Tests cover example files, mandatory features, dependencies, unknown features,
boolean values, and a model with different feature names.

## Configuration experiment

From `project-2/`, run:

```text
python analyze_configurations.py
```

On macOS, if using the project's virtual environment, first activate it with
`source .venv/bin/activate`. Alternatively use `python3` for the experiment,
which needs no third-party packages.

The script reads the model and enumerates every false/true combination of its
optional features, keeping mandatory features selected. It calls the existing
validator for each configuration. It does not add or repair selected features.
It repeats this analysis with no constraints, then with each successive prefix
of the constraints listed in the model. For the current model these are S0
(none), S1 (Statistics requires Categories), and S2 (both rules).

Results are saved in `../results/`:

- `summary.json`: total, valid and invalid counts, rejection percentage, and
  the number of configurations violating each dependency.
- `configurations.json`: every configuration, its validity, and failure reasons.
- `comparison.json`: active constraints and summaries for all scenarios.
- `scenarios/S0.json`, `scenarios/S1.json`, `scenarios/S2.json`: per-scenario
  constraints, summary and complete configuration results.

The original two files always describe the complete model. Each run overwrites
the generated files for its active scenarios. The ordering is deterministic.
Use `--model path/to/model.json` or `--output-dir path/to/results` to change inputs
or the output directory.

For the current model, five optional features give 2^5 = 32 combinations.
Exactly 16 are valid and 16 are invalid, so constraints reject 50%.
Each dependency is violated in eight configurations. In general, one
configuration can violate multiple rules, so reason counts should not be added
to calculate the number of invalid configurations.

The counts can also be explained without running the program: Categories,
Statistics and Export allow four selections (none; Categories; Categories with
Statistics; all three). Priority and Deadlines each have two independent choices,
giving 4 × 2 × 2 = 16 valid products.

This experiment measures dependency violations with Core always selected;
missing mandatory features and malformed input remain covered by validator tests.
Enterprise Architect diagrams are maintained separately.

The comparison produces 32, 24 and 16 valid configurations, respectively.
See [results and interpretation](../results/README.md) and the
[experiment design](../experiment-design.md).
