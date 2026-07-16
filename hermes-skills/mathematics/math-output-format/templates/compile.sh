#!/bin/bash
# 数学教材一键编译脚本
# 用法：./compile.sh
# 要求在 book.tex 同级目录下运行

DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

cd "$DIR" || { echo "❌ 无法进入目录 $DIR"; exit 1; }

echo "=== 第1次编译（生成 .aux）==="
xelatex -interaction=nonstopmode book.tex | grep -E "Output written|Error|! "

echo "=== 第2次编译（生成目录）==="
xelatex -interaction=nonstopmode book.tex | grep -E "Output written|Error|! "

if [ -f book.pdf ]; then
    echo ""
    echo "✅ 编译成功"
    ls -lh book.pdf
else
    echo "❌ 编译失败，查看 book.log 获取详情"
    exit 1
fi
