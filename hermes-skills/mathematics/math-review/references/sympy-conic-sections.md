# 解析几何高考题 — SymPy 符号求解工作流

源自 2026-07-05 会话。完整解了一道椭圆 + 焦点弦 + 面积比 + 角度最值的高考题。

## 总体流程

文字题 => (1) 参数提取 => (2) SymPy 符号联立 => (3) 韦达定理 => (4) 目标表达式化简 => (5) 解方程/不等式 => (6) 数值验证

## Step-by-Step

### 步骤1: 提取椭圆参数

```python
from sympy import *

c = 1                    # 焦距 (从焦点坐标)
e = Rational(1, 2)       # 离心率
a = c / e                # a = 2
b2 = a**2 - c**2         # b^2 = 3
```

验证: a > b > 0, c^2 = a^2 - b^2.

### 步骤2: 设直线方程并联立

直线过焦点 F(-c, 0), 斜率 k > 0:

```python
k = symbols('k', positive=True)

# 直线 y = k(x + c) 代入椭圆
eq = x**2/a**2 + (k*(x + c))**2/b2 - 1
eq_simplified = simplify(eq * (a**2 * b2))     # 清分母
```

### 步骤3: 韦达定理

```python
coeffs = Poly(eq_simplified, x).coeffs()
A, B, C = coeffs[0], coeffs[1], coeffs[2]

x_sum = -B/A
x_prod = C/A

# 判别式
Delta = factor(B**2 - 4*A*C)
```

对典型题: A = 3+4k^2, B = 8k^2, C = 4k^2-12, Delta = 144(k^2+1).

### 步骤4: 交点坐标

```python
x1 = (-B + sqrt(Delta)) / (2*A)     # P (右交点, y > 0)
x2 = (-B - sqrt(Delta)) / (2*A)     # Q (左交点, y < 0)
y1 = k * (x1 + c)
y2 = k * (x2 + c)
```

用 simplify() 化简. 验证: x1 > -c > x2, y1 > 0 > y2.

### 步骤5: 面积比条件

利用对称性: R = -P (因为 PO 过原点 O, O 是椭圆中心).

```python
# S△PFO = (1/2) * |FO| * |y1| = y1/2
S_pfo = y1 / 2

# S△PQR = |x1*y2 - x2*y1| = k(x1 - x2)  (见下方推导)
S_pqr = k * (x1 - x2)
```

**关键化简**: x1*y2 - x2*y1 = x1*k(x2+c) - x2*k(x1+c) = k(x1 - x2).

面积条件方程:

```python
eq_area = simplify(S_pqr - 3 * S_pfo)
solve(eq_area, k)
# -> [sqrt(5)/2]
```

### 步骤6: tan(角PQR) 推导

```python
qp = Matrix([x1 - x2, y1 - y2])
qr = Matrix([-x1 - x2, -y1 - y2])

det_q = qp[0]*qr[1] - qp[1]*qr[0]   # 叉积
dot_q = qp[0]*qr[0] + qp[1]*qr[1]   # 点积

tan_angle = simplify(abs(det_q) / dot_q)
# -> 4k + 3/k
```

### 步骤7: 求最值

```python
tan_expr = 4*k + 3/k
dtan = diff(tan_expr, k)             # -> 4 - 3/k^2
solve(dtan, k)                       # -> [sqrt(3)/2] (k > 0)
tan_expr.subs(k, sqrt(3)/2)          # -> 4*sqrt(3)
```

或 AM-GM: 4k + 3/k >= 2*sqrt(4k * 3/k) = 4*sqrt(3).

## 关键代数化简技巧

| 表达式 | 化简方法 | 结果 |
|--------|---------|------|
| x1 - x2 | 韦达差公式 | 12*sqrt(k^2+1)/(4k^2+3) |
| x1*y2 - x2*y1 | 代入 y_i = k(x_i+1) | k(x1-x2) |
| tan(角PQR) | det(QP,QR) / dot(QP,QR) | 4k + 3/k |
