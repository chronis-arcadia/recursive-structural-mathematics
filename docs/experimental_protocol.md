# Experimental Protocol

## 1. Primary hypothesis

Recursive trajectory features provide predictive information about downstream failure beyond one-shot and terminal-only baselines.

## 2. Unit of analysis

Each experiment specifies:

- seed object,
- domain,
- transformation family,
- transform strength or temperature,
- recursion depth,
- replicate count,
- projections and metrics,
- external validator,
- stability profile,
- baseline methods,
- primary outcome.

## 3. Stability and correctness

For seed (x),

$$
V(x)\in\{pass,fail,unknown\}
$$

and

$$
C_P(x)\in\{C1,C2,C3\}.
$$

The two fields are recorded independently.

## 4. Benchmark domains

### Text and factual claims

Transforms:

- paraphrase,
- summarize-expand,
- translation round trip,
- model-to-model relay,
- controlled corruption.

Validators:

- curated fact labels,
- source-grounded QA,
- human adjudication.

### Code

Transforms:

- refactor,
- language translation,
- summarize-regenerate,
- repair loops,
- controlled mutation.

Validators:

- unit tests,
- static analysis,
- formal verification.

### Mathematics and symbolic logic

Transforms:

- canonical rewrite,
- explanation-reconstruction,
- symbolic simplification,
- symbolic expansion.

Validators:

- proof assistants,
- CAS equivalence,
- model checking.

### Graphs and plans

Transforms:

- serialize-deserialize,
- summarize-reconstruct,
- edge perturbation,
- planner revision.

Validators:

- graph invariants,
- constraint satisfaction,
- task success.

## 5. Baselines

Minimum baseline set:

1. seed-to-first-transform distance,
2. terminal-only distance,
3. direct task validator,
4. self-consistency or majority agreement,
5. evaluator confidence or verifier score.

LLM experiments may also include semantic entropy, NLI contradiction rate, and model probability features.

## 6. Ablations

Evaluate:

- (k=1),
- multiple recursion depths,
- each metric independently,
- full metric vector,
- vector-only analysis,
- scalar aggregation,
- single transform family,
- transform ensemble,
- single evaluator,
- evaluator ensemble,
- deterministic transforms,
- stochastic transforms.

## 7. Analyses

Primary analyses include:

- early drift vs. final task failure,
- slope vs. terminal distortion,
- replicate variance vs. brittleness,
- cycle features vs. recoverability,
- cross-evaluator variance vs. abstention performance,
- component-level feature contribution.

## 8. Statistical reporting

Predictive experiments report as applicable:

- AUROC,
- AUPRC,
- calibration error,
- precision and recall at declared operating points,
- bootstrap confidence intervals,
- effect sizes,
- sample counts,
- predeclared exclusions.

Regression experiments report error metrics and uncertainty.

## 9. Negative controls

### Identity

$$
T(x)=x.
$$

Expected behavior: near-zero drift for every seed.

### Destructive transform

Use a transform that removes a declared invariant.

Expected behavior: high drift on the affected component.

### Metric mismatch

Evaluate a semantic task with a surface-only metric.

Expected behavior: weak correspondence with semantic failure.

### Two-cycle

Use a reversible period-2 transform such as string reversal.

Expected behavior: cycle detection plus alternating trajectory.

## 10. Evaluation criteria

Evidence for useful recursive signal includes:

- improved failure prediction over baselines,
- earlier warning than terminal-only evaluation,
- replication across transform families,
- useful component-level failure attribution,
- improved selective prediction,
- reliable recovery detection.

Weak evidence includes:

- no gain over direct validators,
- held-out performance collapse,
- dependence on a single arbitrary metric,
- no contribution from recursion depth,
- cross-model replication failure,
- per-example threshold tuning.

## 11. Reproducibility record

Store:

- code commit,
- dataset version,
- model and provider version,
- prompts and decoding parameters,
- random seeds,
- recursion depth,
- replicate count,
- metric versions,
- audit profile,
- validator version,
- raw trajectories.
