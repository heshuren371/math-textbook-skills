# 立体几何题的文字→坐标重建工作流

用于纯文字描述的立体几何问题：用户不会给图，你需要从文字中重建坐标系并计算。

## 标准流程

```
用户文字描述 → ① 确定几何类型 → ② 建立坐标系 → ③ SymPy 向量运算 → ④ 数值验证 → ⑤ matplotlib 3D 渲染确认
```

## ① 常见几何体的坐标映射规则

| 用户描述 | 坐标系设定 |
|---------|-----------|
| **长方体/四棱柱** \(ABCD-A_1B_1C_1D_1\)，底面边长 \(a,b\)，高 \(h\) | \(A(0,0,0), B(a,0,0), C(a,b,0), D(0,b,0)\)，\(A_1(0,0,h)\) 等 |
| **正四棱柱**，底面边长 \(a\)，高 \(h\) | 同上，\(b=a\)，底面为正方形 |
| **直三棱柱** \(ABC-A_1B_1C_1\)，底面三角形 + 高 \(h\) | 底面放 \(z=0\) 平面，顶面在 \(z=h\)；三角形用坐标法: \(A(0,0,0), B(c,0,0), C(p,q,0)\) |
| **正四面体** 边长 \(a\) | 底面正三角形在 \(z=0\)，顶点在 \(z=\sqrt{2/3}a\)；例: \(A(0,0,0), B(a,0,0), C(a/2,a\sqrt{3}/2,0)\), \(D(a/2,a\sqrt{3}/6,a\sqrt{2/3})\) |
| **四棱锥** \(P-ABCD\)，底面正方形，\(PA\perp\) 底面 | \(A(0,0,0), B(a,0,0), C(a,a,0), D(0,a,0), P(0,0,h)\) |
| **正三棱锥** \(P-ABC\) | 底面正三角形在 \(z=0\)，顶点在中心上方 |
| **圆柱/圆锥** | 用参数方程，或对称性简化 |
| **球** | 球心在原点，或用球坐标 |
| **中点** \(E\) 为 \(BC\) 中点 | \(E = (B+C)/2\) |
| **三等分点** \(F\) 为 \(BC\) 上 \(BF:FC=2:1\) | \(F = B + (C-B)\times\frac{2}{3}\) |

## ② 关键计算公式

```python
import sympy as sp

# 向量
v = sp.Matrix([x2-x1, y2-y1, z2-z1])

# 点积
dot = v1.dot(v2)

# 叉积（法向量）
cross = v1.cross(v2)

# 长度
norm = sp.sqrt(v.dot(v))

# 夹角（异面直线）
cos_theta = abs(v1.dot(v2)) / (sp.sqrt(v1.dot(v1)) * sp.sqrt(v2.dot(v2)))

# 点到平面距离（平面过点 P0，法向量 n）
dist = abs(n.dot(P - P0)) / sp.sqrt(n.dot(n))

# 二面角（两个面的法向量 n1, n2）
cos_alpha = abs(n1.dot(n2)) / (sp.sqrt(n1.dot(n1)) * sp.sqrt(n2.dot(n2)))
```

## ③ 可视化验证（matplotlib 3D）

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')

# 绘制顶点
for v, label in zip(vertices, labels):
    ax.scatter(*v, color='red', s=30)
    ax.text(*(v + offset), label, fontsize=10)

# 绘制棱
for (v1, v2) in edges:
    ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'b-', alpha=0.3)

# 绘制向量（用 quiver）
ax.quiver(*start, *vec, color='red', linewidth=2, arrow_length_ratio=0.1)

ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
ax.view_init(elev=25, azim=-60)  # 视角
plt.savefig('/tmp/3d-geometry.png', dpi=120)
```

## ④ 高级模式：复杂多面体的坐标重建

当题目涉及**非标准多面体**（不只是棱柱/棱锥），需要根据约束条件逐点推导坐标。典型场景：菱形/平行四边形底面 + 平面垂直关系 + 等边三角形。

### 典型案例：多面体 \(ABCDEF\)

**已知条件：**
- 四边形 \(ABCD\) 是菱形，边长 \(2\)，\(\angle BAD = 60^\circ\)
- \(DE \perp\) 平面 \(ABCD\)
- 平面 \(BCF \perp\) 平面 \(ABCD\)，\(\triangle BCF\) 等边三角形（边长 \(2\)）

**坐标推导流程：**

```
Step 1: 菱形 ABCD 放 z=0 平面
  A = (0, 0, 0)
  D = (2, 0, 0)           # 沿 x 轴，边长 2
  B = (1, √3, 0)          # AB=2, ∠BAD=60°
  C = B + (D-A) = (3, √3, 0)  # 平行四边形法则

Step 2: DE ⟂ 底面 → E 在 D 正上方
  E = (2, 0, h)           # h = DE（未知或已知）

