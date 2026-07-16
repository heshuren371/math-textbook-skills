# SymPy 常见陷阱 (含 v1.14 API 迁移清单)

## Eq vs ==（最常犯的错误）

```python
# ❌ 错误：parse_expr("x**2 + y**2 == 1")  → 返回 False（bool）
#    因为 Python 的 == 比较 SymPy 对象的结构，不是数学等式
# ✅ 正确：parse_expr("Eq(x**2 + y**2, 1)")  → 返回 Eq(x**2 + y**2, 1)
```
**规则**：凡涉及等式，一律用 `Eq(a, b)` 而非 `a == b`。

## SymPy v1.14 API 迁移清单（踩坑记录）

以下 API 在 SymPy v1.13–1.14 间迁移，旧用法在新版本中失效。**交付前必须跑通全部代码。**

### 已移除/重命名的属性

| 旧 API | 错误信息 | 替换 |
|--------|---------|------|
| `G.subgroups()` | `AttributeError: no attribute 'subgroups'` | 手工枚举元素构造子群 |
| `G.is_simple` | `AttributeError: no attribute 'is_simple'` | 删除该行（已移除） |
| `FiniteField.order()` | `AttributeError: no attribute 'order'` | `F.characteristic()` 或直接用 p |
| `Permutation.sign()` | `AttributeError: no attribute 'sign'` | `p.parity()`（返回 0=偶/1=奇） |
| `np.trapz()` | `AttributeError: no attribute 'trapz'` | `scipy.integrate.trapezoid()` |

### 模块路径变化

```python
# ❌ 旧路径（直接报 ImportError）
from sympy.ntheory import crt                     # 失效
from sympy.ntheory.continued_fraction import ...  # 失效

# ✅ 新路径
from sympy.ntheory.modular import crt
from sympy.ntheory import continued_fraction_convergents  # 已在顶层重新导出
```

### gcdex 返回值顺序

```python
# gcdex(a, b) 返回 (s, t, g)，其中 s*a + t*b = g = gcd(a, b)
# ❌ 错误：g, x0, _ = gcdex(a1, m1)      # (g, s, t) 是错的
# ✅ 正确：x0, _, g = gcdex(a1, m1)       # (s, t, g) 才是对的
#     x_sol = (x0 * b1) % m1
```

### 已废弃的符号函数（会报 DeprecationWarning）

```python
# 仍可从 sympy.ntheory 导入，但应迁移到：
from sympy.functions.combinatorial.numbers import legendre_symbol, totient, mobius
```

## 表达式解析

```python
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

# 基本解析
expr = parse_expr("x**2 + 2*x + 1")

# 允许隐式乘法（如 "2x" → 2*x）
from sympy.parsing.sympy_parser import implicit_multiplication_application
trans = standard_transformations + (implicit_multiplication_application,)
expr = parse_expr("2x + 3y", transformations=trans)
```

## 符号创建

```python
from sympy import symbols, Symbol
x, y, z = symbols('x y z', real=True)      # 批量 + 实数约束
k = symbols('k', positive=True)             # 正数约束
n = symbols('n', integer=True, positive=True)  # 正整数（数列）
```

## 常用验证模式

```python
# 化简验证
diff = simplify(expr1 - expr2)
assert diff == 0

# 代入验证
val = expr.subs({x: 1.0, y: 2.0}).evalf()

# 方程求解
solve(Eq(expr, 0), x)   # 推荐
solve(expr, x)           # 简写（expr=0）

# 方程组
solve([Eq(f, 0), Eq(g, 0)], [x, y])

# 符号求导
f = x**3 + 2*x
df = diff(f, x)           # 3*x² + 2
d2f = diff(f, x, 2)       # 6*x

# 数值积分验证 (SciPy)
from scipy.integrate import trapezoid
import numpy as np
xs = np.linspace(0, 1, 10001)
ys = f_numpy(xs)
result = trapezoid(ys, xs)
```
