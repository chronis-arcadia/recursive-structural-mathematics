# RSM.VEC — Recursive Drift Vector Analysis

RSM.VEC analyzes **where drift comes from** and **how sensitive the result is to transform and evaluator choice**.

It does not attribute truth.

## 1. Inputs

For seed x_0, transform family K_q, evaluator e, component j, and recursion step t:

$$
D^{(q,e)}_{t,j}
=
d^{(e)}_j(
\phi^{(e)}_j(x_t),
\phi^{(e)}_j(x_0)
).
$$

The full measurement object is therefore a tensor over:

- recursion step,
- metric component,
- transform family,
- evaluator,
- replicate.

Collapsing this object too early destroys information.

## 2. Drift attribution

A practical attribution report should ask:

- Which metric component moved first?
- Which component dominates peak drift?
- Is the effect specific to one transform family?
- Is the effect specific to one evaluator?
- Does drift recover?
- Is the process cyclic?
- Is the variance between stochastic replicates larger than the mean effect?

## 3. Cross-evaluator variance

The old term "Observer Drift Variance" is replaced by the more literal **Cross-Evaluator Variance (CEV)**.

For scalar scores:

$$
CEV_t
=
\frac{1}{|E|}
\sum_e
(S_t^{(e)} - \bar S_t)^2.
$$

For vector measurements, compute component-wise variance.

High CEV means the classification is sensitive to evaluator choice.

## 4. Cross-transform variance

Likewise,

$$
CTV_t
=
\frac{1}{|Q|}
\sum_q
(S_t^{(q)} - \bar S_t)^2.
$$

High CTV means stability depends strongly on the perturbation or regeneration regime.

A seed that is C1 under identity and C3 under lossy summarization is not contradictory. Those are different profiles.

## 5. Recursive Drift Chain Monitor

The retained **RDCM** concept is simply trajectory monitoring.

For each component or scalar score, store:

- current value,
- first difference,
- fitted slope,
- peak,
- tail mean,
- replicate variance,
- cycle metadata.

Alerts should be based on declared operating thresholds rather than metaphors such as "entropy metastasis."

## 6. Attribution Memory Buffer

The **AMB** is a cache of recent audit signatures.

A signature may include:

- profile identifier,
- transform/evaluator versions,
- score trajectory,
- vector trajectory,
- cycle period,
- class,
- external validator result if available.

Useful purposes:

- regression detection,
- repeated-failure clustering,
- profile comparison,
- reproducibility,
- audit trails.

The AMB must not silently convert previous labels into ground truth.

## 7. SDL integration

SDL may use VEC outputs to decide whether to:

- commit,
- abstain,
- request another evaluator,
- request external verification,
- continue recursion,
- escalate to a human.

Example policy:

- low drift + low CEV + validator pass -> commit,
- low drift + validator fail -> reject despite stability,
- moderate drift + high CEV -> abstain / gather evidence,
- high drift + validator unavailable -> hold rather than infer falsehood.

## 8. CPP integration

A policy may adapt weights or propose new metrics, but a running audit cannot rewrite the profile used to judge that same run.

Profile changes create a new version.

This prevents an adaptive system from moving its own goalposts.

## 9. Minimum report

Every RSM.VEC report should include:

1. profile identifier,
2. transform family and parameters,
3. evaluator set,
4. recursion depth and replicate count,
5. component trajectories,
6. scalar trajectory if used,
7. CEV / CTV where applicable,
8. cycles,
9. class,
10. external validator result separately.

Anything less is an anecdote, not a reproducible recursive audit.
