# Drift Metrics and Classification

## 1. Terminology

**Drift** is the generic term for measured divergence across recursive states.

**Entropy** is reserved for quantities explicitly defined as entropy in an information-theoretic or probabilistic model.

## 2. Drift vector

For seed (x_0), recursive state (x_t), projection (phi_j), and normalized distance (d_j),

$$
D_{t,j}=d_j(\phi_j(x_t),\phi_j(x_0))\in[0,1].
$$

Collect the components as

$$
\mathbf{D}_t=(D_{t,1},\ldots,D_{t,m}).
$$

Each component specifies:

- domain,
- projection,
- distance,
- normalization,
- failure cases,
- score direction,
- anchor definition.

## 3. Metric families

### 3.1 Surface distance

Examples:

- normalized edit distance,
- sequence similarity,
- token overlap.

Surface metrics capture representation change and may ignore semantic equivalence.

### 3.2 Semantic distance

Examples:

- embedding cosine distance,
- NLI-derived entailment or contradiction distance,
- domain-specific semantic parsers.

Semantic evaluators may share systematic errors with the transform model.

### 3.3 Structural distance

Examples:

- AST edit distance,
- production-rule mismatch,
- tree edit distance,
- schema-diff score.

### 3.4 Topological distance

Examples:

- edge-set distance,
- graph edit distance,
- spectral summaries,
- connectivity changes.

### 3.5 Description-length distance

For encoding-length function (L),

$$
D_{DL}(x_t,x_0)
=
\frac{|L(x_t)-L(x_0)|}
{\max(L(x_t),L(x_0),1)}.
$$

### 3.6 Task distance

Examples:

- unit-test pass-rate delta,
- proof-checker status,
- planner constraint violations,
- answer-set disagreement,
- reward or utility delta.

Task-specific metrics directly measure the invariant of interest when such a validator exists.

## 4. Scalar aggregation

Vector trajectories are retained as the primary record.

A scalar summary may be defined as

$$
S_t=\sum_jw_jD_{t,j}
$$

with

$$
w_j\ge0,
\qquad
\sum_jw_j=1.
$$

Weights are part of the audit profile.

## 5. Recursive summaries

For (S_0,\ldots,S_k):

### Tail mean

$$
\mu_{tail}=\frac{1}{|H|}\sum_{t\in H}S_t.
$$

### Peak

$$
S_{max}=\max_tS_t.
$$

### Terminal score

$$
S_k.
$$

### Linear slope

Fit

$$
S_t\approx a+bt.
$$

The coefficient (b) estimates linear drift rate.

### Recovery rate

A simple recovery statistic is

$$
R=\frac{1}{k}\sum_{t=1}^{k}\mathbf{1}[S_t<S_{t-1}].
$$

### Replicate variance

For replicate (r),

$$
\sigma_t^2=\operatorname{Var}_r[S_t^{(r)}].
$$

## 6. Cycles

Exact cycles can be detected from canonical state hashes.

Projected cycles satisfy

$$
\phi(x_t)=\phi(x_{t-p})
$$

for period (p>0).

Cycle period is reported separately from drift magnitude.

## 7. Reference classification

Let:

- (alpha): stable threshold,
- (gamma): divergence threshold,
- (eta): allowed positive slope,
- (H): tail window.

C1:

$$
\max_{t\in H}S_t\le\alpha
$$

and

$$
slope(S)\le\beta.
$$

C2:

$$
\max_{t\in H}S_t\le\gamma
$$

and

$$
slope(S)\le\beta.
$$

C3 covers all remaining trajectories.

The reference classifier is a baseline. Domain-specific classifiers use calibrated development data and held-out evaluation.

## 8. Threshold calibration

Calibration procedure:

1. split calibration and evaluation data,
2. define metrics,
3. estimate thresholds on calibration data,
4. freeze the audit profile,
5. evaluate held-out data,
6. report uncertainty and failure cases.

Thresholds are profile parameters rather than universal constants.

## 9. Cross-evaluator variance

For evaluator-specific scalar scores (S_t^{(e)}),

$$
\bar S_t=\frac{1}{|E|}\sum_eS_t^{(e)}
$$

and

$$
V_t=\frac{1}{|E|}\sum_e(S_t^{(e)}-\bar S_t)^2.
$$

(V_t) measures evaluator sensitivity.

## 10. Validity threats

### Transform leakage

Evaluator-transform similarity can reward shared artifacts.

### Identity triviality

For (T(x)=x), every seed has zero transformation drift.

### Metric blindness

A metric may fail to capture the invariant relevant to the task.

### Threshold overfitting

Threshold selection on evaluation data inflates apparent performance.

### Shared-model bias

Generator and evaluator models from the same family may share systematic errors.

### Endpoint bias

Oscillatory trajectories can produce misleading terminal classifications. Full trajectories retain the relevant structure.

## 11. Reference implementation

The reference implementation includes:

- sequence distance,
- token Jaccard distance,
- zlib description-length delta,
- recursive audit execution,
- weighted aggregation,
- slope estimation,
- exact cycle detection,
- C1/C2/C3 classification.

Additional semantic and structural metrics plug into the same audit interface.
