We are working in a university repository for the Software Architecture course at FIIT STU.

IMPORTANT:
Do not modify anything inside project-1 unless I explicitly ask you to.
Project 1 contains a separate architecture-comparison project and must stay untouched.

We are now starting PROJECT 2.

==================================================
PROJECT 2 – SOFTWARE PRODUCT LINES / FEATURE MODEL
==================================================

Original topic:
"Riadenie variability v rade softvérových výrobkov pomocou feature modelu"

After consultation with our instructor, the original scope was considered too broad.
We therefore narrowed the project specifically to FEATURE MODELLING and CONFIGURATION VALIDATION.

Main research question:

"How can a feature model be used to describe variants of a Task Manager and determine which combinations of features are valid?"

The Task Manager is only a small example system.
The main subject of the project is the FEATURE MODEL, constraints between features, and validation of configurations.

==================================================
FEATURE MODEL
==================================================

Root product:

Task Manager

Mandatory feature:

Core

Core contains the common Task Manager functionality:
- Create task
- View tasks
- Update task
- Delete task
- Change task status TODO / DONE
- Persistence

Optional features:

- Priority
- Categories
- Deadlines
- Statistics
- Export

Current cross-tree constraints:

1. Statistics REQUIRES Categories
2. Export REQUIRES Statistics

Examples:

VALID:
Core

VALID:
Core + Priority + Deadlines

VALID:
Core + Categories + Statistics

VALID:
Core + Categories + Statistics + Export

INVALID:
Core + Statistics

Reason:
Statistics requires Categories.

INVALID:
Core + Export

Reason:
Export requires Statistics.
Statistics then requires Categories.

==================================================
PROJECT GOAL
==================================================

We want to demonstrate:

1. how variability of the Task Manager can be represented using a feature model,
2. how mandatory and optional features are represented,
3. how dependencies between features are expressed,
4. how valid and invalid product configurations can be identified,
5. how configuration validity can be checked automatically.

We do NOT currently want to build a large Task Manager application.

The implementation should mainly support the feature-model experiment.

==================================================
PLANNED PROJECT STRUCTURE
==================================================

Create/use this structure inside:

project-2/

Preferred structure:

project-2/
├── feature-model/
│   ├── model.json
│   ├── README.md
│   └── configurations/
│       ├── basic.json
│       ├── student.json
│       ├── full.json
│       └── invalid/
│
├── validator/
│   ├── __init__.py
│   └── validator.py
│
├── tests/
│   └── test_validator.py
│
└── results/

Do not create unnecessary architecture layers unless they are needed.

==================================================
MODEL REPRESENTATION
==================================================

The feature model should have a machine-readable representation.

Start with JSON.

Example structure:

{
  "product": "Task Manager",
  "mandatory": [
    "Core"
  ],
  "optional": [
    "Priority",
    "Categories",
    "Deadlines",
    "Statistics",
    "Export"
  ],
  "constraints": [
    {
      "type": "requires",
      "feature": "Statistics",
      "requires": "Categories"
    },
    {
      "type": "requires",
      "feature": "Export",
      "requires": "Statistics"
    }
  ]
}

Do not hard-code the specific feature names into the validation logic if avoidable.

The validator should primarily interpret the model.

==================================================
CONFIGURATION FORMAT
==================================================

A configuration can initially be represented as JSON.

Example:

{
  "Core": true,
  "Priority": true,
  "Categories": false,
  "Deadlines": true,
  "Statistics": false,
  "Export": false
}

The validator should return whether the configuration is VALID or INVALID.

For invalid configurations it should also provide understandable reasons.

Example:

INVALID
Statistics requires Categories.

==================================================
TESTING
==================================================

Use pytest.

We need tests for at least:

- valid Basic configuration,
- valid configuration with optional features,
- Statistics + Categories -> valid,
- Statistics without Categories -> invalid,
- Export + Statistics + Categories -> valid,
- Export without Statistics -> invalid,
- mandatory Core missing -> invalid,
- unknown feature in configuration -> invalid or clearly handled.

Tests should be deterministic and easy to explain in a university presentation.

==================================================
EXPERIMENT / RESULTS
==================================================

Later we want to use the validator to analyse configurations.

Potential measurements include:

- total possible configurations,
- number of valid configurations,
- number of invalid configurations,
- percentage of configurations rejected by constraints,
- reasons for invalid configurations.

Do not implement advanced analysis yet unless I explicitly ask.

==================================================
ENTERPRISE ARCHITECT
==================================================

A teammate is separately preparing diagrams in Enterprise Architect:

1. Feature Model
2. Use Case Diagram
3. Component Diagram

Do not replace those diagrams with generated code diagrams unless I ask.

The code representation should correspond to the same feature model.

==================================================
TECHNICAL REQUIREMENTS
==================================================

Language:
Python 3.12

Testing:
pytest

The code must work on both:
- macOS
- Windows

Therefore:
- do not use hard-coded OS-specific paths,
- use pathlib if filesystem paths are needed,
- do not assume shell-specific behaviour.

Keep dependencies minimal.
Prefer Python standard library where possible.

==================================================
WORKING RULES
==================================================

Before making a large structural change, explain what you want to change.

Do not perform unrelated refactoring.

Do not modify project-1.

Do not silently expand the project scope.

Keep the implementation small and understandable.

This is a university project, so readability and the ability to explain the implementation are more important than enterprise-level complexity.

When implementing a task:
1. tell me briefly what files you plan to create/change,
2. make the implementation,
3. run relevant tests,
4. tell me what was changed and whether the tests passed.

==================================================
FIRST TASK
==================================================

First inspect the current repository.

Do not modify project-1.

Then check whether project-2 already contains any files.

Propose the smallest initial structure required for the feature-model project described above.

Do not implement anything until you have shown me the proposed changes.