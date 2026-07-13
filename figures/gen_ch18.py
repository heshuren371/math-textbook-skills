#!/usr/bin/env python3
"""第18-21章：导数综合矢量图"""
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

# 1: 中值定理
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0.5, 4.5, 400)
y = 0.5*(x-2)**3 + 2*(x-2) + 3
ax.plot(x, y, '#2b83ba', lw=2.5, label='f(x)')
a, b = 1, 4
fa, fb = 0.5*(1-2)**3+2*(1-2)+3, 0.5*(4-2)**3+2*(4-2)+3
ax.scatter([a, b], [fa, fb], color='red', s=100, zorder=5)
ax.plot([a, b], [fa, fb], 'r--', lw=1.5, alpha=0.7, label='割线')
c = 2.5  # 近似
fc = 0.5*(c-2)**3+2*(c-2)+3
slope = 3*(c-2)**2/2 + 2  # 导数
tan_x = np.linspace(c-0.8, c+0.8, 10)
tan_y = fc + slope*(tan_x - c)
ax.plot(tan_x, tan_y, 'green', lw=2, ls='--', label=f'切线在 c={c}')
ax.scatter([c], [fc], color='green', s=100, zorder=5)
ax.axhline(0, color='gray', lw=0.8)
ax.grid(True, alpha=0.3)
ax.set_title('拉格朗日中值定理：存在c使f\'(c)=割线斜率', fontsize=13)
ax.legend(fontsize=11)
save('ch19_mvt')

# 2: 极值
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(-2, 2, 400)
y = -x**4 + 2*x**2
ax.plot(x, y, '#2b83ba', lw=2.5)
ax.scatter([-1, 0, 1], [-1+2, 0, -1+2], color='red', s=120, zorder=5)
ax.annotate('极大值', (1, 1.2), fontsize=13, color='red')
ax.annotate('极大值', (-1, 1.2), fontsize=13, color='red')
ax.annotate('极小值', (0, -0.3), fontsize=13, color='blue')
ax.axhline(0, color='gray', lw=0.8)
ax.grid(True, alpha=0.3)
ax.set_title('极值点：导数为0', fontsize=15)
save('ch21_extrema')

# 3: 凹凸
fig, ax = plt.subplots(figsize=(8, 5))
x1 = np.linspace(-2, 0, 200)
ax.plot(x1, x1**2, '#2b83ba', lw=2.5)
x2 = np.linspace(0, 2, 200)
ax.plot(x2, -x2**2, '#d7191c', lw=2.5)
ax.axvline(0, color='gray', ls='--', alpha=0.5)
ax.annotate('凹 (二阶导>0)', (-1, 1.5), fontsize=14, color='#2b83ba')
ax.annotate('凸 (二阶导<0)', (1, -1.5), fontsize=14, color='#d7191c')
ax.axhline(0, color='gray', lw=0.8)
ax.grid(True, alpha=0.3)
ax.set_title('凹凸性——二阶导数决定', fontsize=15)
save('ch21_concavity')

print('完成')
