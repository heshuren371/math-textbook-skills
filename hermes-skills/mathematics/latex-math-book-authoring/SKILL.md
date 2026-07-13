---
name: latex-math-book-authoring
description: 高等数学/微积分教材全流程生成——从读者画像→认知依赖图→元认知设计→大纲→逐章撰写→矢量图→数值验证→编译交付
emoji: 📘
---

# LaTeX 中文数学教材编写

本技能覆盖**教材生成的全流程**——从教学法设计（读者画像、认知依赖图、元认知主线）到技术实现（LaTeX 排版、矢量图生成、数值验证、编译交付）。实战产出：《自学高数》（88页/10章）和《数学 for AI》（199页/3卷/72天/10模块极致平滑路线）。

---

## 🚪 快速启动（写完一章的标准操作）

> **2026-07-13 更新：统一管线 `mathbook-pipeline.py` 已就位。**
> 支持可插拔审计域（analysis/topology/algebra）、分层修复层（syntax/pairing/unicode/mathmode），
> 兼容 Claude Code / Codex CLI（见 `agents/MATH_TEXTBOOK_AGENT.md`）。

```bash
# 在教材项目根目录下操作

# 1. 写新章节前加载两个 skill（必做）
skill_view(name='latex-math-book-authoring')   # 看主流程
skill_view(name='epsilon-n-delta-audit')        # 看审计清单

# 2. 创建章节骨架
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
python3 mathbook-pipeline.py chapter new chXX "标题"

# 3. 写正文 + 画图 + 补习题（见各章节细则）

# 4. 审计（可指定域）
python3 mathbook-pipeline.py audit analysis chXX     # 数学分析 ε 审计
python3 mathbook-pipeline.py audit topology chXX     # 拓扑学审计
python3 mathbook-pipeline.py audit structural chXX   # 仅结构审计

# 5. 分层修复
python3 mathbook-pipeline.py fix syntax chXX         # LaTeX 语法
python3 mathbook-pipeline.py fix pairing chXX        # 环境配对
python3 mathbook-pipeline.py fix unicode chXX        # Unicode 字符
python3 mathbook-pipeline.py fix all chXX            # 全量修复

# 6. 编译
tectonic book.tex

# 7. 全书报告
python3 mathbook-pipeline.py audit
```

### 用户授权自动续写模式

当用户说「就按这样的工作流一直写下去」「自己跑完」「继续」「我给你权限自动进行下一章的编写」时：

- **不需要等用户确认**，写完一章后直接开始下一章
- 每章仍保持完整流程：画图 → 写内容 → 补习题 → 编译前检查 → 编译
- 如果编译报错，自动修复后重试，无需中断
- 仅在以下情况停下来问用户：(1) 需求不明确无法推进；(2) 全书写完；(3) 编译错误反复出现且自动修复无效

### ε-N/ε-δ 审计入口

**严格模式交付前必做（2026-07-13 血泪教训）：** 先 `skill_view(name='epsilon-n-delta-audit')` 加载审计清单，再逐条检查全书的每个 `\lim` 都有 ε-N/ε-δ 表述或明确引用。遗漏 ε 证明 = FAIL。

可用 `mathkit chapter report` 自动扫描全书漏洞。

---

## 一、读者画像（出大纲前必须先做）

**不动笔写任何内容之前，先锁定读者。**

### 1.1 读者画像问卷

向用户逐条追问（不要一次性全抛）：

```
Q1：数学起点？（因式分解/三角函数/对数/全忘了）
Q2：为什么学？（考研/转行AI/工作遇到/兴趣）
Q3：每天能花多少时间？[分钟/天]
Q4：对数学的态度？（看公式紧张/不排斥/愿意啃）
Q5：学完想达到什么水平？
Q6：习题难度偏好？是否需要竞赛级题目？
   （成人自学者往往不需要竞赛题，极难题1道就够了）
```

**根据 Q6 调整习题参数**：如果用户明确不需要竞赛题，则去掉竞赛题（9级），极难（8级）最多保留1道。送分→拔高（7级）不变。全9级体系的结构不动，只在每章实例化时裁剪顶层难度。

### 1.2 输出：读者画像声明

```
本教材面向 [起点描述] 的读者。
学习动机：[动机]，日均学习时间：[时间]。
内容策略：[策略描述]
```

---

## 二、认知依赖图

从目标知识点反向推导，标记每个概念的前置依赖。每章引用的应用引导必须引用依赖图中的上下游。

```
函数 ──→ 极限 ──→ 导数 ──→ 积分
  ↑         ↑         ↑
指数/对数 ─┘         │
三角函数 ────────────┘
```

---

## 三、元认知设计

| 能力 | 出现环节 |
|------|---------|
| 数学思维 | 定义框之前的直觉引入段 |
| 批判性思维 | 每个定理后问"局限在哪" |
| 独立思考 | ≥20% 开放题 |
| 创造性思维 | 每章末尾"拓展思考"框 |

正文语调是**提出问题**，不是**宣布答案**。

---

## 四、核心写作原则

### 4.1 教学模式与难度界限

根据读者目标选择教学模式——**两种模式不可混用，选定后贯穿全书**：

