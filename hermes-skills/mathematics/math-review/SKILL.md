---
name: math-review
description: "Use when reviewing mathematical content for correctness — numerical stability, property-based verification, proof checking, edge case analysis, and symbolic computation validation. Unlike scientific-figure-making (creates visual figures) or triangle-verification-team (multi-agent verification protocol), math-review is a human-readable mathematical correctness review of content. Do NOT use for generating figures (scientific-figure-making) or orchestrating verification agents (triangle-verification-team)."
version: 1.0.0
author: Hermes Agent (xiandaishuxuejia profile)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [math, numerical-analysis, code-review, verification, property-testing]
    related_skills: [requesting-code-review, test-driven-development, systematic-debugging]
---

# Math Review — Numerical Correctness & Stability

## Overview

Mathematical correctness is **not** the same as passing unit tests. Code that compiles and returns finite outputs can still be mathematically wrong — `exp(x)` without `x - max(x)` before softmax, `inv(A) @ b` instead of `solve(A, b)`, `log(1+x)` instead of `log1p(x)`. This skill is the procedural side of the **xiandaishuxuejia** (现代数学家) profile: bridge mathematical theory with engineering implementation.

**Core principle:** Every mathematical invariant must survive an actual computational attack, not just a hand-wavy "that looks right."

## When to Use

**Always activate when:**

- Asked to review PRs involving: loss functions, softmax/normalization, linear algebra, probability computations, optimization algorithms
- Asked to debug training instability (NaN/Inf losses, gradient explosion, convergence failure)
- Asked to verify a derivation, proof, or algorithm against a code implementation
- Asked to analyze numerical precision or choose between float16/32/64
- Asked about matrix conditioning, rank deficiency, or eigenvalue problems
- Asked to write tests for mathematical functions

**Skip for:** pure infrastructure/CI changes, UI layout, string parsing, config file edits.

## Pre-requisites

## `mathkit` / `physicskit` / `advmath` — Triple Launcher System

All tools accessible via **three launchers** after venv activation:

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
mathkit <tool> [args]      # 基础数学 — 10 tools (numerical/symbolic/matrix/contradiction/scaffold...)
physicskit <tool> [args]   # 物理验证 — 4 tools (dim/const/valid/kinematics)
advmath <tool> [args]      # 高等数学 — 3 tools: aa(抽象代数) ra(实分析) dg(微分几何)
```

`mathkit` lives at `.venv/bin/mathkit` (auto-PATH). `physicskit` and `advmath` at `workspace/physics-templates/` and `workspace/advanced-math-templates/` — source venv first.

## Proof-Gap Resolution (Session 2026-07-05)

For trigonometric高考 techniques (cos 5x expansion, critical-point families, minimax argument) see `references/trigonometric-hk-analysis.md`.

This session's main mathematical output was **closing a proof gap** in a 高考 abstract-function problem. Unlike the Hypothesis counterexamples above (which were about numerical/tool correctness), this was a **logical proof gap** in a human-written solution.

### Discovery Process

1. **Identify**: The solution said "篇幅所限，其余子情况的论证与上述核心逻辑类似" — this is a signal that the proof is incomplete.
2. **Isolate**: The gap only affected Step 2's case where $f(a) \geq 1$.
3. **Verify**: Tried existing methods (interval construction) — confirmed they fail because $2^x$ range $(0,1)$ can't cover $\geq 1$ values.
4. **Resolve**: Found the `a - b` test element technique — a contradiction that doesn't depend on the failing construction.

### The Key Insight

The trick is to **stay within the KNOWN region** of the function. When $f(b) < 1$, you know $f(b) = 2^{t_b}$ and can characterize $D(t_b)$. Even without knowing the exact form of $D(t_b)$ (which would require the odd extension from part (2)), you know one crucial property: **$D(t_b)$ contains NO negative numbers**. This is enough to create a contradiction with $d = a - b < 0$ being forced into $D(b) = D(t_b)$.

### Generic Pattern

This technique generalizes to any abstract-function problem with D-sets:

1. When a function value falls in the range of a known fragment ($2^x$ on negatives), use condition ① to link the D-set to the known fragment's D-set.
2. Even a partial characterization of the known D-set (like "no negatives") may be enough to force a contradiction.
3. Look for "test elements" — specific numbers that must belong to certain D-sets but are excluded from others.

The full analysis is in `references/gaokao-proof-gap-analysis.md`.

## Trigonometric Inequality Proof Technique (Distance-from-πℤ Method)

A general technique for proving inequalities involving \( |\sin(m\alpha)|, |\sin(n\alpha)|, |\sin(mn\alpha)| \) was developed in session 2026-07-07. The core strategy:

1. **Rewrite** to canonical form \( AB(mA+mB-1) + C(A+B) > 0 \)
2. **Case split** on \( mA+mB \ge 1 \) (trivial) vs \( mA+mB < 1 \)
3. **Small-C contradiction lemma**: if \( C \le 1/(16m) \), use \( \operatorname{dist}(mn\alpha, \pi\mathbb Z) \le \pi/(32m) \) to bound \( A+B \) from below, proving \( m(A+B) > 1 \) — contradicting the Case 2 assumption
4. **Combined bound**: when truly in Case 2, \( C > 1/(16m) \ge T(1-mT)/4 \) for \( T=A+B \), giving \( CT > T^2(1-mT)/4 \ge AB(1-mT) \)
5. **Boundary**: \( m=1 \) or \( n=1 \) handled by direct substitution

The key reusable insight is **Step 3**: a small value of \( |\sin(mn\alpha)| \) forces \( mn\alpha \) near \( k\pi \), which (via the triangle inequality on distances) forces \( |\sin(m\alpha)| + |\sin(n\alpha)| \) to be large enough to escape the hard case.

Full proof, tools table, and pitfalls in `references/trigonometric-inequality-distance-method.md`.

含参三角函数恒等式（\((1-a-x)\sin x-(1+a+x)\cos x\ge0\) 型）的处理模式见 `references/trigonometric-parametric-inequality.md`。

含参指数+对数不等式（\(ae^{x-1}-\ln x+\ln a\ge1\) 型）的消参工作流见 `references/parametric-exponential-log-pattern.md`。

## Symbolic Conic Sections (解析几何) Problem-Solving

高考解析几何大题可以用 SymPy 符号求解 + matplotlib 几何验证的完整流程来解。流程如下:

1. **参数提取** → SymPy: `c`, `e`, `a = c/e`, `b² = a² - c²`
2. **直线-椭圆联立** → `Poly(eq_simplified, x)` + 韦达定理
3. **目标表达式化简**（面积/角度/比值）→ 代入 `y_i = k(x_i+1)`, 利用 `R = -P` 对称性
4. **解方程或求最值** → `solve()` 或 `diff` + AM-GM
5. **数值验证 + 几何画图** → `float()` + `matplotlib` + `Polygon` patches

### 关键代数化简技巧

| 表达式 | 化简方法 | 结果 |
|--------|---------|------|
| `x₁ - x₂` | 韦达差公式 `(x₁-x₂)² = (x₁+x₂)² - 4x₁x₂` | `12√(k²+1)/(4k²+3)` |
| `x₁y₂ - x₂y₁` | 代入 `y_i = k(x_i+1)` | `k(x₁ - x₂)` |
| `tan∠PQR` | `det(QP,QR) / dot(QP,QR)` | `4k + 3/k` |

对称性: **R = -P**（PO 过原点 O 时），得 `S(△PQR) = |x₁y₂ - x₂y₁| = k|x₁ - x₂|`.

完整工作流含可复用的代码模板见 `references/sympy-conic-sections.md`。

## `mathplot` — Chinese Matplotlib Convenience Module

A new helper module `templates/mathplot.py` (also at `workspace/math-templates/mathplot.py`) provides one-line Chinese font configuration and default math-viz styling.

for geometry figures (ellipse, triangles, focus annotations) see `references/geometry-plotting.md`.

For document-to-structured-math-input (images/PDFs/scan → OCR → structured Markdown) see `references/external-doc-parsing.md`.

For TikZ figure quality rules (overlapping labels, tick fonts, angle arc alignment, `\hfill` spacing) see `references/tikz-figure-qa.md`.

```python
import sys; sys.path.insert(0, '.')
import mathplot  # auto-configures PingFang SC, axes.unicode_minus, grid, font sizes

