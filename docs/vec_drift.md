# RSM.VEC — Recursive Drift Vector Analysis

RSM.VEC decomposes recursive drift across metrics, transforms, evaluators, and replicates.

## 1. Measurement tensor

For seed (x_0), transform family (K_q), evaluator (e), component (j), and step (t),

$$
D^{(q,e)}_{t,j}
=
d^{(e)}_j(
\phi^{(e)}_j(x_t),
\phi^{(e)}_j(x_0)
).
$$

The measurement tensor spans:

- recursion step,
- metric component,
- transform family,
- evaluator,
- replicate.

## 2. Drift attribution

An attribution report records:

- first component to move,
- dominant peak component,
- transform-specific effects,
- evaluator-specific effects,
- recovery,
- cycle structure,
- replicate variance.

## 3. Cross-evaluator variance

For scalar score (S_t^{(e)}),

$$
CEV_t
=
\frac{1}{|E|}
\sum_e
(S_t^{(e)}-\bar S_t)^2.
$$

Component-wise CEV uses the same form for each drift dimension.

## 4. Cross-transform variance

For transform family (q),

$$
CTV_t
=
\frac{1}{|Q|}
\sum_q
(S_t^{(q)}-\bar S_t)^2.
$$

CTV measures sensitivity to perturbation regime.

## 5. Recursive Drift Chain Monitor

RDCM stores, per component or scalar score:

- current value,
- first difference,
- fitted slope,
- peak,
- tail mean,
- replicate variance,
- cycle metadata.

Alerts are profile-defined.

## 6. Attribution Memory Buffer

AMB stores audit signatures containing:

- profile identifier,
- transform and evaluator versions,
- score trajectory,
- vector trajectory,
- cycle period,
- stability class,
- external validator result.

Applications include:

- regression detection,
- failure clustering,
- profile comparison,
- reproducibility,
- audit trails.

## 7. SDL integration

SDL consumes VEC outputs for routing.

Example policy:

- low drift + low CEV + validator pass -> commit,
- low drift + validator fail -> reject,
- moderate drift + high CEV -> additional evaluation,
- high drift + unavailable validator -> hold,
- unresolved disagreement -> human review.

## 8. CPP integration

Audit parameters remain fixed for the duration of a run.

Changing metric definitions, invariants, weights, thresholds, evaluator sets, or validator criteria creates a distinct audit profile.

## 9. Report schema

An RSM.VEC report contains:

1. profile identifier,
2. transform family and parameters,
3. evaluator set,
4. recursion depth and replicate count,
5. component trajectories,
6. scalar trajectory when configured,
7. CEV and CTV,
8. cycle metadata,
9. stability class,
10. external validator result.
