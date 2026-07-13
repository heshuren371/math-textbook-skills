# mathbook-pipeline.py — 通用数学教材自动化管线

## 位置

- 项目内：`mathbook-pipeline.py`（直接放在教材项目根目录）
- Profile 内：`~/.hermes/profiles/xiandaishuxuejia/workspace/math-templates/mathbook-pipeline.py`
- Agent 指令：`~/.hermes/profiles/xiandaishuxuejia/agents/MATH_TEXTBOOK_AGENT.md`

## 架构

```
init → chapter → audit(可插拔域) → fix(分层修复) → build → report
```

## 子命令速查

```bash
python3 mathbook-pipeline.py init "教材名"           # 初始化项目
python3 mathbook-pipeline.py chapter new ch01 "标题" # 创建新章
python3 mathbook-pipeline.py chapter add ch01        # 加入 book.tex
python3 mathbook-pipeline.py audit structural       # 结构审计
python3 mathbook-pipeline.py audit analysis          # ε-N/ε-δ 审计
python3 mathbook-pipeline.py audit topology          # 开集/紧致审计
python3 mathbook-pipeline.py audit algebra           # 群/环/域审计
python3 mathbook-pipeline.py fix syntax             # LaTeX 语法修复
python3 mathbook-pipeline.py fix pairing            # 环境配对修复
python3 mathbook-pipeline.py fix unicode            # Unicode 字符修复
python3 mathbook-pipeline.py fix mathmode           # \blacksquare 修复
python3 mathbook-pipeline.py fix all                # 全量修复
python3 mathbook-pipeline.py build                  # 编译全书
python3 mathbook-pipeline.py report                 # 量化报告
```

## 审计域

| 域 | 领域 | 检查内容 |
|:---|:-----|:---------|
| `structural` | 通用 | 环境配对、数学模式配对、Unicode 毒瘤 |
| `analysis` | 数学分析 | ε-N/ε-δ 追踪、`\lim` 定义完备性 |
| `topology` | 拓扑学 | 开集/闭集/紧致/连通/度量 定义 |
| `algebra` | 代数学 | 群/环/域/同态/同构 定义 |
| `number-theory` | 数论 | 素数/ζ函数/L函数 定义 |

## 修复层

| 层 | 修复内容 |
|:---|:---------|
| `syntax` | `\begin{examplebox}[...}` 花括号错、`\end{examplebox]` 方括号错 |
| `pairing` | 连续 `\begin{exercise}` 缺 `\end{exercise}`、`\[` 缺 `\]` |
| `unicode` | `→✓✗【】℃` → LaTeX 命令 |
| `mathmode` | `\blacksquare` 数学模式包裹、双重 `\(\(` 修复 |
| `all` | 以上全部 |

## 添加新审计域

在 `AUDIT_DOMAINS` 字典中添加：

```python
AUDIT_DOMAINS['my-field'] = ('我的领域', _my_field_audit)
```

审计函数签名：`def _my_field_audit(files) -> int`（返回失败数）。

## 配置

项目根目录 `.mathbook.yml` 或环境变量 `MATHBOOK_DOMAIN=topology`：

```yaml
title: 一般拓扑学
domain: topology
chapters_dir: chapters
compiler: tectonic
```

## Agent 兼容

详见 `MATH_TEXTBOOK_AGENT.md`（同一目录），适用于 Claude Code / Codex CLI：

```bash
claude-code --context MATH_TEXTBOOK_AGENT.md
```
