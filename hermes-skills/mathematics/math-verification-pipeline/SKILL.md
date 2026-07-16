---
name: math-verification-pipeline
description: "Use when running mathematical verification — numerical safety checks + SymPy/Wolfram triple-track verification + Hypothesis property-based testing + matrix diagnostics + precision comparison. Unlike jupyter-live-kernel (interactive Python via Jupyter) or math-review (human-readable correctness review), math-verification-pipeline is a structured automated verification system for mathematical results. Do NOT use for interactive exploration (jupyter-live-kernel) or text-based math review (math-review)."
emoji: 🧪
color: "#1B5E20"
---

# 数学验证管线

> **注意**: 本技能专注于三个核心验证模板。更全面的技能是 `math-review`（含所有 6 个工具 + 证明审查 + 解析几何求解 + 几何绘图）。

## 何时使用

- 收到 AI 工程师提交的「这个 loss 稳定吗？」「这个算法收敛吗？」
- 在 Dev-QA 门禁中执行数学审查（L1 纯推导、L3 代码实现）
- 实现或审查涉及 exp/log/sqrt/除法/归一化的数值敏感代码
- 需要自动搜索数学反例来攻破自己的定理推导
- 高考／竞赛立体几何题建模求解（坐标 → 向量 → 符号解 → 交叉验证）
- **对抗性博弈/追逃问题分析**：猎人-兔子、追逐-逃逸、噪声观测下的跟踪等。需要交替考虑攻防双方行动，用极小极大策略分析 + 备选策略穷举来证明「不可能」结论。

## 六模板架构（完整套件）

所有 6 个工具通过 `mathkit` 启动器访问（venv 激活后即入 PATH）：

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
mathkit              # 列出所有工具
mathkit numerical    # 数值安全检查
mathkit symbolic     # 符号双轨验证
mathkit property     # 反例搜索
mathkit matrix       # 矩阵诊断
mathkit precision    # 精度对比
mathkit convergence  # 收敛可视化
```

以下详细介绍最核心的 3 个模板：

```
workspace/math-templates/
├── numerical-check.py    — 数值安全扫描（log/exp/sqrt/除法/softmax）
├── symbolic-check.py     — 手算 vs SymPy 双轨验证（导数/积分/梯度）
└── property-test.py      — Hypothesis 反例自动搜索（15+ 数学不变式）
```

### 1. numerical-check.py — 三段式数值安全检查

**触发场景**：代码中使用了 `np.exp`、`np.log`、`np.sqrt`、除法、softmax、layer-norm。

**用法**：
```bash
python3 numerical-check.py                  # float32 全套
python3 numerical-check.py --all            # float16/32/64 三档精度
python3 numerical-check.py softmax           # 单类检查
```

**自动扫描 5 项**：
| 检查 | 发现过的问题 |
|------|-------------|
| log 守卫 | `log(0)` → NaN，`log(负数)` → NaN |
| exp 审查 | `exp(>88)` → Inf (float32) |
| sqrt 守卫 | `sqrt(-0.0)` 和 `sqrt(-1e-17)` → NaN |
| 除法守卫 | `x / 0` → Inf/NaN |
| Softmax 稳定性 | 朴素 `exp(x)/sum(exp(x))` → Inf，稳定版 `exp(x-max(x))` 通过 |

### 2. symbolic-check.py — 双轨验证（SymPy + 数值差分）

**触发场景**：你推了一条导数/积分链，需要独立验证。

**用法**：
```bash
python3 symbolic-check.py deriv 'sin(x)' x 'cos(x)'      # 导数匹配
python3 symbolic-check.py deriv 'exp(x**2)' x             # 无手算 → 数值差分
python3 symbolic-check.py integrate 'x**2' x              # 不定积分
python3 symbolic-check.py gradient 'x**2+y**2' x y        # 多变量梯度
```

**核心原则**：自己推导的结果必须由 SymPy（或数值差分）独立验证。一条 10 步的链在第 7 步犯错是常见幻觉，双轨验证是唯一解药。

### 3. property-test.py — 反例自动搜索（关键武器）

**触发场景**：
- 你声称「这个数学恒等式成立」→ 不，让 Hypothesis 试试能不能攻破
- 你要审查别人的代码中某个数值不变式是否被保持
- 你需要生成大量随机输入来测试一个数学断言

**用法**：
```bash
python3 property-test.py                     # 全部 15 个测试
python3 property-test.py softmax             # 单组测试
python3 property-test.py --list              # 列出所有测试
python3 property-test.py --seed 42           # 可复现种子
```

**内置测试组**：

| 组名 | 测试数 | 验证内容 |
|------|--------|---------|
| `softmax` | 6 | 和为1、非负、平移不变、单调性、交叉熵非负、自熵非负 |
| `matrix` | 2 | `A @ inv(A) ≈ I`、对称性 |
| `algebra` | 3 | `log(exp(x))≈x`、`log(ab)=log(a)+log(b)`、`sin²+cos²=1` |
| `stats` | 2 | z-score 均值=0 标准差=1、min≤mean≤max |
| `numeric` | 2 | 灾难性抵消、大数组累加精度 |

---

## WolframScript 第三验证轨道（2026-07-06 新增）

当确认 `wolframscript` 可用（`/usr/local/bin/wolframscript`）且 Wolfram Engine 已安装激活时，可以将三轨验证引入整个推导链。

### 何时触发

| 场景 | 原因 | 示例 |
|------|------|------|
| 立体几何建模 | Wolfram 原生向量/叉积语法更简洁 | `Cross[AD, AG]` 比 `np.cross()` 更直观 |
| 复杂符号化简 | `Simplify[]` 比 `sp.simplify()` 在某些场景更强 | 多变量有理式 |
| 二面角/线面角计算 | 一步到位 | 法向量 → 余弦 → 解方程 |
| 需要第三独立验证 | 防 SymPy 和手算同时出错 | 三轨：手算 → SymPy → Wolfram |

### 基本用法

```bash
# 直接计算
wolframscript -code '2+2'
wolframscript -code 'Integrate[x^2, {x, 0, 1}]'