# or use convenience wrappers:
from mathplot import savefig, subplots, demo
fig, axes = subplots(1, 2, figsize=(10, 4))
# ... plot ...
savefig('/tmp/output.png')
```

The module auto-detects system Chinese fonts (PingFang SC → Heiti SC → Hiragino Sans GB → STKaiti) and falls back gracefully if none are found. See the `demo()` function for a ready-to-run verification example.

Templates live at `workspace/math-templates/` (inside the profile):

| Tool | File | mathkit alias | What it does |
|------|------|--------------|-------------|
| numerical-check | `numerical-check.py` | `mathkit numerical` | log/exp/sqrt/div/softmax safety scan |
| symbolic-check | `symbolic-check.py` | `mathkit symbolic` | SymPy dual-track derivation verification |
| property-test | `property-test.py` | `mathkit property` | Hypothesis counterexample search (15 invariants) |
| matrix-health | `matrix-health.py` | `mathkit matrix` | Cond number, SVD, eigenvalue, rank analysis |
| precision-compare | `precision-compare.py` | `mathkit precision` | float16/32/64 cross-precision error report |
| convergence-viz | `convergence-viz.py` | `mathkit convergence` | Optimization trajectory, loss curve, gradient norm |
| **kde-1d** | `utils_kde.py` (workspace/math-templates/) | 直接运行 `python3 utils_kde.py` | Self-contained KDE — Silverman 高斯核密度，无需 scipy |

## Workflow

### Step 1 — Identify the math domain

Before running tools, map the problem to its mathematical structure:

- **Numerical stability** (softmax, log, exp, division) → numerical-check
- **Derivative/integral verification** → symbolic-check
- **Algorithm invariants** (sum-to-1, monotonicity, symmetry) → property-test
- **Matrix properties** (conditioning, rank, definiteness) → matrix-health
- **Precision choice** (is float32 enough?) → precision-compare
- **Convergence behavior** (does it oscillate? diverge?) → convergence-viz

### Step 2 — Run the relevant checks

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate

# Numerical safety scan (default: float32) — use mathkit from any dir
mathkit numerical

# Symbolic derivation
mathkit symbolic deriv 'x**3 + sin(x)' x '3*x**2 + cos(x)'

# Property-based counterexample search
mathkit property softmax

# Matrix diagnosis
mathkit matrix

# Precision comparison
mathkit precision softmax

# Convergence visualization
mathkit convergence saddle
```

### Step 3 — Check mathematical invariants

The invariants that matter most (ordered by how often they break in practice):

| Invariant | Tool | Common failure |
|-----------|------|----------------|
| `Σ softmax(x) = 1` | property-test softmax | `exp(x-max(x))` not used, overflow at x=88+ |
| `log(exp(x)) ≈ x` | property-test algebra | `exp(x)` overflow for x>88 (float32) |
| `A @ inv(A) ≈ I` | property-test matrix | `cond(A) > 1e12`, using `inv()` instead of `solve()` |
| `min ≤ mean ≤ max` | property-test stats | float64 accumulation error for large identical values |
| Cross-entropy non-negative | property-test softmax | p_pred=0 → log(0) |
| z-score mean=0, std=1 | property-test stats | std=0 (constant input) division by zero |

### Step 4 — Classify findings (QA gate severity)

Use the same four-level scale as the mathematician profile:

| Rating | Meaning | Action |
|--------|---------|--------|
| 🔴 **FAIL** | Math error, NaN risk, invariant broken, `np.linalg.inv` used | Block merge. Must fix. |
| 🟡 **PASS+** | All invariants hold, numerically stable, precision documented | Ready to merge |
| 🟠 **PASS** | Correct but missing edge-case handling or precision boundary | Fix before merge |
| 🟢 **PASS+** | Mathematically proven + tested + precision-verified | Gold standard |

**Rule:** A single `np.linalg.inv` = auto-FAIL. No exceptions.

### Step 5 — Report (include evidence)

Each finding must include:

```
PROBLEM:  log(x) without +eps guard → NaN when x ≤ 0
EVIDENCE: numerical-check.py confirmed 2 NaN cases in float32
FIX:      x = log(x + 1e-8)  [or appropriate eps for dtype]
SEVERITY: 🔴 FAIL — blocks merge
```

## Known Pitfalls (from real counterexamples found)

### Pitfall 1: `return True` in Hypothesis `@given` tests