Step 3: 平面 BCF ⟂ 底面，△BCF 等边
  BC = (2, 0, 0) 是两平面的交线
  BC 中点 M = (2, √3, 0)
  等边三角形高 = √3
  在平面 BCF 中垂直于 BC 的直线 ⟂ 底面 → 沿 z 轴
  F = (2, √3, √3)

验证: |BF| = |CF| = |BC| = 2 ✅
```

**关键洞察：** 当平面 \(BCF \perp\) 平面 \(ABCD\) 且 \(BC\) 是交线时，平面 \(BCF\) 中垂直于 \(BC\) 的直线垂直于平面 \(ABCD\)（即平行于 \(z\) 轴）。这是确定 \(F\) 的 z 坐标的关键定理。

### 参数点处理

当点 \(G\) 在线段 \(BF\) 上，引入参数 \(t \in [0,1]\)：

\[
G = B + t(F - B) = (1+t,\; \sqrt3,\; t\sqrt3)
\]

以此可以将几何约束（如二面角条件）转化为关于 \(t\) 的方程。

### 二面角计算步骤

```
① 取棱 AG
② 计算两个半平面的法向量:
   n₁ = AD × AG（平面 DAG）
   n₂ = AE × AG（平面 EAG）
③ 二面角余弦:
   cos θ = |n₁·n₂| / (|n₁|·|n₂|)
④ 代入已知条件解方程，求出参数 t
```

**为什么用叉积求法向量：** 法向量方向不唯一（反方向也可），但二面角余弦公式中的绝对值保证结果是正确的锐角。

## ⑤ 验证管线：Symbolic + Numerical 双轨

完成解析推导后，执行双轨验证：

```python
# 轨道 1: SymPy 符号验证（在上面的流程中已内嵌）
import sympy as sp
t = sp.symbols('t', real=True)
# ... 符号推导 ...
sp.solve(sp.Eq(cos_theta_simplified, sp.Rational(1,5)), t)
# → t = [1/2, 2]，取 t=1/2

# 轨道 2: 数值交叉验证
import numpy as np
t_vals = np.linspace(0, 1, 11)
cos_vals = [... for t in t_vals]  # 扫描验证趋势
# 精确点验证
t = 0.5
cos_theta = ...  # 应精确等于 1/5
assert abs(cos_theta - 0.2) < 1e-12
```

## ⑥ 常见陷阱

- **坐标方向选择不一致**：始终保证右手系，底面在 \(z=0\) 或 \(xy\) 平面
- **"正四棱柱" vs "正四棱锥"**：棱柱是上下底面平行全等，棱锥是底面+顶点
- **"E 为 CC₁ 中点"**：\(E = (C+C_1)/2\)，不是 \(C + (C_1-C)/2\)（结果一样但前者更简单）
- **异面直线夹角取锐角**：\(\cos\theta = |\vec{v}_1\cdot\vec{v}_2|/(|\vec{v}_1||\vec{v}_2|)\)，加绝对值
- **法向量方向**：二面角计算中，法向量方向可能相反导致符号错误，加绝对值取锐角
- **平面垂直条件的误用**：平面 \(BCF \perp\) 平面 \(ABCD\) 且交线为 \(BC\) → 在平面 \(BCF\) 中垂直于 \(BC\) 的直线 ⟂ 平面 \(ABCD\)（这个推论不是直接从"两平面垂直"得出，而是要加上"该直线垂直于交线"的条件——这是判定定理）
- **参数取值范围**：点在线段上 → \(t \in [0,1]\)，解方程后要验证
- **🟡 使用 sp.rad() 转换角度**：SymPy 的 `sp.cos(sp.rad(60))` 在实际使用中可能直接写 `cos(pi/3)` 更可靠，因为 `sp.rad()` 返回的是数值近似而不是符号精确值。推荐直接使用 \(\pi\) 的分数形式：`sp.cos(sp.pi/3)`。
- **菱形顶点顺序**：菱形 \(ABCD\) 的顶点应按时序（顺时针或逆时针）排列，向量求 \(C\) 时用平行四边形法则 \(\overrightarrow{OC} = \overrightarrow{OB} + \overrightarrow{OD} - \overrightarrow{OA}\)，其中 \(O\) 为原点。

## ⑦ 在考试中 vs 在计算中的差异

在高考中，立体几何题通常用**几何法**（线面平行的判定、三垂线定理等）或**空间向量法**（建系→坐标→计算）。我采用的**坐标重建+向量计算**方案本质上是空间向量法的自动化版本。

| 场景 | 方法 | 优势 |
|------|------|------|
| 考试 | 建系后手算 | 快速，适应考场 |
| 验证 | SymPy 符号推导 | 无计算错误 |
| 交叉检查 | 数值验证 | 反向检查推导链 |

**重点**：坐标系选择会极大影响计算量。好的坐标系让大部分坐标为 0 或简单值（如菱形中把一条对角线放 x 轴，中心放原点）。但坐标系选择的自由度不影响最终几何关系（垂直/平行/角度值）。
