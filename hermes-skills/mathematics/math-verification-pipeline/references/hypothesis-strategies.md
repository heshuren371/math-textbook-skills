# Hypothesis Strategy Recipes for Numerical Verification

## 原则

策略 = 输入空间的先验分布。好的策略：
- 覆盖具体任务的正常区域 + 边缘区域
- 排除 NaN/Inf（用 `allow_nan=False, allow_infinity=False`）
- 排除会直接崩溃的无意义输入（用 `filter` 或 `assume`）
- 对精度浮点容差比默认值更松

## 常用策略模式

### 有限浮点数
```python
def finite_floats(min_v=-1e6, max_v=1e6):
    """排除 NaN/Inf/subnormal 的干净浮点数。"""
    return st.floats(min_value=min_v, max_value=max_v,
                     allow_nan=False, allow_infinity=False,
                     allow_subnormal=False)
```

### 定长向量
```python
def fixed_vector(n=3):
    """n 维向量，用于矩阵乘法等定长运算。"""
    return st.lists(finite_floats(-5, 5), min_size=n, max_size=n).map(np.array)
```

### 概率向量
```python
def probability_vector():
    """归一化到和为 1 的非负向量。
    
    注意: 由于 + 1e-30 守卫，不会出现全零导致除以零。
    """
    return st.lists(st.floats(0, 1, allow_nan=False, allow_infinity=False),
                    min_size=2, max_size=10
                    ).map(lambda x: np.array(x) / (sum(x) + 1e-30))
```

### 正定矩阵
```python
def positive_definite_matrix(n=3):
    """通过 A^T A + εI 保证正定性。
    
    策略: 先随机生成 n×n 矩阵，然后正交化以保证对称正定。
    更简单: 直接用 A^T A + εI 构造。
    """
    return st.lists(finite_floats(-5, 5), min_size=n*n, max_size=n*n
                    ).map(lambda x: np.array(x).reshape(n, n)
                    ).map(lambda A: A.T @ A + np.eye(n) * 0.1
                    ).filter(lambda A: np.all(np.isfinite(A)))
```

### 避免病态
```python
# 病态矩阵会让 inv(A) ⊕ I 的残差膨胀
# 用条件数阈值过滤
.filter(lambda A: np.linalg.cond(A) < 1e12)
```

## @settings 配置要点

```python
@settings(
    max_examples=200,        # 默认 100，复杂不变式可加大
    deadline=None,           # 默认 200ms，矩阵运算等耗时操作会超时
    suppress_health_check=list(HealthCheck),  # 大输入/慢函数时抑制健康检查
)
```

## 本 Session 发现的反例时间线

| 回合 | 测试 | 发现 | 根因 |
|------|------|------|------|
| 1 | softmax 单调性 | argsort 在相等值上乱序 | 改为逐对检查严格不等 |
| 2 | 自交叉熵 | H(p,p) = 0.69 断言失败 | 均匀分布熵 = log(n)，非零正常 |
| 3 | min≤mean≤max | mean 比 max 大 1 ULP | 全等大数组浮点累加误差 |
| 4 | A@inv(A)≈I | 病态矩阵误差过大 | 条件数阈值 + 分级容差 |
