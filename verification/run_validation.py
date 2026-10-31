#!/usr/bin/env python3
"""Deterministic scientific checks for the sequential replay theorem.

This is finite numerical evidence, not a proof or a performance benchmark.
The Ramsey simulation uses the exact conservative schedule in science/replay-algorithm.md.
Run from any directory: python verification/run_validation.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
from typing import Any

import numpy as np


SEED = 20261031
I2 = np.eye(2, dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)
X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    delta = (a - b + (a - b).conj().T) / 2
    return float(np.abs(np.linalg.eigvalsh(delta)).sum() / 2)


def norm_error(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b, ord=2))


def random_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r) / np.abs(np.diag(r))
    return q * phases


def unitary_with_probability(
    d: int, p: float, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Random good/bad garbage vectors and random orthogonal completion."""
    half = d // 2
    bad = rng.normal(size=half) + 1j * rng.normal(size=half)
    good = rng.normal(size=d - half) + 1j * rng.normal(size=d - half)
    bad /= np.linalg.norm(bad)
    good /= np.linalg.norm(good)
    column = np.concatenate((math.sqrt(1 - p) * bad, math.sqrt(p) * good))
    raw = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    raw[:, 0] = column
    u, r = np.linalg.qr(raw)
    u *= np.diag(r) / np.abs(np.diag(r))
    if norm_error(u[:, :1], column[:, None]) > 1e-12:
        raise AssertionError("Constructed source has the wrong first column")
    projector = np.diag([0.0] * half + [1.0] * (d - half))
    return u, projector


def gadget_kraus(
    u: np.ndarray, projector: np.ndarray, inverse: np.ndarray | None = None
) -> list[np.ndarray]:
    """Build the full circuit, then extract each measured workspace branch."""
    d = u.shape[0]
    s = np.eye(d) - 2 * projector
    middle = (
        math.cos(math.pi / 4) * np.eye(2 * d)
        + 1j * math.sin(math.pi / 4) * np.kron(s, Z)
    )
    inverse = u.conj().T if inverse is None else inverse
    circuit = np.kron(inverse, I2) @ middle @ np.kron(u, I2)
    return [circuit[2 * j : 2 * j + 2, :2] for j in range(d)]


def check_arbitrary_garbage(rng: np.random.Generator) -> dict[str, Any]:
    maxima = {
        "source_unitarity_operator_error": 0.0,
        "success_kraus_operator_error": 0.0,
        "failure_kraus_operator_error": 0.0,
        "branch_probability_error": 0.0,
        "success_reference_trace_distance": 0.0,
        "corrected_failure_reference_trace_distance": 0.0,
        "corrected_instrument_trace_distance": 0.0,
    }
    cases = 0
    bell = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
    for d in (2, 4, 8, 16):
        for p in (0.0, 1e-4, 0.01, 0.2, 0.5, 0.8, 0.9999, 1.0):
            for _ in range(3):
                u, pi = unitary_with_probability(d, p, rng)
                maxima["source_unitarity_operator_error"] = max(
                    maxima["source_unitarity_operator_error"],
                    norm_error(u.conj().T @ u, np.eye(d)),
                )
                b = u.conj().T @ (np.eye(d) - 2 * pi) @ u
                z = 1 - 2 * p
                success = (1 + z * z) / 2
                kraus = gadget_kraus(u, pi)
                expected_success = (I2 + 1j * z * Z) / math.sqrt(2)
                maxima["success_kraus_operator_error"] = max(
                    maxima["success_kraus_operator_error"],
                    norm_error(kraus[0], expected_success),
                )
                rotation = np.diag(np.exp(1j * math.atan(z) * np.array([1, -1])))
                psi = np.kron(random_unitary(2, rng), I2) @ bell
                # An entangled pure input and an entangled full-rank input.
                pure = np.outer(psi, psi.conj())
                for rho in (pure, 0.8 * pure + 0.2 * np.eye(4) / 4):
                    target = np.kron(rotation, I2) @ rho @ np.kron(rotation.conj().T, I2)
                    channel = np.zeros_like(rho)
                    for j, operator in enumerate(kraus):
                        local = operator if j == 0 else Z @ operator
                        joint = np.kron(local, I2)
                        out = joint @ rho @ joint.conj().T
                        probability = float(np.trace(out).real)
                        channel += out
                        expected_probability = success if j == 0 else abs(b[j, 0]) ** 2 / 2
                        maxima["branch_probability_error"] = max(
                            maxima["branch_probability_error"],
                            abs(probability - expected_probability),
                        )
                        if j:
                            expected_failure = 1j * b[j, 0] * Z / math.sqrt(2)
                            maxima["failure_kraus_operator_error"] = max(
                                maxima["failure_kraus_operator_error"],
                                norm_error(operator, expected_failure),
                            )
                        if probability > 1e-13:
                            key = (
                                "success_reference_trace_distance"
                                if j == 0
                                else "corrected_failure_reference_trace_distance"
                            )
                            maxima[key] = max(
                                maxima[key],
                                trace_distance(out / probability, target if j == 0 else rho),
                            )
                    maxima["corrected_instrument_trace_distance"] = max(
                        maxima["corrected_instrument_trace_distance"],
                        trace_distance(channel, success * target + (1 - success) * rho),
                    )
                cases += 1
    if max(maxima.values()) > 2e-10:
        raise AssertionError(f"Arbitrary-garbage/reference audit failed: {maxima}")
    return {"unitary_cases": cases, "reference_states_per_case": 2, **maxima}


