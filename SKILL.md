---
name: math-textbook-authoring
description: 📘 数学教材自动化编写 Skill——从章节骨架到 ε-N/ε-δ 审计到编译交付，全流程覆盖。
emoji: 📘
tags: [latex, textbook, mathematics, analysis, pipeline]
---

# 📘 math-textbook-authoring Skill

数学教材自动化编写——从函数重建到严格分析，适用于数学分析、拓扑学、代数学、数论等任何数学分支。

## 快速开始

```bash
# 1. 安装依赖
brew install tectonic          # LaTeX 编译器
python3 mathbook-pipeline.py --help   # 查看所有命令

# 2. 创建新项目
python3 mathbook-pipeline.py init "我的教材"

# 3. 创建第一章
python3 mathbook-pipeline.py chapter new ch01 "函数的概念"

# 4. 写内容 → 审计 → 修复 → 编译（循环）
python3 mathbook-pipeline.py audit ch01
python3 mathbook-pipeline.py fix ch01
python3 mathbook-pipeline.py build
```

## 管线架构

```
┌─────────────────────────────────────────────────────┐
│                 mathbook-pipeline.py                 │
├──────────┬──────────┬──────────┬──────────┬──────────┤
│  init    │ chapter  │  audit   │   fix    │  build   │
│ 初始化   │ 创建/管理  │  审计    │  修复    │  编译    │
├──────────┴──────────┼──────────┼──────────┴──────────┤
│    领域无关核心      │ 可插拔域  │   分层修复层         │
│  - 项目骨架          │ - structural │ - syntax         │
│  - 章节骨架          │ - analysis  │ - pairing        │
│  - 图脚本骨架        │ - topology  │ - unicode        │
│  - book.tex 管理     │ - algebra   │ - mathmode       │
└─────────────────────┴──────────┴─────────────────────┘
```

## 每章结构

每章必须包含以下 6 个段落，缺一不可：

```
┌─ ① 应用引导 ──────────────────────────────┐
│  \begin{applicationbox}                    │
│  学完本章你能做什么？（3条）                │
│  \end{applicationbox}                     │
├─ ② 前置知识补充（仅第1章需要）──────────────┤
│  \section*{知识补充：集合、数集与区间}      │
│  定义：集合、∈、常见数集(N/Z/Q/R)、区间     │
│  ([a,b]/(a,b)/[a,b)/(a,b])、并集∪、交集∩   │
├─ ③ 核心内容 ──────────────────────────────┤
│  直觉引入 → 定义框 → 例题(8-12个，第1个    │
│  完全展开不跳步) → 定理框 → 图              │
├─ ④ 符号卡片 ──────────────────────────────┤
│  \begin{symbolcard}  新符号注音             │
├─ ⑤ 代码验证 ──────────────────────────────┤
│  \begin{lstlisting}  Python 数值验证        │
├─ ⑥ 本章小结 ──────────────────────────────┤
│  进步宣言 + 「从上一章来」+「通往下一章」     │
├─ ⑦ 习题 ──────────────────────────────────┤
│  30道 / 9级难度（见下表）                   │
└────────────────────────────────────────────┘
```

### 前置知识模块（第1章必修）

所有从零开始的教材，第1章必须先插入 **知识补充：集合、数集与区间** 模块：

| 概念 | 用法 | 示例 |
|:-----|:-----|:-----|
| 集合定义 | $\{1,2,3\}$，$a\in A$，$a\notin A$ | $2\in\{1,2,3\}$ |
| 常见数集 | $\mathbb{N},\mathbb{Z},\mathbb{Q},\mathbb{R}$ | $\mathbb{N}\subset\mathbb{Z}\subset\mathbb{Q}\subset\mathbb{R}$ |
| 区间 | $[a,b]$, $(a,b)$, $[a,b)$, $(a,b]$ | $[0,1)$ 表示 $0\le x<1$ |
| 并集 | $A\cup B$ | $\{1,2\}\cup\{2,3\}=\{1,2,3\}$ |
| 交集 | $A\cap B$ | $\{1,2\}\cap\{2,3\}=\{2\}$ |

确保读者理解：**集合是函数的容器，区间是函数的活动范围。**

## 习题难度体系

| 代码 | 难度 | 题量 | 说明 |
|:----:|:----:|:----:|:------|
| [0] | 送分 | 4 | 直接代入公式，1步 |
| [1] | 简单 | 4 | 一个知识点直接用，1-2步 |
| [2] | 基础 | 4 | 核心概念直接应用，2-3步 |
| [3] | 普通 | 5 | 需要简单推理，3-4步 |
| [4] | 中等 | 5 | 概念综合，4-6步 |
| [5] | 进阶 | 4 | 技巧性推理，6-8步 |
| [6] | 拔高 | 3 | 跨章节联系，8-10步 |
| [7] | 极难 | 1 | 竞赛风格，10+步 |

无竞赛题。每章 30 道。

## 三种分析语言覆盖（严格模式必修）

### 1️⃣ ε-N 语言（数列极限）
- 位置：第11章
- 定义：\(\forall\varepsilon>0,\exists N\in\mathbb{N}, n>N\Rightarrow|a_n-L|<\varepsilon\)
- 用于：数列收敛、级数收敛（第26-28章）

