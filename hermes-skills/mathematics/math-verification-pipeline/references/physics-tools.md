# 物理工具参考 — Physics Tools Reference

## 概述

4 个物理工具脚本 + 1 个 `physicskit` 启动器，位于：

```
~/.hermes/profiles/xiandaishuxuejia/workspace/physics-templates/
├── dimensional-check.py    ← 量纲一致性检查（pint 驱动）
├── constants-lookup.py     ← 物理常数速查（~50 个 CODATA 常数）
├── physics-validate.py     ← 物理合理性检验（速度/能量/温度/数量级）
├── kinematics-symbolic.py  ← 运动学符号推导（SymPy 驱动）
└── physicskit              ← 启动器（已加入 PATH）
```

新增 Python 库依赖：`pint`（单位/量纲）, `uncertainties`（误差传播）。

---

## 1. dimensional-check.py — 量纲一致性检查

### 用途
验证物理公式左右量纲是否一致。对应高考/竞赛题中的公式推导验证。

### 用法

```bash
# 单条公式
python3 dimensional-check.py check 'F = m * a'

# 多条
python3 dimensional-check.py check 'E = m * c^2' 'F = G * m1 * m2 / r^2'

# 交互模式
python3 dimensional-check.py -i
```

### 输出示例

```
✅ F = m * a
  ✅ 量纲一致
  L: M * L / T ^ 2
  R: M * L / T ^ 2
```

### 已注册物理量（~60 个）

| 类别 | 变量 |
|------|------|
| 力学 | m(质量), t(时间), s/x/y/z/r/h(长度), v/u/c(速度), a/g(加速度), F(力), E/W(能量), P(功率), p(动量), I(转动惯量), ω(角速度) |
| 电磁学 | q/Q(电荷), U/V(电压), I(电流), R(电阻), C(电容), B(磁场), L(电感), ε₀, μ₀ |
| 常数 | G(引力), ħ, k_B(玻尔兹曼) |
| 热学 | T(温度), S(熵) |

### 实现陷阱（本次 session 发现并修复）

#### 陷阱 1: 指数位置的数值必须保留原值

```python
# ❌ 错误: 将 c^2 转为 (m/s)^1 (因为是数值 -> '1')
numeric_token → '1'

# ✅ 正确: 检查前一个 token 是否 ^ (已转为 **)
if prev_token == '**':
    result.append(t)   # 保留原始值如 '2'
else:
    result.append(t)   # 保留系数
```

**症状**：`E = m*c^2` 量纲会报 `M*L^2/T^2 != M*L/T`，因为 `c^2` 变成了 `(m/s)^1`。

#### 陷阱 2: 歧义变量名消歧

单字母变量在物理中含义不唯一：

| 变量 | 力学语境 | 电磁学语境 | 热学语境 |
|------|---------|-----------|---------|
| `m` | 质量 (kg) | — | — |
| `I` | 转动惯量 (kg·m²) | 电流 (A) | — |
| `R` | 半径 (m) | 电阻 (kg·m²/s³/A²) | — |
| `T` | 周期 (s) | — | 温度 (K) |
| `L` | 长度 (m) | 电感 (kg·m²/s²/A²) | — |

通过检测全局变量列表中的关键词推断语境：
- 若出现 `q`/`V`/`B`/`C` → 电磁语境（`I`=电流, `R`=电阻）
- 若出现 `k_B`/`S_ent` → 热学语境（`T`=温度）
- 默认 → 力学语境

#### 陷阱 3: `+` 操作符需要两边的量纲完全一致

pint 解析 `(kg)*(m/s^2)*(m)+(0.5)*(kg)*(m/s)^2` 时，要求 `+` 两侧的维度完全匹配才能正确归约。修复后确认 `E = m*g*h + 0.5*m*v^2` 正常工作。

---

## 2. constants-lookup.py — 物理常数速查

### 用途
快速查询高考/竞赛常用物理常数的精确值、精度和别名。

### 用法

```bash
python3 constants-lookup.py           # 列出所有常数（按类别分组）
python3 constants-lookup.py g         # 搜索含 'g' 的常数
python3 constants-lookup.py 引力       # 搜索含 '引力' 的常数
python3 constants-lookup.py --help
```

### 支持的别名查询

| 别名 | 对应常数 |
|------|---------|
| `g0`, `g_n`, `g_std` | 标准重力加速度 9.80665 m/s² |
| `hbar`, `h_bar` | 约化普朗克常数 |
| `k`, `k_B`, `kb` | 玻尔兹曼常数 |
| `me`, `m_e` | 电子质量 |
| `mp`, `m_p` | 质子质量 |
| `mn`, `m_n` | 中子质量 |
| `a0`, `a_0` | 玻尔半径 |
| `pi`, `Pi` | 圆周率 |
| `euler` | 自然对数的底 |

### 常数分类

- **基本常数**：c, μ₀, ε₀, G, h, ħ, e, k_B, N_A, R
- **电磁学**：k_e, μ_B, μ_N, α
- **原子物理**：m_e, m_p, m_n, r_e, a_∞, R_∞, eV
- **地球物理**：g (4 地点), M_E, R_E (3 形态), AU, M_S, R_S, M_M, R_M, d_EM
- **物理化学**：atm, V_m, 三相点, 绝对零度
- **量子**：λ_C, Φ₀, G₀

