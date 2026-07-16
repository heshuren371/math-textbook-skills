---
name: epsilon-n-delta-audit
description: 🔴 数学分析教材交付强制审计——ε-N/ε-δ 完备性 + 今日全部教训
emoji: 🔴
---

# 🔴 数学分析交付强制审计清单

> **血泪教训：** 2026-07-13 交付30章数学分析教材，遗漏了大量 ε-N/ε-δ 严格证明。
> 原因是赶进度犯了10类错误。此 skill 编码全部教训，每次写数学分析内容前必须加载。
>
> **2026-07-13 更新：自动化管线已就位。**
> 在教材项目根目录运行 `python3 mathbook-pipeline.py audit analysis` 即可自动扫描全书 ε 缺陷。
> 并用 `python3 mathbook-pipeline.py fix all` 自动修复常见错误。

## 何时加载

**每次写数学分析/严格微积分教材的新章节前。** 先 `skill_view(name='epsilon-n-delta-audit')` 看完清单再动笔。
写完一章后再次加载逐条检查。**不检查就交付 = 等着返工。**

---

## 🅰 致命错误：ε-N/ε-δ 证明缺失

### A1. 每个 `\lim` 必须有 ε 追踪

**铁律：** 不能只写 `\lim_{x\to a} f(x) = L` 就跳过。每个 `\lim` 符号在全书范围内至少有一处对应的 ε 定义。全部 `\lim` 追踪到第11章（数列 ε-N）或第14章（函数 ε-δ）。

### A2. 第3-5编关键定理的 ε-δ 证明清单

| 章节 | 定理 | 必须给出 ε-δ 证明？ |
|:----|:-----|:----------------:|
| ch17 | 导数定义 lim_{h→0} | ✅ 至少一个 example 展开 |
| ch18 | 乘法法则、链式法则 | ✅ 定义推导 |
| ch19 | 罗尔/拉格朗日/柯西 MVT | ✅ 辅助函数+极值 ε 论证 |
| ch20 | 洛必达法则 | ✅ 柯西 MVT 证明 |
| ch20 | 泰勒定理+拉格朗日余项 | ✅ 证明框架 |
| ch22 | 黎曼和极限 | ✅ ε-δ 定义 |
| ch22 | 连续⇒可积 | ✅ 一致连续+达布上下和 |
| ch23 | FTC 证明（上限函数求导） | ✅ 积分中值+ε-δ |
| ch25 | 广义积分比较判别法 | ✅ ε-N 柯西准则 |
| ch26 | 级数收敛定义 | ✅ ε-N 部分和柯西 |
| ch26-27 | 比较/比值/积分判别法 | ✅ ε-N 证明 |
| ch28 | 收敛半径（柯西-阿达马） | ✅ ε-N 根值法 |
| ch29 | 傅里叶收敛定理 | ✅ 狄利克雷核+ε 拆分 |
| ch30 | 混合偏导相等（Clairaut） | ✅ ε-δ 中值定理证明 |

**凡此表中有遗漏 → 立即补全。**

### A3. 反例自检

对每个 ε-N/ε-δ 证明：
- 取 ε = 0.1，手动算一遍对应的 N 或 δ
- 取 ε = 0.0001 再算一遍
- 确认 "ε 越小，N/δ 的表达式确实给出更大的 N/更小的 δ"

---

## 🅱 LaTeX 编译陷阱

### B1. `\begin{examplebox}[...]` 参数中 `}` 误写为 `]`
```
❌ \begin{examplebox}[标题内容}
✅ \begin{examplebox}[标题内容]
```

### B2. examplebox 标题中禁止 `^` `_` `\frac`
```
❌ \begin{examplebox}[证明 1/2^n → 0]    # ^ 触发数学模式
✅ \begin{examplebox}[证明 1/2的n次方 趋于 0]
```

### B3. `\blacksquare` 必须在数学模式内
```
❌ 所以 \lim a_n = 0。\blacksquare
✅ 所以 \(\displaystyle \lim a_n = 0\quad\blacksquare\)
```

### B4. 连续 `\begin{exercise}` 缺 `\end{exercise}`
每个 `\begin{exercise}` 必须有对应的 `\end{exercise}`。

### B5. `\end{section}` 不存在 — 不要写

### B6. `\verb` 在 tabular / symbolcard 中不稳定
用 `\texttt{\textbackslash name}` 替代。

### B7. 空白页 — 使用 `openany` 而非 `openright`

### B8. Unicode 字符
`→` → `\to`，`✓` → `[OK]`，`✗` → `[X]`，`【】` → `[]`，`℃` → `°C`

### B9. `\]` 与 `\end{cases}` / `\end{definitionbox}` 的顺序 ⭐（最隐蔽）
```
# ❌ 错误：数学环境在 \] 之后才关闭
\[
\begin{cases}
...
\]
\end{cases}

# ✅ 正确：cases 在 \] 之前关闭
\[
\begin{cases}
...
\end{cases}
\]

# ❌ 错误：box 环境在 \] 之前关闭
\[
...
\]
\end{definitionbox}

# ✅ 正确：box 在 \] 之后关闭
\[
...
\]
\end{definitionbox}
```
**规则：** math-only 环境（`cases`, `aligned`, `pmatrix`, `array`）的 `\end{xxx}` 必须在 `\]` 之前。
tcolorbox 环境（`definitionbox`, `examplebox`, `theorembox`）和 `exercise` 的 `\end{xxx}` 必须在 `\]` 之后。
违反此规则的症状是 `Missing $ inserted` 或 `Bad math environment delimiter`。

---

## 🅲 流程教训

### C1. 写完正文后立即补30道习题（不可转头做别的）

习题配比：送分4 + 简单4 + 基础4 + 普通5 + 中等5 + 进阶4 + 拔高3 + 极难1 = 30

### C2. 编译检查顺序
```
□ 写正文 → □ 补习题 → □ 环境配对 → □ \[配对 → □ \(配对
→ □ examplebox参数 → □ \blacksquare → □ Unicode毒瘤 → □ 编译
→ □ ε审计
```

### C3. 交付前五问
1. ✅ 每个 `\lim` 有 ε 追踪？
2. ✅ 第3-5编关键定理有 ε 证明？
3. ✅ 无跳步（"显然""易证""篇幅所限"=0）？
4. ✅ 无编译毒瘤（B1-B9检查通过）？
5. ✅ 习题已补（`\begin{exercise}` 计数=30）？

---

## 🅳 参考命令

```bash
# 使用自动化管线（推荐）
python3 mathbook-pipeline.py audit analysis          # ε审计
python3 mathbook-pipeline.py fix all                  # 全量修复
python3 mathbook-pipeline.py fix mathmode             # \blacksquare修复
python3 mathbook-pipeline.py report                   # 量化报告

# 手动检查
grep -rn '\\lim' part3/ part4/ part5/ | grep -v '习题'
grep -rn 'begin{examplebox}.*}$' part*/               # B1检查
grep -rn 'blacksquare' part*/**/*.tex                 # B3检查
grep -rn '[→✓✗【】℃]' part*/                          # B8检查
```

---

## 成功指标

- 5/5 强制五问通过 → 可交付
- 4/5 通过 → 退回补全
- 3/5 以下 → 不可交付