```python
@given(st.floats())
def test_something(x):
    assert x == x
    return True  # ❌ Hypothesis rejects non-None returns
```

**Fix:** Remove `return True`. Hypothesis tests must return `None` or raise.

### Pitfall 2: `hypothesis.seed()` is NOT a context manager

```python
# ❌ Runtime error: 'function' object does not support context manager
with seed(42):
    test_fn()

# ✅ Use the decorator
@seed(42)
@given(...)
def test_fn(x): ...

# Or call directly (Hypothesis uses deterministic seeds internally)
test_fn()
```

### Pitfall 3: Self cross-entropy `H(p,p)` is entropy, not zero

The invariant `H(p,p) ≈ 0` is WRONG. For a uniform distribution over n classes, `H(p,p) = log(n)`. Only a delta distribution (one-hot) has zero entropy.

```python
# ❌ Wrong
assert ce < 1e-6

# ✅ Correct: entropy is non-negative, zero only for one-hot
assert ce >= -1e-10
if np.max(p) > 0.9999:
    assert ce < 0.01
```

### Pitfall 4: `min ≤ mean ≤ max` needs relative tolerance for large values

For arrays of identical large values (e.g., all elements ≈ 699051), float64 mean accumulation can be 1 ULP above max:

```python
# ❌ Fails for large identical floats
assert mn - 1e-12 <= mu <= mx + 1e-12

# ✅ Relative tolerance
tol = 1e-10 * max(1.0, abs(mu))
assert mn - tol <= mu <= mx + tol
```

### Pitfall 5: Softmax monotonicity needs pairwise comparison, not argsort

`argsort(x) == argsort(softmax(x))` fails when logits have equal values (floating tie).

```python
# ❌ Fails on ties (equal logits → argsort order is arbitrary)
assert np.array_equal(np.argsort(x), np.argsort(p))

# ✅ Pairwise strict comparison
for i, j in product(range(len(x)), range(len(x))):
    if x[i] > x[j] + 1e-12:
        assert p[i] > p[j] - 1e-12
```

### Pitfall 6: Hypothesis sometimes finds "bugs in the test, not the code"

When Hypothesis finds a counterexample, it might be a bug in:
- The code under test (the real find)
- The test invariant itself (you wrote the wrong property)
- The floating-point tolerance (too tight for the dtype)

Always investigate before declaring a code bug.

### Pitfall 7: Parallel-line folding geometry — 邻补角 vs 同位角混淆（严重）

在平行纸带折叠问题中，给定 AD ∥ BE，折痕 DE，A-D-H 共线（上边及其延长线）。

❌ **常见错误**：认为 ∠EDH = ∠BED（如图中看上去像同位角，或凭直觉认为"DE截平行线"）。

✅ **正确关系**：
```
AD ∥ BE，DE 截线
⇒ ∠ADE = ∠BED   (内错角)  
A-D-H 共线
⇒ ∠ADE + ∠EDH = 180°  (邻补角)
⇒ ∠EDH = 180° − ∠BED
```

**原因**：∠EDH 的顶点 D 在平行线 AD 上，但边 DH 是 AD 的**延长线**（不是平行线的另一条），所以 DE 与 DH 的夹角不是同位角关系，而是与 ∠ADE 互补的邻补角关系。

**纠正测试**：代入具体值检验——若 ∠BED = 36°，则 ∠EDH = 144°（不是 36°）。在 SymPy 中验证：
```python
x = sp.symbols('x')
# ❌ 错误假设
eq_wrong = sp.Eq(x, sp.pi - x)  # ∠EDH = ∠BED
# ✅ 正确假设  
eq_right = sp.Eq(sp.pi - x, sp.pi - x)  # ∠EDH = π - ∠BED
```

**触发场景**：任何平行纸带折叠问题中，当上边上的点 D 与延长线上的点 H 构成 ∠EDH 时。追问：H 是否与 A、D 共线？若是，∠ADE 和 ∠EDH 是邻补角（和为 180°），不是同位角。

## Template Quick Reference

All commands use `mathkit` (available on PATH after venv activation).

### numerical-check.py
```bash
# All checks at float32 default
mathkit numerical

# All three precisions
mathkit numerical --all

# Single check
mathkit numerical softmax
```

### symbolic-check.py
```bash
# Derivative verification
mathkit symbolic deriv 'sin(x)' x 'cos(x)'

# Integral (no manual → auto numeric fallback)
mathkit symbolic integrate 'x**2' x

# Gradient (multivariate)
mathkit symbolic gradient 'x**2 + y**2' x y
```

### property-test.py
```bash
# All test groups
mathkit property

# Single group
mathkit property softmax

# Reproducible seed
mathkit property matrix --seed 42

# List available tests
mathkit property --list
```

### matrix-health.py
```bash
# Demo with examples (Hilbert, Vandermonde, etc.)
mathkit matrix

# Check a numpy file
mathkit matrix check my_matrix.npy

# Generate and check random matrix
mathkit matrix random 50
```

### precision-compare.py
```bash
# Full benchmark suite
mathkit precision

# Single benchmark
mathkit precision softmax

# Custom function
mathkit precision custom "x ** 3 - 2 * x"

# Save plots
mathkit precision --save /tmp/
```

### convergence-viz.py
```bash
# Full demo (5 scenarios)
mathkit convergence

# Single scenario
mathkit convergence saddle
mathkit convergence optimizers
mathkit convergence lr

# Save images
mathkit convergence --save /tmp/
```

## Physics & Advanced Math Tools Extension (物理验证 & 高等数学)

### Physics Tools (physicskit)

When the math review involves **physics-applied problems** (水压力、抛体、碰撞、简谐), use physics-specific tools alongside the math review tools:

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate

# 量纲一致性验证
physicskit dim 'F = m*a' 'E = m*g*h + 0.5*m*v^2'

# 物理常数查询
physicskit const g

# 物理合理性验证 (速度/能量/力的日常范围检查)
physicskit valid check speed 300000000 m/s