| 模式 | 适用场景 | ε-δ 语言 | 证明要求 |
|:----:|:--------:|:--------:|:--------:|
| **直觉模式** | AI/应用导向 | ❌ 禁止 | 直观推理为主 |
| **严格模式** | 数学分析/理论导向 | ✅ 必修 | 完整 ε-N/ε-δ 证明链 |

**直觉模式难度：** 不用 ε-δ、实数完备性、勒贝格积分。最多用到初等函数求导、定积分求面积、一阶线性微分方程。

**严格模式难度：** ε-N（数列极限）和 ε-δ（函数极限）为必修。实数完备性逐步引入（确界原理→单调有界→闭区间套）。完整证明链（罗尔→拉格朗日→柯西→泰勒→洛必达）。黎曼积分的严格定义（达布和、可积性条件）。具体证明模板见 `references/strict-mode-proofs.md`。

**⚠️ 严格模式交付前必做：** 加载 `skill_view(name='epsilon-n-delta-audit')`，逐条检查全书的每个 `\lim` 都有 ε-N/ε-δ 表述或明确引用。遗漏 ε 证明 = FAIL（详见该 skill）。

**两模式均适用：** 每个新符号附读音标注；重要定理标注失效条件。

### 4.2 五步法

```
直觉引入 → 可视化描述 → 非严格定义 → 严格定义（定义框） → 立即跟例子
```

### 4.3 应用引导三问

```
1. 这章解决什么真实问题？
2. 学之前做不到什么？学之后能做到什么？
3. 给一个日常生活例子。
```

### 4.4 禁忌词

| 禁止 | 替换 |
|------|------|
| 显然、不难看出、易证 | 给出具体推理或数值趋势 |
| 由定义可知 | 回顾定义并逐句翻译 |
| 众所周知、你可能记得 | 读者不知道不记得 |

---

## 五、AI 特化课程设计

### 5.1 AI 相关性星级

| 星级 | 含义 | 代表内容 |
|------|------|---------|
| ⭐⭐⭐⭐⭐ | AI 最核心 | 链式法则、线性变换、梯度、Softmax、交叉熵 |
| ⭐⭐⭐⭐ | 非常重要 | 向量/矩阵、偏导数、概率分布、凸优化 |
| ⭐⭐⭐ | 用得着 | 极限思想、积分基础、微分方程直觉 |
| ⭐⭐-⭐ | 背景/几乎不用 | 连续性细节、ε-δ 证明、中值定理证明 |

### 5.2 AI 正确的概念顺序

```
第 1 层：线性世界 —— y=kx+b = 一个神经元
第 2 层：弯曲能力 —— 平方/多项式 → Loss 是个碗
第 3 层：概率的灵魂 —— 指数 e^x → Softmax，对数 ln → 交叉熵
第 4 层：导数 —— 链式法则 → 反向传播
第 5 层：优化 —— 梯度下降
第 6 层：概率与累积 —— 积分基础
第 7 层：微分方程直觉 —— 扩散模型
```

### 5.3 三卷分离策略

| 卷 | 内容 | 大约天数 |
|----|------|---------|
| 第一卷 | 高等数学速通——AI版 | 35~40 天 |
| 第二卷 | AI核心数学（线性代数+多元微积分+概率+优化） | 60~70 天 |
| 第三卷 | 进阶（信息论+泛函+DL数学） | 按需 |

---

## 六、写作风格铁律（用户偏好嵌入）

### 6.1 "把我当傻瓜教"——极致详细

- **零前置假设**：不假设读者记得任何事。从负数开始。
- **每步展开**：$2x+1$ 代入 $x=3$ 必须写成 $2\times3+1=6+1=7$，不能跳步。
- **先数字再符号**：先算具体数字例子，再给一般公式。
- **符号恐惧消除**：$x$ = 一个空盒子。
- **不要"你记得吗"**：读者不记得。直接讲。

### 6.2 语速控制

| 场景 | 要求 |
|------|------|
| 新概念第一次出现 | 至少 200-300 字直觉引入 |
| 第一个数字例子 | 展开每一步，不准跳步 |
| 第二个例子 | 正常速度 |
| 第三个以后 | 常规教材速度 |

---

## 七、极致平滑模式（AI/自学专用）

当读者明确要求"把我当傻瓜教"或"极致详细"时，切换到此模式。

### 7.1 每日结构（45 分钟）

```
1. 应用引导（3行）：今天学完能做什么？+ AI例子  （2分钟）
2. 核心概念 1-2 个（绝不超过 3 个）           （10分钟）
3. 符号卡片：长什么样、怎么读、干什么用         （3分钟）
4. 直觉引入：故事/比喻/生活场景                （5分钟）
5. 手算例子：数字代入，每步展开不跳步          （10分钟）
6. 动手验证：3-5 个自测题                     （10分钟）
7. 今天学到的核心：三条总结                    （5分钟）
8. （可选）AI 小剧场：这个概念在 AI 哪里出现
```

### 7.2 每天只加 1-2 件新事

| 错误的做法 | 正确的做法 |
|-----------|-----------|
| 第1天讲函数+六类函数+复合+反函数 | 第1天只认识负数/变量/等式 |
| 一次教完三角函数和指数 | 先只学线性函数，曲线放到两周后 |
| 第2天讲极限+运算法则+连续 | 第2天只做代入运算练习 |

