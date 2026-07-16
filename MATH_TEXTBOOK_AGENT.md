# 📘 MATH_TEXTBOOK_AGENT.md — 数学教材通用编写 Agent 指令集

让 Claude Code、Codex CLI 或其他 LLM Agent 自动化完成数学教材编写。

> 作者：xielunwen（数学分析基础项目）
> 版本：2.0

---

## 目录

1. [前置环境依赖](#1-前置环境依赖)
2. [项目结构](#2-项目结构)
3. [工具集清单](#3-工具集清单)
4. [Claude Code 使用说明](#4-claude-code-使用说明)
5. [Codex CLI 使用说明](#5-codex-cli-使用说明)
6. [管线命令速查](#6-管线命令速查)
7. [审计域说明](#7-审计域说明)
8. [修复层说明](#8-修复层说明)
9. [编写规范](#9-编写规范)
10. [故障排除](#10-故障排除)

---

## 1. 前置环境依赖

### 1.1 硬件要求

- macOS / Linux / Windows（WSL）
- 内存 ≥ 4GB（编译全书约需 2GB）
- 磁盘空闲 ≥ 500MB（含 LaTeX 宏包）

### 1.2 核心依赖

| 依赖 | 版本要求 | 安装命令 |
|:-----|:---------|:---------|
| Python | ≥ 3.10 | `python3 --version` 检查 |
| tectonic | ≥ 0.12 | `brew install tectonic`（macOS）或 [官网](https://tectonic.newton.systems/) |
| Git | ≥ 2.30 | `brew install git` / `apt install git` |
| matplotlib | ≥ 3.7 | `pip3 install matplotlib`（矢量图生成） |

### 1.3 可选依赖

| 依赖 | 用途 | 安装命令 |
|:-----|:-----|:---------|
| numpy | 数值计算 | `pip3 install numpy` |
| sympy | 符号推导验证 | `pip3 install sympy` |
| scipy | 科学计算 | `pip3 install scipy` |

### 1.4 环境验证

```bash
# 验证全部依赖
python3 -c "
import sys, subprocess
assert sys.version_info >= (3,10), 'Python >= 3.10  required'
r = subprocess.run(['tectonic', '--version'], capture_output=True, text=True)
assert r.returncode == 0, 'tectonic required'
print('✅ all dependencies met')
"
```

---

## 2. 项目结构

```
math-analysis/                      # 教材根目录（可改名）
├── book.tex                        # 主文件（手动编辑）
├── mathbook-pipeline.py            # ⭐ 自动化管线（核心工具）
├── MATH_TEXTBOOK_AGENT.md          # 本文件（Agent 读取此文件）
├── README.md                       # 项目说明
├── LICENSE                         # MIT
├── .gitignore
├── shared/preamble.tex             # LaTeX 导言区（颜色、定理环境）
├── part0/ ~ part5/                 # 6编 × 30 个 .tex 文件
│   ├── ch01-function-concept.tex
│   ├── ch02-function-graph.tex
│   └── ...
├── figures/                        # 矢量图（.pdf + gen_ch*.py 生成脚本）
└── appendix/                       # 习题答案
```

### 编目对应

| 目录 | 章节范围 | 主题 |
|:----|:---------|:-----|
| part0/ | ch01–ch08 | 函数基础重建 |
| part1/ | ch09–ch12 | 数列极限 |
| part2/ | ch13–ch16 | 函数极限与连续 |
| part3/ | ch17–ch21 | 导数与微分 |
| part4/ | ch22–ch25 | 黎曼积分 |
| part5/ | ch26–ch30 | 进阶与拔高 |

---

## 3. 工具集清单

### 3.1 管线工具：`mathbook-pipeline.py`

```
┌─────────────────────────────────────────────────────┐
│                 mathbook-pipeline.py                 │
├──────────┬──────────┬──────────┬──────────┬──────────┤
│  init    │ chapter  │  audit   │   fix    │  build   │
│ 初始化   │ 创建/管理  │  审计    │  修复    │  编译    │
├──────────┴──────────┼──────────┼──────────┴──────────┤
│     领域无关核心     │ 可插拔域  │   分层修复层         │
│  - 项目骨架          │ - structural │ - syntax         │
│  - 章节骨架          │ - analysis  │ - pairing        │
│  - 图脚本骨架        │ - topology  │ - unicode        │
│  - book.tex 管理     │ - algebra   │ - mathmode       │
└─────────────────────┴──────────┴─────────────────────┘
```

### 3.2 调用方式

```bash
# 方法 A：直接 Python 调用
python3 mathbook-pipeline.py init "新教材"
python3 mathbook-pipeline.py chapter new ch01 "章节标题"
python3 mathbook-pipeline.py audit
python3 mathbook-pipeline.py fix
python3 mathbook-pipeline.py build

# 方法 B：通过 mathkit（Hermes Agent 环境）
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
mathkit pipeline init "新教材"
mathkit pipeline audit analysis
mathkit pipeline build

# 方法 C：通过 Agent（Claude Code / Codex CLI）
# 见第 4、5 节
```

### 3.3 Hermes Agent Profile 集成

如果使用 Hermes Agent，完整 profile 位于：
```
~/.hermes/profiles/xiandaishuxuejia/
├── .venv/bin/mathkit             # 启动器
├── workspace/math-templates/     # 模板工具
│   ├── mathbook-pipeline.py
│   ├── numerical-check.py
│   └── symbolic-check.py
├── skills/mathematics/
│   ├── latex-math-book-authoring/  # 教材编写主流程 skill
│   └── epsilon-n-delta-audit/     # ε-N/ε-δ 审计 skill
└── agents/MATH_TEXTBOOK_AGENT.md  # 本文件
```

---

## 4. Claude Code 使用说明

### 4.1 初始化

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 进入项目目录
cd ~/math-analysis

# 启动 Claude Code 并加载 agent 指令
claude-code --context MATH_TEXTBOOK_AGENT.md
```

### 4.2 常见指令

进入 Claude Code REPL 后，直接说中文指令：

```
# 创建新章
「创建第31章《多元函数微分学》」
→ 自动调用 python3 mathbook-pipeline.py chapter new ch31 "多元函数微分学"

# 审计
「审计第31章」
→ python3 mathbook-pipeline.py audit ch31

# 修复
「修复第31章语法错误」
→ python3 mathbook-pipeline.py fix syntax ch31

# 编译
「编译全书」
→ python3 mathbook-pipeline.py build

# 批量管线
「从31章写到35章」
→ python3 mathbook-pipeline.py pipeline ch31 ch35
```

### 4.3 编写章节的标准提示词

```
「写第31章《多元函数微分学》。要求：
1. 从第30章过渡，先讲直观再给定义
2. 8-12个例题，第一个完全展开不跳步
3. 包含定义框、定理框、符号卡片
4. 30道习题（送分4+简单4+基础4+普通5+中等5+进阶4+拔高3+极难1）
5. 本章小结 + 通往下一章
6. 用 ε-δ 语言给出偏导数的严格定义」
```

---

## 5. Codex CLI 使用说明

### 5.1 初始化

```bash
# 安装 Codex CLI
# 详见 https://github.com/openai/codex

# 进入项目目录
cd ~/math-analysis

# 启动 Codex
codex run --instructions MATH_TEXTBOOK_AGENT.md
```

### 5.2 常用指令

进入 Codex CLI 后：

```
# 创建章节
Create chapter 31 "多元函数微分学" using the pipeline tool:
python3 mathbook-pipeline.py chapter new ch31 "多元函数微分学"

# 审计
Run mathbook-pipeline.py audit ch31

# 修复
Run mathbook-pipeline.py fix all

# 编译全书
Run mathbook-pipeline.py build
```

### 5.3 .cursorrules 集成

在项目根目录创建 `.cursorrules`（Cursor IDE 用户）：

```
你正在使用 mathbook-pipeline.py 自动化管线。
- 创建章节用: python3 mathbook-pipeline.py chapter new <id> "<标题>"
- 审计用: python3 mathbook-pipeline.py audit [id]
- 修复用: python3 mathbook-pipeline.py fix <layer> [id]
- 编译用: python3 mathbook-pipeline.py build
每章需包含：应用引导 → 核心内容(8-12例题) → 符号卡片 → 代码验证 → 小结 → 30道习题
```

---

## 6. 管线命令速查

### 6.1 子命令一览

| 命令 | 功能 | 示例 |
|:-----|:-----|:------|
| `init` | 初始化新教材项目 | `python3 mathbook-pipeline.py init "实分析"` |
| `chapter new` | 创建新章骨架 | `python3 mathbook-pipeline.py chapter new ch31 "多元函数"` |
| `chapter add` | 加入 book.tex | `python3 mathbook-pipeline.py chapter add ch31` |
| `chapter list` | 列出已有章节 | `python3 mathbook-pipeline.py chapter list` |
| `audit` | 全面审计 | `python3 mathbook-pipeline.py audit` |
| `fix` | 自动修复 | `python3 mathbook-pipeline.py fix all` |
| `build` | 编译全书 | `python3 mathbook-pipeline.py build` |
| `report` | 量化报告 | `python3 mathbook-pipeline.py report` |
| `pipeline` | 批量管线 | `python3 mathbook-pipeline.py pipeline ch31 ch35` |

### 6.2 完整工作流

```bash
# 第1步：初始化
python3 mathbook-pipeline.py init "数学分析基础"

# 第2步：创建章节
python3 mathbook-pipeline.py chapter new ch01 "函数的概念"

# 第3步：手动编写 .tex 文件内容（8-12个例题，30道习题）

# 第4步：生成矢量图
python3 figures/gen_ch01.py

# 第5步：审计
python3 mathbook-pipeline.py audit ch01

# 第6步：修复（如果需要）
python3 mathbook-pipeline.py fix all ch01

# 第7步：编译
python3 mathbook-pipeline.py build

# 第8步：批量（多章连续）
python3 mathbook-pipeline.py pipeline ch01 ch05
```

---

## 7. 审计域说明

设置领域通过环境变量 `MATHBOOK_DOMAIN` 或项目根目录 `.mathbook.yml`：

```yaml
# .mathbook.yml
title: 实分析
domain: analysis  # structural | analysis | topology | algebra | number-theory
```

### 审计内容

| 审计域 | 领域 | 检查内容 |
|:-------|:-----|:---------|
| `structural` | **通用**（默认） | 环境配对、数学模式、Unicode 毒瘤、编译检查 |
| `analysis` | **数学分析** | ε-N/ε-δ 追踪、极限/连续/导数/积分定义完备性 |
| `topology` | **拓扑学** | 开集/闭集/紧致/连通/度量定义完备性 |
| `algebra` | **代数学** | 群/环/域/同态/同构定义完备性 |
| `number-theory` | **数论** | 素数/ζ函数/L函数/渐进公式完备性 |

### 添加新审计域

在 `mathbook-pipeline.py` 中添加：

```python
def _my_domain_audit(files):
    for fp in files:
        # 对每个 .tex 文件做领域特定的关键词检查
    return fail_count  # 返回失败数

AUDIT_DOMAINS['my-domain'] = ('我的领域', _my_domain_audit)
```

---

## 8. 修复层说明

| 修复层 | 修复内容 | 安全级别 |
|:-------|:---------|:---------|
| `syntax` | `\begin{examplebox}[...}` 花括号错、`\end{examplebox]` 方括号错 | ✅ 安全 |
| `pairing` | 连续 `\begin{exercise}` 缺 `\end{exercise}`、`\[` 缺 `\]` | ✅ 安全 |
| `unicode` | `→` `✓` `✗` `【` `】` `℃` 等 Unicode 替换为 LaTeX 兼容形式 | ⚠️ 可能改变显示 |
| `mathmode` | `\blacksquare` 不在数学模式内、孪生 `\(\(` `\)\)` 修复 | ✅ 安全 |
| `all` | 以上全部 | ✅ |

---

## 9. 编写规范

### 9.1 每章结构

```
┌─ 应用引导 ──────────────────────────────┐
│  \begin{applicationbox}                 │
│  学完本章你能做什么？                    │
│  \end{applicationbox}                  │
├─ 核心内容 ──────────────────────────────┤
│  ↓ 直觉引入 → 定义框 → 例题(8-12) → 图 │
├─ 符号卡片 ──────────────────────────────┤
│  \begin{symbolcard} 新符号注音          │
├─ 代码验证 ──────────────────────────────┤
│  \begin{lstlisting} Python 代码         │
├─ 本章小结 ──────────────────────────────┤
│  进步宣言 + 通往下一章                   │
├─ 习题 ──────────────────────────────────┤
│  30道 / 9级难度（送分→极难）            │
└─────────────────────────────────────────┘
```

### 9.2 习题难度分布

| 难度 | 级别代码 | 题量 |
|:-----|:--------|:----:|
| 送分 | `[0]` | 4 |
| 简单 | `[1]` | 4 |
| 基础 | `[2]` | 4 |
| 普通 | `[3]` | 5 |
| 中等 | `[4]` | 5 |
| 进阶 | `[5]` | 4 |
| 拔高 | `[6]` | 3 |
| 极难 | `[7]` | 1 |

### 9.3 LaTeX 陷阱（禁止清单）

```
❌ \begin{examplebox}[...}     → 花括号应为方括号 ]
❌ \blacksquare 在数学模式外    → 用 \(\blacksquare\)
❌ 连续 \begin{exercise} 缺 end → 每个 begin 对应一个 end
❌ \end{section}                → 不存在此命令
❌ \verb 在 tabular/symbolcard  → 用 \texttt 替代
❌ openright                    → 用 openany（防空白页）
❌ → ✓ ✗ 【】℃ 等 Unicode     → 用 LaTeX 命令或纯文本替代
❌ [\frac{...]{...}]            → ] 先于 } 结束 \frac 参数
❌ ^ _ 在 examplebox 标题中      → 简化标题或用 {} 包裹
```

### 9.4 交付前自检

```
1. 环境配对？     （所有 \begin{xxx} 的计数 == \end{xxx}）
2. 数学模式配对？  （\( vs \)、\[ vs \] 计数一致）
3. 无 Unicode 毒瘤？（→✓✗【】℃ 全部替换）
4. 无跳步词？     （"显然""易证""篇幅所限" 应为 0）
5. 习题已补？     （\begin{exercise} 计数 == 30）
```

---

## 10. 故障排除

### 10.1 编译错误速查

| 错误信息 | 原因 | 修复 |
|:---------|:-----|:-----|
| `Missing $ inserted` | 数学模式没有正确关闭 | 检查 `\[` 和 `\]` 配对 |
| `Argument of \examplebox has an extra }` | `\begin{examplebox}[...}` 花括号误写 | 把 `}` 改为 `]` |
| `File ended while scanning use of \frac` | `\frac` 缺少参数 | 检查 `\frac{...}{...}` 花括号 |
| `Paragraph ended before \end was complete` | 环境缺少结束标签 | 检查 `\end{xxx}` |
| `Bad math environment delimiter` | 数学模式嵌套错误 | 检查 `\(` 和 `\)` 嵌套 |

### 10.2 自动修复

```bash
# 一键修复全部已知问题
python3 mathbook-pipeline.py fix all

# 编译后如果还有错误，逐层修复
python3 mathbook-pipeline.py fix syntax
python3 mathbook-pipeline.py build
# 如果还有错误
python3 mathbook-pipeline.py fix pairing
python3 mathbook-pipeline.py build
```

### 10.3 已知问题

- Unicode 字符 `℃` `：` 在 Times New Roman 字体中缺失（编译警告，不影响输出）
- 第0编部分章节的历史 `\]/end{cases}` 排序问题已修复
- 附录习题答案尚未填写