# 运动学符号推导 (抛体/SHM/碰撞/圆周运动)
physicskit kin projectile v0=10 theta=45
```

### 定积分物理应用 — 验证模式

For hydrostatic pressure problems (`F = ∫ ρg·y·w(y)·dy`):

| 步骤 | 方法 | 容差 |
|------|------|------|
| 1. SymPy 符号积分 | `sp.integrate` | — |
| 2. 量纲验证 | `physicskit dim` | 左右量纲一致 |
| 3. 数值积分 (梯形法 N=10000) | `np.sum` | 相对误差 < 0.01% |
| 4. 比例验证 | 代入给定比例 | 精确匹配 |

### 概率问题 — Monte Carlo 验证模式

For probability/expectation problems (泊松分布、期望、方差):

```python
import numpy as np
np.random.seed(42)

# 例: X ~ P(1), Z=Y-X ~ P(2), X⊥Z, Y=X+Z
X = np.random.poisson(1, 10**6)
Z = np.random.poisson(2, 10**6)
Y = X + Z

# 验证
E_XY_mc = np.mean(X * Y)           # ≈ 4
cov_XZ = np.cov(X, Z)[0,1]         # ≈ 0 (独立性)
assert abs(E_XY_mc - 4) / 4 < 5e-4
assert abs(cov_XZ) < 0.01
```

| 检查项 | 期望值 | 容差 |
|--------|--------|------|
| `E[XY]` (Monte Carlo) | 与解析解一致 | 相对误差 < 5×10⁻⁴ |
| `Cov(X, Y-X)` | ≈ 0 (独立性) | < 0.01 (N=10⁶) |
| `E[X]`, `E[Y-X]` | 与分布参数一致 | 相对误差 < 5×10⁻⁴ |

### Advanced Math Tools (advmath)

Three tools for abstract algebra, real analysis, and differential geometry:

```bash
# 抽象代数
advmath aa group S4            # 置换群信息 (阶/生成元/子群阶分布/可解性)
advmath aa galois GF 5         # 有限域 GF(5)
advmath aa nt 30               # 数论函数 (φ/μ/因子分解)

# 实分析
advmath ra epsilon 100 0.01 '1/n'    # ε-N 验证 (自动找 N)
advmath ra uniform 'x/n' 0 1 0.01    # 一致收敛性
advmath ra series '1/n**2'           # 级数收敛
advmath ra fourier 'x' -3.14 3.14 5  # Fourier 级数 + 数值验证
advmath ra lp-norm 'x**2' a=0 b=1 p=2  # Lp 范数

# 微分几何
advmath dg sphere r=2                # 球面: Christoffel + 曲率 (验证 2/R²)
advmath dg curvature 'x**2+1'        # 自定义度规曲率
advmath dg lie-bracket '[-y,x]' '[x,y]'  # Lie 括号
```

**抽象代数验证模式**（群同态定理验证）：

当需要验证抽象代数定理（如同态基本性质）时，用 SymPy `combinatorics` 做实例验证：

```python
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup

# 构造同态 φ: S₃ → S₄ (嵌入, 固定第4点)
def phi(p):
    return Permutation([p(i) if i < 3 else 3 for i in range(4)])

# 验证三条性质
e3, e4 = SymmetricGroup(3).identity, SymmetricGroup(4).identity
assert phi(e3) == e4                                                    # 性质1
assert all(phi(a**-1) == phi(a)**-1 for a in S3.elements)              # 性质2
assert all(int(a.order()) % int(phi(a).order()) == 0 for a in S3.elements)  # 性质3
```

## Integration with Other Skills

**`requesting-code-review`** — Run this skill *before* the general code review. Math errors caught here won't make it into the security/lint pipeline.

**`test-driven-development`** — Property-based tests (Hypothesis) are TDD for math invariants: write the invariant as the test, watch it fail against the naïve implementation, then write the numerically stable version.

**`systematic-debugging`** — NaN/Inf in training loss? Run `mathkit numerical` on the loss function first. Then `mathkit property` on softmax/log/exp components. The root cause is almost always a numerical stability issue, not an architecture issue.

---

## Extended Application: 高考数学证明审查 (Proof Structure Review)

While the main skill above focuses on **numerical/code correctness**, mathematicians also review **proof logic** — the abstract deductive chain where no code runs. The session that produced this addition reviewed a 高考 (Chinese Gaokao) abstract-function problem solution.

### When to Activate Proof Review Mode

Use this extension when the deliverable is a **formal proof** (not a code implementation):
- 高考/竞赛数学压轴题
- Algorithm correctness proofs
- Convergence/optimality proofs
- Theorem derivations

### Workflow

#### Step 1 — Map the dependency graph

Before analyzing each sub-problem, draw the dependency chain:

```
(3)(i): f(0) ≥ 1  ──→  Lemma: f(x) < 1 for x∈(0,1)  ──→  Step 1: monotonic on (0,1)  ──→  Step 2: monotonic on [1,∞)
```

Check for:
- **Circular dependencies** (A needs B, B needs A — fatal unless mutual induction)
- **Hidden assumptions** imported from earlier problem parts that may not carry over
- **Unstated premises** the proof assumes but the problem didn't give

#### Step 2 — Sub-problem decomposition with todo

Break the proof into logically independent units and check each one:

```markdown
1. ✅ Part (1): D(-1) computation — check endpoints, classification
2. ✅ Part (2): D(x₂) ⊆ D(x₁) — verify D(x) formulas, case coverage
3. 🔶 Part (3)(ii) Step 2: monotonic on [1,∞) — GAP FOUND
```

#### Step 3 — Check each sub-problem against a fixed set of criteria

| Criterion | What to look for |
|-----------|------------------|
| **Correctness** | Are the algebraic/algebraic steps valid? |
| **Completeness** | Are ALL cases handled? "分类讨论" must be exhaustive |
| **Assumption honesty** | Does the proof import assumptions not established in this part? |
| **Edge-case handling** | 0, negative, boundary, extremal values — are they covered? |
| **Gap detection** | "显然" "同理" "类似可证" "篇幅所限" — translate these into actual reasoning before accepting |

#### Step 4 — Use symbolic verification where possible

Even for abstract proofs, verify the concrete sub-parts numerically:

```python
# Verify D(-1) endpoints
for d in [0, 0.5, 1, 1.2, 1.5]:
    f_val = f_part1(-1 + d)
    print(f'd={d}: f(..)={f_val}, >1/2? {f_val > 0.5}')