# 多行代码（用单引号括起来，每行分号结尾）
wolframscript -code '
  A = {0, 0, 0};
  B = {2, 0, 0};
  Print["AB = ", Norm[B-A]];
'

# 绘图（输出 -Graphics3D- 表示成功）
wolframscript -code 'Plot3D[Sin[x]Cos[y], {x,-Pi,Pi},{y,-Pi,Pi}, ImageSize->Small]'
```

### 关键 Pitfall：保护符号冲突

Wolfram 中 `C`、`D`、`E`、`N` 是内置保护符号（分别用于默认常数、求导、自然底数、数值计算），**不能用作变量名**。

```wolfram
(* ❌ 会报错 Set::wrsym *)
C = {3, 0, 0};
D = {2, 0, 0};

(* ✅ 正确做法：加前缀 *)
pA = {0, 0, 0};
pB = {2, 0, 0};
pC = {3, 0, 0};
pD = {2, 0, 0};
```

受保护的内置符号清单：`C`, `D`, `E`, `I`, `N`, `Pi`, `Epsilon`, `Infinity`, `Re`, `Im`, `Abs`, `Sin`, `Cos`, ... 最佳实践：所有坐标点一律用 `p` 前缀（`pA`, `pB`, `pC`, ...）。

### 高考立体几何题的标准工作流

以 22. (2025宁夏银川二模) 折叠问题为例：

```
1. 建系（2D梯形→3D折叠）
   wolframscript -code '
     pA = {0,0,0}; pB = {2,0,0}; pC = {2,2,0}; pD = {0,2,0};
     (* 折叠：DQ绕x轴转60° *)
     Rx = {{1,0,0},{0,Cos[60Degree],-Sin[60Degree]},{0,Sin[60Degree],Cos[60Degree]}};
     pP = pD + Rx.(pQ-pD);
   '

2. 验证（(1) 垂直）
   Print[DM.PB]  (* 应为0 *)