### 7.3 每步展开示例

```latex
% ❌ 跳步
代入 x=3：2x+1=7

% ✅ 每步写清
原式：2x+1
代入：2×3+1
先乘：6+1
再加：7
```

---

## 八、工作流程

```
步骤0：读者画像 + 认知依赖图 + 元认知规划
步骤1：全书大纲
步骤2：逐章撰写（每日/每节）
  2.1 写 LaTeX 内容（含「从上一章来」「应用引导」「例题」「符号卡片」「代码验证」
          「本章小结」「通往下一章」）
  2.2 写习题（30道，9级难度，见9.5节）——写完正文后立即补，不可跳过
  2.3 画图（Python → PDF 矢量图，见第十节）
步骤3：编译前五查（提交前强制检查）
  [ ] 配对检查：`\[` vs `\]`、`\(` vs `\)` 计数一致
  [ ] Exercise 配对：`\begin{exercise}` 计数 = `\end{exercise}` 计数
  [ ] 习题存在性：`grep -c "begin{exercise}"` > 0
  [ ] Examplebox 括号检查：所有 `\begin{examplebox}[...]` 的右括号是 `]` 不是 `}`
  [ ] 图存在性：`\includegraphics` 中引用的 PDF 文件在 figures/ 下存在
步骤4：编译（tectonic book.tex）
步骤5：自动修复 + 重编译（如果报错，修复后回到步骤3）
```

---

## 九、技术实现细节

### 9.1 项目目录结构

```
project/
├── book.tex              # 主文件
├── compile.sh
├── shared/preamble.tex
├── step0/ step1/ ...     # 按 part/step 分目录
├── appendix/answers.tex
└── figures/
    ├── gen_ch*.py
    └── *.pdf
```

### 9.2 导言区

```latex
\documentclass[12pt,a4paper,openany]{ctexbook}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry, hyperref, fancyhdr}
\usepackage[most]{tcolorbox}
\usepackage{graphicx, array, booktabs, tikz}
\graphicspath{{figures/}}
```

### 9.3 六色 tcolorbox 环境

```latex
\newtcolorbox{applicationbox}{colback=teal!5!white, colframe=teal!60!black,
  fonttitle=\bfseries\large, title=学完本章你能做什么？}
\newtcolorbox{definitionbox}[1][]{colback=green!5!white, colframe=green!60!black,
  fonttitle=\bfseries, title=定义 #1}
\newtcolorbox{theorembox}[1][]{colback=blue!5!white, colframe=blue!60!black,
  fonttitle=\bfseries, title=定理 #1}
\newtcolorbox{propositionbox}[1][]{colback=purple!5!white, colframe=purple!60!black,
  fonttitle=\bfseries, title=命题 #1}
\newtcolorbox{examplebox}[1][]{colback=orange!5!white, colframe=orange!70!black,
  fonttitle=\bfseries, title=例题 #1}
\newtcolorbox{notebox}[1][]{colback=red!5!white, colframe=red!70!black,
  fonttitle=\bfseries, title=注意 #1}
\newtcolorbox{progressbox}{colback=yellow!10!white, colframe=yellow!60!orange,
  fonttitle=\bfseries\large, title=进步宣言}
```

### 9.4 符号卡片（4列版——含读法）

```latex
\newenvironment{symbolcard}{%
  \par\vspace{6pt}
  \\noindent\\begin{tcolorbox}[colback=gray!3!white, colframe=gray!50!black, arc=2pt, title=[卡] 符号卡片]
  \renewcommand{\arraystretch}{1.3}
  \\begin{tabular}{c|c|c|p{4.5cm}}
  \\toprule
  \\bfseries 符号 & \\bfseries LaTeX 写法 & \\bfseries 读法 & \\bfseries 含义 \\\\
  \midrule
}{%
  \bottomrule \end{tabular} \end{tcolorbox} \par\vspace{6pt}
}
```

必须包含「读法」列——读者需要知道每个符号怎么读。比「含义」列先列出，因为读法是第一需求。

### 9.5 练习与答案环境

每章习题按 **9 级难度**分层编排。题号旁标注难度符号，答案按章节+难度分组放在附录。

| 级别 | 星级 | 含义 | 每题约需步骤 | 每章题量 |
|:----:|:----:|------|:----------:|:--------:|
| 1 | ⭐ | **送分**——直接代入公式 | 1 步 | 2-3 |
| 2 | ⭐⭐ | **简单**——一个知识点直接用 | 1-2 步 | 3-5 |
| 3 | ⭐⭐⭐ | **基础**——核心概念直接应用 | 2-3 步 | 3-5 |
| 4 | ⭐⭐⭐⭐ | **普通**——需要简单推理 | 3-4 步 | 5-8 |
| 5 | ⭐⭐⭐⭐⭐ | **中等**——概念综合 | 4-6 步 | 5-8 |
| 6 | 🔥 | **进阶**——技巧性推理 | 6-8 步 | 3-5 |
| 7 | 🔥🔥 | **拔高**——跨章节联系 | 8-10 步 | 2-3 |
| 8 | 🔥🔥🔥 | **极难**——竞赛风格 | 10+ 步 | 1-2 |
| 9 | 🏆 | **竞赛**——真正竞赛难度 | 多步+创造性 | 1 |

