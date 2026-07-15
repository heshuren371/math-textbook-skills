# Changelog

## 2026-07-15 — 自学教学设计升级

### `latex-math-book-authoring` 📘 **核心教材编写** — 828→957 行 (+129)

**描述更新：** 改为中英双语描述，明确与 `latex-figure-drawing`（制图）和 `math-output-format`（格式）的职责边界。

**新增自学教学设计体系：**
- **前置知识模块** — 第1章必修插入「集合、数集与区间」，解决函数定义依赖集合概念但读者可能零基础的问题
- **例题渐退序列（Fading Scaffolding）** — 🔓 完全展开 → 🔒₁ 去最后1步 → 🔒₂ 去最后2步 → 🔒₃ 只给第一步 → 独立完成
- **信心校准框** — 每道例题后让学生自评信心等级（≥90%/60-89%/<60%），翻答案后比对
- **先想后看门禁** — 习题与答案之间加检索门禁，鼓励自学者先尝试不看答案
- **跨章回顾标记** — 习题区标注 `[回顾第N-1章]`，强制间隔检索

**新增 LaTeX 环境：** `hintref`（渐进提示框）、`confidencebox`（信心校准）、`retrievalgatebox`（先想后看）— 均为自学教学设计服务

**新增参考文件：**

| 文件 | 大小 | 内容 |
|------|------|------|
| `self-study-pedagogy.md` | 6.3KB | 自学教学设计原则（提取自 education-agent-skills 仓库 165 技能） |
| `chapter-pedagogy-upgrade.md` | 7.7KB | 章节教学升级工作流（第4章指数函数实战验证） |
| `external-skill-evaluation.md` | 2.8KB | 外部 6 个数学 skill 评估结论：均不需要集成 |
| `20260713-full-book-lessons.md` | 2.7KB | 全书写完教训：ε-N/ε-δ 证明遗漏、段落长度控制 |
| `chinese-in-math-mode-fix.md` | 2.2KB | 中文在数学模式内未用 `\text{}` 的修复记录 |

### `latex-figure-drawing` 📊 **矢量图绘制** — 修改描述

**描述更新：** 改为中英双语。

### `math-output-format` 📐 **数学格式规范** — 修改描述

**描述更新：** 改为中英双语。

### `math-review` 🔍 **数学审查** — 1051→1052 行

**描述更新：** 改为中英双语，明确与 `scientific-figure-making`（制图）和 `triangle-verification-team`（多Agent验证）的职责边界。

**新增 `kde-1d` 工具：** `utils_kde.py`（独立 KDE 核密度估计，Silverman 高斯核，无需 scipy）

### `math-verification-pipeline` 🔬 **数学验证管线** — 修改描述

**描述更新：** 改为中英双语。