3. 参数化求点（(2) N在PC上）
   pN = pC + s(pP-pC);
   n = Cross[pD-pB, pN-pB];  (* 法向量 *)

4. 线面角 → 解方程
   sinPhi = Abs[n.PB]/(Norm[n]*Norm[PB]);
   Solve[{sinPhi==1/4, s>=0, s<=1}, s]

5. 距离（(3)点到平面）
   d = Abs[(pA-pD).n]/Norm[n] /. s->sVal
```

### 三轨验证契约（Triple-Track Mandate）

```
手算/SymPy 得到结果 A
Wolfram 独立得到结果 B
数值随机采样得到结果 C

若 A ≈ B ≈ C → CONFIDENCE = CERT
若 A ≈ B ≠ C → 检查数值实现是否正确
若 A ≠ B ≈ C → 手算/SymPy 推导有误 → 回溯链条
若 A ≈ C ≠ B → Wolfram 建模有误 → 检查坐标设定
```

---

## CERT 升级管线（2026-07-13 新增）

### 何时需要

你完成了一个数学证明，置信度评估为 **HIGH**（逻辑链完整但包含多步级联放缩，每步正确但累积效应需要额外确认）。Dev-QA 门禁要求 **CERT** 才能合入。

典型信号：
- 证明包含 5+ 步的级联放缩链（如 \(C\le X \Rightarrow d_1\ge Y \Rightarrow A\ge Z \Rightarrow \cdots\)）
- 证明依赖多个不等式的同时使用（\(\arcsin\) 界 + \(\sin\) 界 + 三角不等式）
- 关键步骤是「放缩」而非「等号变换」

### 四轨升格协议

将 HIGH → CERT 需要四条独立轨道全部通过，缺一不可：

```
轨道1: SymPy 符号验证   → 每条代数恒等式/不等式有符号证明
轨道2: Z3 SMT 逻辑检查  → 逻辑蕴含的不可反驳性编码验证
轨道3: 穷举/边界枚举    → 参数空间中关键子区域的**全覆盖验证**
轨道4: 第三轨独立计算    → WolframScript 独立实现
```

### 轨道2：Z3 逻辑链检查（关键新增）

Z3 负责验证「前提 ⇒ 结论」的逻辑蕴含。不是测试数值——是证明**不存在**满足前提但不满足结论的赋值。

```python
import z3

m = z3.Int('m')
n = z3.Int('n')
A = z3.Real('A')
B = z3.Real('B')

s = z3.Solver()
# 前提
s.add(m >= 2, n >= 2)
s.add(A > 0, B > 0, A <= 1, B <= 1)
# 下界约束（来自已证的 sin/bound 不等式）
a_lb = (32 * z3.ToReal(m) - 1) / (16 * z3.ToReal(m) * z3.ToReal(n))
b_lb = (32 * z3.ToReal(m) - 1) / (16 * z3.ToReal(m) * z3.ToReal(m))
s.add(A >= a_lb, B >= b_lb)
# 假设结论不成立
s.add(z3.ToReal(m) * (A + B) <= 1)

result = s.check()
assert result == z3.unsat, "逻辑链有漏洞！"
```

**要点**：
- Z3 无法处理 \(\sin\) 等超越函数——所以只编码代数骨架（下界/上界/符号约束）
- \(\sin\) 和 \(\arcsin\) 的不等式先由 SymPy 独立证明，结果以**代数边界**形式输入 Z3
- `z3.ToReal(m)` 将整数提升为实数——Z3 要求表达式类型一致
- 结果 `unsat` ⇒ 逻辑链无漏洞；`sat` ⇒ 存在未覆盖的反例路径

**Pitfall 1**：Z3 `ToReal()` 接收 Python int 时报 `AttributeError: 'int' object has no attribute 'ctx'`。修复：将裸整数包装为 Z3 表达式：`z3.IntVal(mm)` 或在 Z3 约束中用 `z3.ToReal(z3.IntVal(mm))`。

**Pitfall 2：Z3 `Optimize` 对非线性问题只保证局部最优**  
Z3 的 `Optimize` 求解器对非凸/非线性目标函数不保证全局最优。例如在追逃问题中最小化 \(\lvert x-P_n\rvert\)（约束 \(\lvert x-B_{n-1}\rvert=1\)），Z3 可能收敛到局部极小（如返回 \((-1,0)\) 而非全局最优 \((1,0)\)）。  
修复：对于凸优化问题，用三角不等式等分析工具推导闭式解，再用 Z3 `Solver`（非 `Optimize`）验证解的存在唯一性，而非依赖优化器自动搜索。

### 轨道3：关键区域穷举枚举

**不要只做"随机抽 50 万"**——随机采样在高维参数空间中覆盖密度极低。对临界区域做**全覆盖扫描**：

```python
import math, numpy as np

