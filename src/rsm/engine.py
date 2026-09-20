"""RIPE: Recursive Integrity Pulse Engine.

The engine measures recursive drift. It does not evaluate truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

Metric = Callable[[str, str], float]
Transform = Callable[[str], str]


@dataclass(frozen=True)
class AuditProfile:
    """Versionable decision parameters for a recursive audit."""

    stable_threshold: float = 0.08
    divergence_threshold: float = 0.35
    slope_threshold: float = 0.02
    tail_fraction: float = 0.50
    weights: Mapping[str, float] | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.stable_threshold <= self.divergence_threshold <= 1.0):
            raise ValueError(
                "thresholds must satisfy 0 <= stable <= divergence <= 1"
            )
        if self.slope_threshold < 0.0:
            raise ValueError("slope_threshold must be non-negative")
        if not (0.0 < self.tail_fraction <= 1.0):
            raise ValueError("tail_fraction must be in (0, 1]")


@dataclass(frozen=True)
class AuditResult:
    """Complete summary of one RIPE audit."""

    classification: str
    mean_scores: tuple[float, ...]
    component_means: Mapping[str, tuple[float, ...]]
    replicate_scores: tuple[tuple[float, ...], ...]
    states: tuple[tuple[str, ...], ...]
    cycle_periods: tuple[int | None, ...]
    slope: float
    profile: AuditProfile

    @property
    def terminal_score(self) -> float:
        return self.mean_scores[-1]

    @property
    def peak_score(self) -> float:
        return max(self.mean_scores)


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _linear_slope(values: tuple[float, ...]) -> float:
    if len(values) < 2:
        return 0.0

    n = len(values)
    x_bar = (n - 1) / 2.0
    y_bar = sum(values) / n
    numerator = sum(
        (i - x_bar) * (value - y_bar) for i, value in enumerate(values)
    )
    denominator = sum((i - x_bar) ** 2 for i in range(n))
    return 0.0 if denominator == 0.0 else numerator / denominator


def _normalized_weights(
    metric_names: tuple[str, ...],
    requested: Mapping[str, float] | None,
) -> dict[str, float]:
    if requested is None:
        weight = 1.0 / len(metric_names)
        return {name: weight for name in metric_names}

    unknown = set(requested) - set(metric_names)
    missing = set(metric_names) - set(requested)
    if unknown or missing:
        raise ValueError(
            f"weights must match metric names exactly; unknown={unknown}, missing={missing}"
        )

    if any(value < 0 for value in requested.values()):
        raise ValueError("weights must be non-negative")

    total = float(sum(requested.values()))
    if total <= 0.0:
        raise ValueError("at least one weight must be positive")

    return {name: float(requested[name]) / total for name in metric_names}


def _classify(scores: tuple[float, ...], profile: AuditProfile) -> tuple[str, float]:
    slope = _linear_slope(scores)

    non_seed_count = max(1, len(scores) - 1)
    tail_count = max(1, round(non_seed_count * profile.tail_fraction))
    tail = scores[-tail_count:]
    tail_peak = max(tail)

    if tail_peak <= profile.stable_threshold and slope <= profile.slope_threshold:
        return "C1", slope

    if tail_peak <= profile.divergence_threshold and slope <= profile.slope_threshold:
        return "C2", slope

    return "C3", slope


def run_audit(
    seed: str,
    transform: Transform,
    metrics: Mapping[str, Metric],
    *,
    steps: int = 8,
    replicates: int = 1,
    profile: AuditProfile | None = None,
) -> AuditResult:
    """Run recursive transformations and measure drift from the original seed.

    The transform may be stochastic; callers can close over their own RNG.
    Reproducibility is the caller's responsibility for stochastic transforms.
    """

    if steps < 1:
        raise ValueError("steps must be >= 1")
    if replicates < 1:
        raise ValueError("replicates must be >= 1")
    if not metrics:
        raise ValueError("at least one metric is required")

    profile = profile or AuditProfile()
    metric_names = tuple(metrics)
    weights = _normalized_weights(metric_names, profile.weights)

    all_scores: list[tuple[float, ...]] = []
    all_states: list[tuple[str, ...]] = []
    all_components: dict[str, list[tuple[float, ...]]] = {
        name: [] for name in metric_names
    }
    cycle_periods: list[int | None] = []

    for _ in range(replicates):
        current = seed
        states = [seed]
        scores = [0.0]
        component_series = {name: [0.0] for name in metric_names}
        seen_at = {seed: 0}
        first_cycle_period: int | None = None

        for step in range(1, steps + 1):
            current = transform(current)
            states.append(current)

            components: dict[str, float] = {}
            for name, metric in metrics.items():
                value = _clip01(metric(seed, current))
                components[name] = value
                component_series[name].append(value)

            scores.append(
                sum(weights[name] * components[name] for name in metric_names)
            )

            if first_cycle_period is None and current in seen_at:
                first_cycle_period = step - seen_at[current]
            else:
                seen_at.setdefault(current, step)

        all_scores.append(tuple(scores))
        all_states.append(tuple(states))
        cycle_periods.append(first_cycle_period)
        for name in metric_names:
            all_components[name].append(tuple(component_series[name]))

    mean_scores = tuple(
        sum(series[i] for series in all_scores) / replicates
        for i in range(steps + 1)
    )

    component_means = {
        name: tuple(
            sum(series[i] for series in all_components[name]) / replicates
            for i in range(steps + 1)
        )
        for name in metric_names
    }

    classification, slope = _classify(mean_scores, profile)

    return AuditResult(
        classification=classification,
        mean_scores=mean_scores,
        component_means=component_means,
        replicate_scores=tuple(all_scores),
        states=tuple(all_states),
        cycle_periods=tuple(cycle_periods),
        slope=slope,
        profile=profile,
    )
