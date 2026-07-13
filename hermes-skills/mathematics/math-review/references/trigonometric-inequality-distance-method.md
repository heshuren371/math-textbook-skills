# Trigonometric Inequality Proof Using Distance-from-πℤ Method

## Origin

2026-07-07 session: Prove that for all real α, positive integers m, n with sin(mα)·sin(nα) ≠ 0:

$$ \frac{1}{|\sin m\alpha|} + \frac{1}{|\sin n\alpha|} > \frac{1}{m\cdot|\sin m\alpha\cdot\sin n\alpha| + |\sin mn\alpha|} $$

The proof developed a general technique applicable to many trigonometric inequalities involving products/sums of |sin(kα)|.

## The General Technique Pattern

### Step 0 — Notation

Let:
- \( A = |\sin(m\alpha)| \), \( B = |\sin(n\alpha)| \), \( C = |\sin(mn\alpha)| \)
- All are positive (strict inequality in problem statement)
- Core relationship: \( C = |\sin(n\cdot(m\alpha))| = |\sin(m\cdot(n\alpha))| \)

### Step 1 — Rewrite the inequality

Cross-multiply to isolate a "core" algebraic form:

$$ (A+B)(mAB+C) > AB \iff mAB(A+B) + C(A+B) - AB > 0 $$

Canonical form:
$$ N := AB(mA+mB-1) + C(A+B) > 0 $$

### Step 2 — Case analysis on \( mA+mB \)

**Case 1:** \( mA+mB \ge 1 \). Then \( AB(mA+mB-1) \ge 0 \) and \( C(A+B) > 0 \), so \( N > 0 \). Trivial.

**Case 2:** \( mA+mB < 1 \). Then \( A+B < 1/m \). Need to show \( C(A+B) > AB(1-mA-mB) \).

### Step 3 — The 1/(16m) threshold lemma

**Key Insight:** The only way Case 2 can hold is if \( C > 1/(16m) \). If \( C \le 1/(16m) \), then we can prove \( m(A+B) > 1 \), contradicting the assumption that we're in Case 2.

**Proof of the lemma:**
If \( C = |\sin(mn\alpha)| \le 1/(16m) \), then:

1. \( \delta := \operatorname{dist}(mn\alpha,\pi\mathbb Z) \le \arcsin(1/(16m)) \le \pi/(32m) \) (using \( \arcsin x \le \pi x/2 \) for \( x\in[0,1] \))

2. There exists integer \( k \) such that \( |mn\alpha - k\pi| \le \pi/(32m) \)

3. Then:
   $$ \begin{aligned}
   d_1 &:= \operatorname{dist}(m\alpha,\pi\mathbb Z) \ge \frac\pi n - \frac\pi{32mn}, \\
   d_2 &:= \operatorname{dist}(n\alpha,\pi\mathbb Z) \ge \frac\pi m - \frac\pi{32m^2}.
   \end{aligned} $$

4. Using \( \sin x \ge 2x/\pi \) for \( x\in[0,\pi/2] \):
   $$ \begin{aligned}
   A &= \sin d_1 \ge \frac{32m-1}{16mn}, \\
   B &= \sin d_2 \ge \frac{32m-1}{16m^2}.
   \end{aligned} $$

5. Hence:
   $$ m(A+B) \ge \frac{32m-1}{16}\!\left(\frac1n+\frac1m\right) \ge \frac{63}{32} > 1. $$

   The last inequality uses \( m,n\ge 2 \). Cases \( m=1 \) or \( n=1 \) are separately trivially provable.

### Step 4 — Back to Case 2

When in Case 2, we must have \( C > 1/(16m) \).

Using \( AB \le T^2/4 \) where \( T = A+B \):
$$ AB(1-mT) \le \frac{T^2(1-mT)}{4} $$

The function \( g(T) = T(1-mT)/4 \) on \( (0, 1/m) \) has maximum \( 1/(16m) \) at \( T = 1/(2m) \).

