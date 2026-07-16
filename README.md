# 数学分析基础

从函数重建到严格分析的完整中文教材。**30 章，257 页，900+ 习题，57 幅矢量图。**

覆盖 ε-N 语言、ε-δ 语言、邻域语言三种分析语言。内建自动化编写管线，支持 Claude Code / Codex CLI 辅助编写。

## 内容结构

| 编 | 主题 | 章节 | 核心内容 |
|:---|:-----|:----|:---------|
| 第〇编 | 函数基础重建 | ch01–ch08 | 函数概念、图像、幂/指数/对数/三角函数、性质 |
| 第一编 | 数列极限 | ch09–ch12 | 数列、极限直观、**ε-N 严格定义**、判别法 |
| 第二编 | 函数极限与连续 | ch13–ch16 | 无穷极限、**ε-δ 严格定义**、连续、闭区间性质 |
| 第三编 | 导数与微分 | ch17–ch21 | 导数、求导法则、MVT、泰勒/洛必达、应用 |
| 第四编 | 黎曼积分 | ch22–ch25 | 定积分、FTC、积分法、广义积分 |
| 第五编 | 进阶与拔高 | ch26–ch30 | 级数、判别法、幂级数、傅里叶、多元微分 |

### 三种分析语言

全书系统覆盖数学分析的三种形式语言：

1. **ε-N 语言**（第11章）：数列极限的严格定义
2. **ε-δ 语言**（第14章）：函数极限的严格定义
3. **邻域语言**（第15章）：开集、开覆盖、海涅-博雷尔定理

每个关键定理均配有 ε-N/ε-δ 严格证明（洛必达法则、泰勒定理、黎曼可积、FTC、比较判别法、柯西-阿达马、Clairaut 等 16 个定理）。

### 习题体系

每章 30 道习题，9 级难度体系：送分 → 简单 → 基础 → 普通 → 中等 → 进阶 → 拔高 → 极难（无竞赛题）。

## 安装与编译

### 前置要求

```bash
# macOS（推荐）
brew install tectonic

# Linux（Ubuntu/Debian）
sudo apt install texlive-full   # 或使用 tectonic
# 或
# curl -fsSL https://tectonic.newton.systems/install | bash

# Windows
# 下载 tectonic 安装包: https://tectonic.newton.systems/download
```

### 编译全书

```bash
git clone https://github.com/heshuren/math-analysis.git
cd math-analysis
tectonic book.tex
```

编译产物为 `book.pdf`。首次编译需下载字体和宏包，约需 1-3 分钟。

### 仅编译单章（调试用）

```bash
# 方法1：修改 book.tex，只保留需要的 \include{...}
# 方法2：用管线工具
python3 mathbook-pipeline.py build
```

## 自动化管线

项目内置 `mathbook-pipeline.py`，提供教材编写全流程自动化：

```bash
# 初始化新教材项目
python3 mathbook-pipeline.py init "新教材名称"

# 创建新章
python3 mathbook-pipeline.py chapter new ch01 "章节标题"

# 全面审计（结构 + 领域特定检查）
python3 mathbook-pipeline.py audit structural     # 通用结构审计
python3 mathbook-pipeline.py audit analysis       # ε-N/ε-δ 审计

# 自动修复
python3 mathbook-pipeline.py fix syntax           # LaTeX 语法修复
python3 mathbook-pipeline.py fix pairing          # 环境配对修复
python3 mathbook-pipeline.py fix unicode          # Unicode 字符修复
python3 mathbook-pipeline.py fix all              # 全量修复

# 编译
python3 mathbook-pipeline.py build
```

### 与 AI Agent 配合

项目包含 `MATH_TEXTBOOK_AGENT.md`，可直接供 Claude Code / Codex CLI 使用：

```bash
# Claude Code
claude-code --context MATH_TEXTBOOK_AGENT.md

# Codex CLI
codex run --instructions MATH_TEXTBOOK_AGENT.md
```

### 其他领域

管线支持可插拔审计域。设置环境变量切换领域：

```bash
MATHBOOK_DOMAIN=topology python3 mathbook-pipeline.py audit
MATHBOOK_DOMAIN=algebra  python3 mathbook-pipeline.py audit
MATHBOOK_DOMAIN=number-theory python3 mathbook-pipeline.py audit
```

## 项目结构

```
math-analysis/
├── book.tex                        # 主文件（6编30章）
├── book.pdf                        # 编译结果
├── mathbook-pipeline.py            # ⭐ 通用教材自动化管线
├── MATH_TEXTBOOK_AGENT.md          # Claude Code / Codex 指令
├── README.md                       # 本文件
├── LICENSE                         # MIT
├── .gitignore
├── shared/preamble.tex             # LaTeX 导言区
├── part0/ ~ part5/                 # 6编 × 30 个 .tex 文件
├── figures/                        # 57 张矢量图 + 16 个生成脚本
└── appendix/                       # 习题答案（编写中）
└── hermes-skills/                   # 现代数学家的 Hermes Skills
    └── mathematics/
        ├── latex-math-book-authoring/   # 📘 LaTeX 数学教材编写
        ├── latex-figure-drawing/        # 📊 LaTeX 矢量图绘制
        ├── math-output-format/          # 📐 数学解答输出格式
        ├── math-verification-pipeline/  # 🔬 数学验证管线
        ├── math-review/                 # 🔍 数学审查
        └── epsilon-n-delta-audit/       # ε-δ 审计清单
```

## Hermes Skills（给 AI Agent 的数学能力）

此仓库包含**现代数学家 📐** 的完整 Hermes Skills 集，可直接供 Hermes Agent / Claude Code / Codex CLI 使用。

| Skill | 行数 | 说明 |
|-------|------|------|
| **`latex-math-book-authoring`** | 957 行 | 🔥 教材全流程：读者画像→认知依赖图→元认知设计→大纲→撰写→矢量图→验证→编译 |
| **`latex-figure-drawing`** | 572 行 | Python + matplotlib 生成精确数学矢量图，替代手写 TikZ |
| **`math-output-format`** | 708 行 | 数学解答输出规范、SymPy/Z3 验证、TinyTeX 编译 |
| **`math-verification-pipeline`** | 563 行 | 数学验证管线：WolframScript、蒙特卡洛、对抗博弈分析 |
| **`math-review`** | 1,052 行 | 数学审查：高考压轴题、几何证明、参数不等式深度分析 |
| **`epsilon-n-delta-audit`** | 120+ 行 | ε-N/ε-δ 严格证明审计清单 |

### 安装到 Hermes Agent

```bash
# 克隆仓库
git clone https://github.com/heshuren371/math-textbook-skills.git

# 复制到你的 Hermes Agent 技能目录
cp -r math-textbook-skills/hermes-skills/* ~/.hermes/profiles/your-profile/skills/
```

### 单独使用 Skill

每个 SKILL.md 可单独作为 Claude Code / Codex CLI 的 instructions 文件加载。

```bash
claude-code --context hermes-skills/mathematics/latex-math-book-authoring/SKILL.md
```

## 许可证

MIT License。可自由使用、修改、分发。

## 贡献

欢迎提交 Issue 和 PR。当前已知可改进项：
- 附录习题答案尚未完成
- 第0编（函数基础重建）部分章节存在 Unicode 字符兼容性问题
- 矢量图生成脚本可统一为单入口
