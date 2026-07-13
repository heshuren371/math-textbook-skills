#!/usr/bin/env python3
"""
第2章函数图 v2 修复版——可作为「函数图顶点标注」和「坐标系O点」问题的参考实现。

本文件记录了从用户反馈"U型函数顶点错了"和"坐标系有两个O点"中总结的修复方案。
"""
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
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'figures')
os.makedirs(OUT, exist_ok=True)

def save(name):
    plt.savefig(f'{OUT}/{name}.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print(f'  OK {name}.pdf')

# ── 图1：平移变换（顶点标注规范）──
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-4, 6, 400)
ax.plot(x, x**2,     'b-', lw=2, label='y = x²')
ax.plot(x, (x-2)**2, 'r-', lw=2, label='y = (x-2)²')
ax.plot(x, x**2 + 3, 'g-', lw=2, label='y = x² + 3')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-3, 6); ax.set_ylim(-1, 12)
ax.grid(True, alpha=0.3)
ax.set_title('图像的平移变换', fontsize=16)
ax.legend(fontsize=12, loc='upper left')

# 顶点标注：大红点+黑边 + 颜色与曲线一致
verts = [(0,0,'b'), (2,0,'r'), (0,3,'g')]
for vx, vy, c in verts:
    ax.scatter([vx], [vy], color=c, s=150, zorder=5, edgecolors='black', linewidths=1)
    if vx == 0 and vy == 0:
        ax.annotate('(0,0)', (vx, vy), xytext=(12, -25),   # y>0? 偏移到下方
                    textcoords='offset points', fontsize=13, color='b', fontweight='bold')
    elif vx == 2 and vy == 0:
        ax.annotate('(2,0)', (vx, vy), xytext=(12, -25),
                    textcoords='offset points', fontsize=13, color='r', fontweight='bold')
    else:
        ax.annotate(f'({vx},{vy})', (vx, vy), xytext=(12, 8),  # y>0区域：偏移到上方
                    textcoords='offset points', fontsize=13, color='g', fontweight='bold')
save('ch02_translation_v2_ref')