```

#### Step 5 — Rate each sub-problem; the overall rating is the WEAKEST link

| Rating | Meaning | Example from session |
|--------|---------|---------------------|
| ✅ EXCELLENT | Correct, complete, rigorous | Part (1), Part (2), (3)(ii) Step 1 |
| ✅ PASS+ | Correct but minor polish needed | Lemma proof |
| 🔶 PASS | Clear gap that doesn't break the whole but needs patching | **Whole solution**, held back by (3)(ii) Step 2 |
| ❌ FAIL | Fatal logical error or gap | (3)(ii) Step 2 — case f(a) ≥ 1 unresolved |

**Rule:** A single unhandled case = the WHOLE proof is downgraded to PASS or FAIL.

### Key finding from session: "Classified Similar" is NOT a valid proof move

The reviewed solution said:

> "篇幅所限，其余子情况的论证与上述核心逻辑类似"

This translates to: "We didn't actually check the other cases." **In a rigorous proof review, this is a FAIL for that part.** Every case must be explicitly addressed or provably reducible to an addressed case.

### Proving a proof has a gap: methodology

When you find a gap (like the `f(a) ≥ 1` case in Step 2), document it precisely:

1. **Locate the exact spot** in the proof where the existing method fails
2. **Explain WHY it fails**: the interval construction requires `f(a) < 1` to find `t_a < 0` with `2^{t_a} = f(a)`. When `f(a) ≥ 1`, `2^x` range `(0,1)` can't cover it.
3. **Map the sub-cases** that would need independent treatment:
   | Sub-case | Attempted path | Closes? |
   |----------|---------------|:-------:|
   | f(0) > f(a) ≥ 1 | -a ∈ D(a) ⊆ D(b) ⇒ f(b-a) > f(b) | ❌ |
   | f(0) ≤ f(a) | D(a) ⊆ D(0) | ❌ |
4. **Assess severity**: Is this a fatal gap (proof collapses) or a recoverable omission?

### Technique: The `a - b` test element

When a proof involves D-sets and a contradiction seems out of reach, try the **`a - b` test element**:

> For $a < b$ with $f(a) > f(b)$, the element $d = a - b < 0$ must satisfy $d \in D(b)$ (because $b + d = a$ and $f(a) > f(b)$). But $D(b)$ may be constrained by the function's behavior on a known domain — forcing $d \notin D(b)$ and creating a contradiction.

**Concretely**, this technique works when:
- $f(a) \geq 1$, so $D(a) = \varnothing$ (and $a$ is a global maximum)
- $f(b) < 1$, so $f(b) = 2^{t_b}$ for some $t_b < 0$, and $D(b) = D(t_b)$
- For $t_b < 0$, $D(t_b)$ cannot contain **any** negative $d$ (because $t_b + d < t_b < 0$ keeps $f(t_b+d)$ in the $2^x$ regime where $2^{t_b+d} < 2^{t_b}$)
- But $d = a - b < 0$ IS in $D(b)$ (by definition), forcing a contradiction

This is a **generic pattern**: whenever a proof has a gap, there are almost always two elements living in different "function regimes" (one $\geq 1$, one $< 1$; one negative, one positive) that produce conflicting membership in the same D-set.

### Pitfall: "Classified Similar" is NOT a valid proof step

When the solution says "篇幅所限" (space limited), "类似可证" (can be proved similarly), or "其余情况同理" (other cases are analogous) — **verify each remaining case explicitly**. A proof that relies on unverified cases is incomplete.

---

## Pursuit-Evasion Game Analysis (新增 2026-07-07)

A pattern for **discrete-time pursuit-evasion games** with noisy/incomplete measurements, where both players move at speed 1 per round.

### Trigger conditions

- Two agents on the plane with equal speed constraints
- Noisy measurement of evader's position with bounded error
- Adversarial feedback ("device reports a point with |P_n - A_n| ≤ 1")
- "Can the pursuer guarantee distance ≤ T after N rounds?" type questions

### Key findings from session

1. **Optimal strategy**: Move toward P_n (minimax optimal, proven by triangle inequality)
2. **Growth rate**: d_n ~ n^0.338, NOT linear despite upper bound d_n ≤ d_{n-1}+2
3. **Critical lesson**: Upper bounds from triangle inequality may NOT be tight — the constraint |A_n - A_{n-1}| = 1 prevents A_n from being at the worst position in Disk(P_n, 1)

### Pitfall: Bounds tightness

After deriving any upper/lower bound, ALWAYS construct an explicit adversarial sequence to check if the bound is achievable. An untight bound can lead to wrong qualitative conclusions (e.g., claiming linear growth when actual growth is n^0.338).

Full pattern, template code, and analysis workflow in `references/pursuit-evasion-analysis.md`.

## 高考含参不等式恒成立问题 (2026-07-07)

高考导数压轴题常见类型：参数在指数/对数+多项式中，要求 \(f(x)\ge0\) （或 \(\le0\)）对 \(x\ge0\) 恒成立。

### 标准流程

1. **参变分离**：\(a\ge g(x)\) 或 \(a\le g(x)\)
2. **Taylor 展开必要条件**：在 \(x=0\) 处展开，最低阶项给出参数的必要范围
3. **求 \(g(x)\) 极值**：将 \(g'(x)\) 分子因式分解为 \((x-x_0)\varphi(x)\)，证明 \(\varphi(x)\) 定号，确认唯一驻点即最值点
4. **整数优化**（参数为整数时）：取比实数阈值大的最小整数
5. **充分性验证**：临界参数值处在 SymPy 中数值扫描

### 关键技巧

\(g'(x)\) 分子通常可分解为 \((x-x_0)\varphi(x)\)，其中 \(\varphi(0)=0\) 且 \(\varphi'(x)<0\) 在 \(x>0\) 恒成立，从而 \(\varphi(x)\) 定负，唯一驻点即为最大值点。

完整工作流和常见变形（含参恒成立、极值点偏移、隐零点代换、切线围面积、三角不等式 \(\sin x\pm\cos x\) 简化）见 `references/derivative-inequality-patterns.md`。

## 极值点偏移 (2026-07-07)

**触发条件**：\(f(x_1)=f(x_2)\)，\(x_1\neq x_2\)，求证 \(x_1+x_2>2c\)（或 \(<2c\)），其中 \(c\) 为极值点。

**统一方法**：构造函数 \(\varphi(x)=f(2c-x)-f(x)\)，证 \(\varphi'(x)\) 在 \(x<c\) 定号，利用 \(\varphi(c)=0\) 得 \(f(2c-x)>f(x)\)，再结合单调性。

**关键**：\(\varphi'(x)\) 通常可分解为 \((x-c)\cdot\psi(x)\)，其中 \(\psi(x)\) 定号。

常见两类：
- \(f(x)=xe^{-x}\)：直接构造，证 \(\varphi'(x)<0\)
- \(f(x)=x\ln x\)：令 \(t=\ln x\) 转为 \(g(t)=te^t\) 后构造

详见 `references/extremum-shift-pattern.md`。

## 无答案可查时的验证方法论 (2026-07-07)

核心原则：**证据群（Swarm of Evidence）**——不依赖单一证明链，构建多重独立证据，每种证据有不同的失效模式。

### CERT 五条件（无标准答案对照时）

1. 至少两种代数结构不同的推导路径 → 双方法交叉
2. 所有退化极限检验通过 → 极限一致性
3. 临界边界零违反 → 枚举覆盖
4. 至少两个独立计算引擎一致 → 三轨验证
5. 逻辑链经机械化检查 → Z3 unsat

当这五个条件全部满足时，答案的正确性置信度可达 CERT——不需要"标准答案"来对照。

详见 `references/unknown-answer-methodology.md`。

## 有理函数裂项求和 (2026-07-07)

**触发条件**：分母可分解为 \((n^2+pn+q)(n^2+rn+s)\) 的有理分式求和，且分子是分母因式的线性组合。

**典型模式**：
\[
\frac{n}{n^4+n^2+1} = \frac{n}{(n^2-n+1)(n^2+n+1)}
= \frac12\!\left(\frac1{n^2-n+1} - \frac1{n^2+n+1}\right)
\]

关键步骤：对 \(n^4+n^2+1\) 配方 \(n^4+n^2+1 = (n^2+1)^2 - n^2 = (n^2+n+1)(n^2-n+1)\)。

裂项后求和 telescoping：
\[
\sum_{n=1}^N \frac{n}{n^4+n^2+1}
= \frac12\!\left(1 - \frac1{N^2+N+1}\right) < \frac12.
\]

**一般步骤**：
1. 配方分解分母：\(n^4 + an^2 + b = (n^2 + \alpha n + \beta)(n^2 - \alpha n + \beta)\)
2. 尝试部分分式 \(\frac{n}{分母} = \frac12(\frac1{n^2-\alpha n+\beta} - \frac1{n^2+\alpha n+\beta})\)
3. 验证：\(\frac1{n^2-\alpha n+\beta} - \frac1{n^2+\alpha n+\beta} = \frac{2\alpha n}{(n^2+\alpha n+\beta)(n^2-\alpha n+\beta)}\)
4. 当系数匹配时（\(\alpha=1\)），消去分子得到 2 倍关系
5. telescoping 求和，化为首尾项差

## 经典构造题模式 (2026-07-07)

**触发条件**：求证存在自然数 \(a,b\) 使 \(n^3 = a^2 - b^2\) 类问题。

**标准方法**：利用平方差公式 \(a^2-b^2 = (a-b)(a+b)\)。设 \(a-b = u, a+b = v\)，则 \(n^3 = uv\)，
\[
a = \frac{u+v}{2},\quad b = \frac{v-u}{2}.
\]
取 \(u=n, v=n^2\)，得 \(a = \frac{n(n+1)}{2}, b = \frac{n(n-1)}{2}\)。

**更一般地**：\(n^k = a^2 - b^2\) 型构造题，分解 \(n^k = uv\)（\(u,v\) 同奇偶），代入即可。

## 用户偏好: LaTeX 公式格式

This user explicitly asked for $$...$$ block-level LaTeX formulas. 所有数学输出必须用 $$...$$ 块级包裹, 不要用 $...$。 多行推导用 \\begin{aligned}, 答案用 \\boxed{}, 分数用 \\dfrac。

### Pitfall: "单调递增" vs "严格单调递增"

In 高考 context:
- **单调递增** (monotone increasing) = $x_1 < x_2 \Rightarrow f(x_1) \leq f(x_2)$ (non-decreasing)
- **严格单调递增** (strictly increasing) = $x_1 < x_2 \Rightarrow f(x_1) < f(x_2)$

When the solution proves "单调递增" but the proof only shows non-decreasing behavior (e.g., constant on a tail), check which definition the problem uses. If the problem says "单调递增" without "严格", constant-on-tail IS acceptable.

### Tool: 高考估分方法论

When asked to estimate a score for a高考 solution, use this structured approach:

| 步骤 | 内容 |
|------|------|
| **① 分题估分** | 按高考标准分值分配推测（通常17分=4+5+4+4或类似，看题目数量） |
| **② 逐题检查** | 每题检查：正确性/完整性/边界处理/推理严谨性 |
| **③ 扣分判定** | 每发现一个问题，判定扣1分/2分/全扣，取决于严重度 |
| **④ 弱链原则** | 整体得分不是平均分，是最弱子题的剩余分之和 |

常见扣分标准：
- 思路正确但某个子情况未处理：-2分
- 边界条件遗漏（开闭区间、零值、负值）：-1分
- 关键步骤推理跳步（"显然""篇幅所限"）：-2分
- 分类讨论不穷尽：-2分
- 整体方向错误/核心技巧用错：全扣

17分题的典型分值分布：
- 简单计算/直接应用 (1): 3-4分
- 中等推理/分类讨论 (2): 5-6分
- 复杂推理第一问 (3)(i): 3-4分
- 复杂推理第二问 (3)(ii): 4-5分

### Pitfall: Non-circular dependency vs. silent assumption carry-over

When reviewing multi-part problems, each part may independently specify its assumptions. A common error:

- Part (2) says "设 f 是奇函数" (f is odd)
- Part (3) may NOT repeat this — it says "设 f 满足条件①, ②"
- **Check**: does the solution carry over the oddness assumption from (2) into (3) silently?
  - If the problem intended it globally, it's fine.
  - If not, the solution makes an unwarranted assumption.
- **Fix**: state explicitly at the start of (3) what assumptions carry over: "本题中 f(x) = 2ˣ (x<0) 是全局定义"

### Report format

Use this structure for proof review delivery:

```markdown
## 📐 数学审查报告
**审查范围**: [题目/证明名称]
**数学评级**: [EXCELLENT/PASS+/PASS/FAIL]

