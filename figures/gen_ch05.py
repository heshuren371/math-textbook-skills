#!/usr/bin/env python3
"""第5章：对数函数——矢量图生成脚本"""
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
# 图1：不同底的对数函数对比（底>1）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0.05, 5, 400)
logs = [(2, 'y = log_2(x)', '#2b83ba'),
        (np.e, 'y = ln(x)', '#d7191c'),
        (10, 'y = lg(x)', '#fdae61')]
for base, label, color in logs:
    ax.plot(x, np.log(x)/np.log(base), color=color, lw=2.5, label=label)
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-0.2, 5)
ax.set_ylim(-4, 4)
ax.grid(True, alpha=0.3)
ax.set_title('对数函数（底 > 1）', fontsize=16)
ax.legend(fontsize=12, loc='upper left')
# 公共点 (1,0)
ax.scatter([1], [0], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(1,0)', (1,0), xytext=(8,5), textcoords='offset points', fontsize=13, fontweight='bold')
# (a,1)
for base, _, color in logs:
    if base <= 5:
        ax.scatter([base], [1], color=color, s=60, zorder=5)
save('ch05_logarithm_bases')

# ============================================================
# 图2：指数与对数互逆关系（2^x 和 log_2(x) 关于 y=x 对称）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))
x1 = np.linspace(-2, 4, 400)
ax.plot(x1, 2**x1, '#2b83ba', lw=2.5, label='y = 2^x')
x2 = np.linspace(0.05, 4, 400)
ax.plot(x2, np.log2(x2), '#d7191c', lw=2.5, label='y = log_2(x)')
# y=x 对称线
x_line = np.linspace(-2, 4, 100)
ax.plot(x_line, x_line, 'k--', lw=1, alpha=0.5, label='y = x（对称轴）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2, 4)
ax.set_ylim(-2, 4)
ax.grid(True, alpha=0.3)
ax.set_title('指数与对数——关于 y=x 对称', fontsize=16)
ax.legend(fontsize=12, loc='upper left')
ax.set_aspect('equal')
# 标注对称点
ax.scatter([1, 2], [2, 1], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(1,2)', (1,2), xytext=(5,5), textcoords='offset points', fontsize=12)
ax.annotate('(2,1)', (2,1), xytext=(5,5), textcoords='offset points', fontsize=12)
save('ch05_exp_log_inverse')

# ============================================================
# 图3：底<1的对数函数（衰减型）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0.05, 4, 400)
ax.plot(x, np.log(x)/np.log(0.5), '#d7191c', lw=2.5, label='y = log_{1/2}(x)')
ax.plot(x, np.log(x)/np.log(1/3), '#2b83ba', lw=2.5, label='y = log_{1/3}(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-0.2, 4)
ax.set_ylim(-4, 4)
ax.grid(True, alpha=0.3)
ax.set_title('对数函数（0 < 底 < 1）——递减', fontsize=16)
ax.legend(fontsize=12)
ax.scatter([1], [0], color='black', s=100, zorder=5, edgecolors='black')
ax.annotate('(1,0)', (1,0), xytext=(8,5), textcoords='offset points', fontsize=13)
save('ch05_logarithm_decay')

# ============================================================
# 图4：对数函数用于"压缩"大数
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0.1, 100, 1000)
# 用换底公式画 lg(x)
y_log = np.log10(x)
ax.plot(x, y_log, '#2b83ba', lw=2.5, label='y = lg(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-5, 105)
ax.set_ylim(-2, 3)
ax.grid(True, alpha=0.3)
ax.set_title('对数压缩效果——把大数"变小"', fontsize=16)
ax.legend(fontsize=12)
# 标注关键点
points = [(1,0), (10,1), (100,2)]
for px, py in points:
    ax.scatter([px], [py], color='red', s=100, zorder=5, edgecolors='black')
    ax.annotate(f'({px},{py})', (px, py), xytext=(8,5), textcoords='offset points',
                fontsize=12, color='red')
# 标注说明
ax.annotate('x 从 1 到 100（扩大了100倍）\ny 只从 0 到 2（增加了2）',
            xy=(50, 0.5), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
save('ch05_log_compression')

print('\n第5章图像全部生成完成！')