Since \( C > 1/(16m) \ge g(T) \):
$$ C > \frac{T(1-mT)}{4} \;\Longrightarrow\; CT > \frac{T^2(1-mT)}{4} \ge AB(1-mT) $$

This gives the needed inequality \( C(A+B) > AB(1-mA-mB) \). ✓

### Step 5 — Boundary cases \( m=1 \) or \( n=1 \)

If \( m=1 \): \( C = |\sin(n\alpha)| = B \). Then:
$$ N = AB(A+B-1) + B(A+B) = A^2B + AB^2 + B^2 > 0 $$
since \( A,B > 0 \). Similarly for \( n=1 \).

## Tools and Inequalities Used

| Tool | Application |
|------|-------------|
| \( |\sin(kx)| \le k|\sin x| \) | Bounding C in terms of A or B |
| \( \sin x \ge 2x/\pi \) for \( x\in[0,\pi/2] \) | Lower-bounding A, B from distance |
| \( \arcsin x \le \pi x/2 \) for \( x\in[0,1] \) | Converting C bound to distance bound |
| \( \operatorname{dist}(x,\pi\mathbb Z) \) | Core technique — track distance to nearest multiple of π |
| Mean value inequality \( AB \le (A+B)^2/4 \) | Bounding the RHS in Case 2 |
| Continuity of Chebyshev polynomials | \( |U_{n-1}(\cos\theta)| = |\sin(n\theta)|/|\sin\theta| \) |
| Triangle inequality for distances | \( d_1 \ge d_0 - |\varepsilon|/n \) |

## Applicability for Other Problems

This technique generalizes to any inequality of the form:

$$ \frac{1}{|\sin(m\alpha)|^p} + \frac{1}{|\sin(n\alpha)|^q} > \frac{1}{r|\sin(m\alpha)||\sin(n\alpha)| + s|\sin(mn\alpha)|} $$

or more generally:

$$ F(A,B,C) > 0 \quad\text{where}\quad A = |\sin(m\alpha)|,\; B = |\sin(n\alpha)|,\; C = |\sin(mn\alpha)| $$

The core strategy is always:
1. **Case split** on whether some linear combination of A, B exceeds a threshold
2. **Small-C contradiction**: If C is too small, constrain α to be near \( k\pi/(mn) \), then bound A and B from below using the distance argument
3. **Combined bound**: When C is large enough and A+B is small, use \( C > \text{bound} \) to dominate the negative term

The distance-from-πℤ technique (Step 3) is the key reusable innovation — it transforms a small value of |sin(mnα)| into a lower bound on |sin(mα)| + |sin(nα)| via the geometry of the sine function near its zeros.

## Pitfalls

1. **Don't forget the m=1/n=1 boundary.** When one of m,n is 1, the distance bounds fail (division by n or m in denominator), but the inequality is trivially provable directly.

2. **The bound \( \sin x \ge 2x/\pi \) only works for \( x\in[0,\pi/2] \).** Always verify that the arguments of sin in the lower bound are within this range. If the distance bounds give values > π/2, the bound is invalid and a different approach is needed.

3. **Epsilon is the same for both \( m\alpha \) and \( n\alpha \)** because it comes from the single constraint \( |mn\alpha - k\pi| \le \varepsilon \). Use the same ε/32m bound derived from \( C \le 1/(16m) \).

4. **Strict vs non-strict inequality.** The proof needs strict > everywhere. The final line uses \( C > 1/(16m) \) and the fact that \( T^2(1-mT)/4 \ge AB(1-mT) \) with strict inequality unless \( A = B = T/2 \). Combined with \( C > g(T) \), strictness follows.

5. **The \( k \) in \( mn\alpha = k\pi + \varepsilon \) is not arbitrary.** It's the nearest integer, so \( |\varepsilon| \) is minimized. This ensures the distance bounds are as tight as possible.