### 逐题审查

#### (1) — ✅ 正确
- [关键检查点1]: ...
- [关键检查点2]: ...

#### (2) — ❌ 不完整
- **缺口定位**: ...
- **原因**: ...
- **严重度**: ...

### 📊 评分汇总
| 小题 | 评级 | 说明 |
|------|:----:|------|
| (1) | ✅ | ... |
| (2) | ❌ | ... |

### 总体: [评级]
[一句话总结]
```

### 12 分制评分体系

对需要打分的证明题，使用三维度评分：

| 维度 | 满分 | 评分标准 | 常见扣分 |
|------|:----:|---------|---------|
| **正确性** | 5 | 每步有定理支撑，逻辑链无断裂 | -2: 跳步 / -5: 结论错 |
| **完整性** | 4 | 分类讨论穷尽，边界条件全处理 | -1: 漏边界 / -4: 漏一类 |
| **严谨性** | 3 | 定理前提已确认，平凡case已处理 | -1: 漏验证条件 / -3: 定理误用 |

规则：整体评分由最弱维度决定（弱链原则）。不取平均。

## 高考立体几何 3D Coordinate Solution (坐标法)

立体几何（线面垂直/二面角/空间角/点到面距离）可以用 **坐标法** 系统求解，避免空间想象力的依赖。以下是从 session 2026-07-06（多面体 ABCDEF，菱形底面 + 垂直棱 + 二面角 D-AG-E）提取的工作流。

### When to Use

- 题目给出明确的几何体（柱/锥/台/多面体），能建系
- 有垂直/平行条件方便定坐标轴
- 求二面角/线面角/异面直线所成角
- 已知条件可用向量合理表达（垂直→点积=0，平行→比例）

### Workflow

#### Step 1 — 建系 (Coordinate Selection)

原则：**尽量多将顶点放在坐标轴/坐标平面上**，减少变量。

```python
# 例：菱形 ABCD 在底面，DE ⟂ 底面
# A 放原点，AD 沿 x 轴，AB 在 xy 平面
A = np.array([0., 0., 0.])
D = np.array([2., 0., 0.])                           # 边长 2
B = np.array([1., math.sqrt(3), 0.])                  # ∠BAD=60°
C = B + (D - A)                                       # 平行四边形法则
# DE ⟂ 底面 → E 在 D 正上方
E = np.array([2., 0., h])                             # h = DE 长度
```

**建系要点：**
- 菱形/正方形：一个顶点在原点，两条邻边沿 x/y 轴
- 直棱柱/垂线：沿 z 轴
- 等腰/等边三角形：底边中点与顶点连线沿对称轴

#### Step 2 — 求所有顶点坐标

利用已知条件（平行、垂直、等长）逐步推导：

| 条件 | 坐标处理 |
|------|---------|
| 线段平行 | 向量成比例：\( \vec{CD} = \vec{AB} \) |
| 线段垂直 | 点积 = 0 |
| 等边三角形 | 高 = \( \frac{\sqrt3}{2} \times \) 边长 |
| 点在线段上 | 参数化：\( G = B + t(F-B) \) |
| 平面垂直 | 交线 + 法线互相垂直 |
| 平面 \(P\perp Q\) | \(Q\) 中垂直于交线的直线垂直于 \(P\) |

**关键案例——等边三角形 + 垂直平面：**

△BCF 等边，边长 2，平面 BCF ⟂ 底面（z=0）。
BC 是两平面交线。BC 中点 M = (2, √3, 0)。
平面 BCF 中垂直于 BC 的直线 ⟂ 底面 → 平行 z 轴。
等边三角形高 = √3。
∴ F = (2, √3, √3)

#### Step 3 — 选择解题工具

| 目标 | 工具 | 公式 |
|:----:|------|:----:|
| 线线垂直 | 点积 | \( \vec{u} \cdot \vec{v} = 0 \) |
| 线面角 | 方向向量与法向量夹角 | \( \sin\theta = \dfrac{|\vec{v}\cdot\vec{n}|}{\|\vec{v}\|\|\vec{n}\|} \) |
| 二面角 | 两平面法向量夹角 | \( \cos\theta = \dfrac{|\vec{n}_1\cdot\vec{n}_2|}{\|\vec{n}_1\|\|\vec{n}_2\|} \) |
| 点到面距离 | 面的单位法向量 | \( d = \dfrac{|\overrightarrow{AP}\cdot\vec{n}|}{\|\vec{n}\|} \) |
| 异面直线所成角 | 方向向量夹角 | \( \cos\theta = \dfrac{|\vec{u}\cdot\vec{v}|}{\|\vec{u}\|\|\vec{v}\|} \) |

**二面角参数化步骤：**

1. 设动点参数：\( G = B + t(F-B) \)，\( t\in[0,1] \)
2. 求两平面法向量（叉积）：
   \[
   \vec{n}_1 = \overrightarrow{AD} \times \overrightarrow{AG},\quad
   \vec{n}_2 = \overrightarrow{AE} \times \overrightarrow{AG}
   \]
3. 代入公式，化简得 \( \cos\theta = f(t) \)
4. 列方程 \( f(t) = \text{给定值} \)，解出 \( t \)
5. 目标长度：\( BG = t \cdot BF \)

#### Step 4 — SymPy 符号推导 + 数值交叉验证 [CERT]

```python
import sympy as sp
t = sp.symbols('t', real=True)
n1 = AD_vec.cross(AG_vec).simplify()    # = (0, -2√3 t, 2√3)
n2 = AE_vec.cross(AG_vec).simplify()    # = (-6, 2√3, 2√3)
cos_theta = abs(n1.dot(n2)) / (sp.sqrt(n1.dot(n1)) * sp.sqrt(n2.dot(n2)))
cos_theta_simplified = sp.simplify(cos_theta)
# → √5·|t-1| / (5·√(t²+1))
eq = sp.Eq(cos_theta_simplified, sp.Rational(1, 5))
solutions = sp.solve(eq, t)             # → [1/2, 2]
```

#### Step 5 — 数值交叉验证（扫描验证）

```python
for t in np.linspace(0, 1, 11):
    G = B + t * (F - B)
    n1 = np.cross(AD, G - A)
    n2 = np.cross(AE, G - A)
    cos_theta = abs(np.dot(n1, n2)) / (np.linalg.norm(n1) * np.linalg.norm(n2))
    # t=0.5 → cos θ = 0.200000 (= 1/5) ✓
