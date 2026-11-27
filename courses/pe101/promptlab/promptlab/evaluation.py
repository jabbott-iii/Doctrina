"""Reference calculations for PE101's later evaluation notebooks."""

from math import sqrt
from random import Random
from statistics import mean


def wilson(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Return a Wilson score interval for independent binary outcomes."""
    if total <= 0 or not 0 <= successes <= total or z <= 0:
        raise ValueError("Require 0 <= successes <= total, a positive total, and z > 0.")
    p = successes / total
    scale = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / scale
    radius = z * sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / scale
    return max(0.0, center - radius), min(1.0, center + radius)


def paired_bootstrap(a, b, *, repeats: int = 2000, seed: int = 101):
    """Estimate B minus A and a percentile interval using paired case means."""
    if len(a) != len(b) or not a or repeats < 2:
        raise ValueError("Provide equal nonempty case scores and at least two resamples.")
    deltas = [right - left for left, right in zip(a, b, strict=True)]
    rng = Random(seed)
    samples = sorted(mean(rng.choices(deltas, k=len(deltas))) for _ in range(repeats))
    return mean(deltas), samples[int(0.025 * (repeats - 1))], samples[int(0.975 * (repeats - 1))]
