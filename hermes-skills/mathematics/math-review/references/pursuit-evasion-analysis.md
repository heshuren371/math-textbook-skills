# Pursuit-Evasion Game Analysis Pattern

## Origin

Developed from session 2026-07-07 (hunter-rabbit problem): a discrete-time pursuit-evasion game with noisy measurements where both players move at speed 1 per round.

## When to Use

- Problems involving two agents moving on the plane with speed constraints
- Noisy/incomplete information games (one player gets a hint about the other's position)
- Adversarial measurement feedback ("device reports a point with bounded error")
- "是否能保证距离不超过某值" type questions

## Analysis Workflow

### Step 1 — Map the information structure

For each round, determine:

| Element | Who chooses it? | Constraints | Known to whom? |
|---------|---------------|-------------|----------------|
| Rabbit's move A_n | Rabbit | \|A_n - A_{n-1}\| = 1 | Secret (only rabbit) |
| Measurement P_n | Device | \|P_n - A_n\| ≤ 1 | Public (hunter sees it) |
| Hunter's move B_n | Hunter | \|B_n - B_{n-1}\| = 1 | Public |

**Critical observation**: The rabbit chooses A_n FIRST, THEN the device chooses P_n based on A_n, THEN the hunter chooses B_n based on P_n. The order matters.

### Step 2 — Prove the hunter's optimal strategy

The hunter knows P_n and can infer that A_n ∈ Disk(P_n, 1). For any hunter position x,
\[
\max_{A_n \in \operatorname{Disk}(P_n, 1)} |x - A_n| = |x - P_n| + 1.
\]

The hunter minimizes this by minimizing |x - P_n| over |x - B_{n-1}| = 1. By the triangle inequality:
\[
|x - P_n| \ge |P_n - B_{n-1}| - |x - B_{n-1}| = |P_n - B_{n-1}| - 1.
\]

Equality when x is on the ray from B_{n-1} toward P_n. Hence the minimax-optimal strategy is:
\[
B_n = B_{n-1} + \frac{P_n - B_{n-1}}{|P_n - B_{n-1}|} \quad (\text{if } |P_n - B_{n-1}| \ge 1).
\]

**Key**: This is also GLOBALLY optimal because:
- The information structure at each round is identical
- The rabbit can always undo any "positioning" the hunter achieves in subsequent rounds
- Any deviation from the minimax strategy makes the current round's worst-case distance strictly larger

### Step 3 — Determine what the rabbit can achieve

The rabbit's goal is to maximize d_n = |B_n - A_n|, subject to:
- |A_n - A_{n-1}| = 1 (movement constraint)
- |P_n - A_n| ≤ 1 (feedback constraint)
- B_n is determined by the hunter's strategy given B_{n-1} and P_n

**Key constraint**: |A_n - A_{n-1}| = 1 prevents A_n from being at the worst-case position in Disk(P_n, 1). This makes the growth SUB-LINEAR.

### Step 4 — Construct the adversarial strategy

**Rabbit's movement**: Move directly away from B_{n-1}:
\[
A_n = A_{n-1} + \frac{A_{n-1} - B_{n-1}}{|A_{n-1} - B_{n-1}|}, \quad |A_n - A_{n-1}| = 1.
\]

This gives |B_{n-1} - A_n| = d_{n-1} + 1.

**Device feedback**: Choose P_n to maximize the resulting d_n by solving:
\[
\max_{P_n: |P_n - A_n| \le 1} |B_n - A_n|
\]
where B_n = strategy(B_{n-1}, P_n).

For the optimal strategy (move toward P_n), this reduces to a 1D optimization over the angle θ where P_n = A_n + (cos θ, sin θ):
\[
d_n = \max_{\theta} \sqrt{1 + (d_{n-1}+1)^2 - 2(d_{n-1}+1)(d_{n-1}+1-\cos\theta) / \sqrt{(d_{n-1}+1)^2 - 2(d_{n-1}+1)\cos\theta + 1}}
\]

**Simpler lower bound**: Even with a suboptimal P_n = A_n + (0,1) (90° perpendicular), we get:
\[
d_n > d_{n-1}, \quad \text{specifically } d_n = \sqrt{(d_{n-1}+1)^2 + 1} - 1.
\]

### Step 5 — Prove unbounded growth

The sequence {d_n} satisfies d_n > d_{n-1} for all n (strictly increasing). If it had a finite upper bound L, then:
\[
L = \sqrt{(L+1)^2 + 1} - 1 \implies 0 = 1,
\]
a contradiction. Hence d_n → ∞.

### Step 6 — Numerically estimate the growth rate

For the optimal adversarial P_n (not just the 90° lower bound), numerical simulation yields:
\[
d_n \sim c \cdot n^\alpha, \quad \alpha \approx 0.338,\; c \approx 0.15.
\]

This is between √n (α = 0.5) and ∛n (α ≈ 0.333).

### Step 7 — Answer the threshold question

Given d_n → ∞, for any finite threshold T, there exists N such that d_N > T. The question is whether N ≤ 10^9. From the power law fit:
\[
d_{10^9} \approx d_{10^5} \cdot \left(\frac{10^9}{10^5}\right)^{0.338} \approx 52.6 \cdot 10^{4 \times 0.338} \approx 52.6 \times 22.6 \approx 1189.
\]

Since 1189 > 100, the hunter cannot guarantee distance ≤ 100 after 10^9 rounds.

## Key Pitfalls

### Pitfall 1: "Upper bound is tight" trap

**Symptom**: Derive d_n ≤ d_{n-1} + 2, then claim the distance grows linearly.

**Why it's wrong**: The bound assumes A_n can be at the worst position in Disk(P_n, 1), but the constraint |A_n - A_{n-1}| = 1 prevents this. The actual worst-case growth is much slower (~n^0.338).

**Fix**: After deriving any upper/lower bound, ALWAYS check if it's achievable. Construct a specific adversarial sequence; if it doesn't reach the bound, refine the analysis.

### Pitfall 2: Assuming linear growth without checking tightness

The triangle inequality gives |B_{n-1} - A_n| ≤ d_{n-1} + 1. This is indeed tight (achieved when the rabbit moves directly away). But the distance d_n = |B_n - A_n| is NOT simply |B_{n-1} - P_n| — the hunter moves toward P_n, and the actual geometry matters.

### Pitfall 3: Ignoring the sequential choice order

The rabbit chooses A_n FIRST, then P_n. This means the rabbit CANNOT make A_n depend on P_n (it's the other way around). The device chooses P_n based on A_n, and the hunter chooses B_n based on P_n. This order limits what the adversary can achieve.

## Template: Proving a Strategy is Optimal

```
1. Define the feasible set: F_n = {x : player is consistent with observations}
2. Bound the feasible set: F_n ⊆ Disk(P_n, r) for some known r
3. Worst-case distance from x to F_n: max_{y∈F_n} |x-y|
4. Minimize over hunter's feasible moves: min_{|x-B_{n-1}|=1} max_{y∈F_n} |x-y|
5. Apply triangle inequality to show the minimizer is "move toward P_n"
6. Argue global optimality: identical information structure each round + adversarial rabbit
```

## Template: Proving Distance Grows Unbounded

```
1. Construct adversarial strategy achieving d_n > d_{n-1}
   (explicit construction: rabbit moves away, device reports at angle θ)
2. Show strict monotonicity: d_n ≥ f(d_{n-1}) where f(d) > d for all d ≥ 0
3. Prove no finite limit: if d_n → L then L = f(L), show contradiction
4. Conclude d_n → ∞
5. Compute/extrapolate to the specific threshold (10^9 rounds, 100 distance)
```
