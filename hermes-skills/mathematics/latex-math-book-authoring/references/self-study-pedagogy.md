# 自学教材教学设计原则

本文件为 `latex-math-book-authoring` 技能的教学设计层，提取自 `education-agent-skills` 仓库（GarethManning/education-agent-skills，165 技能/20 领域）中与成人自学数学教材最相关的 5 条研究支撑原则。

---

## 原则1：例题展开渐退（Worked Example Fading）

**来源**：Sweller & Cooper (1985), Atkinson et al. (2000), Renkl (2014), van Merriënboer & Kirschner (2018)

**核心发现**：新手从完全展开的例题直接跳到独立做题，中间缺了关键桥梁。最有效的序列：**完全展开 → 逐步留空 → 独立练习**。渐变从末尾步骤开始，逐步推向中间步骤。

**每章例题按展开度分四级**：

| 序号 | 展开度 | 说明 |
|:----:|:------:|------|
| 例1 | **完全展开** 🔓 | 每步带 WHY 注释 |
| 例2 | **去最后1步** 🔒₁ | 前部步骤全，最后一步留空 |
| 例3 | **去最后2步** 🔒₂ | 留空 20-30% |
| 例4 | **只给开头** 🔒₃ | 仅给出第一步 |
| 例5+ | **完全独立** | 标准练习 |

**渐退方向**：从末尾往开头。末尾是纯计算，中间是方法选择。先去掉机械的，再去掉概念的。

---

## 原则2：渐进提示梯（Progressive Hint Ladder）

**来源**：Aleven et al. (2016), VanLehn (2011)

**核心实现决策：提示必须可隐藏。** 不能把提示嵌入正文，否则学习者不经思考就看到答案。

**四级体系**：

| 级别 | 触发条件 | 内容 |
|:----:|---------|------|
| L1 | 读完题无从下手 | 回顾哪个章节/定义 |
| L2 | 知道概念但选不出方法 | 提醒用哪个定理/公式 |
| L3 | 知道用什么但不知从哪开始 | 给出第一步 |
| L4 | 做了几步卡住了 | 完整解题思路 |

**正确做法（关键教训：正文不放任何引用）**：
1. 新建 `part0/chXX-hints.tex` 存放所有提示
2. `book.tex` 中 `\include{part0/chXX-hints}` 跟在主章节之后
3. 正文习题区**不放任何提示框或引用框**——学习者自己去附录查找
4. 提示框（`hintref` 环境）和行内引用（`参见本章提示附录`）也都不要——第 5 章实战证明这些引用反而让文件臃肿，去掉后更干净

**实施规则**：

| 习题难度 | 提示级别 | 说明 |
|:--------:|:--------:|------|
| 0-2（送分/简单/基础） | 不给 | 应能直接完成 |
| 3（普通） | L2 | 提醒用哪个定理 |
| 4-5（中等/进阶） | L3 + L4 | 第一步 + 完整思路 |
| 6-7（拔高/极难） | L2 + L3 + L4 | 知识点梳理 + 第一步 + 完整思路 |

---

## 原则3：先想后看（Retrieve-First Gate）——可选

**来源**：Roediger & Karpicke (2006), 效应量 \\(d \\approx 0.8\\)

**实现**：每章习题区末尾放 `retrievalgatebox`，三件事：
1. 用一句话说出本章核心概念
2. 有做错的题？找一道同类型、同难度的新题独立做一遍（**不是重做原题**——重做只是默写答案，测不出真理解。做出来 = 真懂了，做不出来 = 没掌握）。
3. 选一道做对的题，讲给想象中的初学者听

**注意**：这条原则是**可选**的。如果加了之后章节显得臃肿，直接删除。第 5 章实战结论：去掉后章节更干净。

---

## 原则4：信心校准（Confidence Calibration）——可选

**来源**：Dunlosky & Rawson (2012)

**核心**：成人自学最大的认知偏差不是"不会"，而是"不知道自己不会"。

**注意事项**：
- 如果使用则每章不超过 2 次：例题渐退中段 + 习题区末尾
- 内容必须极简（2-4 行），直接一句话点出关键
- 这条原则是**可选**的。第 5 章实战结论：去掉后章节更干净，例题渐退和提示附录已足够
- 如果加了显得臃肿，果断删除

---

## 原则5：间隔检索标记（Spaced Retrieval Tagging）

**来源**：Cepeda et al. (2006)

**实现**：习题中标注 `[回顾第N章]`。每章至少 5 道，间隔比：
- 第 N 章回顾第 N-1 章（1 天）
- 第 N 章回顾第 N-2 章（3 天）
- 第 N 章回顾第 N-4 章（7 天）
- 第 N 章回顾第 N-7 章（14 天）

---

## LaTeX 实现

### 环境定义（shared/preamble.tex）

```latex
\newtcolorbox{hintref}{colback=gray!5!white, colframe=gray!40!black,
  arc=2pt, left=4pt, right=4pt, top=3pt, bottom=3pt,
  fonttitle=\small\bfseries, title=提示}
\newtcolorbox{confidencebox}{colback=white, colframe=purple!40!black,
  arc=2pt, left=6pt, right=6pt, top=4pt, bottom=4pt,
  fonttitle=\small\bfseries, title=信心校准}
\newtcolorbox{retrievalgatebox}{colback=white, colframe=orange!60!black,
  arc=2pt, left=6pt, right=6pt, top=4pt, bottom=4pt,
  fonttitle=\small\bfseries, title=先想后看}
```

### 不可踩的坑

- 标题中不用 `[...]` 包裹文字，会被解析为可选参数，产生 `options@for` 乱码
- 标题和框中不用 emoji（💡、🎯、⚠️）和 Unicode 特殊字符（□、∴）——Times New Roman 不含这些字形
- 框体文字简洁（2-6 行），不宜长篇大论

### 提示附录文件模板

```latex
% part0/chXX-hints.tex
\section{第X章习题提示}
需要提示时再查阅。先尝试独立完成，卡住后逐级查看。

\subsection*{练习N（难度4）}
\textbf{L2 提醒：} ......

\subsection*{练习M（难度6）}
\textbf{L3 第一步：} ......\\
\textbf{L4 完整思路：} ......
```

---

## 落地优先级

| 优先级 | 原则 | 改动量 | 效果 |
|:------:|------|:------:|:----:|
| 第一 | 例题展开渐退 | 需改写例题序列 | 最大 |
| 第二 | 渐进提示梯 | 创建 hints.tex + 习题区加 1 行引用 | 大幅降低放弃率 |
| 第三 | 先想后看 | 每章加一个框 | 几乎零成本 |
| 第四 | 信心校准 | 每章加两个框 | 几乎零成本 |
| 第五 | 间隔检索标记 | 习题加标记 | 需前期规划 |

## 参考文献

- Sweller & Cooper (1985). *Cognition and Instruction*, 2(1), 59–89.
- Atkinson et al. (2000). *Review of Educational Research*, 70(2), 181–214.
- Renkl (2014). *Cognitive Science*, 38(1), 1–37.
- Roediger & Karpicke (2006). *Psychological Science*, 17(3), 249–255.
- Cepeda et al. (2006). *Psychological Bulletin*, 132(3), 354–380.
- Wood, Bruner & Ross (1976). *Journal of Child Psychology and Psychiatry*, 17(2), 89–100.
