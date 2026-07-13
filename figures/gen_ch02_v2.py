#!/usr/bin/env python3
"""第2章：函数的图像——矢量图生成脚本（v2，修复顶点和O点问题）"""
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
# 图1：描点法画 y = x²（简化标注，突出顶点）
# ============================================================
fig, ax = plt.subplots(figsize=(7, 6))
ax.set_xlim(-4, 4)
ax.set_ylim(-1, 10)
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.grid(True, alpha=0.3)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('描点法画 y = x²', fontsize=16)

xs = np.linspace(-3.5, 3.5, 200)
ax.plot(xs, xs**2, 'b-', lw=2.5, label='y = x²')

# 描点——只标出几个关键点，不全部标注坐标（避免拥挤）
points = [(-3,9), (-2,4), (-1,1), (0,0), (1,1), (2,4), (3,9)]
px, py = zip(*points)
ax.scatter(px, py, color='red', s=80, zorder=5, label='描点')

# 只标注顶点(0,0)和两侧端点
key_points = {'顶点 (0,0)': (0,0), '(3, 9)': (3,9), '(-3, 9)': (-3,9)}
for label, (x, y) in key_points.items():
    offset = (-40, 10) if x < 0 else (10, 10)
    ax.annotate(label, (x, y), xytext=offset,
                textcoords='offset points', fontsize=12, color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

ax.legend(fontsize=12, loc='upper left')
save('ch02_sketch_x2')

# ============================================================
# 图2：六种基本函数对比（每个子图加关键点标注）
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(14, 9))

# 每个函数的额外标注：位置、文字
funcs = [
    ('y = x',      lambda x: x,        (-3,3), (-3,3),   [],          [(2,2,'(2,2)')]),
    ('y = x\xb2',  lambda x: x**2,     (-3,3), (-1,10),  [(0,0)],     [(2,4,'(2,4)')]),
    ('y = x\xb3',  lambda x: x**3,     (-3,3), (-10,10), [(0,0)],     [(2,8,'(2,8)')]),
    ('y = 1/x',    lambda x: 1/x,      (-3,3), (-5,5),   [],          [(1,1,'(1,1)'),(-1,-1,'(-1,-1)')]),
    ('y = |x|',    lambda x: np.abs(x),(-3,3), (-0.5,4), [(0,0)],     [(2,2,'(2,2)')]),
    ('y = sqrt(x)',lambda x: np.sqrt(x) if x>=0 else np.nan, (-0.5,5), (-0.5,3), [(0,0)], [(4,2,'(4,2)')]),
]

for ax, (title, f, xr, yr, vertices, annotations) in zip(axes.flat, funcs):
    xs = np.linspace(xr[0], xr[1], 1000)
    ys = np.array([f(x) for x in xs])
    if title == 'y = 1/x':
        ys[np.abs(xs) < 0.02] = np.nan
    ax.plot(xs, ys, '#2b83ba', lw=2.5)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_xlim(*xr)
    ax.set_ylim(*yr)
    ax.set_title(title, fontsize=15)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    # 标注顶点（大红点）
    for vx, vy in vertices:
        ax.scatter([vx], [vy], color='red', s=100, zorder=5)
        ax.annotate(f'({vx},{vy})', (vx, vy), xytext=(8, 8),
                    textcoords='offset points', fontsize=12, color='red',
                    fontweight='bold')
    for ax2, ay2, label in annotations:
        ax.annotate(label, (ax2, ay2), xytext=(8, 8),
                    textcoords='offset points', fontsize=11, color='#2b83ba')

plt.tight_layout()
save('ch02_six_basic_funcs')

# ============================================================
# 图3：平移变换（用大红点突出顶点位置）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-4, 6, 400)
ax.plot(x, x**2, 'b-', lw=2, label='y = x\xb2')
ax.plot(x, (x-2)**2, 'r-', lw=2, label='y = (x-2)\xb2')
ax.plot(x, x**2 + 3, 'g-', lw=2, label='y = x\xb2 + 3')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-3, 6)
ax.set_ylim(-1, 12)
ax.grid(True, alpha=0.3)
ax.set_title('图像的平移变换', fontsize=16)
ax.legend(fontsize=12, loc='upper left')

# 用大红点标顶点 + 无歧义标注
verts = [(0,0,'b'), (2,0,'r'), (0,3,'g')]
for vx, vy, c in verts:
    ax.scatter([vx], [vy], color=c, s=150, zorder=5, edgecolors='black', linewidths=1)
    if vx == 0 and vy == 0:
        ax.annotate('(0,0)', (vx, vy), xytext=(12, -25),
                    textcoords='offset points', fontsize=13, color='b', fontweight='bold')
    elif vx == 2 and vy == 0:
        ax.annotate('(2,0)', (vx, vy), xytext=(12, -25),
                    textcoords='offset points', fontsize=13, color='r', fontweight='bold')
    else:
        ax.annotate(f'({vx},{vy})', (vx, vy), xytext=(12, 8),
                    textcoords='offset points', fontsize=13, color='g', fontweight='bold')
save('ch02_translation')

