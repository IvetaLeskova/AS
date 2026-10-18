# Literature review and comparison

## Purpose and scope

This focused review connects the Task Manager experiment to published work on
feature modelling and automated validation. It is a starting point for the essay,
not a systematic review or a benchmark against another implementation. The three
sources were selected for modelling foundations, logical semantics and analysis
terminology. They are historical foundations rather than a survey of current tools.

## 1. Modelling commonality and variability: Kang et al. (1990)

The FODA report describes feature diagrams and composition rules. Its window
manager case study includes requires and mutual-exclusion relationships, with
automated support for checking feature selections. Relevant reading is Sections
7.3.2.2 and 7.3.2.6. [FODA report, SEI PDF](https://www.sei.cmu.edu/documents/1011/1990_005_001_15872.pdf)

**Comparison with our project:** Core represents common functionality, while
Priority, Categories, Deadlines, Statistics and Export represent variation.
Our two dependencies are composition rules of the requires kind. The project
implements a small subset: a flat model with mandatory/optional declarations
and requires rules. It does not implement mutual exclusion, feature groups or
FODA's full domain-analysis process. Its requirements were chosen for a teaching
example rather than derived from a study of existing Task Manager products.

## 2. Logical semantics and reasoning: Batory (2005)

Batory connects feature models with grammars and propositional formulas. The
work supports general propositional constraints, constraint propagation through
a logic truth maintenance system, and SAT-based checks during model debugging.
Relevant reading is Sections 3, 4 and 5.2 of the university technical-report
version. [Batory, UT Austin PDF](https://www.cs.utexas.edu/ftp/techreports/tr05-14.pdf)

**Our derivation using that logical viewpoint:** With the Task Manager root
assumed selected, the current model can be written as:

```text
Core AND (Statistics -> Categories) AND (Export -> Statistics)
```

Equivalently:

```text
Core AND (NOT Statistics OR Categories) AND (NOT Export OR Statistics)
```

Priority and Deadlines are unconstrained Boolean variables. Our validator checks
each implication directly for a given assignment. The analysis script enumerates
assignments to count valid products. It does not translate models into a SAT
solver's input or perform automatic constraint propagation.

For example, `{Core: true, Export: true}` is invalid in our API because omitted
features are treated as unselected. A partial-configuration solver could instead
leave omitted features undecided and ask whether a valid completion exists.
Selecting Statistics and Categories would complete this example. These are
different questions; our validator implements the complete-selection check.

## 3. Positioning the analysis: Benavides, Segura and Ruiz-Cortés (2010)

The review distinguishes valid-product checking (Section 5.2), valid partial
configuration (5.3), listing all products (5.4), and counting products (5.5).
Its Section 6 discusses automated support using propositional logic, constraint
programming, description logic and other methods.
[Author-uploaded paper](https://www.researchgate.net/publication/223760542_Automated_analysis_of_feature_models_20_years_later_A_literature_review)

**Mapping our implementation to these operations:**

| Operation in the review | Corresponding project behaviour |
| --- | --- |
| Valid product | `validate(model, configuration)` checks a selected product. |
| All products | Filtering generated rows by `valid: true` yields every valid product of this model. |
| Number of products | `valid_configurations` counts those products. |
| Valid partial configuration | Not implemented; omitted features mean false, not undecided. |

The last distinction prevents claiming a capability the code does not provide.
The root is implicit in the project's JSON configurations, while Core is an
explicit mandatory selection. Listing all candidate assignments, including
invalid ones, is our way to expose evidence for the comparison experiment.

## Comparison of scope and method

The following assessment concerns capabilities and conceptual agreement; we have
not executed the published tools on our inputs.

| Dimension | Published reference point | This project |
| --- | --- | --- |
| Feature relationships | FODA includes composition rules [1]. | Mandatory and optional declarations, two requires rules. |
| Logical expressiveness | Batory supports propositional constraints [2]. | Direct checks of the supported requires rules. |
| Reasoning | Batory uses propagation and SAT-based checking [2]. | One complete selection checked at a time; enumeration for analysis. |
| Analysis operations | The review separates checking, listing and counting [3]. | All three are demonstrated on a small model. |
| Diagnostics | Batory discusses explanations of inferred selections [2]. | Messages identify directly violated rules; no inferred selections. |

## Relating our measured results to the literature

Our experiment found 32, 24 and 16 valid products for S0, S1 and S2, respectively.
These are measurements for our Task Manager model, not counts reported by these
authors. The shrinking sets illustrate the constraint-based interpretation above:
adding a conjunction restricts the assignments that satisfy the model.

The project's contribution is an explainable example linking a diagram, JSON
rules, validation messages and exhaustive results. Its 50% rejection rate is a
property of these features and dependencies; it is not an improvement over a
published algorithm. Different models need not have comparable rejection rates.

Enumeration checks 2^n candidates for n optional features. Its transparency is
useful for this five-feature example. No runtime comparison, scalability claim,
proof of general validator correctness or claim of a new validation method follows
from this experiment. The independent manual counts and automated tests support
the reported small-model results.

## References and reading notes

1. K. C. Kang, S. G. Cohen, J. A. Hess, W. E. Novak and A. S. Peterson.
   *Feature-Oriented Domain Analysis (FODA) Feasibility Study*. Technical Report
   CMU/SEI-90-TR-021, Software Engineering Institute, Carnegie Mellon University,
   1990. [Official record](https://www.sei.cmu.edu/library/feature-oriented-domain-analysis-foda-feasibility-study/).
2. D. Batory. *Feature Models, Grammars, and Propositional Formulas*. In
   *Software Product Lines (SPLC 2005)*, LNCS 3714, pp. 7–20, 2005.
   [DOI: 10.1007/11554844_3](https://doi.org/10.1007/11554844_3).
   The text consulted here is UT Austin Technical Report 05-14, March 2005,
   with the same title. Section references above refer to that version;
   check the conference version before using conference page-specific citations.
3. D. Benavides, S. Segura and A. Ruiz-Cortés. *Automated analysis of feature
   models 20 years later: A literature review*. Information Systems, 35(6),
   pp. 615–636, 2010. [DOI: 10.1016/j.is.2010.01.001](https://doi.org/10.1016/j.is.2010.01.001).
   [University repository record](https://idus.us.es/items/1caeeba0-3d7b-4c06-bb65-9045a54fa136).
   The consulted full text is the author-uploaded preprint linked in Section 3;
   the repository download could not be retrieved during this review.

No passages from the sources are quoted verbatim. The comparisons and Task
Manager logical formulas are our analysis of the project. Before final submission,
read the indicated sections and adapt this material to the essay's length and
required citation format.