习题按难度分组排列，同组内由易到难。答案放在附录，按 `章号.题号` 索引，标注难度级别。

```latex
% 练习环境（支持难度标注）
\newcounter{exercise}[chapter]
\renewcommand{\theexercise}{\thechapter.\arabic{exercise}}
\newenvironment{exercise}[1][]{%
  \refstepcounter{exercise}
  \par\vspace{8pt}
  \noindent\textbf{练习 \theexercise} \textcolor{gray}{(#1)}\quad
}{\par\vspace{4pt}}
\newenvironment{answer}[1]{%
  \par\vspace{6pt}
  \noindent\textbf{#1} 解答\quad
}{\par\vspace{4pt}}

% 习题分组环境（每章开头按难度定义组）
\newcommand{\difficultygroup}[2]{%
  \subsection*{\textcolor{purple}{#1}\hfill\textcolor{gray}{#2}}}
```

### 9.6 每章模板

章节模板遵循「从上一章来 → 核心内容 → 通往下一章」三段结构：

```latex
\chapter{标题}

% ── 段1：从上一章来（过渡桥梁） ──
\section*{从上一章来}
上一章我们学了……现在我们要往前走一步……
每章开头必须有 3-8 行回顾，连接上一章的终点和本章的起点。

% ── 段2：应用引导 ──
\begin{applicationbox}
\textbf{学完本章你能做什么？}
\begin{enumerate}
  \item 学之前做不到？学之后能做到？
  \item 给一个日常例子。
\end{enumerate}
\end{applicationbox}

% ── 段3：核心内容（每章 8-12 个例题） ──
\section{问题：……}
\subsection{直觉引入}
\subsection{定义}
\begin{definitionbox}[概念] 定义 \end{definitionbox}
\subsection{例题}
\begin{examplebox}[1] 第一步完全展开不跳步 \end{examplebox}
\subsection{符号卡片}
\begin{symbolcard} 符号 & \verb|写法| & 读法 & 含义 \\ \end{symbolcard}
\subsection{数值验证}
\begin{lstlisting}[language=Python] ... \end{lstlisting}

% ── 段4：本章小结 ──
\section{本章小结}
\begin{progressbox}
\textbf{之前你……} \textbf{现在你……}
\end{progressbox}

% ── 段5：通往下一章（过渡桥梁） ──
\subsection*{通往下一章}
每一章结尾必须有一段过渡（3-8 行），回答三个问题：
1. 本章学会了什么？2. 引出了什么新问题？3. 下一章解决什么？

\subsection*{⚠️ 主动发现课程缺口（2026-07-13 教训）}
写严格模式数学分析教材时，必须在设计阶段主动检查以下三种语言的覆盖：
- **ε-N 语言**（数列极限，ch11-12）
- **ε-δ 语言**（函数极限与连续，ch14-16）
- **邻域/开集语言**（开覆盖、紧致性，ch15 末）
**不要在教材中使用未定义的术语。** 如果在 ch16 的证明中要用"开覆盖"概念，
必须先在最前面的章节（ch15）定义开集、开覆盖、海涅-博雷尔定理。
用户会发现问题并质问"为什么不让邻域语言系统化"——应该在用户指出之前自己补上。

\subsection*{📊 量化审计报告}
交付前运行以下命令获得全书量化审计：
```
mathkit pipeline audit   # 或 mathkit chapter report
```
报告会列出每章的 lim 数、ε 覆盖、例题数、习题数、图数、编译毒瘤数和通过状态。
标准：5/5 强制五问全通过方可交付。

% ── 段6：习题（9 级难度，30-40 道） ──
\section{习题}
% 按 9 级难度排列，见 9.5 节
\end{lstlisting}

每章深度目标（严格模式适用）：

| 维度 | 目标 |
|:----|:----|
| 页数 | 25-35 页 |
| 例题 | 8-12 个（第1个完全展开不跳步） |
| 习题 | 30-40 道（9 级难度） |
| 插图 | 至少 5 幅（见 10.3 节） |
| 过渡桥梁 | 章首「从上一章来」+ 章末「通往下一章」 |
| 代码验证 | 每章至少 1 段 Python 代码 |

---

## 十、配图策略（Python → PDF 矢量图）

### 10.1 图片生成模板

```python
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC'],
    'font.size': 13, 'axes.unicode_minus': False})
