# Drift Metrics and Classification

## 1. Naming

Earlier RSM documents called almost every divergence quantity "entropy." v0.2 stops doing that.

Use **entropy** only when the quantity is actually an entropy in the information-theoretic or explicitly defined probabilistic sense.

The generic object measured here is **drift**.

## 2. Drift vector

For seed x_0 and recursive state x_t, define projections phi_j and normalized distances d_j.

$
D_{t,j} = d_j(\phi_j(x_t), \phi_j(x_0)) \in [0,1].
$

Collect them as

$
\mathbf{D}_t = (D_{t,1}, \ldots, D_{t,m}).
$

A component must document:

- domain,
- projection,
- distance function,
- normalization,
- failure cases,
- whether lower is always better,
- whether it is anchored to x_0 or x_{t-1}.

## 3. Suggested components

### 3.1 Surface distance

Useful for exact or near-exact textual preservation.

Examples:

- normalized edit distance,
- sequence similarity,
- token overlap.

Weakness: surface change may be semantically harmless.

### 3.2 Semantic distance

Useful for meaning preservation.

Examples:

- embedding cosine distance,
- NLI-derived contradiction/entailment distance,
- domain-specific semantic parsers.

Weakness: semantic models can share systematic errors with the generator.

### 3.3 Structural distance

Useful for code, formulas, trees, or schemas.

Examples:

- AST edit distance,
- production-rule mismatch,
- normalized tree edit distance,
- schema-diff score.

### 3.4 Topological distance

Useful for graphs and dependency structures.

Examples:

- edge-set distance,
- graph edit distance,
- spectral summaries,
- component/connectivity changes.

### 3.5 Description-length distance

Let L(.) be a declared compressor or encoding length.

A simple normalized component is

$
D_{DL}(x_t,x_0)
=
\frac{|L(x_t)-L(x_0)|}
{\max(L(x_t),L(x_0),1)}.
$

This is a compression proxy, not Kolmogorov complexity.

### 3.6 Task distance

When a downstream behavior is the actual invariant of interest, measure it directly.

Examples:

- unit-test pass-rate change,
- proof-checker status,
- planner constraint violations,
- answer-set disagreement,
- reward or utility delta.

Task distance is often more meaningful than generic semantic similarity.

## 4. Optional scalar aggregation

The vector should be retained.

When a scalar is operationally necessary, define

$
S_t = \sum_j w_j D_{t,j}
$

subject to

$
w_j \ge 0, \qquad \sum_j w_j = 1.
$

Weights must be versioned with the audit profile.

Do not fit weights on a test set.

## 5. Recursive summaries

For score series S_0, ..., S_k:

### Mean tail score

$
\mu_{tail} = \frac{1}{|H|}\sum_{t\in H}S_t.
$

### Peak score

$
S_{max}=\max_t S_t.
$

### Terminal score

$
S_k.
$

### Linear drift slope

For t = 0,...,k, fit

$
S_t \approx a + bt.
$

The coefficient b is a crude drift-rate estimate.

### Recovery

One simple statistic is

$
R = \frac{1}{k}\sum_{t=1}^{k} \mathbf{1}[S_t < S_{t-1}].
$

More useful domain-specific recovery measures may ask whether the orbit re-enters a declared stable basin after perturbation.

### Replicate variance

For stochastic transforms with replicate r,

$
\sigma_t^2 = \operatorname{Var}_r[S_t^{(r)}].
$

Always report replicate count.

## 6. Cycles

Exact state repetition is easy to detect by hashing canonical states.

Projected cycles can also be useful:

$
\phi(x_t) = \phi(x_{t-p})
$

for period p > 0.

A cycle is not automatically good or bad. It may indicate:

- harmless canonicalization,
- reversible alternation,
- unresolved oscillation,
- a transform artifact.

The interpretation belongs to the audit profile.

## 7. Default classification rule

The reference implementation uses a deliberately simple rule so that the baseline is easy to understand.

Let:

- alpha = stable threshold,
- gamma = divergence threshold,
- beta = allowed positive slope,
- H = latter half of the score trajectory.

Then:

**C1** if

$
\max_{t\in H} S_t \le \alpha
$

and

$
|slope(S)| \le \beta.
$

**C2** if the C1 rule fails but

$
\max_{t\in H} S_t \le \gamma
$

and

$
slope(S) \le \beta.
$

Otherwise **C3**.

This rule is a baseline, not a law.

A serious domain should calibrate a classifier on development data and evaluate it on held-out data.

## 8. Threshold calibration

Thresholds are part of the experimental hypothesis.

Recommended process:

1. split calibration and test sets,
2. choose metrics without looking at final test labels,
3. estimate thresholds on calibration data,
4. freeze the profile,
5. evaluate on held-out data,
6. report confidence intervals and failure cases.

Avoid treating alpha=0.05 or gamma=0.20 as universal constants. The old repo did this without evidence; v0.2 removes that assumption.

## 9. Cross-evaluator disagreement

Suppose multiple evaluators e produce scores S_t^(e).

Report:

$
\bar S_t = \frac{1}{|E|}\sum_e S_t^{(e)}
$

and

$
V_t = \frac{1}{|E|}\sum_e (S_t^{(e)}-\bar S_t)^2.
$

High V_t means the result is evaluator-sensitive.

It does not mean "truth is subjective" and low V_t does not mean "objective truth."

## 10. Validity threats

### Transform leakage

If the evaluator is too similar to the transform, it may reward its own artifacts.

### Identity triviality

For T(x)=x, every seed is perfectly stable. Stability therefore cannot be intrinsic.

### Metric blindness

Token overlap can miss semantic corruption; embeddings can miss precise logical changes.

### Threshold overfitting

A hand-picked threshold can manufacture classes from noise.

### Recursive self-confirmation

A model evaluating generations from the same model family may share the same systematic bias.

### Depth cherry-picking

An oscillatory process can look stable or unstable depending on whether evaluation stops on an even or odd step.

Always report the full trajectory.

## 11. Reference implementation

The dependency-free implementation provides:

- sequence distance,
- token Jaccard distance,
- zlib description-length delta,
- recursive audit execution,
- weighted aggregation,
- slope estimation,
- exact cycle detection,
- C1/C2/C3 baseline classification.

It is intentionally simple. Sophisticated semantic or structural metrics should be plugged in by the experimenter rather than hidden inside the core.
