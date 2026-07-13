# 概率验证 — Monte Carlo 采样模式

## 适用场景

| 问题类型 | 示例 | 验证目标 |
|---------|------|---------|
| 期望值计算 | \(E[XY]\)，\(X\sim P(1), Y\sim P(3), X\perp(Y-X)\) | 解析解 vs 采样均值 |
| 独立性验证 | 泊松分裂 \(X\perp(Y-X)\) | 协方差 ≈ 0 |
| 分布参数验证 | \(E[X]\approx\lambda_1\), \(E[Y-X]\approx\lambda_2\) | 参数一致性 |
| 条件期望 | \(E[X\mid Y]\) | 条件均值曲线拟合 |
| 方差/协方差 | \(\text{Cov}(X,Y)\), \(\text{Var}(X+Y)\) | 解析公式 vs 样本统计量 |

## 标准工作流

### 1. SymPy 符号推导

```python
import sympy as sp
# 验证代数展开
# 例: E[XY] = E[X²] + E[X]·E[Y-X]
```

### 2. 生成采样数据

```python
import numpy as np
np.random.seed(42)
N = 10**6

# 离散分布
X = np.random.poisson(1, N)
Z = np.random.poisson(2, N)  # Z = Y-X
Y = X + Z

# 连续分布
# X = np.random.normal(mu, sigma, N)
```

### 3. 验证断言

```python
E_XY_mc = np.mean(X * Y)
E_X_mc = np.mean(X)
E_Z_mc = np.mean(Z)
cov_XZ = np.cov(X, Z)[0, 1]

assert abs(E_XY_mc - E_XY_analytic) / E_XY_analytic < 5e-4
assert abs(cov_XZ) < 0.01  # 独立性
assert abs(E_X_mc - 1) / 1 < 5e-4
assert abs(E_Z_mc - 2) / 2 < 5e-4
```

### 4. 额外验证

- 验证分布形状（直方图 vs PMF/PDF）
- 验证协方差矩阵对称性
- 对稀有事件增大 N（如 \(N=10^7\)）

## 常见陷阱

| 陷阱 | 说明 | 修复 |
|------|------|------|
| 采样量不足 | N 太小导致蒙特卡洛误差过大 | N ≥ 10⁶ |
| 种子未固定 | 不可复现 | `np.random.seed()` |
| 独立性检验疏忽 | 忘记验证 Cov ≈ 0 | 加入协方差断言 |
| 容差过紧 | MC 误差 ≈ 1/√N，N=10⁶ 时约 0.001 | 相对容差 5×10⁻⁴ |