fig, ax = plt.subplots(figsize=(8, 5))
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig('figures/chXX_name.pdf', format='pdf', bbox_inches='tight')
```

### 10.2 关键提醒

- `\\displaystyle` 在 matplotlib 中不可用
- 用 `from math import factorial` 而非 `np.math.factorial`（NumPy 2.x 已弃用）
- `\\xrightarrow` 在 matplotlib mathtext 中不可用，改用 `\\to`
- 中文和 LaTeX 混排时，中文在 $...$ 外面

### 10.3 插图密度原则

避免「文字堆砌、图像稀少」——读者反馈「之前的教材图像太少」：

- **每节至少 1 幅图**：函数定义配图像、定理证明配几何示意图、例题配数轴/坐标系图
- **抽象概念必须配图**：ε-N 示意图（数列向极限点收敛的可视化）、ε-δ 示意图（函数在 x₀ 附近被控制在带内）、定积分示意图（黎曼和与曲边梯形）
- **每章至少 5 幅图**：含主图（核心概念）+ 子图（对比/特例）+ 应用图
- **图不是装饰，是论证的一部分**：每张图必须在正文中被引用（"如图 X 所示…"）

### 10.4 图质量陷阱（用户反馈驱动的检查清单）

用户曾反馈「U型函数的顶点是错的」「坐标系有两个O点」——在教材用图中，以下问题必须检查：

| # | 陷阱 | 症状 | 修复 |
|---|------|------|------|
| 1 | **顶点标注不精确** | 标注文字位置偏移，用户认为顶点位置不对 | 用 `ax.scatter()` 先画大红点（s=100+, edgecolors='black'），再用 `ax.annotate()` 配箭头指向该点。箭头偏移量 `xytext` 不要太大（10-20pt足够）。 |
| 2 | **原点有多余标注** | 坐标轴标签 `0` 和用户添加的注释 `O` 或 `(0,0)` 同时出现，用户认为有两个O | 原点处最多只标一个东西：要么刻度标签 `0`（默认），要么手动标注。不要在原点既标 `0` 又标 `(0,0)` 或 `O`。 |
| 3 | **matplotlib 中使用 Unicode/emoji 标题字符** | `Missing character` 警告 — PingFang SC 不含 ✓ ✗ 💪 等字形 | 在标题中用纯文本替代：`✓` → `[是]` 或 `[OK]`，`✗` → `[不是]` 或 `[X]`。在 `ax.set_title()` 中不要用任何 emoji。 |
| 4 | **matplotlib 中使用 Unicode 上标** | ² ³ 等可能在某些字体中缺失或渲染不一致 | 用 `\xb2`（`'y = x\\xb2'`）或 LaTeX 数学模式写法（`'$y = x^2$'`）替代 Unicode ²。优先用前者（无需 LaTeX 解析）。 |
| 5 | **关键点散点图层级被曲线覆盖** | 散点画在曲线下面，用户看不清楚 | 设置 `zorder=5` 确保散点在最上层；加 `edgecolors='black'` 让点有边界，在彩色曲线上也清晰可见。 |
| 6 | **多曲线共用同一张图的标注拥挤** | 标注文字重叠或指向不明 | 每条曲线的关键点用不同颜色散点区分。顶点用大红点（不论曲线颜色）+ 黑边。标注文字用与曲线同色的字体，加 `fontweight='bold'` 增强可读性。 |
| 7 | **`ax.set_aspect('equal')` 被遗忘** | 圆看起来像椭圆，正方形看起来不像正方形 | 几何图（圆、对称关系图、正方形等）必须加上 `ax.set_aspect('equal')`。 |

### 10.5 figure 生成前检查清单

- [ ] 所有 `ax.set_title()` 无 emoji/Unicode 特殊字符
- [ ] 所有 vertex 用 `ax.scatter(..., s=100+, zorder=5, edgecolors='black')` 标记
- [ ] 所有 annotate 文字箭头指向精确位置，偏移量适中
- [ ] 原点处无重复标注（默认刻度 `0` 就够了）
- [ ] 对称关系图/圆等设了 `set_aspect('equal')`
- [ ] 在开发环境中运行脚本无 `Missing character` 警告
- [ ] 每张图在 PDF 中实际插入后，用人体工学检查：标注不拥挤、箭头指向清晰

---

## 十一、编译与验证

### 11.1 编译命令

```bash
brew install tectonic        # 首次
cd project && tectonic book.tex
```

### 11.2 数值验证（每章必须）

- 导数：中心差分 `(f(x+h)-f(x-h))/(2h)`
- 积分：黎曼和 `np.sum(f(x))*dx`
- 级数：部分和
- 微分方程：解代入验证

---

## 十二、定义先于使用原则（2026-07-13 教训）

**在证明中使用任何一个概念之前，必须先给出其形式化定义。**

### 教训来源

写30章数学分析教材时，在ch16有界性定理的证明中使用了"开覆盖"和"有限子覆盖"概念，
但没有在前面章节定义开集、开覆盖。用户发现后质问"为什么不让邻域语言系统化？"
——这是一个本应主动发现和修复的缺口。

### 补救方法

在ch15末尾增加了完整的邻域语言章节，包含：
- ε-邻域 \(U(a,\varepsilon)\) 的定义
- 开集与闭集的定义  
- 开覆盖与有限子覆盖的定义
- 海涅-博雷尔定理

### 检查清单

写严格模式教材时，在设计阶段主动检查三种语言的覆盖：
- [ ] **ε-N 语言**（数列极限，用于序列收敛证明）
- [ ] **ε-δ 语言**（函数极限与连续，用于导数/积分证明）
- [ ] **邻域/开集语言**（开覆盖、紧致性，用于闭区间性质证明）

**规则：不要在教材中使用未定义的术语。** 如果在ch16的证明中要用"开覆盖"概念，
必须先在ch15定义开集、开覆盖、海涅-博雷尔定理。

---

## 十三、交付前检查清单

### 知识层

- [ ] 每章开头有「从上一章来」过渡桥梁？（3-8 行，连接上一章终点与本章起点）
- [ ] 每章结尾有「通往下一章」过渡桥梁？（3-8 行，回答"学会什么→引出什么→下章解决什么"）
- [ ] 每章页数达到目标？严格模式 25-35 页，直觉模式 15-20 页
- [ ] 每章例题 8-12 个？第一个完全展开不跳步
- [ ] 习题 30-40 道，9 级难度全覆盖？
- [ ] 至少 5 幅插图，且在正文中被引用（"如图 X 所示……"）
- [ ] 每章开头有应用引导三问？
- [ ] 所有新符号标注了读法？
- [ ] 每个定义之前有直觉引入？
- [ ] 每节至少 2 道例题？
- [ ] 练习答案放入附录？
- [ ] 检查难度是否符合所选模式？（直觉模式→无 ε-δ；严格模式→ε-N/ε-δ 完整）

### LaTeX 编译检查

可用 `python3 scripts/precompile-fix.py --stats` 快速查看所有章节习题统计。  
批量自动修复三类常见错误：`python3 scripts/precompile-fix.py`（详见该脚本）。

**提交前五查（必做）：**
```
1. 配对检查：\[ vs \]、\( vs \) 计数一致
2. Exercise配对：\begin{exercise} 计数 = \end{exercise} 计数  
3. 习题存在性：grep -c "begin{exercise}" > 0（否则忘记写习题）
4. Examplebox括号：所有 \begin{examplebox}[...] 的右括号是 ] 不是 }
5. 图存在性：\includegraphics 中的PDF文件在 figures/ 下存在
```

```bash
# 1. 数学模式配对（\[  vs  \]）
python3 -c "import glob
for f in ['book.tex']+glob.glob('part*/*.tex')+glob.glob('appendix/*.tex'):
    with open(f) as fh: t=fh.read()
    ob, cb = t.count('\\\\['), t.count('\\\\]')
    if ob!=cb: print(f'{f}: [ {ob} ] {cb} 差 {ob-cb}')"

