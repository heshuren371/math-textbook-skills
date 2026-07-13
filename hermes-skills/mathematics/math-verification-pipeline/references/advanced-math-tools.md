# 高等数学工具参考

## 抽象代数 `advmath aa`

### 可用命令

| 命令 | 参数 | 示例 |
|------|------|------|
| `group` | 群名 | `advmath aa group S4` — S₄: 阶24, 子群阶{1,2,3,4,6,8,12,24} |
| `cayley` | 群名 | `advmath aa cayley S3` — Cayley 表 |
| `galois` | `GF <p>` | `advmath aa galois GF 5` — GF(5) 特征=5, 乘法群阶=4 |
| `nt` | 整数 | `advmath aa nt 30` — 30=2×3×5, φ(30)=8, μ(30)=-1 |
| `poly-ideal` | 多项式列表 | `advmath aa poly-ideal 'x**2+1' 'x-1'` — Gröbner 基 |
| `coset` | 生成元 母群 | `advmath aa coset '(1 2)' S4` |

### 实现限制 (SymPy API)

- `PermutationGroup` 无 `subgroups()` → 枚举两生成元子群算阶分布
- `FiniteField` 无 `order()` → 用 `.characteristic()` 直接引用 p
- `GF(p, order='grevlex')` 不接受 `order` 参数 → 去掉
- `is_simple` 属性不存在 → 跳过

---

## 实分析/泛函分析 `advmath ra`

### 可用命令

| 命令 | 参数 | 示例 |
|------|------|------|
| `epsilon` | N ε 序列 | `advmath ra epsilon 100 0.01 '1/n'` → 找 N=101 |
| `uniform` | 函数列 a b ε | `advmath ra uniform 'x/n' 0 1 0.01` — 一致收敛检查 |
| `series` | 通项 | `advmath ra series '1/n**2'` — 比值/根值 + 部分和 |
| `fourier` | 函数 a b n | `advmath ra fourier 'x' -3.1416 3.1416 5` |
| `lp-norm` | 函数 a b p | `advmath ra lp-norm 'x**2' a=0 b=1 p=2` → 0.4472 |
| `metric` | d f g | `advmath ra metric '\|x-y\|' 'x**2' 'y**2'` |

### 参数解析

支持 `p=2` 风格键值对和位置参数混合。`_parse_kwargs()` 函数自动分离。

### 已知限制

- `fourier_series` 必须从 `sympy.series.fourier` 导入（`sympy.series` 是模块）
- 数值积分用 SciPy `quad`，异常时回退 SymPy 符号积分
- 序列验证时 N 自动搜索上限 1000，超过则报告未找到

---

## 微分几何 `advmath dg`

### 设计决策

不使用 `sympy.diffgeom` 模块（该模块期望 TwoForm 对象，不接受 Matrix），改用直接张量公式：

- **Christoffel 第二类**：Γᵏ_{ij} = ½g^{kl}(∂ᵢg_{jl} + ∂ⱼg_{il} - ∂ₗg_{ij})
- **Riemann 曲率**：R^{l}_{kij} = ∂ᵢΓ^{l}_{kj} - ∂ⱼΓ^{l}_{ki} + Γ^{m}_{kj}Γ^{l}_{mi} - Γ^{m}_{ki}Γ^{l}_{mj}
- **Ricci 曲率**：R_{jl} = R^{i}_{jil}
- **标量曲率**：R = g^{jl}R_{jl}

### 可用命令

| 命令 | 参数 | 示例 |
|------|------|------|
| `metric` | g_xx | `advmath dg metric 'x**2 + y**2'` |
| `curvature` | g_xx | `advmath dg curvature 'x**2+1'` → 平坦空间 R=0 |
| `sphere` | `r=N` | `advmath dg sphere r=2` → 曲率标量 = 0.5 = 2/R² ✅ |
| `lie-bracket` | X Y | `advmath dg lie-bracket '[-y,x]' '[x,y]'` → [X,Y]=0 |
| `diff-form` | f var1 var2 | `advmath dg diff-form 'x*y' 'x' 'y'` |

### 验证标准

- 平直空间 (g_xx = 1): Riemann 曲率 = 0, 标量曲率 = 0
- S² 球面 (R = 2): 标量曲率 = 2/R² = 0.5 ✅
- 度规 g = diag(x²+1, 1): Christoffel 仅 Γ¹₁₁ = x/(x²+1)，曲率 = 0 (二维流形)

### 2D 度规输入格式

只接受 g_xx 表达式，默认为 g_yy = 1, g_xy = g_yx = 0。
已知要检查的度规：`'x**2 + y**2'`, `'x**2 + 1'`, `'exp(x)'`, `'1 + x'`
