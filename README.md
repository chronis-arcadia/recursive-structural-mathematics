# Recursive Structural Mathematics (RSM)

RSM measures the stability of specified structure under repeated transformation.

Given a seed object, a transformation process, a set of projections, and distance functions, RSM records how distortion evolves across recursive application.

## Core model

Let (x_0) be the seed and (K) a deterministic transform or stochastic transformation kernel.

$$
x_{t+1} \sim K(\cdot \mid x_t)
$$

For projection (phi_j) and distance (d_j),

$$
D_{t,j} = d_j(\phi_j(x_t), \phi_j(x_0)).
$$

The recursive drift vector is

$$
\mathbf{D}_t = (D_{t,1}, D_{t,2}, \ldots, D_{t,m}).
$$

A stability classification is defined relative to an audit profile:

$$
C(x \mid K, \Phi, d, k, \theta, w, \tau).
$$

The profile fixes the transform family, projections, distances, recursion depth, transform parameters, optional weights, and thresholds.

## Stability classes

- **C1 — Stable basin:** drift remains within the stable region.
- **C2 — Bounded / context-sensitive:** drift is material but bounded, oscillatory, recoverable, or evaluator-dependent.
- **C3 — Divergent / destructive:** declared structure degrades beyond the divergence boundary or shows sustained positive drift.

## Validation channels

Recursive stability and external correctness are recorded independently.

| | External validator: pass | External validator: fail |
|---|---:|---:|
| C1 | stable validated representation | stable invalid representation |
| C2/C3 | fragile validated representation | unstable invalid representation |

External validation may come from a proof checker, test suite, database, source-grounded evaluator, constraint system, or other domain-specific authority.

## Components

- **RIPE — Recursive Integrity Pulse Engine:** executes recursive audits and records drift trajectories.
- **SDL — Semantic Delay Layer:** routes unstable or unresolved states to abstention, additional evaluation, or human review.
- **CPP — Core/Policy Partition Principle:** separates audit definitions from adaptive policy.
- **RSM.VEC:** analyzes component, evaluator, transform, and replicate-level drift.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/primer.md` | Formal model and system components |
| `docs/metrics.md` | Drift metrics, aggregation, classification, and calibration |
| `docs/experimental_protocol.md` | Evaluation protocol and baselines |
| `docs/vec_drift.md` | Multi-transform and multi-evaluator analysis |
| `src/rsm/` | RIPE reference implementation |
| `tests/` | Core behavioral tests |
| `calibration/cdd_v1.json` | Calibration controls |
| `notebooks/demo_RIPE.ipynb` | Executable examples |

## Quick start

~~~bash
python -m pip install -e .
python -m unittest discover -s tests -v
~~~

~~~python
from rsm import AuditProfile, run_audit
from rsm.metrics import sequence_distance, token_jaccard_distance

result = run_audit(
    seed="The Sun orbits Earth once per day.",
    transform=lambda x: x,
    metrics={
        "sequence": sequence_distance,
        "tokens": token_jaccard_distance,
    },
    profile=AuditProfile(),
)

print(result.classification)
~~~

Identity transformation produces zero drift regardless of factual validity. External correctness remains a separate field.

## Research hypothesis

Recursive trajectory features may improve prediction of downstream failure over one-shot similarity, terminal-only distance, self-consistency, verifier scores, or direct task metrics.

Experiments evaluate that contribution through held-out data, ablations, negative controls, and cross-transform replication.

## License

MIT. See `LICENSE`.
