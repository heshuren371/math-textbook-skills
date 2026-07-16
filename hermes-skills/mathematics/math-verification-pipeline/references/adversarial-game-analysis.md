# 对抗性博弈/追逃问题分析模式

## 问题结构

追逃（Pursuit-Evasion）类问题通常具有以下结构：

- **攻守双方**：追赶者（猎人）和被追赶者（兔子/逃逸者）在平面上交替移动
- **信息不对称**：追赶者获得被追赶者位置的噪声观测
- **速度**：双方每回合移动距离相同（通常为 1）
- **问题**：追赶者能否（或如何）在 N 回合后保证与被追赶者的距离不超过给定值

## 核心分析方法

### Step 1：确定最优策略

给定追赶者已知的信息 \(P_n\)（满足 \(|A_n-P_n|\le 1\)），选择下一步位置 \(B_n\)（\(|B_n-B_{n-1}|=1\)）。

**极小极大原理**：追赶者最小化最坏情况下的距离：

\[
\min_{|x-B_{n-1}|=1}\max_{|A_n-P_n|\le 1}|x-A_n| = |P_n-B_{n-1}| \quad\text{(当}\ge1\text{)}
\]

最优策略：**向 \(P_n\) 移动**。

### Step 2：递推分析

建立距离 \(d_n = |B_n-A_n|\) 的递推关系。

在最坏情况下（逃逸者直接远离 + 设备报偏）：

\[
d_n \ge \sqrt{(d_{n-1}+1)^2+1} - 1 > d_{n-1}
\]

**性质**：
- 严格递增：\(d_n > d_{n-1}\) 对所有 \(d_{n-1}\ge0\) 成立
- 无上界：若 \(d_n\to L\)，则 \(L = \sqrt{(L+1)^2+1}-1 \Rightarrow 0=1\)，矛盾

### Step 3：增长速率估计

幂律拟合 \(d_n \sim c\cdot n^\alpha\)。典型值 \(\alpha \approx 0.34\)（介于 1/4 和 1/2 之间）。

外推公式：\(d_N \approx d_{n_0} \cdot (N/n_0)^\alpha\)

### Step 4：替代策略穷举

验证最优策略确实是增长最慢的。典型替代策略集：

| 策略 | 描述 | 增长 |
|------|------|------|
| **optimal** | 向 \(P_n\) 移动 | 最慢 (\(n^{0.34}\)) |
| stay | 不动 | 线性 (\(n\)) |
| random | 随机方向 | 近线性 |
| antipodal | 背离 \(P_n\) | 超线性 |
| perpendicular | 垂直 \(P_n\) | 线性 |
| average | 向 \(B_{n-1}\) 与 \(P_n\) 中点 | 与 optimal 等价 |

## 工具代码模板

```python
import math, numpy as np

def simulate_one_round(B, A, hunter_strategy='optimal'):
    """One round of hunter-rabbit simulation."""
    # 逃逸者直接远离
    dx, dy = A[0]-B[0], A[1]-B[1]
    dist = math.hypot(dx, dy)
    angle = 0.0 if dist < 1e-12 else math.atan2(dy, dx)
    A_new = [A[0] + math.cos(angle), A[1] + math.sin(angle)]
    
    # 设备选最坏的 P_n
    worst_d, best_P = -1, None
    for t_deg in range(0, 360, 2):
        rad = math.radians(t_deg)
        P = [A_new[0] + math.cos(rad), A_new[1] + math.sin(rad)]
        d_BP = math.hypot(P[0]-B[0], P[1]-B[1])
        # 按策略移动
        if hunter_strategy == 'optimal':
            B_new = [B[0], B[1]] if d_BP < 1e-12 else (
                [P[0], P[1]] if d_BP <= 1 else 
                [B[0]+(P[0]-B[0])/d_BP, B[1]+(P[1]-B[1])/d_BP]
            )
        # ... 其他策略
        d_new = math.hypot(B_new[0]-A_new[0], B_new[1]-A_new[1])
        if d_new > worst_d:
            worst_d, best_P = d_new, P
    
    # 应用
    P = best_P
    d_BP = math.hypot(P[0]-B[0], P[1]-B[1])
    if hunter_strategy == 'optimal':
        if d_BP < 1e-12: B_new = [B[0], B[1]]
        elif d_BP <= 1: B_new = [P[0], P[1]]
        else: B_new = [B[0]+(P[0]-B[0])/d_BP, B[1]+(P[1]-B[1])/d_BP]
    return B_new, A_new
```

## 常见陷阱

1. **低估增长**：仅用下界递推 \(d_n = \sqrt{(d+1)^2+1}-1\) 估算时，实际最坏情况增长更快（最优 P_n 角度不是 90° 而是在 60° 附近）。应通过数值优化搜索精确的 P_n 角度。
2. **漏掉全局最优性论证**：仅证明"向 P_n 移动是当前回合最优"还不够，需要额外论证为什么长期策略不会更好（对手每回合可破坏任何定位）。
3. **随机化不改变最坏情况**：追赶者的随机策略在最坏情况分析中不提供更好的保证，因为对手可以先选择 A_n 和 P_n 再观察 B_n（回合内顺序：兔子→设备→猎人）。