# ============================================================
# 图4：对称变换（标注关键点坐标）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-3, 3, 400)
ax.plot(x, x**2, 'b-', lw=2.5, label='y = x\xb2')
ax.plot(x, -x**2, 'r-', lw=2.5, label='y = -x\xb2')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-10, 10)
ax.grid(True, alpha=0.3)
ax.set_title('图像的对称变换（关于 x 轴翻转）', fontsize=16)
ax.legend(fontsize=12)
# 对称点对
pairs = [(2, 4, -4), (1, 1, -1)]
for px, py_up, py_down in pairs:
    ax.scatter([px], [py_up], color='b', s=100, zorder=5, edgecolors='black')
    ax.scatter([px], [py_down], color='r', s=100, zorder=5, edgecolors='black')
    ax.plot([px, px], [py_up, py_down], 'k--', lw=0.8, alpha=0.5)
    ax.annotate(f'({px},{py_up})', (px, py_up), xytext=(8, 5),
                textcoords='offset points', fontsize=12, color='b')
    ax.annotate(f'({px},{py_down})', (px, py_down), xytext=(8, 5),
                textcoords='offset points', fontsize=12, color='r')
# 标顶点
ax.scatter([0], [0], color='black', s=80, zorder=5)
save('ch02_symmetry')

# ============================================================
# 图5：翻折变换
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-3, 3, 500)
ax.plot(x, x**2 - 1, 'b--', lw=1.5, label='y = x\xb2 - 1')
ax.plot(x, np.abs(x**2 - 1), 'r-', lw=2.5, label='y = |x\xb2 - 1|')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
x_fill = np.linspace(-1, 1, 200)
y_fill = x_fill**2 - 1
ax.fill_between(x_fill, 0, -y_fill, color='red', alpha=0.15)
ax.set_xlim(-3, 3)
ax.set_ylim(-1.5, 5)
ax.grid(True, alpha=0.3)
ax.set_title('翻折变换  y = |f(x)|', fontsize=16)
ax.legend(fontsize=12)
# 标注翻折区域
ax.annotate('x 轴下方部分\n翻折到上方', xy=(0, -0.8), xytext=(80, -30),
            textcoords='offset points', fontsize=12,
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.3))
# 标顶点
ax.scatter([0, 0], [-1, 1], color='red', s=80, zorder=5, edgecolors='black')
ax.annotate('翻折前 (-1)', (0, -1), xytext=(10, -20),
            textcoords='offset points', fontsize=11, color='b')
ax.annotate('翻折后 (1)', (0, 1), xytext=(10, 8),
            textcoords='offset points', fontsize=11, color='r')
save('ch02_abs_flip')

# ============================================================
# 图6：从图像读信息
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))
x = np.linspace(-2, 2, 400)
y = x**3 - x
ax.plot(x, y, 'b-', lw=2.5, label='f(x) = x\xb3 - x')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
zeros = [-1, 0, 1]
for z in zeros:
    ax.scatter([z], [0], color='red', s=100, zorder=5, edgecolors='black')
    ax.annotate(f'x={z}', (z, 0), xytext=(10, -30),
                textcoords='offset points', fontsize=12, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))
ax.annotate('定义域: R', xy=(0.8, 1.5), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax.annotate('值域: R', xy=(0.8, 1), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, alpha=0.3)
ax.set_title('从图像读信息', fontsize=15)
ax.legend(fontsize=12)
save('ch02_read_from_graph')

# ============================================================
# 图7：垂线检验法（用符号替代✓✗）
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

x = np.linspace(-2, 2, 400)
ax1.plot(x, x**2, 'b-', lw=2.5)
ax1.axvline(1, color='red', ls='--', alpha=0.7, lw=1.5)
ax1.set_title('是函数\n每条竖线只交1个点', fontsize=14, color='green')
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-0.5, 4.5)
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('x')
ax1.set_ylabel('y')

theta = np.linspace(0, 2*np.pi, 400)
ax2.plot(2*np.cos(theta), 2*np.sin(theta), 'r-', lw=2.5)
ax2.axvline(0.5, color='red', ls='--', alpha=0.7, lw=1.5)
ax2.set_title('不是函数\n竖线 x=0.5 交了2个点', fontsize=14, color='red')
ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-2.5, 2.5)
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')
ax2.set_xlabel('x')
ax2.set_ylabel('y')

plt.tight_layout()
save('ch02_vertical_line_test')

# ============================================================
# 图8：y=1/x 渐近线图
# ============================================================
fig, ax = plt.subplots(figsize=(7, 6))
x = np.linspace(-5, 5, 2000)
y = 1/x
y[np.abs(x) < 0.02] = np.nan
ax.plot(x, y, '#2b83ba', lw=2.5, label='y = 1/x')
ax.axhline(0, color='gray', lw=1, ls='--')
ax.axvline(0, color='gray', lw=1, ls='--')
ax.annotate('水平渐近线 y=0', xy=(3.5, 0.3), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
ax.annotate('垂直渐近线 x=0', xy=(0.3, 3.5), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
# 标注关键点
ax.scatter([1, -1], [1, -1], color='red', s=80, zorder=5, edgecolors='black')
ax.annotate('(1,1)', (1,1), xytext=(10,5), textcoords='offset points', fontsize=12)
ax.annotate('(-1,-1)', (-1,-1), xytext=(10,5), textcoords='offset points', fontsize=12)
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.grid(True, alpha=0.3)
ax.set_title('y = 1/x 的双曲线与渐近线', fontsize=16)
ax.legend(fontsize=12)
save('ch02_reciprocal')

print('\n全部图像生成完成（v2版）！')