```

#### Step 6 — 3D 可视化

```python
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
# 半透明面 + 棱 + 顶点标签 + 法向量示意
ax.view_init(elev=22, azim=-65)
```

### Verification Checklist (立体几何坐标法)

- [ ] 建系是否可逆（答案与坐标系选择无关）？
- [ ] 所有顶点坐标都验证过（边长/垂直条件）？
- [ ] SymPy 符号推导与手算一致？
- [ ] 数值交叉验证通过（随机采样 5+ 组）？
- [ ] 动点参数范围正确（t ∈ [0,1]）？
- [ ] 二面角余弦公式用绝对值了吗（\( \cos\theta \geq 0 \)）？
- [ ] 3D 图能直观验证（视觉检查）？

### Pitfalls

**Pitfall 1：建系不唯一，不同建系结果应一致。** 如果发现答案依赖坐标选择，说明运算有误。

**Pitfall 2：二面角余弦的正负。** 用 \( |\vec{n}_1\cdot\vec{n}_2|/(\|\vec{n}_1\|\|\vec{n}_2\|) \) 的绝对值会给锐角，需确认题目要求锐角还是钝角。

**Pitfall 3：动点参数范围。** G 在线段 BF 上 → t ∈ [0,1]。解出的 t 如超出此范围要舍去。

**Pitfall 4：等边三角形顶点方向。** △BCF 有两种可能（F 在 BC 两侧），需根据几何体位置判断。

**Pitfall 5：TUI 环境无交互式 3D 窗口。** 用 `plt.savefig('/tmp/fig.png')` 保存后通过 vision 工具查看。

### 组合拓扑约束：网格路径转向分析

对网格上的闭合路径问题（哈密顿回路、一笔画、机器人路径规划等），使用 **转向拓扑约束**：

\[
R - L = \pm 4
\]

其中 \(R\) 为右转次数，\(L\) 为左转次数，路径沿网格边行进。

**推导**：平面简单闭合正交曲线的总转向角 = \(\pm 2\pi\)。每个右转贡献 \(+\pi/2\)，左转贡献 \(-\pi/2\)，直行贡献 \(0\)。

**应用方法**：
1. 统计总顶点数 \(n\)：\(R + S + L = n\)（\(S\) = 直行次数）
2. 代入拓扑约束 \(R - L = \pm 4\)
3. 求解目标表达式：\(S + 2L = n \mp 4\)
4. 在两种走向（顺/逆时针）中选优
5. 用小规模回溯验证（2×2 至 4×4）确认模式成立

**转向方向判定（叉积法）**：

```python
def turn_type(in_dir, out_dir):
    """R=右转, S=直行, L=左转. 方向: (dx,dy)"""
    dx1, dy1 = in_dir
    dx2, dy2 = out_dir
    if (dx1, dy1) == (dx2, dy2):
        return 'S'
    cross = dx1 * dy2 - dy1 * dx2
    return 'L' if cross > 0 else 'R'
