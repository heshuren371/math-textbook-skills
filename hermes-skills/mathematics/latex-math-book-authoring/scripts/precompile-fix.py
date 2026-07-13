#!/usr/bin/env python3
"""预编译修复脚本：一键修复 LaTeX 教材的常见编译错误

在 tectonic book.tex 之前运行，自动修复：
  1. 数学模式配对（\[ 缺 \]）
  2. exercise 环境闭合（连续 \begin{exercise} 缺 \end{exercise}）
  3. examplebox 括号误写（[...} → [...]）
  4. \blacksquare 在数学模式外
  5. 习题存在性检查

用法：
  python3 precompile-fix.py          # 修复并打印报告
  python3 precompile-fix.py --check  # 只检查不修复
  python3 precompile-fix.py --stats  # 只统计各章习题数
"""
import glob, re, sys

CHECK_ONLY = '--check' in sys.argv
STATS_ONLY = '--stats' in sys.argv

def fix_file(fpath):
    with open(fpath, encoding='utf-8') as f:
        text = f.read()
    original = text
    report = []

    # ── 修复1：examplebox 括号误写 ──
    fixed = re.sub(r'(\\begin\{examplebox\}\[.*?)\}', r'\1]', text)
    if fixed != text:
        report.append('  [括号] examplebox [...]} → [...]')
        text = fixed

    # ── 修复2：\[ 缺 \] 关闭 ──
    lines = text.split('\n')
    fixed_lines, in_math = [], False
    for line in lines:
        s = line.strip()
        if '\\[' in line and '\\]' not in line:
            if in_math:
                fixed_lines.append('\\]')
            in_math = True
        if '\\]' in line:
            in_math = False
        if in_math and '\\end{exercise}' in s:
            fixed_lines.append('\\]')
            in_math = False
        fixed_lines.append(line)
    if in_math:
        fixed_lines.append('\\]')
    candidate = '\n'.join(fixed_lines)
    if candidate != text:
        report.append('  [数学] 补了缺失的 \\]')
        text = candidate

    # ── 修复3：连续 exercise 缺 end ──
    open_c = text.count('\\begin{exercise}')
    close_c = text.count('\\end{exercise}')
    if open_c > close_c:
        ex_section = text.find('\\section{习题}')
        if ex_section >= 0:
            before = text[:ex_section]
            after = text[ex_section:]
            ex_lines = after.split('\n')
            fixed_ex, open_pending = [], 0
            for line in ex_lines:
                s = line.strip()
                if '\\begin{exercise}' in s:
                    if open_pending > 0:
                        fixed_ex.append('\\end{exercise}')
                    open_pending += 1
                if '\\end{exercise}' in s:
                    open_pending -= 1
                fixed_ex.append(line)
            while open_pending > 0:
                fixed_ex.append('\\end{exercise}')
                open_pending -= 1
            text = before + '\n'.join(fixed_ex)
            report.append(f'  [习题] 补了 {open_c - close_c} 个 \\end{{exercise}}')

    # ── 修复4：\blacksquare 在数学模式外 ──
    fixed = re.sub(r'(?<!\$)\\blacksquare', r'\\(\\blacksquare\\)', text)
    if fixed != text:
        report.append('  [符号] 补了 \\blacksquare 的数学模式括号')
        text = fixed

    # ── 报告 ──
    if text != original:
        if not CHECK_ONLY:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(text)
        return report
    return []

def count_exercises(fpath):
    with open(fpath, encoding='utf-8') as f:
        t = f.read()
    return t.count('\\begin{exercise}'), t.count('\\end{exercise}')

if STATS_ONLY:
    print(f'{"文件":40s} {"习题":>4s}  {"闭合":>4s}  {"状态"}')
    print('-' * 60)
    for f in sorted(glob.glob('part*/*.tex')):
        op, cl = count_exercises(f)
        status = 'OK' if op == cl else f'缺 {op-cl}'
        print(f'{f:40s} {op:4d}  {cl:4d}  {status}')
    sys.exit(0)

print('=== 预编译修复 ===')
found_any = False
for f in sorted(glob.glob('part*/*.tex')):
    reports = fix_file(f)
    if reports:
        found_any = True
        print(f'{f}:')
        for r in reports:
            print(f'  {r}')

# ── 习题存在性检查 ──
print('\n--- 习题存在性检查 ---')
missing = False
for f in sorted(glob.glob('part*/*.tex')):
    cnt, _ = count_exercises(f)
    if cnt == 0:
        print(f'WARNING: {f} 没有习题！')
        missing = True
if not missing:
    print('所有章节都有习题 ✓')
print()

if not found_any and not missing:
    print('无需修复。')
