# TinyTeX 安装与配置（macOS）

## 安装（无需 sudo）

```bash
curl -sL "https://yihui.org/gh/tinytex/tools/install-unx.sh" | sh
```

安装位置：`~/Library/TinyTeX/`
二进制路径：`~/Library/TinyTeX/bin/universal-darwin/`

## 配置 PATH

```bash
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
echo 'export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"' >> ~/.zshrc
```

## 设置镜像（墙内推荐用清华镜像）

```bash
tlmgr option repository https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/tlnet/
```

## 安装中文支持

```bash
tlmgr install ctex
```

ctex 宏包会自动处理：
- xeCJK（中文排版）
- 中文字体（macOS 下自动使用 PingFang SC）
- 中文标题、目录、章节编号

## 额外常用包

```bash
# 基础排版
tlmgr install listings xcolor geometry titling titlesec fancyhdr

# 数学
tlmgr install amsmath amssymb amsthm

# 图形与引用
tlmgr install hyperref graphicx tikz booktabs

# 分数教学用
tlmgr install cancel        # 约分划线 \cancel{...}

# 同济版排版
tlmgr install bm            # 粗体数学符号
```

## 编译命令

```bash
xelatex -interaction=nonstopmode book.tex    # 第一次编译
xelatex -interaction=nonstopmode book.tex    # 第二次编译（生成目录）
```

### 编译脚本模板

```bash
#!/bin/bash
# compile.sh — 一键编译
DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
cd "$DIR"
echo "=== 第1次编译 ==="
xelatex -interaction=nonstopmode book.tex | grep -E "Output written|Error|! "
echo "=== 第2次编译（目录） ==="
xelatex -interaction=nonstopmode book.tex | grep -E "Output written|Error|! "
echo ""
echo "=== 完成 ==="
ls -lh book.pdf
```

## 注意事项

- TinyTeX 是 TeX Live 的精简版，按需下载安装包
- 首次安装 ctex 时会自动下载大量依赖（~40个包），需耐心等待
- 如果 `tlmgr install` 卡住，尝试换镜像源
- macOS 的 `/usr/local/bin` 不可写时，TinyTeX 的符号链接创建会失败，这不影响使用——只要 PATH 设置正确，xelatex 命令仍可用
- 文档类用 `ctexbook` 而非 `book`，自动处理中文版式