---

## 3. physics-validate.py — 物理合理性检验

### 用途
验证数学推导结果的物理合理性：速度是否超光速？能量数量级是否正确？温度是否低于绝对零度？

### 用法

```bash
# 检查速度合理性
python3 physics-validate.py check speed 1000 m/s

# 检查能量合理性
python3 physics-validate.py check energy 1e10 J

# 机械能守恒计算
python3 physics-validate.py energy m=0.01 v=300 h=0

# 数量级检查
python3 physics-validate.py order 5.97e24 kg

# 列出所有物理量合理范围
python3 physics-validate.py range
```

### 支持的物理量范围

| 物理量 | 单位 | 典型范围 | 日常参考值 |
|--------|------|---------|-----------|
| speed | m/s | 0 ~ 3e8 | 步行 1.4, 声速 340, 光速 3e8 |
| acceleration | m/s² | 0 ~ 1e10 | 重力 9.8, 子弹 1e5 |
| mass | kg | > 0, ≤ 1e31 | 电子 9e-31, 人 70, 地球 6e24 |
| force | N | ≤ 1e20 | 日常 < 1e4 |
| energy | J | 0 ~ 1e40 | 子弹 1e3, 原子弹 6e13, 超新星 1e44 |
| temperature | K | ≥ 0 | 室温 293, 太阳表面 5778 |
| time | s | ≥ 0 | 一天 86400, 宇宙年龄 4e17 |
| length | m | ≥ 0 | 原子 1e-10, 人 1.7, 地球 6e6 |

### 实现注意

- 非交互式模式：直接处理参数后退出，不进入 `input()` 循环
- `speed 300000000 m/s` → 超光速警告（max_error = 3.03e8）
- 每个物理量给出最接近的典型参考值（如超光速检查会匹配"光速"）

---

## 4. kinematics-symbolic.py — 运动学符号推导

### 用途
用 SymPy 自动推导运动方程。5 类场景：抛体、简谐运动、自由落体、圆周运动、弹性碰撞。

### 用法

```bash
# 抛体运动
python3 kinematics-symbolic.py projectile v0=20 theta=30

# 简谐运动
python3 kinematics-symbolic.py shm A=3 omega=2 phi=0.5

# 自由落体/竖直上抛
python3 kinematics-symbolic.py freefall v0=10 h0=50
# v0>0 → 上抛, v0=0 → 自由落体

# 匀速圆周运动
python3 kinematics-symbolic.py circular v=7900 r=6370000
# 参数 v=7900m/s, r=6370km → ω=0.0012, T=5066s, a_c=9.8m/s²

# 一维弹性碰撞
python3 kinematics-symbolic.py collision m1=2 v1=3 m2=1 v2=-2
```

### 各场景输出内容

| 场景 | 输出 |
|------|------|
| **projectile** | x(t), y(t), v_x(t), v_y(t), y(x) 轨迹方程 ± 标准形式, 飞行时间, 射程, 最高点, 落地速度, 对称性验证 |
| **shm** | x(t), v(t), a(t), a+ω²x=0 验证, E_k/E_p/E_total（t=0 数值 + 对 t 求导=0 验证）, 极值 |
| **freefall** | y(t), v(t), 落地时间, 落地速度, 最高点（仅上抛） |
| **circular** | ω, T, f, a_c, v=ωr 验证, ω²r=a_c 验证 |
| **collision** | v₁', v₂', 标准公式验证, 动量/能量守恒验证, 相对速度验证 |

### 实现陷阱（本次 session 发现并修复）

#### 陷阱: 轨迹方程必须消去时间参数

```python
# ❌ 错误: y(x) 表达式仍含 t
y_of_x = y.subs(...)  # 未正确代入 t = x/(v₀cosθ)

# ✅ 正确: 显式代入 t = x/v₀ₓ，再化简
y_of_x = (v0y / v0x) * x_sym - (g / (2 * v0x**2)) * x_sym**2
```

**症状**：输出 `y(x) = -4.9*t^2 + 7.07*t`（仍含 t，完全错误）。正确应为 `y(x) = 0.577x - 0.0163x²`。

---

## physicskit 启动器

`physicskit` 是一个 shell 脚本，接受 `dim`, `const`, `valid`, `kin` 作为子命令。

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate

physicskit dim 'F = m * a'          # → dimensional-check check F ...
physicskit const g                   # → constants-lookup.py g
physicskit valid check speed 1e8    # → physics-validate check speed 1e8
physicskit kin projectile v0=10     # → kinematics-symbolic projectile v0=10
```

使用 `$(dirname "${BASH_SOURCE[0]}")` 做可移植路径解析，不依赖绝对路径。

### 新增库依赖

```bash
pip install pint uncertainties
```

- `pint 0.25.3` — 物理单位/量纲系统（UnitRegistry）
- `uncertainties 3.2.3` — 自动误差传播（实验物理）