def scan_critical_region(m_range, n_range, alpha_range=(-10, 10), grid_density=200000):
    violations = 0
    worst_diff = float('inf')
    for m in range(m_range[0], m_range[1] + 1):
        for n in range(n_range[0], n_range[1] + 1):
            for _ in range(grid_density):
                alpha = np.random.uniform(*alpha_range)
                A = abs(math.sin(m * alpha))
                B = abs(math.sin(n * alpha))
                if A * B < 1e-300:
                    continue
                if m * (A + B) < 1:
                    C = abs(math.sin(m * n * alpha))
                    lhs = 1/A + 1/B
                    rhs = 1/(m * A * B + C)
                    diff = lhs - rhs
                    if diff < worst_diff:
                        worst_diff = diff
                    if diff < -1e-15:
                        violations += 1
    return violations, worst_diff
```

额外的 \(C=0\) 邻域精细扫描——证明中最脆弱的地方是 \(\sin(mn\alpha)=0\) 的邻域：

```python
for m in range(2, 11):
    for n in range(2, 11):
        for k in range(1, m*n):
            alpha0 = k * math.pi / (m * n)
            A0 = abs(math.sin(m * alpha0))
            B0 = abs(math.sin(n * alpha0))
            if A0 * B0 < 1e-300:
                continue
            for delta in np.linspace(-0.01, 0.01, 501):
                if delta == 0: continue
                # ... 验证不等式
```

### 轨道5（追加）：不可行性证明的替代策略测试

当证明「某某策略不可能达到某目标」时（如追逃问题中「猎人能否保证距离有界」），仅证明策略 A 不行是不够的——必须排除所有可能的策略。

**模式**：
1. 识别问题的最优策略（用极小极大分析或三角不等式证明策略最优性）
2. 对最优策略证明发散（严格递增递推 + 无上界反证法）
3. 枚举所有明显不同的替代策略，用模拟+最坏对手验证它们发散更快
4. 若发现某策略增长比最优策略还慢，表明最优策略分析有漏洞

**典型替代策略集**：optimal（向 P_n）、stay（不动）、random（随机方向）、antipodal（背离 P_n）、perpendicular（垂直 P_n）、average（向中点）

**何时触发**：
- 证明结论是「无法保证/不可能确保」
- 涉及对抗性博弈（对手可自适应选择行动）
- 需要排除存在某种聪明策略的可能性

### 完整的 CERT 升格检查清单

```markdown
- [ ] 轨道1 (SymPy): 每条代数恒等/不等式都跑过 sp.simplify()
- [ ] 轨道2 (Z3): 逻辑蕴含编码为 SMT, .check()=unsat
- [ ] 轨道3 (枚举): 临界区域零违反 + C=0 邻域零违反
- [ ] 轨道4 (Wolfram): 独立实现, 10万+随机点零失败
- [ ] 特例覆盖: m=1, n=1, 边界 T=1/(2m) 等单独验证
- [ ] 严格性审计: 每条 ">" 号的传递链都逐级确认
```

---

### MCP + Wolfbook 方案的局限

**不推荐**将 Wolfbook 的 MCP 服务器作为主要 Wolfram 调用方式。原因：

| 方案 | 缺点 |
|:----:|------|
| MCP + Wolfbook | 需要 VS Code 开着 `.wb` 文件；HTTP 桥接延迟；60s 启动等待 |
| **直接 `wolframscript`** 🏆 | 无需 VS Code；秒级响应；无中间层 |

MCP 配置仅在你**想在 VS Code 笔记本里交互式写 Wolfram 代码**时有价值。对 AI 代理直接计算而言，`terminal(wolframscript -code '...')` 更简单可靠。

---

## 关键 Pitfalls（本技能发现并修复过的）

### Pitfall 1: Hypothesis `@given` 测试必须返回 None
```python
# ❌ 错
@given(...)
def test_something(x):
    assert foo(x) == bar(x)
    return True   # 会炸: "Tests run under @given should return None"