### 2️⃣ ε-δ 语言（函数极限与连续）  
- 位置：第14章
- 定义：\(\forall\varepsilon>0,\exists\delta>0, 0<|x-a|<\delta\Rightarrow|f(x)-L|<\varepsilon\)
- 用于：函数极限、连续、导数（第17-22章）

### 3️⃣ 邻域语言（开集与覆盖）
- 位置：第15章
- 定义：\(U(a,\varepsilon)=\{x:|x-a|<\varepsilon\}\)，开集、开覆盖、海涅-博雷尔
- 用于：有界性定理的有限覆盖证明

## 关键定理的 ε-δ/ε-N 证明清单

| 章节 | 定理 | 证明要求 |
|:----|:-----|:---------|
| ch17 | 导数定义 | 至少在一个 example 中用 ε-δ 展开 `lim_{h→0}` |
| ch18 | 乘法法则、链式法则 | ε-δ 定义推导 |
| ch19 | 罗尔/拉格朗日/柯西 MVT | 辅助函数法 + 极值 ε 论证 |
| ch20 | 洛必达法则 | 柯西 MVT 证明 |
| ch20 | 泰勒定理 + 拉格朗日余项 | 证明框架 |
| ch22 | 黎曼和极限 | ε-δ 定义 |
| ch22 | 连续 ⇒ 可积 | 一致连续 + 达布上下和 |
| ch23 | FTC（上限函数求导） | 积分中值 + ε-δ |
| ch25 | 广义积分比较 | ε-N 柯西准则 |
| ch26 | 级数收敛定义 | ε-N 部分和柯西 |
| ch26-27 | 比较/比值/积分判别法 | ε-N 证明 |
| ch28 | 柯西-阿达马（收敛半径） | ε-N 根值法 |
| ch29 | 傅里叶收敛定理 | 狄利克雷核 + ε 拆分 |
| ch30 | Clairaut（混合偏导相等） | ε-δ 中值定理证明 |

## LaTeX 编译陷阱清单

| # | 问题 | 错误信息 | 修复 |
|---|------|---------|------|
| 1 | `\begin{examplebox}[...}` 花括号误写 | `Argument of \examplebox has an extra }` | `}`→`]` |
| 2 | `^` `_` `\frac` 在 examplebox 标题中 | `Missing $ inserted` | 简化标题或用 `{...}` 包裹 |
| 3 | `\blacksquare` 在数学模式外 | `Missing $ inserted` | 改为 `\(\blacksquare\)` |
| 4 | 连续 `\begin{exercise}` 缺 `\end{exercise}` | 环境未闭合 | 每个 begin 对应一个 end |
| 5 | `\end{section}` 不存在 | `Undefined control sequence` | 删除 |
| 6 | `\verb` 在 tabular/symbolcard 中 | 编译异常 | 用 `\texttt` 替代 |
| 7 | `openright` | 空白页 | 改为 `openany` |
| 8 | `→` `✓` `✗` `【` `】` `℃` 等 Unicode | `Missing character` | 用 LaTeX 命令或纯文本替代 |
| 9 | `\frac{...]{...}` 括号错 | `File ended while scanning \frac` | `]`→`}` |
| 10 | `\]` 在 `\end{cases}` 之前 | `Missing $ inserted` | 交换顺序：先 `\end{cases}` 后 `\]` |
| 11 | `\end{aligned}` 在 `\]` 之后 | `Bad math environment delimiter` | `\]` 在最后 |

自检命令：`python3 mathbook-pipeline.py fix all` 一键修复 1-11 全部。

## 审计域说明

| 域 | 审计内容 | 适用领域 |
|:---|:---------|:---------|
| `structural` | 环境配对、数学模式、Unicode 毒瘤 | **通用** |
| `analysis` | ε-N/ε-δ 追踪 | 数学分析、实分析 |
| `topology` | 开集/闭集/紧致/连通 | 拓扑学、点集拓扑 |
| `algebra` | 群/环/域/同态/同构 | 抽象代数、近世代数 |
| `number-theory` | 素数/ζ函数/L函数 | 解析数论、代数数论 |

切换：`MATHBOOK_DOMAIN=topology python3 mathbook-pipeline.py audit`

## 交付前强制五问

```
1. ✅ 每个 \lim 都有 ε 追踪？（第3-5编无裸 lim）
2. ✅ 第3-5编关键定理有 ε 证明？（见上表 16 项）
3. ✅ 无跳步词？（grep "显然|易证|篇幅所限" 应为 0）
4. ✅ 无编译毒瘤？（grep 检查 LaTeX 陷阱清单 1-11）
5. ✅ 习题已补？（\begin{exercise} 计数 == 30）
```

**5/5 通过 → 可交付。4/5 → 退回补全。3/5 以下 → 不可交付。**

## 添加新审计域

在 `mathbook-pipeline.py` 的 `AUDIT_DOMAINS` 字典中添加：

```python
def _my_domain_audit(files):
    for fp in files:
        # 自定义检查逻辑
    return fail_count

AUDIT_DOMAINS['my-domain'] = ('我的领域', _my_domain_audit)
```

然后运行：`python3 mathbook-pipeline.py audit my-domain`
