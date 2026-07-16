# 成人数学教材编写工作流

从本会话（2026-07-12）中总结的完整工作流，用于根据用户需求从零开始编写系统化数学教材。

## 触发条件

用户说"从最基础开始教我数学"或类似表述，且：
- 用户自评数学水平低（"数学太烂""学到XX年级就忘了"）
- 用户拒绝聊天式教学（"别这样教我"）
- 用户要求结构化、可保存的教材格式（LaTeX、PDF）

## 工作流

### 第1步：需求诊断

先问清楚三件事（不要一次全抛，先聊出第一件）：
1. **当前水平**：上到几年级？哪部分最虚？
2. **学习目标**：高考？工作？日常够用？
3. **最痛的点**：什么概念一直没搞懂？

用户可能答不上来第3点——此时给一道题试探深浅，或者接受"整体烂"作为有效答案。

### 第2步：设计大纲

- 写成 `大纲.md`，包含：教学理念、章节列表（每章含"本质"概要）、附录说明
- 大纲要覆盖用户声明的起点到终点
- **必经用户确认才能开始写正文**
- 对于多编教材，每编设计要体现**螺旋上升**——同一个概念在不同编中以不同深度反复出现
- 每编的起点是上一编的局限（"第一编处理已知数的运算，第二编处理未知数的推理"）

### 第3步：搭建 LaTeX 环境

```bash
# 安装 TinyTeX（无需 sudo）
curl -sL "https://yihui.org/gh/tinytex/tools/install-unx.sh" | sh

# 配置 PATH
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

# 安装中文支持 + 常用包
tlmgr install ctex listings xcolor geometry titling titlesec fancyhdr hyperref amsmath amssymb amsthm

# 墙内换镜像
tlmgr option repository https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/tlnet/
```

### 第4步：创建目录结构

```
~/math-notes/
├── book.tex            ← 主文件，\include 各章
├── compile.sh          ← 一键编译脚本
├── 大纲.md
├── shared/
│   └── preamble.tex    ← 共用宏包与文档类设定
├── part1/              ← 各编子目录
│   ├── ch01-xxx.tex
│   └── ch02-xxx.tex
├── part2/
│   └── ...
└── appendix/
    └── answers.tex     ← 所有练习答案
```

### 第5步：写前导文件 (preamble.tex)

**必装包：** `ctex listings xcolor geometry titling titlesec fancyhdr hyperref amsmath amssymb amsthm cancel bm`

**文档类：** `ctexbook`（自动中文排版）

**同济版高数排版风格配置：**

```latex
% 公式按节编号
\usepackage{amsmath,amssymb,amsthm}
\usepackage{bm}
\usepackage{cancel}
\numberwithin{equation}{section}
\allowdisplaybreaks

% 定理环境（带颜色：定义蓝 | 定理红 | 命题青绿 | 猜想橙 | 例紫）
\newtheoremstyle{defstyle}
  {3pt}{3pt}{}{}{\color{blue!60!black}\bfseries}{.}{.5em}{}
\newtheoremstyle{thmstyle}
  {3pt}{3pt}{}{}{\color{red!60!black}\bfseries}{.}{.5em}{}
\newtheoremstyle{propstyle}
  {3pt}{3pt}{}{}{\color{teal!70!black}\bfseries}{.}{.5em}{}
\newtheoremstyle{conjstyle}
  {3pt}{3pt}{}{}{\color{orange!70!black}\bfseries}{.}{.5em}{}
\newtheoremstyle{exstyle}
  {3pt}{3pt}{}{}{\color{purple!60!black}\bfseries}{.}{.5em}{}
\newtheoremstyle{exerstyle}
  {3pt}{3pt}{}{}{\bfseries}{.}{.5em}{}

\theoremstyle{defstyle}   \newtheorem{definition}{定义}[chapter]
\theoremstyle{thmstyle}   \newtheorem{theorem}{定理}[chapter]
\theoremstyle{propstyle}  \newtheorem{proposition}{命题}[chapter]
\theoremstyle{conjstyle}  \newtheorem{conjecture}{猜想}[chapter]
\theoremstyle{exstyle}    \newtheorem{example}{例}[chapter]
\theoremstyle{exerstyle}  \newtheorem{exercise}{练习}[chapter]

% 证明环境（同济版风格：黑体"证"，末尾 □）
\renewenvironment{proof}[1][\textbf{证}]%
  {\par\pushQED{\qed}\normalfont\topsep1\parskip\trivlist\item[\hskip\labelsep#1]\ignorespaces}
  {\popQED\endtrivlist\@endpefalse}
```