# ✅ 对
@given(...)
def test_something(x):
    assert foo(x) == bar(x)
```

### Pitfall 2: 自交叉熵 H(p, p) 不是 0
```python
# ❌ 错
def test_cross_entropy_self_zero(logits):
    p = stable_softmax(logits)
    ce = -np.sum(p * np.log(p))
    assert ce < 1e-6   # 对均匀分布的软最大来说 ce = log(n) > 0

# ✅ 对
def test_cross_entropy_self_zero(logits):
    p = stable_softmax(logits)
    ce = -np.sum(p * np.log(p + 1e-30))
    assert ce >= -1e-10   # 熵始终非负
    if np.max(p) > 0.9999:
        assert ce < 0.01  # 只有近似 one-hot 时熵 ≈ 0
```

### Pitfall 3: 全等大数组的均值可能偏移 1 ULP
大规模相同浮点值累加时，`mean` 可能比 `max` 大 1 ULP。`min ≤ mean ≤ max` 必须带相对容差：
```python
# 用相对容差而不是绝对容差
tol = 1e-10 * max(1.0, abs(mu))
assert mn - tol <= mu <= mx + tol
```

### Pitfall 4: softmax 单调性断言不能用 argsort 比较
当 logits 有相等值时 `argsort` 的次序不确定。改为逐个比较严格不等对：
```python
for i in range(len(x)):
    for j in range(len(x)):
        if x[i] > x[j] + 1e-12:
            assert p[i] > p[j] - 1e-12
