# 中文在 `\[...\]` 内未用 `\text{}` 包裹的修复日志

## 问题

2026-07-13：第1章「常见数集」定义框的 `array` 内中文被渲染为数学变量（斜体+间距错乱）。

## 根因

`\[...\]` 内的所有内容默认在数学模式。中文汉字 `自然数集：` 被 LaTeX 当成变量名：
- 每个汉字独立排版（数学斜体）
- 字间间距按数学变量间距处理（过宽或过窄）

## 修复前

```latex
\[
\begin{array}{c|l}
\mathbb{N} & \textbf{自然数集}：\{1,2,3,4\} \\
\mathbb{Q} & \textbf{有理数集}：可以写成分数 \frac{p}{q}（p,q 是整数）
\end{array}
\]
```

`自然数集`、`可以写成分数` 等中文裸在 `\[...\]` 内 → 渲染为斜体乱码。

## 修复后

```latex
\[
\begin{array}{c|l}
\mathbb{N} & \text{自然数集：}\{1,2,3,4\} \\
\mathbb{Q} & \text{有理数集：可以写成分数 } \frac{p}{q} \text{（}p,q \text{ 是整数）}
\end{array}
\]
```

所有中文/标点用 `\text{}` 包裹。数学符号（`\mathbb{N}`, `\frac`, `\sqrt`）保持裸在数学模式中。

## 规则

| 上下文 | 处理方式 | 示例 |
|--------|---------|------|
| `\[...\]` 内的中文 | 必须 `\text{}` | `\text{自然数集：}` |
| `\[...\]` 内的全角标点 `：；（）` | 必须 `\text{}` 或换成半角 | `\text{：}` 或 `:` |
| `\[...\]` 内的数学命令 | 裸写 | `\mathbb{N}`、`\frac{p}{q}`、`\sqrt{2}` |
| `\(...\)` 内的中文 | 建议 `\text{}` | 同上 |
| 正文中的中文（不在数学模式） | 裸写 | 正常 |

## 验证方法

编译后打开 PDF，检查 `array`/`tabular` 列中的中文。如果：
- ✅ 字形正常、间距均匀 → 正确
- ❌ 字形斜体、字距异常 → 缺 `\text{}`

## 自动检测

```python
import re, glob
for f in glob.glob('part*/*.tex'):
    with open(f) as fh:
        t = fh.read()
    # 找到 \[...\] 内的中文（不在 \text{} 内的）
    for m in re.finditer(r'\\\[.*?\\\]', t, re.DOTALL):
        block = m.group()
        # 去掉 \text{...} 内的内容
        stripped = re.sub(r'\\text\{[^}]*\}', '', block)
        chinese = re.findall(r'[\u4e00-\u9fff]', stripped)
        if chinese:
            print(f'{f}: 裸中文 {chinese}')
```
