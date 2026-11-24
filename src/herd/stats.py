# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Statistics without scipy: intervals, Student t tail, bootstrap and Holm adjustment."""

from __future__ import annotations

import math

import numpy as np

from .model import ModelError

Z95 = 1.959963984540054
Z99 = 2.5758293035489004


def _betacf(a: float, b: float, x: float, max_iter: int = 500, eps: float = 3e-16) -> float:
    """Continued fraction for the incomplete beta function (modified Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            return h
    raise ArithmeticError("incomplete beta continued fraction did not converge")


def betainc_reg(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a, b)."""
    if a <= 0 or b <= 0:
        raise ModelError("a and b must be positive")
    if not 0.0 <= x <= 1.0:
        raise ModelError("x must lie in [0, 1]")
    if x in (0.0, 1.0):
        return x
    ln_front = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(ln_front) * _betacf(a, b, x) / a
    return 1.0 - math.exp(ln_front) * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t: float, df: float) -> float:
    """Two-sided p-value of Student's t with df degrees of freedom."""
    if df <= 0:
        raise ModelError("df must be positive")
    if math.isinf(t):
        return 0.0
    return betainc_reg(df / 2.0, 0.5, df / (df + t * t))


def wilson_interval(successes: int, n: int, z: float = Z99) -> tuple[float, float]:
    if n <= 0 or successes < 0 or successes > n:
        raise ModelError("need 0 <= successes <= n and n > 0")
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def mean_interval(x: np.ndarray, z: float = Z95) -> dict:
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ModelError("need a 1-D sample of size >= 2")
    m = float(x.mean())
    sd = float(x.std(ddof=1))
    se = sd / math.sqrt(x.size)
    return {"mean": m, "sd": sd, "se": se, "ci_low": m - z * se, "ci_high": m + z * se, "n": int(x.size)}


def bootstrap_mean_interval(x: np.ndarray, resamples: int, seed: int, level: float = 0.95,
                            chunk: int = 200) -> tuple[float, float]:
    """Percentile bootstrap interval for the mean, resampling observations."""
    x = np.asarray(x, dtype=float)
    if resamples < 1:
        raise ModelError("resamples must be >= 1")
    rng = np.random.Generator(np.random.PCG64(seed))
    means = np.empty(resamples)
    done = 0
    while done < resamples:
        b = min(chunk, resamples - done)
        idx = rng.integers(0, x.size, size=(b, x.size))
        means[done : done + b] = x[idx].mean(axis=1)
        done += b
    alpha = (1 - level) / 2
    return float(np.quantile(means, alpha)), float(np.quantile(means, 1 - alpha))


def paired_contrast(treat: np.ndarray, control: np.ndarray, bootstrap_resamples: int = 0,
                    bootstrap_seed: int = 0) -> dict:
    """Mean paired difference treat - control with a normal 95% interval and a paired t-test.

    A zero-variance difference is reported explicitly (degenerate=True, p = 1 if the mean is 0)."""
    treat = np.asarray(treat, dtype=float)
    control = np.asarray(control, dtype=float)
    if treat.shape != control.shape or treat.ndim != 1:
        raise ModelError("treat and control must be 1-D arrays of equal length")
    d = treat - control
    out = mean_interval(d)
    out["degenerate"] = bool(out["sd"] == 0.0)
    if out["degenerate"]:
        out["t"] = None
        out["p_value"] = 1.0 if out["mean"] == 0.0 else 0.0
    else:
        t = out["mean"] / out["se"]
        out["t"] = float(t)
        out["p_value"] = float(t_two_sided_p(t, d.size - 1))
    if bootstrap_resamples > 0:
        lo, hi = bootstrap_mean_interval(d, bootstrap_resamples, bootstrap_seed)
        out["boot_ci_low"], out["boot_ci_high"] = lo, hi
    return out


def holm(p_values: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (monotone, capped at 1)."""
    m = len(p_values)
    if any((p is None) or not (0.0 <= p <= 1.0) for p in p_values):
        raise ModelError("p-values must lie in [0, 1]")
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[idx]))
        adjusted[idx] = running
    return adjusted
