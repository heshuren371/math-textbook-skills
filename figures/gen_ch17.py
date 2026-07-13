#!/usr/bin/env python3
"""第17章：导数的概念——矢量图"""
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

# 1: 切线——割线逼近
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-1, 3, 400)
y = x**2 - x + 1
ax.plot(x, y, '#2b83ba', lw=2.5, label='f(x)')
a = 1
# 割线
h_vals = [1.5, 0.8, 0.3]
colors = ['#cccccc', '#999999', '#666666']
for h, c in zip(h_vals, colors):
    sec_x = np.linspace(a-0.2, a+h+0.2, 10)
    sec_y = (a**2-a+1) + ((a+h)**2-(a+h)+1 - (a**2-a+1))/h * (sec_x - a)
    ax.plot(sec_x, sec_y, color=c, lw=1.5, ls='--', alpha=0.6)
# 切线
tan_x = np.linspace(a-0.5, a+1.5, 10)
tan_y = (a**2-a+1) + (2*a-1)*(tan_x - a)
ax.plot(tan_x, tan_y, '#d7191c', lw=2.5, label='切线 (h→0)')
ax.scatter([a], [a**2-a+1], color='red', s=100, zorder=5)
ax.set_title('割线→切线：h→0时割线的极限位置', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
save('ch17_tangent')

# 2: 切线斜率 = 导数
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-2, 2, 400)
y = x**3/3 - x
ax.plot(x, y, '#2b83ba', lw=2.5, label='f(x)=x³/3 - x')
# 在 x=1 处画切线
a = 1
slope = a**2 - 1  # 导数为 x²-1
tan_x = np.linspace(a-0.8, a+0.8, 10)
tan_y = (a**3/3 - a) + slope*(tan_x - a)
ax.plot(tan_x, tan_y, '#d7191c', lw=2, ls='--', label=f'切线: 斜率={slope:.1f}')
ax.scatter([a], [a**3/3 - a], color='red', s=100, zorder=5)
ax.annotate(f'f\'({a})={slope:.1f}', (a, a**3/3 - a), xytext=(15, -30),
            textcoords='offset points', fontsize=13, color='red',
            arrowprops=dict(arrowstyle='->', color='red'))
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.grid(True, alpha=0.3)
ax.set_title('导数 = 切线的斜率', fontsize=15)
ax.legend(fontsize=12)
save('ch17_derivative_slope')
print('完成')
