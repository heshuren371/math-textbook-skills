# 新工具的验证模式（Session 2026-07-05 建立，2026-07-06 更新）

## 三套工具启动器对照

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
# 基础数学工具
mathkit <tool> [args]
# 物理验证工具
physicskit <tool> [args]
# 高等数学工具
advmath <tool> [args]
```

| 启动器 | 领域 | 工具组 | PATH 位置 |
|--------|------|--------|----------|
| `mathkit` | 基础数学 | 10 个工具 | `.venv/bin/mathkit`（自动在 PATH） |
| `physicskit` | 物理验证 | 4 个工具 | `workspace/physics-templates/` |
| `advmath` | 高等数学 | 3 个工具 | `workspace/advanced-math-templates/` |

---

## proof-scaffold.py — 结构化证明脚手架

### 用途
把自然语言的证明拆成原子步骤，逐步骤做 SymPy 代数验证 + 依赖追踪 + 环检测。

### 典型调用
```bash
mathkit scaffold                    # 运行内置示例（椭圆面积比）
mathkit scaffold template           # 生成空白证明模板 proof-template.json
mathkit scaffold check proof.json   # 检查外部证明文件
```

### 验证项
| 检查项 | 方法 |
|--------|------|
| 代数恒等式 | `verify_algebra(expr, simplify_to=target)` |
| 方程验证 | `verify_algebra(expr, eval_at=pt, expected_value=val)` |
| 依赖完整性 | 每个步骤的 `depends_on` 必须在前面定义过 |
| 循环依赖 | DFS 检测依赖图中的环 |

---

## deduction-verifier.py — 推导原子验证器

### 用途
给定一组前提和一个声称的结论，自动检查结论是否能从前提中推出。

### 典型调用
```bash
mathkit deduce                              # 内置示例
python3 math-templates/deduction-verifier.py 'k > 0' '4*k+3/k >= 4*sqrt(3)'
python3 math-templates/deduction-verifier.py check --premises 'x>0,y>0' --conclusion 'x+y>0'
```

### 验证策略
| 方式 | 原理 | 适用场景 |
|------|------|---------|
| 符号化简 | `simplify(结论 - 前提的推论)` | 代数等式 |
| 数值抽样 | 随机采样参数，检查前提→结论是否恒真 | 不等式 |
| 边界代入 | 从前提解出变量范围，检查边界 | 不等式传递性 |

---

## contradiction-engine.py — Z3 逻辑矛盾检测

### 用途
自动发现反证法中的逻辑矛盾，或验证一组约束是否可满足。

### 典型调用
```bash
mathkit contradiction       # 运行所有内置示例
```

### 与 SymPy 的分工
| SymPy | Z3 |
|-------|----|
| 代数化简 `simplify(expr)` | 可满足性检查 `s.check()` |
| 解方程 `solve(Eq(a,b), x)` | 约束求解 `s.model()` |
| 符号积分/求导 | 逻辑蕴涵/矛盾检测 |
| 等式/代数推理 | 不等式/集合/逻辑推理 |

---

## cross-validate.py — 交叉验证协议

### 用途
同一问题用两种独立方法求解，对比答案一致性。

### 典型调用
```bash
mathkit crossval    # 运行内置示例（椭圆面积比：坐标法 vs 几何法）
```

### 适用场景
| 问题类型 | 方法A | 方法B |
|---------|------|------|
| 解析几何 | 坐标法（联立+韦达） | 几何法（面积比+相似） |
| 最值 | 导数法 | AM-GM 不等式 |
| 定积分 | 换元法 | 分部积分 |
| 数列求和 | 通项法 | 数学归纳法 |

---

## physicskit — 物理验证工具（Session 2026-07-06 建立）

4 个物理工具，位于 `workspace/physics-templates/`。用于数学问题涉及物理应用时的附加验证。

### 工具总览

```bash
physicskit dim   'F = m * a'          # 量纲一致性
physicskit const g                      # 物理常数查询
physicskit valid check speed 1e8 m/s   # 物理合理性
physicskit kin projectile v0=10 theta=45  # 运动学推导
```

### 定积分物理应用标准工作流（以闸门水压力为例）

1. **物理建模**：建坐标系 `y=0` 在水面，向下为正；压强 `P=ρgy`；微元 `dF = ρg·y·w(y)·dy`
2. **符号积分**（SymPy）：分别计算矩形部分 `F₁` 和抛物线部分 `F₂`，消去 ρg 得纯代数方程
3. **量纲验证**：`physicskit dim 'F=rho*g*h^2'` 验证 `M·L²/T² = M·L²/T²` ✅
4. **比例方程**：由 `F₁/F₂ = 5/4` 解出 `h = 2d`
5. **几何定参**：由抛物线方程 `x² = y` 得 `d=1`，故 `h=2`
6. **数值积分验证**：梯形法则 N=10000，验证 `F₁=39200, F₂=31360, F₁/F₂=1.250047 ≈ 5/4`
7. **数量级检查**：`physicskit valid check force 39200 N` → 合理

### 关键陷阱（2026-07-06 发现并修复）

| 问题 | 根因 | 修复 |
|------|------|------|
| 轨迹方程 `y(x)` 显示 t | 直接用符号 `t` 代入，未消去时间参数 | 改为 `y = (v0y/v0x)·x - (g/(2v0x²))·x²` |
| 量纲检查 `c²` 错误 | 数值指数被映射为 `1`（无量纲） | 保留指数原值：检测前一个 token 是否为 `**` |
| physics-validate 非交互 EOFError | 命令行模式进入 `input()` 循环 | 添加独立的分支：解析命令后直接 `sys.exit(0)` |
| `m` 变量歧义（质量 vs 长度） | 单字母 `m` 映射为 `kg`，但长度语境需要 `m` | 通过全局变量列表推断电磁/热学关键词做语境消歧 |

---

## advmath — 高等数学工具（Session 2026-07-06 建立）

3 个工具，位于 `workspace/advanced-math-templates/`。

### 抽象代数 `advmath aa`

```bash
advmath aa group S4            # S₄ 群信息（阶/生成元/子群/可解性）
advmath aa galois GF 5         # GF(5) 有限域
advmath aa nt 30               # 数论函数（φ/μ/因子分解）
advmath aa poly-ideal 'x**2+1' 'x-1'  # 多项式理想 Gröbner 基
```

**验证能力：**
- 置换群：阶、生成元、Cayley 表、陪集分解、可解性、换位子群、中心
- 有限域：特征、乘法群阶、不可约多项式
- 数论：素因数分解、欧拉函数 φ、Möbius μ
- 多项式理想：Gröbner 基（lex/grevlex）、理想成员判定

### 实分析/泛函分析 `advmath ra`

```bash
advmath ra epsilon 100 0.01 '1/n'   # ε-N 验证（找 N 使 n>N 时误差 < ε）
advmath ra uniform 'x/n' 0 1 0.01    # 一致收敛性检查
advmath ra series '1/n**2'           # 级数收敛性判别
advmath ra fourier 'x' -3.14 3.14 5  # Fourier 级数展开 + 数值验证
advmath ra lp-norm 'x**2' a=0 b=1 p=2  # Lp 范数
```

**验证能力：**
- ε-N 收敛验证：对给定 ε 自动找 N
- 函数列一致收敛：检查 sup 范数
- 级数判别：比值法/根值法 + 数值部分和
- Fourier 级数：展开 + 采样点精度验证
- Lp 范数：数值积分（SciPy）

### 微分几何/拓扑 `advmath dg`

```bash
advmath dg metric 'x**2 + y**2'      # 2D 度规分析
advmath dg sphere r=2                # 球面 S²（Christoffel + 曲率）
advmath dg lie-bracket '[-y, x]' '[x, y]'  # Lie 括号
```

**验证能力：**
- Christoffel 符号（直接公式计算，不依赖 SymPy diffgeom 模块）
- Riemann 曲率张量 + Ricci 曲率 + 曲率标量
- Lie 括号 + Jacobi 恒等式
- 标准验证：S² 曲率标量 = 2/R² ✅

---

## 三套工具的验证策略选择器

| 问题类型 | 优先工具 | 次优先 | 补充验证 |
|---------|---------|-------|---------|
| **代数/微积分** | `mathkit symbolic` | `mathkit contradiction` | 数值随机 |
| **解析几何** | `mathkit crossval` 双方法 | SymPy 联立求解 | `mathkit mathplot` 作图 |
| **定积分/面积** | `mathkit symbolic` 符号积分 | SciPy 数值积分 | Monte Carlo N=10⁶ |
| **定积分·物理应用** | `mathkit symbolic` + `physicskit dim` | `physicskit kin`（运动学） | 数值积分 + 数量级检查 |
| **概率/统计** | SymPy 符号求和 | NumPy Monte Carlo 10⁶ | 协方差/相关性验证 |
| **抽象代数(群/域)** | `advmath aa group/galois` | SymPy combinatorics 查表 | Cayley 表封闭性 |
| **实分析(ε-N/级数)** | `advmath ra epsilon/series` | SymPy limit/summation | 比值/根值交叉验证 |
| **微分几何(度规/曲率)** | `advmath dg sphere` 标准验证 | 手写公式符号计算 | 与已知曲面解析解对比 |
| **偏导/分段函数** | 沿多路径数值代入 | 差商定义直接计算 | 路径极限一致性检验 |
| **纯分析证明** | `mathkit scaffold` 逻辑拆解 | `mathkit deduction` 前提→结论 | 分类讨论完备性审计 |
| **数量级检查** | `physicskit valid check speed/force` | — | — |