def superoperator(kraus: list[np.ndarray]) -> np.ndarray:
    return sum(np.kron(k.conj(), k) for k in kraus)


def routed_unitary(u: np.ndarray) -> np.ndarray:
    """Three route labels: no use, forward, inverse; one controlled invocation."""
    result = np.zeros((6, 6), dtype=complex)
    result[:2, :2] = I2
    result[2:4, 2:4] = u
    result[4:, 4:] = u.conj().T
    return result


def coin_driven_channel(coin: int) -> np.ndarray:
    kraus = []
    idle = np.zeros((6, 6), dtype=complex)
    idle[:2, :2] = I2
    kraus.append(idle)
    for direction in (1, 2):
        for bit in (0, 1):
            op = np.zeros((6, 6), dtype=complex)
            op[2 * direction + (bit ^ coin), 2 * direction + bit] = 1
            kraus.append(op)
    return superoperator(kraus)


def check_single_use_twirl() -> dict[str, Any]:
    t0, t1 = coin_driven_channel(0), coin_driven_channel(1)
    worst = 0.0
    rows = []
    for p in (0.0, 1e-5, 0.01, 0.125, 0.37, 0.5, 0.875, 0.99999, 1.0):
        r = np.array(
            [[math.sqrt(1 - p), -math.sqrt(p)], [math.sqrt(p), math.sqrt(1 - p)]],
            dtype=complex,
        )
        averaged = np.zeros((36, 36), dtype=complex)
        no_global_phase_average = np.zeros_like(averaged)
        for a in (0, 1):
            for b in (0, 1):
                base = np.linalg.matrix_power(Z, a) @ r @ np.linalg.matrix_power(Z, b)
                no_global_phase_average += superoperator([routed_unitary(base)]) / 4
                for c in range(4):
                    averaged += superoperator([routed_unitary((1j**c) * base)]) / 16
        target = (1 - p) * t0 + p * t1
        error = norm_error(averaged, target)
        worst = max(worst, error)
        rows.append(
            {
                "p": p,
                "superoperator_operator_error": error,
                "error_if_global_phase_twirl_is_omitted": norm_error(
                    no_global_phase_average, target
                ),
            }
        )
    if worst > 1e-12:
        raise AssertionError("The controlled-direction twirl is not a one-coin channel")
    return {
        "input_dimension": 6,
        "phase_choices": 16,
        "covers_arbitrary_reference": "Full superoperator equality, not selected input states",
        "max_superoperator_operator_error": worst,
        "cases": rows,
    }


def choose_k(p0: float, m: int) -> int:
    cap = min(m / 2, 1 / (4 * math.sqrt(p0)))
    k = math.floor(cap)
    if k % 2 == 0:
        k -= 1
    if k < 1:
        raise ValueError("The theorem needs m>=2 and p0<=1/16")
    return k


def amplified_probability(p: np.ndarray | float, k: int) -> np.ndarray | float:
    return np.sin(k * np.arcsin(np.sqrt(p))) ** 2


def relative_phase(p: np.ndarray | float, k: int) -> np.ndarray | float:
    return 2 * np.arctan(1 - 2 * amplified_probability(p, k))