# 2. exercise 环境配对
python3 -c "import glob
for f in glob.glob('part*/*.tex'):
    with open(f) as fh: t=fh.read()
    b,e=t.count('\\\\begin{exercise}'),t.count('\\\\end{exercise}')
    if b!=e: print(f'{f}: begin={b}, end={e}')"

# 3. examplebox 括号检查（防止 } 误写为 ]）
python3 -c "import glob, re
for f in glob.glob('part*/*.tex'):
    with open(f) as fh:
        for i,l in enumerate(fh,1):
            if re.search(r'\\\\begin\{examplebox\}\[.*?\}', l):
                print(f'{f}:{i}: } 误写 -> {l.rstrip()[:60]}')"

# 4. 习题存在性检查（防止忘记写习题）
python3 -c "import glob
for f in glob.glob('part*/*.tex'):
    with open(f) as fh: t=fh.read()
    cnt = t.count('\\\\begin{exercise}')
    if cnt == 0: print(f'WARNING: {f} 没有习题！')"

# 5. emoji 角色检测
python3 -c "import re,glob
for f in ['book.tex']+glob.glob('step*/*.tex'):
    with open(f) as fh:
        for i,l in enumerate(fh,1):
            if re.search(r'[\\\\U0001F300-\\\\U0001F9FF\\\\u2705]',l): print(f'{f}:{i}')"

# 6. tabular 行末缺 \\\\\\\\ 检测（检查 symbolcard 内非`\\\\`结尾行）
python3 -c "import glob, re
for f in glob.glob('step*/*.tex'):
    with open(f) as fh: t=fh.read()
    in_card=False
    for i,line in enumerate(fh,1):
        if 'begin{symbolcard}' in line: in_card=True; continue
        if 'end{symbolcard}' in line: in_card=False; continue
        if in_card and line.strip() and not line.strip().endswith('\\\\\\\\\\\\\\\\'):
            print(f'{f}:{i}: 缺 \\\\\\\\\\\\\\\\ -> {line.strip()[:40]}')"

# 7. 搜索 \\\\textbf}\\\\textit} 等误写
python3 -c "import glob, re
for f in ['book.tex']+glob.glob('part*/*.tex')+glob.glob('appendix/*.tex'):
    with open(f) as fh:
        for i,l in enumerate(fh,1):
            if re.search(r'\\\\\\\\textbf\\\\}|\\\\\\\\textit\\\\}|\\\\\\\\textsf\\\\}', l):
                print(f'{f}:{i}: \\\\\\\\textbf}}误写 -> {l.rstrip()[:60]}')"
