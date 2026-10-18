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

`../results/` is reserved for later experiments. Configuration enumeration and
statistical analysis are deferred. Enterprise Architect diagrams are maintained
separately. Older placeholder directories remain unused.
