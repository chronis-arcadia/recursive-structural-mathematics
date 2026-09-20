# Recursive Structural Mathematics (RSM)

RSM is an experimental framework for measuring **how well specified structure survives repeated transformation**.

The project originally made a much stronger claim: that "truth" could be defined as structural survival under recursive compression. **That claim is withdrawn.** Recursive stability is a property of an object *under a declared transformation and measurement regime*; it is not a truth predicate.

The useful research question is narrower and testable:

> Given an object, a family of transformations, and explicit invariants, how does distortion accumulate, recover, oscillate, or collapse across recursive application?

## Status

**v0.2 — research reset.**

This repository now treats RSM as a robustness / invariance framework. It does **not** claim to bypass Gödel's incompleteness theorems, solve paradoxes, provide observer-independent truth, or replace proof.

The old material remains available in Git history.

## Core model

Let the seed object be x_0 and let K be a deterministic transform or stochastic transformation kernel.

$
x_{t+1} \sim K(\cdot \mid x_t)
$

Let phi_j extract an invariant or representation relevant to the task, and d_j compare that representation with the seed.

$
D_{t,j} = d_j(\phi_j(x_t), \phi_j(x_0))
$

The recursive drift vector is:

$
\mathbf{D}_t = (D_{t,1}, D_{t,2}, \ldots, D_{t,m})
$

RSM studies the trajectory of this vector: magnitude, slope, variance, recovery, cycles, and cross-transform disagreement.

A stability class is therefore conditional:

$
C(x \mid K, \Phi, d, k, \theta)
$

—not an intrinsic label attached to x.

## Stability classes

- **C1 — Stable basin:** declared invariants remain within a calibrated tolerance and drift does not trend upward.
- **C2 — Bounded / context-sensitive:** drift is non-trivial but bounded, oscillatory, recoverable, or strongly dependent on transform/evaluator choice.
- **C3 — Divergent / destructive:** declared invariants degrade beyond the profile's divergence boundary or show sustained positive drift.

These are engineering/research labels. They do not mean "true", "partly true", or "false".

## Truth and stability are orthogonal

A false statement can be perfectly stable under identity or paraphrase transforms. A true statement can be mangled by a lossy transform. RSM therefore keeps any external correctness signal separate from the stability measurement.

| | Externally correct | Externally incorrect |
|---|---:|---:|
| Recursively stable | robust knowledge / representation | robust misconception |
| Recursively unstable | fragile representation | unstable error |

This distinction is a hard design constraint.

## Components

- **RIPE — Recursive Integrity Pulse Engine:** runs recursive audits and reports drift trajectories.
- **SDL — Semantic Delay Layer:** an abstention/hold policy; downstream systems may delay commitment when uncertainty or cross-evaluator disagreement is high.
- **CPP — Core/Policy Partition Principle:** evaluation policy may consume measurements but must not silently mutate the definitions and invariants used to judge itself.
- **RSM.VEC:** vector-level drift attribution and cross-transform analysis.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/primer.md` | Current conceptual and mathematical specification |
| `docs/metrics.md` | Drift vector, aggregation, classification, and caveats |
| `docs/experimental_protocol.md` | Falsifiable evaluation plan and baselines |
| `docs/vec_drift.md` | Multi-transform / multi-evaluator drift analysis |
| `src/rsm/` | Minimal dependency-free RIPE implementation |
| `tests/` | Behavioral tests for the core invariants |
| `calibration/cdd_v1.json` | Calibration examples with stability and truth kept separate |
| `notebooks/demo_RIPE.ipynb` | Small executable demonstration |

## Quick start

~~~bash
python -m pip install -e .
python -m unittest discover -s tests -v
~~~

The package intentionally has no runtime dependencies.

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

print(result.classification)  # C1
~~~

The sentence is factually false, yet the identity transform produces C1. That is not a bug; it demonstrates the boundary of what RSM measures.

## Research target

The strongest version of the project is empirical:

> Does recursive drift provide predictive information about downstream failure beyond simpler baselines such as one-shot similarity, self-consistency, verifier scores, semantic entropy, or direct task evaluation?

If the answer is no, RSM should be discarded or narrowed further. If the answer is yes, the contribution is a general recursive robustness diagnostic—not a replacement for logic or epistemology.

## Design rules

1. **No intrinsic stability labels.** Every result names its audit profile.
2. **No truth from drift alone.** Correctness requires an external validator when one exists.
3. **No "entropy" unless it is actually entropy.** Generic divergence is called drift.
4. **No single scalar by default.** Preserve the vector unless aggregation is justified.
5. **No self-validation.** A framework surviving criticism is not evidence for the framework.
6. **Baselines first.** New machinery must outperform or explain something simpler methods do not.
7. **Git history is the archive.** Current documentation describes the current theory only.

## License

See `LICENSE`.