```

---

## 十四、常见编译陷阱

| # | 陷阱 | 症状 | 修复 |
|---|------|------|------|
| 1 | `figure` 在 `tcolorbox` 内 | Not in outer par mode | 去掉 `figure`，裸用 `\\includegraphics` |
| 2 | emoji 在 LaTeX 中 | Missing character | 替换为纯文本或 `[OK]` |
| 3 | `\\\\` 在 `\\[...\\]` 内 | Missing $ inserted | 加 `gathered` 包裹 |
| 4 | `_` 在文本列中 | Missing $ inserted | `$a_n$` 或 `\\ensuremath{}` |
| 5 | `\\times` 在文本模式 | Missing $ inserted | `\\( \\times \\)` |
| 6 | `\\end{exercise}` 遗漏 | 未闭合环境 | grep 计数检查 |
| 7 | **tabular 行末缺 `\\\\`** | Misplaced \\noalign | 每条 tabular 行末必须加 `\\\\`。symbolcard 内容行最常见 |
| 8 | **`\\verb` 定界符与内容冲突** | 编译异常 | 用 `+`/`!` 等不含在内容中的字符做定界符：`\\verb+\\|v\\|+` |
| 9 | **`\\mathbf` 在 tabular 列中** | \\mathbf allowed only in math mode | 确保在 `$...$` 内；`$\\lVert\\mathbf{v}\\rVert$` |
| 10 | **`\\textbf}` 右花括号误写** | 格式错不报错 | 全局搜索 `\\textbf}` → `\\textbf{...}` |
| 11 | **第 1 个 tabular 行少列** | Extra alignment tab | 每行 `&` 数量 = 列数-1 |
| 12 | **symbolcard 内容行间有空行** | Misplaced \\\\noalign | tabular 内不允许空行 |
| 13 | **反引号 `` ` `` 在文本模式** | Missing $ inserted | 用 `\\\\texttt{}` 包裹；`_` 在 `\\\\texttt` 内也须转义 → `\\\\texttt{batch\\\\_size}` |
| 14 | **Unicode 箭头 `→` 在文本模式** | Missing $ inserted | 全部替换为 `$\\to$` |
| 15 | **emoji/Unicode 在 tcolorbox title 中** | Missing character | 纯文本替代：`💪`→`进步`，`✅`→`[OK]`，`📖`→`[卡]` |
| 16 | **✓ ✗ 等 Unicode 符号在 lstlisting 中** | Missing character | 用 `[OK]`/`[X]` 替代 `✓`/`✗`；用 `->` 替代 `→` |
| 17 | **`\\newcases` 不是标准 LaTeX 命令** | Undefined control sequence | 用 `\\begin{cases}` 替代 |
| 18 | **习题区 `\\[` 缺 `\\]` 关闭** | Missing $ inserted 在 `\\end{exercise}` 行 | 在 `\\end{exercise}` 前补 `\\]` |
| 19 | **`\\begin{examplebox}[...}` 方括号闭合成花括号** | `Argument of \\examplebox has an extra }` | 把 `}` 改为 `]` |
| 20 | **连续 `\\begin{exercise}` 缺 `\\end{exercise}`** | 环境计数不匹配 | 每道习题独立闭合 |
| 21 | **忘记写习题部分** | PDF 无习题 | `grep -c "begin{exercise}" partX/*.tex` 确认 > 0 |
| 22 | **`\\blacksquare` 在数学模式外** | `Missing $ inserted` | 改为 `\\(...\\blacksquare\\)` |
| 23 | **`^`/`_` 在 examplebox 标题参数中** | `Missing $ inserted` | `2^n`→`2的n次方`，或加 `{...}` 包裹标题 |
| 24 | **`\\frac` 在 examplebox 标题参数中** | 花括号嵌套误解 | 加 `{...}` 包裹：`\\begin{examplebox}[{含 \\(\\frac{1}{2}\\)}]` |
| 25 | **`\\end{section}` 不存在** | `Undefined control sequence` | 直接删除 |
| 26 | **全角字符 `℃` `：` `【` `】` 在英文字体中** | `Missing character` | `℃`→`°C`；`【`→`[`；`】`→`]` |
| 27 | **`openright` 产生空白页** | PDF 中出现空白页 | 改为 `\\documentclass[...,openany]{...}` |
| 28 | **`\blacksquare` 修复脚本双重嵌套** | `\(\blacksquare\)\)` — 多余 `\)` | 字节级修复；`mathbook-pipeline.py fix mathmode` |
| 29 | **`\]` 在 `\end{cases}`/`\end{aligned}` 之前** | `\begin{cases}...\]...\end{cases}` → `Missing $ inserted` | `\end{cases}` 必须早于 `\]`。正确：`\begin{cases}...\end{cases}\\]` |
| 30 | **`\frac{...]{...}` 花括号混用方括号** | `\frac{dx]{x^2}` → `File ended while scanning \frac` | 全局搜索 `\frac{...]` 确保参数边界是 `{}` 非 `[]` |
### 编译-修复循环（编译报错时工作流）

编译报错后的标准操作：

```
第1步：tectonic book.tex 2>&1 | grep -E "error|Writing"
第2步：如果报错 → 读错误行（grep 行号）
第3步：检查该行及前后2行
第4步：用 patch 修复
第5步：回到第1步
```

**常见修复速查（按频次排序）：**

