# Counterexamples Found During property-test.py Development

This document records 3 real counterexamples that Hypothesis found during the development of the `workspace/math-templates/property-test.py` tool. These are useful as reference when analyzing future Hypothesis failures — they show the range of possible root causes.

## Counterexample 1: Cross-Entropy Self-Test Was Wrong

**Test:** `test_cross_entropy_self_zero(logits_val)` — "H(p,p) ≈ 0"

**Finding:** Hypothesis generated uniform logits (all equal), producing a uniform softmax distribution where H(p,p) = log(n).

```
EXAMPLE: logits = [0.0, 0.0, 0.0, 0.0, 0.0]
         softmax = [0.2, 0.2, 0.2, 0.2, 0.2]
         H(p,p) = log(5) ≈ 1.609, NOT 0
```

**Root cause:** Test invariant was mathematically wrong. H(p,p) = entropy(p). For a uniform distribution over n classes, entropy = log(n). Only a delta distribution (one-hot p) has zero entropy. The test should verify that cross-entropy ≥ 0, and that it approaches 0 only when p approaches a one-hot.

**Resolution:** Rewrote the test to check `ce >= -1e-10` always, and `ce < 0.01` only when `max(p) > 0.9999`.

## Counterexample 2: `min ≤ mean ≤ max` Failed on Large Identical Floats

**Test:** `test_min_leq_mean_leq_max(data)` — Basic statistical invariant

**Finding:** Hypothesis generated an array where all elements were ≈ 699051.1926003604, and `np.mean()` returned a value 1 ULP higher than both min and max.

```
EXAMPLE: data ≈ [699051.1926003604, 699051.1926003604, ...]
         min = 699051.1926003604
         mean = 699051.1926003605  (1 ULP higher!)
         max = 699051.1926003604
```

**Root cause:** Float64 summation for large identical values accumulates rounding error. The mean of identical values should equal that value, but IEEE 754 summation is not exact for large arrays. 699051 ≈ 2¹⁹, and the repeated addition introduces ±1 ULP error.

**Resolution:** Changed from absolute tolerance `1e-12` to relative tolerance `1e-10 * max(1.0, abs(mu))`.

## Counterexample 3: Softmax Monotonicity via argsort Failed on Ties

**Test:** `test_softmax_monotonic(x)` — "大 logit 应得大概率"

**Finding:** Hypothesis generated logits with equal values, where `np.argsort` has arbitrary ordering for ties. The argsort of logits and argsort of probabilities could legitimately differ while the strict monotonicity property holds.

```
EXAMPLE: x = [-0.0, 0.0, 0.0, 0.0, 0.001]
         # Ties at -0.0 = 0.0 → argsort can return any permutation
```

**Root cause:** `np.array_equal(np.argsort(x), np.argsort(p))` is too strict — it requires consistent ordering of equal elements, but floating-point representation can give -0.0 vs 0.0 different positions in memory while treating them as equal in value comparison.

**Resolution:** Replaced the argsort comparison with pairwise strict checks: "if x_i > x_j + 1e-12, then p_i > p_j - 1e-12". This correctly handles ties while preserving the mathematical invariant.

## Summary Table

| # | What broke | Root cause | Fix |
|---|-----------|------------|-----|
| 1 | Cross-entropy H(p,p) ≈ 0 | Test invariant wrong | Rewrite: entropy ≥ 0, zero only for one-hot |
| 2 | min ≤ mean ≤ max | IEEE 754 accumulation error | Relative tolerance, not absolute |
| 3 | softmax argsort equality | Float ties (-0.0 vs 0.0) | Pairwise strict comparison |

## Lessons for Future Counterexample Analysis

When Hypothesis finds a counterexample, classify it as:

1. **Code bug (real find):** The implementation violates the mathematical invariant.
2. **Test bug (false alarm):** The test invariant is wrong or too strict.
3. **Precision limitation:** The math is correct but floating-point arithmetic can't represent it exactly at the requested tolerance.

Don't assume it's (1) — always check (2) and (3) first.

## Tool Growth (Session 2026-07-05)

This session added 3 new tools to the `mathkit` suite, bringing the total to 6:

| Tool | mathkit alias | Purpose |
|------|--------------|---------|
| `matrix-health.py` | `mathkit matrix` | Diagnose condition number, SVD, eigenvalues, numerical rank. Catches near-singular, rank-deficient, and non-positive-definite matrices. |
| `precision-compare.py` | `mathkit precision` | Cross-precision error analysis (float16/32/64). 10 benchmarks ranging from softmax to catastrophic cancellation to log1p. |
| `convergence-viz.py` | `mathkit convergence` | Simulate SGD/Momentum/Adam on Beale, Rosenbrock, saddle, Rastrigin, quadratic surfaces. Plots optimization trajectory, loss curve, gradient norm. |

Key findings from developing these tools:
- **Saddle points are optimizer killers:** SGD flies along the negative curvature direction (loss → -10²⁴). Adam limits it to -500. Momentum is in between.
- **log1p vs log(1+x):** Even float32 has 5.96e+22 relative error for `log(1+x)` at small x. Use `log1p` always.
- **Hilbert matrix cond:** 8×8 Hilbert has cond ≈ 1.5e+10, making `solve()` produce garbage without regularization.

## `mathkit` Launcher

All 6 tools are now accessible via `mathkit <tool> [args]` after venv activation. The launcher lives at `~/.hermes/profiles/xiandaishuxuejia/bin/mathkit` and is symlinked into `.venv/bin/` for PATH access.

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
mathkit              # list all tools
mathkit numerical    # run numerical safety scan
mathkit matrix       # run matrix health check
```
