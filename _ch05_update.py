#!/usr/bin/env python3
"""Batch update Chapter 5: retro tags, hint refs, gate, confidence box."""
import re

with open('/Users/heshuren/math-analysis/part0/ch05-logarithm.tex', 'r') as f:
    content = f.read()

# ── 1. Retro tags ──
# Exercise 1 (diff 0) - after "\end{exercise}" that follows "(3)\; \log_3 9 = 2 \qquad (4)\; \log_2 0 = 0"
content = content.replace(
    r'\\[4pt]',
    r'\\\\[4pt]'
)

# Ex1 retro: 指数式化对数式 → ch4
content = content.replace(
    r'\(3)\; \log_3 9 = 2 \qquad (4)\; \log_2 0 = 0',
    r'(3)\; \log_3 9 = 2 \qquad (4)\; \log_2 0 = 0'
)

# Actually the file uses single backslashes which get read as-is by Python
# Let me read and work with the raw content
print("File length:", len(content))

# Let me just find the exact strings
# Search for specific markers
for i, line in enumerate(content.split('\n'), 1):
    if '简单 =====' in line:
        print(f"Line {i}: {repr(line[:80])}")

# Let me take a different approach and use simple marker replacement
markers = {
    # Ex1: after "判断正误" block, before 简单 section
    r'\end{exercise}' + '\n' + '\n' + r'% ===== 简单':
        r'\end{exercise}' + '\n' + r'\qquad \textcolor{gray}{[回顾第4章：指数与对数的互逆]}%' + '\n' + '\n' + r'% ===== 简单',
}

for old, new in markers.items():
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"Applied: {old[:40]}... (count={count})")
    else:
        print(f"NOT FOUND: {repr(old[:60])}")

# Let me verify the line is there
lines = content.split('\n')
for i, line in enumerate(lines):
    if '简单 =====' in line:
        print(f"Line {i+1}: {repr(line)}")
        print(f"Line {i}: {repr(lines[i-1])}")
        print(f"Line {i-1}: {repr(lines[i-2])}")
        break

with open('/Users/heshuren/math-analysis/part0/ch05-logarithm.tex', 'w') as f:
    f.write(content)
print("Done")
