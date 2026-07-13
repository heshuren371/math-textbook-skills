# 2026-07-13 全书编译错误修复记录

## 问题概览

30章教材在交付前编译全面失败，共发现 60+ 处 LaTeX 结构错误。
主要分为 3 类：`\]` 顺序错误、`\frac` 花括号错位、`\blacksquare` 双重包裹。

## 错误类型 1：`\]` 与 `\end{xxx}` 顺序颠倒（60+处，占 90%）

### 症状
```
part0/ch01-function-concept.tex:456: Missing $ inserted
part0/ch02-function-graph.tex:458: Missing $ inserted
part0/ch07-trigonometry-2.tex:202: Bad math environment delimiter.
part1/ch09-sequences.tex:97: Missing $ inserted
```

### 根因
预分析章节中，`\end{cases}` 或 `\end{aligned}` 被放在 `\]` 之后。
而 `\end{definitionbox}` 或 `\end{exercise}` 被放在 `\]` 之前。

### 修复代码（已验证在 30 章上全部通过）
```python
import glob, re
for f in sorted(glob.glob('part*/*.tex')):
    with open(f) as fh:
        t = fh.read()
    # 对 math 环境：把 \] 移到 \end{cases} 之后
    for env in ['cases', 'aligned', 'pmatrix', 'array']:
        t = re.sub(rf'(\\\])\s*\n\s*(\\end\{{{env}\}})', r'\2\n\1', t)
    # 对 box 环境：把 \] 移到 \end{definitionbox} 之前
    for env in ['definitionbox','examplebox','theorembox','exercise']:
        t = re.sub(rf'(\\end\{{{env}\}})\s*\n\s*(\\\])', r'\2\n\1', t)
    # Clean consecutive \]
    t = re.sub(r'\\\]\s*\n\s*\\\]', r'\\]', t)
    # 修复 matrix 在两个 \] 之间的问题
    t = re.sub(r'(\\end\{[a-z]*matrix\})\s*\n\s*\\\]\s*\n\s*(\\begin\{[a-z]*matrix\})', r'\1\n\2', t)
    with open(f, 'w') as fh:
        fh.write(t)
```

## 错误类型 2：`\frac` 花括号使用 `]` 而非 `}`（3处）

### 症状
```
book.tex:64: File ended while scanning use of \frac
```

### 位置
- `part4/ch23-ftc.tex:28`: `\frac{x^3]{3]` → `\frac{x^3}{3}`
- `part4/ch25-improper-integrals.tex:19`: `\frac{dx]{x^2]` → `\frac{dx}{x^2}`
- `part0/ch01-function-concept.tex`: `\frac{...]` pattern (various locations)

### 修复
```bash
# 全局搜索
grep -rn '\\frac{[^}]*]' part*/
# 人工检查每个匹配
```

## 错误类型 3：`\blacksquare` 双重包裹（2处）

### 症状
```
part1/ch11-epsilon-n.tex:94: Bad math environment delimiter.
```

### 根因
自动修复脚本错误地将 `\quad\blacksquare\)` 改为 `\quad\(\blacksquare\)\)`
导致 `\(` 在已有的 `\(...\)` 内嵌套。

### 修复
```python
# 字节级精确修复
old = b'\x5c\x71\x75\x61\x64\x5c\x28\x5c\x62\x6c\x61\x63\x6b\x73\x71\x75\x61\x72\x65\x5c\x29'
new = b'\x5c\x71\x75\x61\x64\x5c\x62\x6c\x61\x63\x6b\x73\x71\x75\x61\x72\x65\x5c\x29'
data = data.replace(old, new)
```

## 错误类型 4：`\begin{pmatrix}` 在两个 `\]` 之间（1处）

### 位置
`part0/ch07-trigonometry-2.tex:200`

### 根因
两个 `pmatrix` 环境被一个多余的 `\]` 分隔：
```
\]   ← 这个 \] 不应该存在
\begin{pmatrix}
```

### 修复
删除中间的 `\]`，使两个矩阵在同一个 `\[...\]` 中。

## 教训总结

1. **`\]` 顺序是 LaTeX 教材中最隐蔽的批量错误。** 30 章中有 22 章存在此问题。
2. **自动修复脚本也会引入错误。** 每次运行自动修复后必须重新编译验证。
3. **增量编译测试不可靠。** 分段编译成功的文件在全量编译中可能失败。
4. **`\blacksquare` 在自动修复中最容易被搞坏。** 优先用字节级替换而非字符串级。