**页眉页脚（同济版风格）：**

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\thepage}
\fancyhead[RE]{\leftmark}
\fancyhead[LO]{\rightmark}
\fancyhead[RO]{\thepage}
\renewcommand{\chaptermark}[1]{\markboth{第\thechapter 章\quad#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\S\thesection\quad#1}}
```

### 第6步：逐章编写

每章的固定结构见 SKILL.md 中的「章节模板」节。

**编写时的关键规则：**
- 每个符号第一次出现必须标注读法和含义（用户明确反馈过"有些符号我都不会读"）
- 不能跳步——至少展示3~5个中间步骤
- 每个核心概念必须配正式定义框（`\begin{definition}...\end{definition}`）
- 定义框后紧跟"符号说明"小节 + 具体例子
- 练习在题后标注"（答案见附录 \ref{ans:chXX}）"
- 练习答案只放在 `appendix/answers.tex`，不在章内
- 练习按难度分层：基础题（模仿）→ 综合题（推理）

### 第7步：编写答案附录

- 每章对应一个 `\section`，用 `\label{ans:chXX}` 标记
- 每个答案写完整解析过程（不只给最终结果）
- 判断正误时用 `\checkmark`（✅）和 `\times`（❌）

### 第8步：编译

```bash
xelatex -interaction=nonstopmode book.tex   # 第一次，生成 .aux
xelatex -interaction=nonstopmode book.tex   # 第二次，生成目录
```

缺少包时用 `tlmgr install <包名>` 安装，然后重新编译。

### 第9步：交付与迭代

- PDF 文件通过 `MEDIA:/path/to/book.pdf` 交付
- 用户反馈后，做针对性修改

**典型迭代序列（本会话实际发生的顺序）：**

| 迭代 | 用户反馈 | 回应 |
|------|---------|------|
| v1 太啰嗦风格不对 | "别这样教我" | 改输出为结构化的 .tex 文件 |
| v1 繁体中文 | "能不能用简体中文" | `opencc -i file.tex -o file.tex -c t2s.json` 批量转 |
| v2 内容不够细 | "把我水平想得太高了" | 每步加3~5行中间推导，每个符号加读法标注 |
| v3 缺定义 | "之前有定义，现在没了" | 加回 `\begin{definition}` 框，永不删除 |
| v3 答案放错了 | "答案放在最后" | 统一移到 `appendix/answers.tex` |
| v4 题量不够 | "基础题可以多出几题" | 每章6~8题，前2~3道基础+后3~5道综合 |
| v5 要颜色区分 | "定理/定义对应颜色" | 加彩色 theoremstyle（蓝定义/红定理/青命题/橙猜想/紫例子） |
| v6 要排版风格 | "参照同济版高等数学" | 加公式编号、页眉、证明环境 □ |
| v7 要更精美 | "要更加精美一些" | 加 TikZ 示意图（天平模型、数轴）、分步对齐标注、颜色高亮、彩框强调、对比表 |
| — 排版瑕疵 | "600（6 看起来像 6006）" | 数字后跟中文括号要加数学模式隔开，全局排查 |

**关键信号：** 如果用户针对同一个方面提了两次意见（如"内容不够详细""定义不够完整"），说明该方面需要系统性的重写，不是小修补。

**数形结合：** 善用 tikz 画示意图（数轴、长方形分割、坐标系等）。用户称赞过"数形结合方便理解"。一张好图胜过三段文字。但注意 tikz 复杂图不要超过 TeX 的 100 错误限制——嵌套 27 层的 `\ifnum` 链会导致编译崩溃，应改用 `array` 表格代替。

**精美排版技术（用户对第9章提出「要更加精美一些」后验证有效的技术集合）：**

a. **TikZ 示意图**：天平模型（等式平衡）、数轴图（不等式的解集范围）、对比箭头图（正向vs逆向推理）、乘负数变号数轴图、不等式组交集图。注意 tikz 图复杂度——超过 10 条路径或嵌套 `\ifnum` 就会炸编译（见「常见陷阱」表）。

b. **分步对齐标注**：在 `aligned` 环境中，每行末尾用 `\quad &\text{操作说明}` 标注当前步骤：
   ```latex
   \begin{aligned}
   3x + 5 &= 20 \\
   3x &= 20 - 5 \quad &\text{移常数项} \\
   3x &= 15 \\
   x &= 15 \div 3 \quad &\text{除以系数} \\
   x &= 5
   \end{aligned}
   ```

c. **颜色高亮运算操作**：用 `\textcolor{red}{}` 标注当前步骤中发生变化的部分：
   ```latex
   3x + 5 \textcolor{red}{- 5} &= 20 \textcolor{red}{- 5}
   ```

d. **彩框强调关键规则**：用 `\fcolorbox{color}{bgcolor}{\parbox{...}{...}}` 制作醒目提示框：
   ```latex
   \fcolorbox{red!30}{red!10}{\parbox{0.85\textwidth}{\textbf{黄金法则：解完方程后一定检验。}}}
   ```

e. **对比表**：当有多个同类项需要对比时，用 `array` 制作表格。

f. **进步宣言彩框**：每章末尾用 `\fcolorbox{blue!40}{blue!5}` 做「之前只能……现在能……」的能力跃迁宣告。模板见 SKILL.md「信心设计模式—进步宣言彩框」节。

## 常见陷阱

| 陷阱 | 后果 | 避免方法 |
|------|------|---------|
| 删定义框 | 用户要求加回，返工 | 每个核心概念必须有 `\begin{definition}`，永不删除 |
| 答案内联在题后 | 用户要求移到最后 | 统一放在 `appendix/answers.tex` |
| 使用繁体中文 | 用户要求全部转简体 | 写作时直接简体，或写完用 `opencc -i input.tex -o output.tex -c t2s.json` 批量转换 |
| 跳步太多 | 用户看不懂 | 每个代数步骤至少3行中间计算 |
| 符号不注释 | 用户说"不会读" | 每个符号首次出现时标注 `读作「xx」` |
| 聊天式教学 | 用户说"别这样教我" | 一律输出结构化 .tex 文件，不在聊天框里一段段教 |
| 用 ∑ 等高级符号 | 超出用户理解范围 | 初阶内容手动展开为长形式，不要用高阶记号 |
| 在 LaTeX 正文中用 `###` 等 markdown 符号 | 编译报错 `! You can't use 'macro parameter character #'` | LaTeX 中 `#` 是特殊字符。章节标题必须用 `\section`/`\subsection` 等 LaTeX 命令 |
| 数字后紧跟中文左括号 `（` | 排版粘连：`600（6` 看起来像 `6006` | 数字放进数学模式 `\( 600 \)（说明...）`，或在数字和括号之间加空格 |
| tikz 嵌套 `\ifnum` 超限 | `! Extra \fi.` 错误累积到100个后编译停止 | 用 `array` 表格代替 tikz 高密度网格图 |
| 占位章节用 `\\TODO{中文}` | `! Missing $ inserted` / `! You can't use \\spacefactor in vertical mode` | 占位章节用 `% 注释` 代替 `\\TODO{}` |
| TikZ 斜率图刻度/标注拥挤 | 用户 `x=??-1 看不清`，三次纠错 | 刻度 `\\scriptsize`，Δx `midway,above`（在轴上方），`[below]`→`align=center` 精确坐标 |
| TikZ 不等式图解集粗线与轴线重叠 | 绿色粗线与黑色坐标轴在 y=0 处重叠不可见 | 用 `line width=4pt` 画在 y=0 上，红蓝箭头分居 y=±0.35 |
| TikZ 图 Δy 标注被箭头线挡住 | `∆=y 看不清/挡住了` 三次指出 | 用 `node[pos=0.65,right,xshift=4pt]`（偏下+右移），不用 `midway,right` |

## 让学习者

中册大纲加入了一个明确的「信心设计」层，适用于所有需要学习者长期坚持的多章教材。

### 三个设计原则

**原则一：每章结尾有「进步宣言」——「之前只能……现在能……」的明确对比**
每章末尾用彩色方框（`\fcolorbox`）醒目展示学习者的能力跃迁，让ta清晰感知到进步。格式：
```
\subsection*{💪 进步宣言}
\begin{center}
\fcolorbox{blue!40}{blue!5}{\parbox{0.85\textwidth}{\centering\Large
\textbf{之前你只能……（旧能力）}\\[6pt]
\textbf{现在你能……（新能力）}\\[6pt]
\textbf{（跃迁的定性描述——如一维到二维、静态到动态、工具到思想）}
}}
\end{center}
```

**原则二：每章开头从「你已经会的」出发**
不假设读者从零开始。每章开头用2~3句话建立「上一章的终点」和「本章的起点」的桥梁：
- 「第11章的终点：你会在一维数轴上定位一个数的位置」
- 「本章的起点：如果要在二维平面上定位一个点的位置呢？」

**原则三：难度缓坡 + 适时小胜利**
每章内部拆成4~5个小节，每节结束都有一个即时可验证的成果（算出一道题、画出一个图、解决一个实际问题），不让学习者走太远才看到结果。

### 中册各章的进步跃迁

| 章 | 学之前（旧能力） | 学之后（新能力） | 跃迁性质 |
|----|----------------|----------------|---------|
| 11 坐标系 | 一维数轴定位 | 二维平面定位 | 一维→二维 |
| 12 线性函数 | 静态方程关系 | 动态变化描述 | 静态→动态 |
| 13 函数与方程 | 代数求解 | 数形结合 | 算→看 |
| 14 角度与三角形 | 只懂长度 | 懂角度 | 一维→二维空间认识 |
| 15 面积 | 背公式 | 推公式 | 记忆→推理 |
| 16 勾股定理 | 会算面积 | 会证明定理 | 工具→思想 |

### 与螺旋上升结构的协同

信心设计和螺旋上升是同一硬币的两面——螺旋上升保证知识不突兀，信心设计保证学习者感受到自己在进步。在每章小结中，既展示螺旋对照表（概念递进），也展示进步宣言（能力跃迁）。

## 系列教材多卷本结构（上册/中册/下册）

当教材规模超过10章、分属不同编时，应拆分为独立卷本。验证过的组织方式：

### 目录结构

```
~/math-notes-shangce/         ← 独立目录
├── book.tex                  ← 独立主文件
├── compile.sh
├── shared/preamble.tex       ← 样式文件（可复用或复制）
├── part1/ part2/ ...
├── appendix/answers.tex
└── book.pdf

~/math-notes-zhongce/         ← 另一独立目录
├── book.tex                  ← 独立主文件
├── compile.sh
├── shared/preamble.tex       ← 复制上册的preamble（保持风格一致）
├── part3/ part4/
├── appendix/answers.tex
└── book.pdf
```

### 各卷起点设计

每卷的起点是上一卷的终点，让读者感觉没有断档：

- 上册结尾：会代数推理（方程、不等式）
- 中册起点：给代数配可视化工具（坐标系）
- 中册结尾：会用代数推理几何（勾股定理）
- 下册起点：从确定性到不确定性（概率）

卷末设「下册预告」页，用2~3句话预告下一卷核心问题。

## 螺旋上升结构设计（第二编验证的方法论）

当编写多编教材时，每编之间需要逻辑递进。验证过的设计模式：

### 三章关系模板

```
第N章：认识概念（会读、会写、会代入）→ 思维工具的准备
        ↓
第N+1章：用概念求解（逆向推理，唯一解）→ 思维工具的使用
        ↓
第N+2章：解的推广（范围解，无穷概念）→ 思维的扩展
```

### 过渡文模板

每章末尾用 2-3 句自然引出下一章问题：

- **第8章→第9章**："现在你会用字母表达未知量、会代入求值、会合并化简。但所有这些都是'已知 x 求值'——如果反过来，已知 3x+5=20，x 是多少？下一章就学这个：方程。"
- **第9章→第10章**："方程给了你精确求解的能力。但现实世界不总是精确的：一个月至少要赚多少钱？车速不超过多少？这些问题的答案不是一个点，而是一个范围。下一章学不等式。"
- **第10章→第三编**："等式和不等式处理的是静态条件。但真正的世界是动态的：温度随时间变化、利润随销量变化。如何描述变化本身？这就是第三编要解决的。"

### 螺旋对照表

在章节小结中，用表格展示同一个概念在不同章节的深度递进：

| 概念 | 第8章（出现） | 第9章（深化） | 第10章（扩展） |
|------|-------------|--------------|---------------|
| 分配律 | 合并同类项、去括号 | 解方程去括号 | 同方程 |
| 负数 | 负号去括号 | 两边乘除负数 | ⚠️乘负数要变号 |
| 解的数量 | 字母代任意值 | 唯一解 | 范围解 |

这种对照表让读者（和自己）看到知识在"螺旋上升"，而不是简单的重复。

## 参考

- 本会话中第1章重写了两次才达到用户满意的详细度
- 第1章从繁体→简体用了 `opencc -i input.tex -o output.tex -c t2s.json`
- 每次 `.tex` 文件修改后必须重新编译并交付新 PDF
- 第6章的 tikz 筛法图（1~100 质数）嵌套 27 层 `\ifnum` 导致 100 个错误，改为 `array` 表格后解决