```

### Pitfall 5: Wolfram 保护符号（2026-07-06 发现）
`C`, `D`, `E` 是 Wolfram 内置符号，不能用作变量名。坐标点一律用 `pA`, `pB`, `pC`, ... 前缀。
详见上方「WolframScript 第三验证轨道」节的 Pitfall 说明。

### Pitfall 6: 折叠问题的旋转轴确定（2026-07-06 发现）
折纸/折叠类立体几何题，折叠线（折痕）是旋转轴，Q点绕该轴转到P点。二面角 A-CD-P 即为旋转角。
确定旋转轴的方向向量后，用绕轴旋转矩阵（或恰当的坐标轴旋转矩阵）计算P点坐标。
折痕沿坐标轴时直接用坐标轴旋转矩阵 `Rx`, `Ry`, `Rz`；否则需用 Rodrigues 旋转公式。

---

## 添加到新测试的方法

1. 在 `property-test.py` 中写一个 `@given(...)` 修饰的测试函数
2. 在 `TEST_GROUPS` dict 中注册（`name, test_fn` 元组）
3. 验证 `--list` 中能看到
4. 运行 `python3 property-test.py <组名>` 确认通过

### 策略指南（st.given 的参数分布）

| 输入类型 | Hypothesis Strategy |
|----------|-------------------|
| 有限浮点数 | `st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False)` |
| 概率向量 | `lists(floats(0,1)).map(normalize)` |
| logits | `lists(floats(-200, 200))` |
| 正定矩阵 | `arrays(..., A.T @ A + eps*I)` |
| 固定长度向量 | 用 `lists(..., min_size=N, max_size=N)` |
| 避免病态 | `filter(lambda x: cond(x) < 1e12)` |

---

## 补充工具（详见 `math-review`）

除上述 3 个核心模板外，工作区还包含：

### 数学基础工具

| 工具 | 命令 | 用途 |
|------|------|------|
| `matrix-health.py` | `mathkit matrix` | 条件数、SVD、特征值、数值秩分析 |
| `precision-compare.py` | `mathkit precision` | float16/32/64 三档精度误差对比 |
| `convergence-viz.py` | `mathkit convergence` | 优化轨迹、损失曲线、梯度范数 |
| `mathplot.py` | `import mathplot` | matplotlib 中文绘图 + 几何作图 |

### WolframScript 集成工具

| 工具 | 命令 | 用途 |
|:----:|:----:|:------|
| `wolframscript` | `/usr/local/bin/wolframscript` | Wolfram Engine 命令行（免费版即可） |
| 参考文件 | `references/wolframscript.md` | WolframScript 速查 + 常见模式 |

WolframScript 已安装（通过 `brew install --cask wolfram-engine`），需要先在 wolfram.com/engine 注册免费许可证。
验证安装：`wolframscript -code '2+2'` → 应返回 `4`。

### 高等数学工具（`advanced-math-templates/`）

| 工具 | 启动器 | 用途 | 依赖 |
|------|--------|------|------|
| `abstract-algebra.py` | `advmath aa` | 置换群、有限域、数论、Gröbner基 | SymPy combinatorics + polys |
| `real-analysis.py` | `advmath ra` | ε-N序列验证、一致收敛、Fourier级数、Lp范数 | NumPy + SciPy |
| `diff-geometry.py` | `advmath dg` | 度规分析、Christoffel符号、Riemann曲率、Lie括号 | SymPy (纯符号计算) |

`advmath` 启动器位于 `workspace/advanced-math-templates/advmath`，已加入 PATH。

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
advmath aa group S4              # S₄ 置换群: 阶24, 子群阶分布
advmath aa galois GF 5           # GF(5): 特征5
advmath aa nt 30                 # 数论: φ(30)=8, μ(30)=-1
advmath ra epsilon 100 0.01 '1/n'  # ε-N: 1/n→0, 找N=101
advmath ra lp-norm 'x**2' a=0 b=1 p=2  # ||x²||₂=0.4472
advmath ra series '1/n**2'       # 比值/根值判别 + 部分和
advmath ra fourier 'x' -3.1416 3.1416 5  # Fourier展开
advmath dg sphere r=2            # S²: 曲率标量R=2/R²✅
advmath dg lie-bracket '[-y,x]' '[x,y]'  # [X,Y]=0
advmath dg curvature 'x**2+1'    # 平坦空间 R=0
```

### 已知限制（该 session 修复过的 SymPy API 变更）

| 问题 | 错误信息 | 修复 |
|------|---------|------|
| `PermutationGroup` 无 `subgroups()` | `'PermutationGroup' has no 'subgroups'` → 枚举两生成元子群计算子群阶分布 |
| `FiniteField` 无 `order()` | `'FiniteField' has no 'order'` → 用 `.characteristic()` 代替 |
| `fourier_series` 导入路径错 | `TypeError: 'module' not callable` → 从 `sympy.series.fourier` 导入 |
| `diffgeom` 不接受 Matrix 度规 | `ValueError: not a two-form` → 手写公式计算 Christoffel/Riemann/Ricci/标量曲率 |

### 微分几何工具的设计决策

`diff-geometry.py` 不使用 `sympy.diffgeom` 模块（该模块需要 TwoForm 对象而非普通 Matrix），改用直接公式：

- **Christoffel 第二类符号**：\( \Gamma^k_{ij} = \frac{1}{2}g^{kl}(\partial_i g_{jl} + \partial_j g_{il} - \partial_l g_{ij}) \)
- **Riemann 曲率张量**：\( R^{l}_{kij} = \partial_i\Gamma^{l}_{kj} - \partial_j\Gamma^{l}_{ki} + \Gamma^{m}_{kj}\Gamma^{l}_{mi} - \Gamma^{m}_{ki}\Gamma^{l}_{mj} \)
- **Ricci 曲率**：\( R_{jl} = R^{i}_{jil} \)
- **标量曲率**：\( R = g^{jl}R_{jl} \)