```

**Pitfall**: 不要用直观推断（"东→北是左转"）——在网格坐标系中，\(+y\) 方向可能向上或向下。叉积法是坐标无关的转向判定，不会受坐标系方向影响。

### \(\mathcal{L}^1\) 收敛证明模式

对泛函分析中的逼近算子收敛问题，使用三段式证明：

1. **算子范数界**：\(\|A_n\|_{\mathcal{L}^1\to\mathcal{L}^1} \le 1\)（逐区间绝对值三角不等式）
2. **稠密子集上收敛**：取 \(g\in C([0,1])\)，利用一致连续性证 \(\|A_n(g)-g\|_1\to0\)
3. **密度论证**：对任意 \(f\)：
   \[
   \|A_n(f)-f\|_1 \le \|A_n(f-g)\|_1 + \|A_n(g)-g\|_1 + \|g-f\|_1
   \le 2\|f-g\|_1 + \|A_n(g)-g\|_1 \to 0
   \]

### Verification Checklist (Proof Review)

- [ ] Assumptions are explicitly listed at entry (not imported from earlier parts without re-stating)
- [ ] Sub-problems are decomposed and each rated independently
- [ ] Every classification case ("分类讨论") is checked for exhaustion
- [ ] "显然" / "同理" / "篇幅所限" / "类似可证" are flagged and the implied reasoning is verified
- [ ] Boundary conditions (0, endpoints, -∞, +∞) are checked
- [ ] Dependency graph has no cycles
- [ ] The overall rating is the weakest link (not the average)

---

## Verification Checklist

### 🔴 ε-N/ε-δ 严格证明审计（所有数学分析类交付必检）

每个数学定理/公式需要自问：

- [ ] 定理陈述中是否包含极限？→ 是否显式给出了 ε-N 或 ε-δ 表述？
- [ ] 是否只写了 `lim` 符号就跳过了？→ 对每个 `lim`，至少在一处给出 ε-N/ε-δ 定义。
- [ ] 证明是否用了"显然""易证""同理""篇幅所限"？→ 补全推理链，不可跳步。
- [ ] 第3-5编（导数/积分/级数/多元）的每个极限论证能否追溯到第11-14章的严格定义？
- [ ] 导数定义中的 `lim_{h→0}` 是否用 ε-δ 展开过？（至少要在一个 example 中展开）
- [ ] 黎曼和极限是否用 ε-δ 定义过？
- [ ] 级数收敛是否用 ε-N（部分和柯西准则）定义过？
- [ ] 洛必达法则、泰勒定理、中值定理是否给出了至少一个严格证明的框架？
- [ ] 反例搜索：是否有意识地构造了"某个 ε 足够小"或"某个 N 足够大"的路径来测试证明的鲁棒性？

### 🟡 通用数学正确性检查

- [ ] All `log(x)` calls have `+ eps` guard (eps appropriate for dtype)
- [ ] All `exp(x)` inputs are confirmed within dtype range (< 88 for float32)
- [ ] All `sqrt(x)` calls have `max(0, x)` guard
- [ ] All divisions have `/(y + eps)` guard
- [ ] softmax uses `x - max(x)` stabilization
- [ ] Matrix inversions use `solve()` not `inv()`
- [ ] No `return True` in Hypothesis `@given` tests
- [ ] Precision boundaries documented (this function is float32-safe, this one needs float64)
- [ ] Hypothesis ran with at least 100 examples per invariant
- [ ] Condition number checked if matrix ops are involved
