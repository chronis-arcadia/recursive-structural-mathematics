# RSM v0.2 Primer — Recursive Structural Stability

## 1. Scope

RSM studies the behavior of representations under repeated transformation.

The object of study may be text, code, a graph, a proof representation, a structured record, a plan, or any other state for which the researcher can define:

1. a transformation process,
2. one or more invariants or projections,
3. distance functions,
4. a recursion horizon,
5. decision thresholds.

RSM does **not** define truth. It measures robustness relative to those choices.

The original RSM documents conflated three separate questions:

- Is a proposition true?
- Is a representation stable under repeated transformation?
- Is a downstream system justified in acting on the representation?

v0.2 separates them.

## 2. Formal object

Let X be a state space and let x_0 in X be the seed.

A recursive transformation is either a deterministic function

$
T: X \to X
$

or a stochastic kernel

$
K_\theta(x' \mid x)
$

parameterized by theta.

The recursive orbit is

$
x_0, x_1, \ldots, x_k
$

with

$
x_{t+1} = T(x_t)
$

or

$
x_{t+1} \sim K_\theta(\cdot \mid x_t).
$

Nothing about the orbit is epistemically privileged by default. It is simply a trajectory induced by the chosen operator.

## 3. Invariants and projections

Raw representation distance is often the wrong quantity.

For each dimension j, define a projection or invariant extractor

$
\phi_j: X \to Y_j
$

and a normalized distance

$
d_j: Y_j \times Y_j \to [0,1].
$

Examples:

- semantic representation,
- abstract syntax tree,
- graph topology,
- normalized logical form,
- schema shape,
- task output,
- compressed description length,
- domain-specific constraints.

The per-step drift component is

$
D_{t,j} = d_j(\phi_j(x_t), \phi_j(x_0)).
$

The drift vector is

$
\mathbf{D}_t = (D_{t,1}, \ldots, D_{t,m}).
$

The seed is used as the default anchor because cumulative pairwise comparison can hide gradual displacement. Pairwise step drift may also be recorded:

$
\Delta D_{t,j} = d_j(\phi_j(x_t), \phi_j(x_{t-1})).
$

Both are useful and answer different questions.

## 4. Audit profile

A result has no meaning without its profile.

Define

$
P = (K, \Phi, d, k, \theta, w, \tau)
$

where:

- K is the transform or transform family,
- Phi is the set of projections,
- d is the set of distance functions,
- k is recursion depth,
- theta contains transform parameters,
- w optionally contains component weights,
- tau contains classification thresholds.

A classification is written as

$
C_P(x)
$

or explicitly

$
C(x \mid K, \Phi, d, k, \theta, w, \tau).
$

Calling an object simply "C1" without the profile is incomplete.

## 5. Derived statistics

A recursive audit should preserve the full vector trajectory. Scalar summaries are secondary.

For an optional weighted scalar score,

$
S_t = \sum_{j=1}^{m} w_j D_{t,j},
\qquad
w_j \ge 0,
\qquad
\sum_j w_j = 1.
$

Useful summaries include:

### 5.1 Tail distortion

$
\bar S_{tail} = \frac{1}{|H|}\sum_{t \in H} S_t
$

where H is a declared tail window.

### 5.2 Drift slope

Fit a least-squares line to S_t over recursion depth. Positive slope suggests accumulating damage; negative slope suggests recovery.

### 5.3 Replicate variance

For stochastic transforms, repeat the orbit R times and estimate

$
\operatorname{Var}[S_t].
$

High variance means the stability claim is sensitive to sampling.

### 5.4 Recovery

A system may move away from the seed and later return to an invariant basin. Recovery therefore matters independently from peak distortion.

### 5.5 Cycles

Repeated states or repeated projected states can reveal fixed points and limit cycles. A two-cycle is structurally different from unbounded divergence.

## 6. Stability classes

The default classes are operational, not ontological.

### C1 — Stable basin

Use C1 when the declared invariants remain below the profile's stable threshold over the evaluation window and no meaningful positive drift trend is present.

Interpretation:

> Under profile P, the representation is robust to this recursive transformation regime.

Nothing more.

### C2 — Bounded / context-sensitive

Use C2 when drift is material but bounded, oscillatory, recoverable, or highly dependent on transform/evaluator choice.

Interpretation:

> Under profile P, behavior is structured but not uniformly stable.

### C3 — Divergent / destructive

Use C3 when the declared invariants cross a divergence threshold, exhibit sustained positive drift, or collapse irreversibly.

Interpretation:

> Under profile P, recursive transformation destroys the declared structure.

## 7. The truth/stability firewall

RSM must never infer factual or formal correctness solely from recursive stability.

Let V(x) be an external validator when one exists:

$
V(x) \in \{true, false, unknown\}.
$

Then the analysis space is at least two-dimensional:

$
(C_P(x), V(x)).
$

Examples:

- (C1, true): robust correct representation.
- (C1, false): robust misconception.
- (C3, true): true content represented or transformed fragily.
- (C3, false): unstable error.

For theorem proving, V may be a proof checker.
For code, V may be tests, formal verification, or execution.
For factual claims, V may be curated evidence or a trusted database.
For open-ended claims, V may remain unknown.

Unknown is a legitimate result.

## 8. RIPE

**RIPE — Recursive Integrity Pulse Engine** is the execution layer.

A RIPE run should record:

- seed,
- transform identity/version,
- transform parameters,
- recursion depth,
- random seed when relevant,
- every intermediate state or a reproducible hash,
- every drift component,
- aggregate score if used,
- replicate statistics,
- detected cycles,
- classification profile,
- final stability class.

RIPE is a measurement engine. It is not a theorem prover or truth oracle.

## 9. SDL

**SDL — Semantic Delay Layer** is retained as a policy concept, but its role is narrower.

SDL means:

> Do not force a semantic or operational commitment when the evidence state is unstable, highly variable, or unresolved.

Examples:

- abstain when model ensembles disagree,
- delay an agent action while a verifier is pending,
- request evidence when recursive transformations disagree,
- keep several hypotheses alive rather than prematurely collapsing them into one label.

SDL is therefore related to selective prediction, abstention, uncertainty gating, and human-in-the-loop control.

It does not create a "Schrodinger truth state." It is a decision policy under uncertainty.

## 10. CPP

**CPP — Core/Policy Partition Principle** replaces the old claim of an immutable epistemic Tier 1.

The useful engineering rule is:

> Measurement definitions and safety invariants used to evaluate a system must not be silently rewritten by the adaptive policy being evaluated.

Examples:

- an optimizer cannot lower its own failure threshold to pass evaluation,
- a model cannot redefine a protected invariant after violating it,
- learned heuristics may propose a new metric, but adoption requires an explicit versioned profile change.

CPP is a versioning and trust-boundary rule.

## 11. Multi-evaluator analysis

The old "observer neutrality" language is removed.

Different evaluators can disagree because they have different inductive biases, embeddings, parsers, training data, or noise.

That disagreement is itself measurable.

For evaluators e in E, estimate

$
D^{(e)}_{t,j}
$

and report cross-evaluator variance or disagreement rather than calling consensus "observer-independent truth."

Agreement strengthens robustness evidence only with respect to the declared evaluator set.

## 12. Compression

Compression remains useful but must be stated carefully.

Description length can reveal regularity and loss of representational structure, but shorter description does not imply greater truth.

RSM may use:

- compressed byte length,
- minimum description length approximations,
- grammar size,
- AST complexity,
- graph encoding length.

Call the resulting quantity a **description-length component**, not generic entropy.

Exact Kolmogorov complexity is not computable in general; practical implementations necessarily use proxies.

## 13. Relation to dynamical systems

RSM can be understood as empirical analysis of an orbit under a transform.

Questions such as these become natural:

- Does the orbit approach a fixed point?
- Does it enter a limit cycle?
- Is there a stable basin?
- How sensitive is the trajectory to perturbations?
- Does distortion grow approximately linearly or explosively?
- Are there phase changes as transform strength or temperature changes?

This language is more precise than treating every failure as "entropy metastasis."

## 14. What would make RSM scientifically interesting?

RSM earns its machinery only if recursive measurements explain something that simpler methods miss.

A useful result would show, for example, that recursive drift:

- predicts downstream task failure earlier than one-shot similarity,
- separates recoverable perturbation from irreversible degradation,
- identifies brittle representations that pass ordinary tests,
- provides useful uncertainty signals across model families,
- improves abstention or routing decisions.

A null result is acceptable.

If direct task evaluation explains everything and recursive drift adds nothing, the framework should be narrowed or abandoned.

## 15. Non-claims

RSM v0.2 explicitly does not claim:

- to bypass or neutralize Goedel incompleteness,
- that paradoxes are false because they drift,
- that multi-model agreement is observer neutrality,
- that compression reveals metaphysical truth,
- that recursive stability replaces proof,
- that LLM agreement validates a theory,
- that all useful distances are forms of entropy,
- that C1/C2/C3 are universal intrinsic properties.

These exclusions are part of the specification.

## 16. Current research program

The next useful work is experimental:

1. build transform families with controlled corruption strength,
2. define domain-specific invariants,
3. collect tasks with external validators,
4. run recursive audits across depths and replicates,
5. compare against simple baselines,
6. perform ablations over metrics and recursion depth,
7. test whether drift adds predictive value,
8. publish negative results as readily as positive ones.

The framework should survive because its measurements are useful, not because its vocabulary can reinterpret every criticism as confirmation.
