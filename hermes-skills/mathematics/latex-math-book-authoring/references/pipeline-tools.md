# 教材自动化管线工具

## 统一管线入口

`mathbook-pipeline.py` 位于 `workspace/math-templates/`，v2 版支持：

| 功能 | 命令 |
|:-----|:-----|
| 初始化项目 | `python3 mathbook-pipeline.py init "书名"` |
| 创建新章 | `python3 mathbook-pipeline.py chapter new chXX "标题"` |
| 结构审计（通用） | `python3 mathbook-pipeline.py audit structural [id]` |
| 数学分析审计 | `python3 mathbook-pipeline.py audit analysis [id]` |
| 拓扑学审计 | `python3 mathbook-pipeline.py audit topology [id]` |
| 代数学审计 | `python3 mathbook-pipeline.py audit algebra [id]` |
| 数论审计 | `python3 mathbook-pipeline.py audit number-theory [id]` |
| 语法修复 | `python3 mathbook-pipeline.py fix syntax [id]` |
| 环境配对修复 | `python3 mathbook-pipeline.py fix pairing [id]` |
| Unicode 修复 | `python3 mathbook-pipeline.py fix unicode [id]` |
| 数学模式修复 | `python3 mathbook-pipeline.py fix mathmode [id]` |
| 全量修复 | `python3 mathbook-pipeline.py fix all [id]` |
| 编译 | `python3 mathbook-pipeline.py build` |
| 报告 | `python3 mathbook-pipeline.py report` |
| 批量管线 | `python3 mathbook-pipeline.py pipeline id1 id2 ...` |

### mathkit 入口

```bash
source ~/.hermes/profiles/xiandaishuxuejia/.venv/bin/activate
mathkit pipeline audit analysis ch31   # 通过 mathkit 调用
```

## 通用 Agent 指令

`agents/MATH_TEXTBOOK_AGENT.md` 包含完整的教材编写工作流和规则，兼容：

```bash
claude-code --context MATH_TEXTBOOK_AGENT.md
codex run --instructions MATH_TEXTBOOK_AGENT.md
```

## 领域配置

在项目 `.mathbook.yml` 中设置：
```yaml
title: 实分析
domain: analysis  # 审计域: structural|analysis|topology|algebra|number-theory
```

或通过环境变量 `MATHBOOK_DOMAIN=topology` 临时覆盖。
