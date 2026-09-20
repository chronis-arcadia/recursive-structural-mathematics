# Experimental Protocol

## Research question

Does recursive structural drift provide useful predictive information about downstream failure beyond simpler one-shot baselines?

That is the main falsifiable question for RSM v0.2.

## 1. Unit of analysis

Every experiment must define:

- seed object,
- domain,
- transformation family,
- transform strength / temperature,
- recursion depth,
- replicate count,
- projections and metrics,
- external validator if available,
- stability profile,
- baseline methods,
- primary outcome.

## 2. Required separation: correctness vs stability

Where ground truth exists, store it separately from RSM stability.

For a seed x:

$
V(x) \in \{true,false,unknown\}
$

and

$
C_P(x) \in \{C1,C2,C3\}.
$

Do not derive one from the other.

The calibration file includes stable falsehoods and stable paradox strings on purpose. Any implementation that assumes C1 means true should fail those cases conceptually.

## 3. Suggested benchmark domains

### Text and factual claims

Transforms:
- paraphrase,
- summarize-expand,
- translate-roundtrip,
- model-to-model relay,
- noisy rewrite.

External validators:
- curated fact labels,
- source-grounded QA,
- human adjudication.

### Code

Transforms:
- refactor,
- translate between languages,
- summarize and regenerate,
- model repair loops.

External validators:
- unit tests,
- static analysis,
- formal verification when feasible.

### Mathematics / symbolic logic

Transforms:
- canonical rewrite,
- natural-language explanation and reconstruction,
- symbolic simplification/expansion.

External validators:
- proof assistants,
- CAS equivalence,
- model checking.

### Graphs / plans

Transforms:
- serialize-deserialize,
- summarize-reconstruct,
- edge perturbation,
- planner revision.

External validators:
- graph invariants,
- constraint satisfaction,
- task success.

## 4. Baselines

At minimum compare RSM against:

1. one-shot distance from seed to first transform,
2. terminal-only distance,
3. direct task validator,
4. self-consistency / majority agreement where applicable,
5. evaluator confidence or verifier score where available.

For LLM experiments, useful additional baselines may include semantic entropy, NLI contradiction rates, or model log-probability measures.

The recursive method is interesting only if it adds information beyond these simpler alternatives.

## 5. Ablations

Run at least:

- no recursion: k=1,
- multiple recursion depths,
- each metric alone,
- full metric vector,
- no scalar aggregation,
- single transform family,
- cross-family transform ensemble,
- single evaluator,
- multiple evaluators,
- fixed vs stochastic transforms.

## 6. Primary analyses

Useful questions include:

- Does early drift predict final task failure?
- Does slope add value beyond terminal distortion?
- Does replicate variance identify brittle seeds?
- Do cycle features distinguish recoverable oscillation from degradation?
- Does cross-evaluator variance improve abstention decisions?
- Which components contribute independent predictive value?

## 7. Statistical reporting

For predictive experiments report, where appropriate:

- AUROC / AUPRC,
- calibration error,
- precision/recall at declared operating points,
- confidence intervals via bootstrap,
- effect sizes,
- sample counts,
- predeclared exclusions.

For regression outcomes, report error metrics and uncertainty.

Do not report only examples selected after seeing the result.

## 8. Negative controls

RSM needs controls that expose nonsense quickly.

### Identity control

T(x)=x.

Expected: near-zero drift for every object, regardless of truth.

### Representation scramble

Use a transform known to destroy the chosen invariant.

Expected: high drift even for externally true seeds.

### Metric mismatch

Evaluate a semantic task using only surface distance.

Expected: demonstrate failure of the metric, not failure of the seed.

### Odd/even cycle control

Use a reversible two-cycle such as string reversal.

Expected: full-trajectory reporting must expose the cycle; endpoint-only classification is unacceptable.

## 9. Success criteria

A compelling RSM result should show at least one of:

- materially better failure prediction than baselines,
- earlier warning than terminal-only evaluation,
- robust detection across transform families,
- useful decomposition of failure source,
- improved selective prediction / abstention,
- discovery of recoverable vs irreversible regimes.

## 10. Failure criteria

The framework should be narrowed or rejected for a domain if:

- direct validators dominate all recursive features,
- results disappear under held-out evaluation,
- performance depends on one arbitrary metric,
- recursive depth adds no information,
- cross-model replication fails,
- thresholds require post-hoc tuning per example.

## 11. Reproducibility checklist

Record:

- code commit,
- dataset version,
- model/provider/version,
- prompts and decoding parameters,
- random seeds,
- recursion depth,
- replicate count,
- metric versions,
- threshold profile,
- external validator version,
- raw trajectories.

RSM v0.2 treats reproducibility as more important than vocabulary.
