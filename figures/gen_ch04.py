#!/usr/bin/env python3
"""第4章：指数函数——矢量图生成脚本"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC'],
    'font.size': 14,
    'axes.unicode_minus': False,
    'figure.dpi': 150,
})
OUT = '/Users/heshuren/math-analysis/figures'
os.makedirs(OUT, exist_ok=True)

def save(name):
    plt.savefig(f'{OUT}/{name}.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print(f'  OK {name}.pdf')

# ============================================================
# 图1：底>1的指数函数对比（2^x, 3^x, 5^x, 10^x）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-2, 3, 400)
bases = [(2, 'y = 2^x', '#2b83ba'),
         (3, 'y = 3^x', '#d7191c'),
         (5, 'y = 5^x', '#fdae61'),
         (10, 'y = 10^x', '#5e3c99')]
for base, label, color in bases:
    ax.plot(x, base**x, color=color, lw=2.5, label=label)
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2, 3)
ax.set_ylim(-0.5, 12)
ax.grid(True, alpha=0.3)
ax.set_title('指数函数（底 > 1）——底越大增长越快', fontsize=16)
ax.legend(fontsize=12, loc='upper left')
# 标公共点 (0,1)
ax.scatter([0], [1], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(0,1)', (0,1), xytext=(8,5), textcoords='offset points', fontsize=13, fontweight='bold')
# 标 (1, base)
for base, _, color in bases:
    ax.scatter([1], [base], color=color, s=60, zorder=5)
save('ch04_exponential_growth')

# ============================================================
# 图2：0<底<1的指数函数（衰减）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-2, 3, 400)
bases = [(0.5, 'y = (1/2)^x', '#2b83ba'),
         (1/3, 'y = (1/3)^x', '#d7191c'),
         (0.2, 'y = (1/5)^x', '#fdae61')]
for base, label, color in bases:
    ax.plot(x, base**x, color=color, lw=2.5, label=label)
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2, 3)
ax.set_ylim(-0.5, 8)
ax.grid(True, alpha=0.3)
ax.set_title('指数函数（0 < 底 < 1）——指数越大衰减越快', fontsize=16)
ax.legend(fontsize=12, loc='upper right')
ax.scatter([0], [1], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(0,1)', (0,1), xytext=(8,5), textcoords='offset points', fontsize=13, fontweight='bold')
save('ch04_exponential_decay')

# ============================================================
# 图3：增长 vs 衰减 对称对比（2^x 和 (1/2)^x）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-3, 3, 400)
ax.plot(x, 2**x, '#2b83ba', lw=3, label='y = 2^x（增长）')
ax.plot(x, (0.5)**x, '#d7191c', lw=3, label='y = (1/2)^x（衰减）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-3, 3)
ax.set_ylim(-0.5, 8)
ax.grid(True, alpha=0.3)
ax.set_title('增长 vs 衰减——关于 y 轴对称', fontsize=16)
ax.legend(fontsize=12)
ax.scatter([0], [1], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(0,1)', (0,1), xytext=(8,5), textcoords='offset points', fontsize=13, fontweight='bold')
# 标注对称关系
ax.plot([1, -1], [2, 2], 'k--', lw=0.8, alpha=0.4)
ax.annotate('对称点', (0, 2.3), fontsize=12, ha='center')
save('ch04_growth_vs_decay')

# ============================================================
# 图4：自然指数 e^x（与 2^x, 3^x 对比）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-2, 2.5, 400)
e = np.e
ax.plot(x, 2**x, '#aaaaaa', lw=1.5, ls='--', label='2^x')
ax.plot(x, 3**x, '#aaaaaa', lw=1.5, ls='--', label='3^x')
ax.plot(x, e**x, '#d7191c', lw=3, label='y = e^x（自然指数）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2, 2.5)
ax.set_ylim(-0.5, 10)
ax.grid(True, alpha=0.3)
ax.set_title('自然指数 e^x——在 x=0 处的切线斜率为 1', fontsize=16)
ax.legend(fontsize=12, loc='upper left')
ax.scatter([0], [1], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(0,1)', (0,1), xytext=(8,5), textcoords='offset points', fontsize=13)
# 画切线
tan_x = np.linspace(-0.5, 1, 100)
tan_y = 1 + tan_x  # e^x 在 x=0 处的切线 y = 1 + x
ax.plot(tan_x, tan_y, 'green', lw=1.5, ls='-', alpha=0.7, label='在 x=0 处的切线')
ax.legend(fontsize=12, loc='upper left')
save('ch04_natural_exponential')

# ============================================================
# 图5：指数 vs 幂函数——增长的竞赛
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0.1, 5, 400)
ax.plot(x, x**2, '#2b83ba', lw=2, label='x^2（幂函数）')
ax.plot(x, x**3, '#fdae61', lw=2, label='x^3（幂函数）')
ax.plot(x, 2**x, '#d7191c', lw=3, label='2^x（指数函数）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(0, 5)
ax.set_ylim(0, 35)
ax.grid(True, alpha=0.3)
ax.set_title('指数增长 vs 幂函数增长——指数最终胜出', fontsize=16)
ax.legend(fontsize=12, loc='upper left')
# 标注交点附近
ax.annotate('2^x 超过 x^3', xy=(4.5, 25), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.3))
ax.axvline(4, color='gray', lw=0.5, ls=':')
save('ch04_expo_vs_power')

print('\n第4章图像全部生成完成！')