def amplified_matrix(u: np.ndarray, pi: np.ndarray, k: int) -> np.ndarray:
    d = len(u)
    s0 = np.eye(d)
    s0[0, 0] = -1
    grover = -u @ s0 @ u.conj().T @ (np.eye(d) - 2 * pi)
    return np.linalg.matrix_power(grover, (k - 1) // 2) @ u


def check_amplification(rng: np.random.Generator) -> dict[str, Any]:
    max_probability_error = 0.0
    min_dq_ratio, max_dq_ratio = math.inf, 0.0
    min_df_ratio, max_df_ratio = math.inf, 0.0
    max_finite_difference_relative_error = 0.0
    matrix_cases = 0
    schedule_rows = []
    for p0 in (1 / 16, 1 / 64, 1 / 1024, 1 / 65536):
        for m in (2, 3, 5, 6, 8, 16, 32, 128, 1024):
            k = choose_k(p0, m)
            if 2 * k > m or k < min(m, 1 / math.sqrt(p0)) / 12:
                raise AssertionError("Replay allocation violates a proved k bound")
            grid = np.linspace(p0 / 2, 3 * p0, 257)
            theta = np.arcsin(np.sqrt(grid))
            dq = k * np.sin(2 * k * theta) / np.sin(2 * theta)
            q = amplified_probability(grid, k)
            df = 4 * dq / (1 + (1 - 2 * q) ** 2)
            min_dq_ratio = min(min_dq_ratio, float(np.min(dq / k**2)))
            max_dq_ratio = max(max_dq_ratio, float(np.max(dq / k**2)))
            min_df_ratio = min(min_df_ratio, float(np.min(df / k**2)))
            max_df_ratio = max(max_df_ratio, float(np.max(df / k**2)))
            if np.max(k * theta) >= math.pi / 4:
                raise AssertionError("Amplification left its monotone Grover lobe")
            schedule_rows.append(
                {"p0": p0, "m": m, "k": k, "calls_per_attempt": 2 * k}
            )
            for p in (p0 / 2, p0, 2 * p0, 3 * p0):
                u, pi = unitary_with_probability(8, p, rng)
                a = amplified_matrix(u, pi, k)
                actual_q = float(np.vdot(a[:, 0], pi @ a[:, 0]).real)
                max_probability_error = max(
                    max_probability_error, abs(actual_q - float(amplified_probability(p, k)))
                )
                matrix_cases += 1
            # An independent finite difference of the trigonometric map checks the
            # derivative implementation; matrix probabilities above check its premise.
            p = 1.5 * p0
            step = p0 * 1e-5
            finite_difference = (
                float(relative_phase(p + step, k)) - float(relative_phase(p - step, k))
            ) / (2 * step)
            theta0 = math.asin(math.sqrt(p))
            dq0 = k * math.sin(2 * k * theta0) / math.sin(2 * theta0)
            q0 = float(amplified_probability(p, k))
            analytic = -4 * dq0 / (1 + (1 - 2 * q0) ** 2)
            max_finite_difference_relative_error = max(
                max_finite_difference_relative_error, abs(finite_difference / analytic - 1)
            )
    if max_probability_error > 1e-10:
        raise AssertionError("Local Grover amplification did not preserve the claimed mean")
    if min_dq_ratio < 2 / math.pi - 1e-12 or max_dq_ratio > 1 + 1e-12:
        raise AssertionError("Amplified probability derivative bound failed")
    if min_df_ratio < 4 / math.pi - 1e-12 or max_df_ratio > 4 + 1e-12:
        raise AssertionError("Amplified phase derivative bound failed")
    if max_finite_difference_relative_error > 1e-5:
        raise AssertionError("Phase derivative finite difference is inconsistent")
    return {
        "matrix_cases": matrix_cases,
        "grid_points_per_schedule": 257,
        "max_probability_error": max_probability_error,
        "observed_dq_over_k_squared_range": [min_dq_ratio, max_dq_ratio],
        "proved_dq_over_k_squared_range": [2 / math.pi, 1],
        "observed_abs_df_over_k_squared_range": [min_df_ratio, max_df_ratio],
        "proved_abs_df_over_k_squared_range": [4 / math.pi, 4],
        "max_derivative_finite_difference_relative_error": max_finite_difference_relative_error,
        "schedule_cases": schedule_rows,
    }


def demonstrate_inverse_error() -> dict[str, Any]:
    """A counterexample check: mean drift does not model inverse error."""
    p = 0.25
    u = np.array([[math.sqrt(1 - p), -math.sqrt(p)], [math.sqrt(p), math.sqrt(1 - p)]])
    pi = np.diag([0.0, 1.0])
    bell = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
    rho = np.outer(bell, bell.conj())
    rows = []
    for error_angle in (1e-4, 1e-3, 1e-2):
        e = math.cos(error_angle) * I2 + 1j * math.sin(error_angle) * X
        inverse = e @ u.conj().T
        kraus = gadget_kraus(u, pi, inverse=inverse)
        corrected = np.kron(Z @ kraus[1], I2)
        failed = corrected @ rho @ corrected.conj().T
        failure_probability = float(np.trace(failed).real)
        failure_error = trace_distance(failed / failure_probability, rho)
        k0 = kraus[0]
        success_p_zero = float(np.linalg.norm(k0[:, 0]) ** 2)
        success_p_one = float(np.linalg.norm(k0[:, 1]) ** 2)
        rows.append(
            {
                "inverse_error_angle": error_angle,
                "inverse_operator_error": norm_error(inverse, u.conj().T),
                "mean_drift": 0.0,
                "corrected_failure_reference_trace_distance": failure_error,
                "success_probability_difference_for_probe_Z_eigenstates": abs(
                    success_p_zero - success_p_one
                ),
            }
        )
    if min(row["corrected_failure_reference_trace_distance"] for row in rows) <= 1e-5:
        raise AssertionError("The inverse-error counterexample was not reproduced")
    return {
        "interpretation": (
            "Unchanged preparation mean does not imply a correctable failure branch when "
            "the paired inverse is perturbed. This is an excluded-error example, not a failure "
            "of the exact-inverse theorem."
        ),
        "cases": rows,
    }


def schedule_from_last_level(k: int, last: int, beta: float) -> dict[str, Any]:
    levels = []
    successes = 0
    for j in range(last + 1):
        batch_length = 2**j
        beta_j = beta * 2.0 ** (j - last - 2)
        repeats = math.ceil(128 * math.log(4 / beta_j))
        levels.append((batch_length, repeats))
        successes += 2 * batch_length * repeats
    attempt_cap = math.ceil(4 * successes + 16 * math.log(2 / beta))
    return {
        "k": k,
        "last_level": last,
        "levels": levels,
        "accepted_gate_count": successes,
        "attempt_cap": attempt_cap,
        "primitive_call_cap": 2 * k * attempt_cap,
    }


def ramsey_schedule(p0: float, epsilon: float, m: int, beta: float) -> dict[str, Any]:
    k = choose_k(p0, m)
    a, rho = 4 / math.pi, math.pi / 8
    last = math.ceil(math.log2(rho / (a * k * k * epsilon)))
    return schedule_from_last_level(k, last, beta)


def global_ramsey_schedule(epsilon: float, beta: float) -> dict[str, Any]:
    last = max(0, math.ceil(math.log2((math.pi / 8) / (2 * epsilon))))
    return schedule_from_last_level(1, last, beta)


def sample_ramsey_quadrature(
    rng: np.random.Generator,
    p: float,
    delta: float,
    k: int,
    batch_length: int,
    repeats: int,
    plus_source_weight: float,
    quadrature: str,
) -> tuple[float, int]:
    """Exact renewal simulation for fresh iid two-point source means.

    A source type is redrawn on EVERY attempted source, including failures. The
    accepted type is tilted by its success probability. The negative-binomial
    wait and accepted type counts are independent for this iid marked process.
    This avoids explicitly allocating one item for each charged oracle call.
    """
    means = np.clip(np.array([p - delta, p + delta]), 0.0, 1.0)
    q = np.asarray(amplified_probability(means, k))
    phases = np.asarray(relative_phase(means, k))
    success_rates = (1 + (1 - 2 * q) ** 2) / 2
    w = plus_source_weight
    s = (1 - w) * success_rates[0] + w * success_rates[1]
    accepted_plus_weight = w * success_rates[1] / s
    plus_count = rng.binomial(batch_length, accepted_plus_weight, size=repeats)
    failures = rng.negative_binomial(batch_length, s, size=repeats)
    angles = batch_length * phases[0] + plus_count * (phases[1] - phases[0])
    expectation = np.cos(angles) if quadrature == "X" else np.sin(angles)
    draws = 2 * (rng.random(repeats) < (1 + expectation) / 2) - 1
    attempts = repeats * batch_length + int(failures.sum(dtype=np.int64))
    return float(np.mean(draws)), attempts


def run_ramsey_trial(
    rng: np.random.Generator,
    p0: float,
    p: float,
    epsilon: float,
    delta: float,
    m: int,
    beta: float,
    mode: str,
    global_case: bool = False,
) -> dict[str, Any]:
    schedule = (
        global_ramsey_schedule(epsilon, beta)
        if global_case
        else ramsey_schedule(p0, epsilon, m, beta)
    )
    k = schedule["k"]
    phase_estimate = 0.0
    attempts = 0
    for j, (batch_length, repeats) in enumerate(schedule["levels"]):
        if mode == "equal_mean":
            weight_x = weight_y = 0.5
        elif mode == "balanced_fresh_drift":
            weight_x = weight_y = 0.5
        elif mode == "quadrature_dependent_drift":
            weight_x = 0.95 if j % 2 else 0.05
            weight_y = 1 - weight_x
        elif mode == "history_dependent_drift":
            # Chosen from the earlier classical phase estimate, not future outcomes.
            weight_x = 0.9 if phase_estimate < float(relative_phase(p, k)) else 0.1
            weight_y = 1 - weight_x
        else:
            raise ValueError(mode)
        x, nx = sample_ramsey_quadrature(
            rng, p, delta, k, batch_length, repeats, weight_x, "X"
        )
        y, ny = sample_ramsey_quadrature(
            rng, p, delta, k, batch_length, repeats, weight_y, "minus_Y"
        )
        attempts += nx + ny
        angle = math.atan2(y, x)
        if j == 0:
            phase_estimate = angle
        else:
            lift = round((batch_length * phase_estimate - angle) / (2 * math.pi))
            phase_estimate = (angle + 2 * math.pi * lift) / batch_length
    low_phase = float(relative_phase(1.0 if global_case else 2 * p0, k))
    high_phase = float(relative_phase(0.0 if global_case else p0, k))
    phase_estimate = min(high_phase, max(low_phase, phase_estimate))
    q_estimate = (1 - math.tan(phase_estimate / 2)) / 2
    q_estimate = min(1.0, max(0.0, q_estimate))
    estimate = math.sin(math.asin(math.sqrt(q_estimate)) / k) ** 2
    capped = attempts > schedule["attempt_cap"]
    return {
        "estimate": estimate,
        "absolute_error": abs(estimate - p),
        "within_epsilon": bool(not capped and abs(estimate - p) <= epsilon),
        "attempt_cap_exceeded": bool(capped),
        "actual_attempts": min(attempts, schedule["attempt_cap"]),
        "actual_primitive_calls": 2 * k * min(attempts, schedule["attempt_cap"]),
    }


def check_ramsey(rng: np.random.Generator, trials: int) -> dict[str, Any]:
    beta = 0.05
    cases = []
    for p0 in (1 / 64, 1 / 1024):
        for m in (2, 8, 32, 128):
            epsilon = p0 / 64
            p = 1.4 * p0
            for mode in (
                "equal_mean",
                "balanced_fresh_drift",
                "quadrature_dependent_drift",
                "history_dependent_drift",
            ):
                delta = 0.0 if mode == "equal_mean" else epsilon / 32
                schedule = ramsey_schedule(p0, epsilon, m, beta)
                outcomes = [
                    run_ramsey_trial(rng, p0, p, epsilon, delta, m, beta, mode)
                    for _ in range(trials)
                ]
                errors = np.array([o["absolute_error"] / epsilon for o in outcomes])
                calls = np.array([o["actual_primitive_calls"] for o in outcomes], dtype=np.int64)
                successes = sum(o["within_epsilon"] for o in outcomes)
                # A one-sided exact binomial lower bound is elementary for all-success
                # data; do not invent a general confidence interval for other outcomes.
                lower_if_all_pass = 0.05 ** (1 / trials) if successes == trials else None
                cases.append(
                    {
                        "p0": p0,
                        "p": p,
                        "epsilon": epsilon,
                        "delta_over_epsilon": delta / epsilon,
                        "m": m,
                        "k": schedule["k"],
                        "source_mode": mode,
                        "nominal_success_guarantee": 1 - beta,
                        "trials": trials,
                        "covered_trials": successes,
                        "observed_coverage": successes / trials,
                        "one_sided_95_percent_binomial_lower_if_all_pass": lower_if_all_pass,
                        "attempt_cap_failures": sum(o["attempt_cap_exceeded"] for o in outcomes),
                        "median_error_over_epsilon": float(np.median(errors)),
                        "maximum_error_over_epsilon": float(np.max(errors)),
                        "accepted_gate_count_per_trial": schedule["accepted_gate_count"],
                        "last_ramsey_batch_length": 2 ** schedule["last_level"],
                        "maximum_uses_of_any_source": 2 * schedule["k"],
                        "median_actual_primitive_calls": int(np.median(calls)),
                        "maximum_actual_primitive_calls": int(np.max(calls)),
                        "worst_case_primitive_call_cap": schedule["primitive_call_cap"],
                        "median_calls_times_k_epsilon": float(np.median(calls) * schedule["k"] * epsilon),
                    }
                )
    return {
        "simulation": "Exact compressed renewal sampling of the proved conservative schedule",
        "source_selection_bias_included": True,
        "physical_controlled_call_cost": 1,
        "new_source_per_attempt": True,
        "confidence_interpretation": (
            "Coverage is finite evidence for these seeded cases. It is not a proof, "
            "and per-case binomial bounds are not simultaneous confidence bounds."
        ),
        "cases": cases,
    }


def check_global_corollary(rng: np.random.Generator, trials: int) -> dict[str, Any]:
    """Target the negative-phase, endpoint-clipping, and K=0 branches."""
    rows = []
    beta = 0.05
    for p, epsilon in (
        (0.0, 0.001),
        (1.0, 0.001),
        (0.5, 0.001),
        (0.5, 0.5),
        (0.01, 0.005),
        (0.99, 0.005),
        (0.3, 0.1),
    ):
        schedule = global_ramsey_schedule(epsilon, beta)
        outcomes = [
            run_ramsey_trial(
                rng, 0.0, p, epsilon, epsilon / 32, 2, beta,
                "quadrature_dependent_drift", global_case=True,
            )
            for _ in range(trials)
        ]
        rows.append(
            {
                "p": p,
                "epsilon": epsilon,
                "delta_over_epsilon": 1 / 32,
                "source_means_clipped_to_unit_interval": True,
                "last_level": schedule["last_level"],
                "maximum_uses_of_any_source": 2,
                "trials": trials,
                "covered_trials": sum(o["within_epsilon"] for o in outcomes),
                "attempt_cap_failures": sum(o["attempt_cap_exceeded"] for o in outcomes),
                "maximum_error_over_epsilon": max(o["absolute_error"] / epsilon for o in outcomes),
                "median_actual_primitive_calls": int(np.median(
                    [o["actual_primitive_calls"] for o in outcomes]
                )),
                "worst_case_primitive_call_cap": schedule["primitive_call_cap"],
            }
        )
    return {"targeted_branches": ["negative phases", "p=0", "p=1", "K=0"], "cases": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be positive")
    seeds = np.random.SeedSequence(SEED).spawn(4)
    report = {
        "schema_version": 1,
        "seed": SEED,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_manifest_sha256": hashlib.sha256(
            Path(__file__).with_name("requirements.txt").read_bytes()
        ).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
        "command": f"python verification/run_validation.py --trials {args.trials}",
        "scope": "Finite scientific validation; no proof, novelty, or practical-speedup certificate",
        "arbitrary_garbage_reference": check_arbitrary_garbage(np.random.default_rng(seeds[0])),
        "controlled_inverse_twirl": check_single_use_twirl(),
        "local_amplification": check_amplification(np.random.default_rng(seeds[1])),
        "inverse_error_counterexample": demonstrate_inverse_error(),
        "multiscale_ramsey": check_ramsey(np.random.default_rng(seeds[2]), args.trials),
        "global_corollary": check_global_corollary(np.random.default_rng(seeds[3]), args.trials),
    }
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    cases = report["multiscale_ramsey"]["cases"]
    compact = {
        "output": str(args.output),
        "arbitrary_garbage_cases": report["arbitrary_garbage_reference"]["unitary_cases"],
        "twirl_error": report["controlled_inverse_twirl"]["max_superoperator_operator_error"],
        "amplification_error": report["local_amplification"]["max_probability_error"],
        "ramsey_cases": len(cases),
        "ramsey_trials": sum(c["trials"] for c in cases),
        "ramsey_covered_trials": sum(c["covered_trials"] for c in cases),
        "ramsey_max_error_over_epsilon": max(c["maximum_error_over_epsilon"] for c in cases),
        "global_corollary_trials": sum(
            c["trials"] for c in report["global_corollary"]["cases"]
        ),
        "global_corollary_covered_trials": sum(
            c["covered_trials"] for c in report["global_corollary"]["cases"]
        ),
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