| 错误信号 | 最可能的原因 | 修复 |
|:---------|:------------|:-----|
| `Argument of \\examplebox has an extra }` | `\begin{examplebox}[...}` 花括号误写 | 把 `}` 改为 `]` |
| `Missing $ inserted` 在 `\end{exercise}` 行 | 习题中 `\[` 缺 `\]` 关闭 | 在 `\end{exercise}` 前补 `\]` |
| `Missing $ inserted` 在 `\begin{examplebox}` 行 | 标题中有 `^`(如 `2^n`) 或 `_` 但没有 `$` 包裹 | 把 `2^n` 改为 `2的n次方`，或在整个标题外套 `{...}` |
| `Missing $ inserted` 在含 `\blacksquare` 行 | `\blacksquare` 在数学模式外 | 改为 `\(...\blacksquare\)` |
| `Paragraph ended before \\@sqrt was complete` | `\sqrt` 没有 `{...}` 或括号配对错 | 检查 `\sqrt` 语法 |
| `Undefined control sequence` | 命令拼写错误或缺少包 | 检查命令名；检查 preamble 是否已加载对应包 |
| `Unable to load picture or PDF file` | 图文件不存在 | 运行 `gen_chXX.py` 生成图后再编译 |

### LaTeX 自动修复脚本（已验证有效）

在遇到大量习题 `\\[` 缺 `\\]`、连续 `\\begin{exercise}` 缺 `\\end{exercise}`、或 `examplebox` 花括号误写时，用以下脚本批量修复：

```bash
# 一键三修：配对检查 + exercise 闭合 + examplebox 括号修复
python3 << 'PYEOF'
import glob, re

for fpath in glob.glob('part*/*.tex'):
    with open(fpath) as f:
        text = f.read()

    changed = False

    # 修复1：examplebox 的 } 误写为 ]
    # 匹配 \begin{examplebox}[...} 模式，把最后一个 } 改为 ]
    fixed1 = re.sub(
        r'(\\\\begin\{examplebox\}\[.*?)\\}',
        r'\1]',
        text
    )
    if fixed1 != text:
        changed = True
        text = fixed1
        print(f'  [括号修复] {fpath}')

    # 修复2：\[ 缺 \] 关闭（在 exercise 内）
    lines = text.split('\n')
    fixed_lines, in_math = [], False
    for line in lines:
        s = line.strip()
        if '\\[' in line and '\\]' not in line:
            if in_math:
                fixed_lines.append('\\]')
            in_math = True
        if '\\]' in line:
            in_math = False
        if in_math and '\\end{exercise}' in s:
            fixed_lines.append('\\]')
            in_math = False
        fixed_lines.append(line)
    if in_math:
        fixed_lines.append('\\]')

    candidate = '\n'.join(fixed_lines)
    if candidate != text:
        changed = True
        text = candidate
        print(f'  [数学模式修复] {fpath}')

    # 修复3：连续 \begin{exercise} 缺 \end{exercise}
    open_count, close_count = text.count('\\\\begin{exercise}'), text.count('\\\\end{exercise}')
    if open_count > close_count:
        # 只在习题区域修复，避免误伤正文中的 exercise 环境
        ex_section = text.find('\\\\section{习题}')
        if ex_section >= 0:
            before = text[:ex_section]
            after = text[ex_section:]
            # 在 after 中，每个 \begin{exercise} 前如果没有 \end{exercise} 就补一个
            ex_lines = after.split('\n')
            fixed_ex, open_pending = [], 0
            for line in ex_lines:
                s = line.strip()
                if '\\\\begin{exercise}' in s:
                    if open_pending > 0:
                        fixed_ex.append('\\\\end{exercise}')
                    open_pending += 1
                if '\\\\end{exercise}' in s:
                    open_pending -= 1
                fixed_ex.append(line)
            while open_pending > 0:
                fixed_ex.append('\\\\end{exercise}')
                open_pending -= 1
            text = before + '\n'.join(fixed_ex)
            changed = True
            print(f'  [exercise闭合] {fpath}')

    if changed:
        with open(fpath, 'w') as f:
            f.write(text)
        print(f'  => 已更新 {fpath}')
    else:
        print(f'  OK {fpath}')
PYEOF
```

---

## 十五、参考资料

- **《自学高数》**（88页/10章/62练习）：`~/zixue-gaoshu/`
- **《数学 for AI》**（199页/72天/3卷/极致平滑）：`~/shuxue-for-ai/`
- `skill:latex-figure-drawing` — matplotlib 绘图
- `skill:math-verification-pipeline` — 数值验证工具链

### 本技能参考文件

- `references/ai-math-project.md` — 《数学 for AI》完整课程设计（124页/5模块/40天）
- `references/mathematical-analysis-outline.md` — 《数学分析基础》30章大纲
- `references/gaoshu-prompt.md` — 系统提示词原文
- `references/project-reference.md` — 《自学高数》项目详情
- `references/strict-mode-proofs.md` — 严格模式 ε-N/ε-δ 证明模板
- `references/mathbook-pipeline.md` — 通用教材自动化管线文档（init/chapter/audit/fix/build/report）
- `scripts/precompile-fix.py` — 预编译修复脚本

### 关联技能

- `skill:epsilon-n-delta-audit` — **严格模式审计层**：写完每章后加载，检查 ε-N/ε-δ 完备性
- `skill:latex-figure-drawing` — matplotlib 矢量图绘制
- `skill:math-verification-pipeline` — 数值验证工具链
- `workspace/math-templates/chapter-cli.py` — `mathkit chapter` 统一入口（new/check/fix/report/pipeline）
