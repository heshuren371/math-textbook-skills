# WolframScript 速查 & 数学验证模式

> Wolfram Engine 免费版 + `wolframscript` CLI 工具
> 安装：`brew install --cask wolfram-engine` + 注册免费许可证 https://wolfram.com/engine/free-license
> 验证：`wolframscript -code '2+2'` → `4`

---

## 基本命令

```bash
# 单表达式
wolframscript -code 'Integrate[x^2, {x, 0, 1}]'

# 多行（分号分隔）
wolframscript -code '
  a = 3; b = 4;
  Print[Sqrt[a^2 + b^2]];
'

# 带输出格式
wolframscript -code 'Plot[Sin[x], {x, 0, 2Pi}]'  # 输出 -Graphics-
```

---

## 保护符号陷阱

**永远不要用以下内置符号作变量名**：

| 符号 | 实际含义 | 替代方案 |
|:----:|:--------:|:--------:|
| `C` | 默认积分常数 | `pC`, `c0`, `cA` |
| `D` | 求导函数 `D[f, x]` | `pD`, `ptD` |
| `E` | 自然底数 \(e\) | `pE`, `ptE` |
| `I` | 虚数单位 \(\sqrt{-1}\) | `pI`, `ii` |
| `N` | 数值计算 `N[expr]` | `pN`, `nVal` |

**铁律**：坐标点一律用 `p` 前缀 → `pA`, `pB`, `pC`, `pD`, `pE`, `pF`, `pG`, `pM`, `pN`, `pP`。

---

## 高频数学模式

### 1. 向量运算（立体几何）

```wolfram
(* 定义点 *)
pA = {0, 0, 0}; pB = {2, 0, 0}; pC = {2, 2, 0};

(* 向量 *)
AB = pB - pA;
Norm[AB]                   (* 长度 *)
AB . (pC - pA)             (* 点积 → 垂直判定 *)
Cross[AB, pC - pA]         (* 叉积 → 法向量 *)

(* 垂直判定 *)
If[Chop[AB . CD] === 0, Print["\[Perpendicular]"], Print["not \[Perpendicular]"]]
```

### 2. 法向量 → 线面角

```wolfram
(* 平面法向量 *)
n = Cross[pD - pB, pN - pB];

(* 直线方向 *)
v = pB - pP;

(* 线面角正弦 *)
sinPhi = Abs[n . v] / (Norm[n] * Norm[v]);

(* 解方程 *)
Solve[{sinPhi == 1/4, s >= 0, s <= 1}, s]
```

### 3. 二面角

```wolfram
(* 两个平面的法向量 *)
n1 = Cross[pA - pD, pC - pD];   (* 平面 ADC *)
n2 = Cross[pP - pD, pC - pD];   (* 平面 PDC *)

(* 二面角余弦 *)
cosTheta = n1 . n2 / (Norm[n1] * Norm[n2]);
```

### 4. 点到平面距离

```wolfram
(* 平面 BDN，点 A *)
n = Cross[pD - pB, pN - pB];
d = Abs[(pA - pD) . n] / Norm[n]
```

### 5. 坐标轴旋转

```wolfram
(* 绕 x 轴旋转 θ 度 *)
Rx = {{1, 0, 0}, {0, Cos[θ], -Sin[θ]}, {0, Sin[θ], Cos[θ]}};
(* 绕 y 轴 *)
Ry = {{Cos[θ], 0, Sin[θ]}, {0, 1, 0}, {-Sin[θ], 0, Cos[θ]}};
(* 绕 z 轴 *)
Rz = {{Cos[θ], -Sin[θ], 0}, {Sin[θ], Cos[θ], 0}, {0, 0, 1}};

(* 应用旋转 *)
pP = pD + Rx . (pQ - pD);
```

### 6. 解方程与化简

```wolfram
Solve[{eq1, eq2, var >= 0, var <= 1}, var]    (* 带约束 *)
Simplify[expr]                                   (* 常规化简 *)
FullSimplify[expr]                               (* 强力化简 *)
Chop[expr]                                       (* 去数值误差 *)
```

---

## 高考立体几何标准模板

```wolfram
(* === 建系 === *)
pA = {0,0,0}; pB = {2,0,0}; pC = {2,2,0}; pD = {0,2,0};

(* === 折叠 / 旋转 === *)
θ = 60 Degree;
Rx = {{1,0,0},{0,Cos[θ],-Sin[θ]},{0,Sin[θ],Cos[θ]}};
pP = pD + Rx.(pQ - pD);

(* === 中点 / 参数点 === *)
pM = (pA + pP)/2;
pN = pC + s(pP - pC);   (* s∈[0,1], CN/CP = s *)

(* === 第(1)问 垂直 === *)
DM = pM - pD; PB = pB - pP;
DM.PB  (* 应为0 *)

(* === 第(2)问 线面角 === *)
n = Cross[pD-pB, pN-pB];
sinΦ = Abs[n.PB] / (Norm[n] * Norm[PB]);
Solve[{sinΦ == 1/4, s>=0, s<=1}, s]

(* === 第(3)问 距离 === *)
d = Abs[(pA-pD).n] / Norm[n] /. s -> sVal
```

---

## 与 SymPy + 数值的三轨验证流程

```
Step 1: Wolfram 建系 + 符号解
        wolframscript -code '...'  → 得到 s = 精确解
Step 2: SymPy 独立建模
        Python sympy 重新建系 → 解方程 → 对比结果
Step 3: 数值随机采样
        对关键参数扫表 → 确认连续性 → 确认解的唯一性

一致 → [CERT]
分歧 → 回溯检查哪一步建模不一致
```

---

## 常见错误排查

| 症状 | 原因 | 修复 |
|:----:|:----:|:----:|
| `Set::wrsym: Symbol X is Protected` | 用了内置符号作变量 | 改用 `pX` 前缀 |
| 结果含 `Abs[t]` 而非 `t` | Wolfram 未假设 t≥0 | `Simplify[expr, t>=0 && t<=1]` |
| `Solve` 返回空列表 | 方程或约束写错 | 去掉约束先解全集，再筛 |
| 打印中文乱码 | Terminal 编码 | 全部用英文 Print |
| `Chop[expr]` 后仍非零 | 数值误差较大 | 用 `Chop[expr, 10^-8]` |