## 物理验证扩展（Physics Verification Extensions）

当数学问题涉及物理应用（抛体、碰撞、简谐、电磁公式）时，使用 `physics-templates/` 下的工具作附加验证。

```bash
# 物理工具集中位于:
# ~/.hermes/profiles/xiandaishuxuejia/workspace/physics-templates/

source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate

# 量纲一致性检查
python3 ~/.hermes/profiles/xiandaishuxuejia/workspace/physics-templates/dimensional-check.py check 'F = m*a' 'E = m*c^2'

# 物理常数速查
python3 ~/.hermes/profiles/xiandaishuxuejia/workspace/physics-templates/constants-lookup.py g

# 物理合理性检验
python3 ~/.hermes/profiles/xiandaishuxuejia/workspace/physics-templates/physics-validate.py check speed 1000000 m/s

# 运动学符号推导
python3 ~/.hermes/profiles/xiandaishuxuejia/workspace/physics-templates/kinematics-symbolic.py projectile v0=10 theta=45
```

`physicskit` 启动器已加入 PATH（通过 `~/.zshrc`），激活 venv 后可直接使用：

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
physicskit dim 'F = m*a'         # 量纲检查
physicskit const g                # 常数查询
physicskit valid check speed 1e8 # 合理性
physicskit kin projectile ...    # 运动学
```

### 何时触发物理验证

| 数学题特征 | 使用的物理工具 | 验证内容 |
|------------|---------------|---------|
| 公式含 `F=ma`/`E=mc²`/万有引力 | `dimensional-check` | 左右量纲一致性 |
| 抛体/自由落体/竖直上抛 | `kinematics projectile/freefall` | 运动方程、射程、最高点、能量守恒 |
| 简谐运动 | `kinematics shm` | x(t)/v(t)/a(t)、a+ω²x=0、能量守恒 |
| 弹性碰撞 | `kinematics collision` | 碰撞后速度、动量/能量双守恒验证 |
| 答案需要确认数量级 | `physics-validate check` | 速度/能量/力的日常物理范围对比 |
| 物理常数参与计算 | `constants-lookup` | CODATA 精确值查询 |

### 关键实现陷阱

1. **量纲检查中数值指数必须保留原值**：`^2` 不能转为 `^1`（无量纲），否则 `c^2` 变成 `(m/s)^1` 导致量纲错误。修复见 `expr_to_unit_expr` 函数中的指数检测。

2. **歧义变量名消歧**：`m` 在质量力学语境是 `kg`，在长度语境是 `m`；`I` 是电流还是转动惯量？`T` 是周期还是温度？通过检查全局变量列表中的电磁/热学关键词做语境推断。

3. **physics-validate 命令行模式**：非交互式调用中直接处理输入后退出，避免进入 `input()` 循环导致 EOFError。

4. **轨迹方程必须消去时间参数 t**：`y(x)` 需要用 `t = x/(v₀cosθ)` 代入，而非保留 t 符号。

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/physics-tools.md` | 物理验证工具 physicskit 详细用法 |
| `references/probability-monte-carlo.md` | 概率/期望问题的 Monte Carlo 验证模式 |
| `references/hypothesis-strategies.md` | Hypothesis 策略指南与浮点容差建议 |
| `references/wolframscript.md` | WolframScript 速查 + 常见模式 + 立体几何工作流 |
| `references/cert-upgrade-workflow.md` | 四轨 CERT 升级管线：SymPy→Z3→穷举枚举→WolframScript |
| `references/pursuit-evasion-analysis.md` | 追逃问题分析模式（位于 math-review skill 下） |

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
# 需要: numpy, scipy, sympy, hypothesis (已在 venv 中预装)
# 可选: wolframscript (通过 brew install --cask wolfram-engine)
```
