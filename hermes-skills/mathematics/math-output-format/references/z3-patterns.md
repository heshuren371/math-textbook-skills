# Z3 在数学证明中的使用模式

## 安装

```bash
pip install z3-solver
```

## 核心导入

```python
from z3 import (
    Solver, Real, Bool, Int, RealVal, BoolVal,
    And, Or, Not, Implies, If,
    sat, unsat, unknown
)
```

## 模式1：检查不等式下界是否紧

```python
s = Solver()
k = Real('k')
s.add(k > 0)
# 检查 tan < 4√3 是否可能
import math
s.add(4*k + 3/k < 4 * math.sqrt(3))
result = s.check()
# unsat → 4√3 是真正的下界
# sat   → 下界可以更低，返回反例
```

## 模式2：检查最优值是否可达

```python
s = Solver()
s.add(k > 0)
eps = RealVal(1e-6)
target = RealVal(4 * math.sqrt(3))
expr = 4*k + 3/k
# |expr - target| < eps
diff = If(expr >= target, expr - target, target - expr)
s.add(diff < eps)
result = s.check()
# sat  → 可达，用 s.model()[k] 获取最优参数
```

## 模式3：有限集合包含关系的建模

```python
d1, d2, d3 = Bools('d1_in_A d2_in_A d3_in_A')
e1, e2, e3 = Bools('d1_in_B d2_in_B d3_in_B')

# B ⊆ A: 对每个 d, 若 d ∈ B 则 d ∈ A
solver.add(Implies(e1, d1))
solver.add(Implies(e2, d2))
solver.add(Implies(e3, d3))

# 条件①: B ⊆ A ⇔ f(A) ≤ f(B)
solver.add(Implies(And(Implies(e1, d1), Implies(e2, d2), Implies(e3, d3)),
                    f_A_le_f_B))
```

## 模式4：反证法假设的矛盾检测

将反证法的假设编码为 Z3 约束：

```
假设: f(a) ≥ 1, f(b) < f(a)
断言: 矛盾
```

编码方式：
```python
a, b = Reals('a b')
s.add(a > 0, b > a)       # 0 < a < b
s.add(f_a >= 1)            # f(a) ≥ 1
s.add(f_b < 1)             # f(b) < 1
s.add(f_a > f_b)           # f(a) > f(b)
# 再加上 D(b) 无负数、a-b ∈ D(b) 等约束
result = s.check()
```

**注意**：集合语义（D(x) 的包含关系）需用有限抽象或布尔变量模拟。

## 常见陷阱

| 问题 | 原因 | 修复 |
|------|------|------|
| `abs(expr)` 报错 | Z3 没有内置 abs | 用 `If(expr >= 0, expr, -expr)` |
| `sqrt(3)` 报 parser error | 混入 SymPy/math.sqrt | 用 `math.sqrt(n)` 算出 float 再传 |
| `a == b` 得到 bool | Python 的 == 不是 Z3 约束 | 只能用 `s.add(a == b)` |
| `s.add(x < some_float)` 报错 | float 未转 RealVal | 用 `RealVal(float_val)` 包装 |
