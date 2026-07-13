"""
第20章数轴图参考实现 — 使用Unicode避免mathtext兼容问题
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = 'figures'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS'],
    'font.size': 11,
    'axes.unicode_minus': False,
})

C_MAIN = '#000000'
C_AUX  = '#666666'
C_BLUE = '#1a5276'
C_RED  = '#922b21'

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.08)
    fig.savefig(path + '.png', format='png', dpi=200, bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
    print(f'  ✓ {name}')

def draw_axis(ax, xmin, xmax):
    ax.plot([xmin, xmax], [0, 0], '-', color=C_MAIN, lw=1.2)
    ax.plot([xmax-0.1, xmax], [0.05, 0], '-', color=C_MAIN, lw=1.0)
    ax.plot([xmax-0.1, xmax], [-0.05, 0], '-', color=C_MAIN, lw=1.0)
    for tick in range(int(xmin)+1, int(xmax)):
        if tick > xmin and tick < xmax:
            ax.plot(tick, 0, '|', color=C_AUX, ms=4, mew=0.8)

def open_circle(ax, x, y=0, r=0.09):
    ax.add_patch(plt.Circle((x, y), r, fill=False, edgecolor=C_RED, lw=2.0, zorder=5))

def closed_circle(ax, x, y=0, r=0.09):
    ax.add_patch(plt.Circle((x, y), r, fill=True, facecolor=C_RED, edgecolor=C_RED, lw=2.0, zorder=5))

def ray_right(ax, x_start, x_end, y=0, color=C_RED):
    ax.plot([x_start, x_end], [y, y], '-', color=color, lw=3.5, solid_capstyle='butt')

def ray_left(ax, x_start, x_end, y=0, color=C_RED):
    ax.plot([x_start, x_end], [y, y], '-', color=color, lw=3.5, solid_capstyle='butt')

# ===== 图1: x > 2（空心圈向右）=====
fig, ax = plt.subplots(figsize=(5.5, 1.6))
ax.set_xlim(-0.5, 6); ax.set_ylim(-0.5, 0.9); ax.axis('off')
draw_axis(ax, 0, 5.5)
open_circle(ax, 2)
ray_right(ax, 2.15, 5.5)
ax.text(4, 0.38, 'x > 2', ha='center', fontsize=12, color=C_RED, fontweight='bold')
ax.text(2, -0.35, '空心圈：不含2', ha='center', fontsize=9, color=C_AUX)
save(fig, 'numline_gt')

# ===== 图2: x ≥ 2（实心点向右）=====
fig, ax = plt.subplots(figsize=(5.5, 1.6))
ax.set_xlim(-0.5, 6); ax.set_ylim(-0.5, 0.9); ax.axis('off')
draw_axis(ax, 0, 5.5)
closed_circle(ax, 2)
ray_right(ax, 2, 5.5)
ax.text(4, 0.38, 'x ≥ 2', ha='center', fontsize=12, color=C_RED, fontweight='bold')
ax.text(2, -0.35, '实心点：含2', ha='center', fontsize=9, color=C_AUX)
save(fig, 'numline_ge')

# ===== 图3: 不等式组 x>2 且 x≤4 → 2<x≤4 =====
fig, ax = plt.subplots(figsize=(6.5, 2.8))
ax.set_xlim(-0.5, 6); ax.set_ylim(-1.2, 1.0); ax.axis('off')
draw_axis(ax, 0, 5.5)
# 上：x > 2
open_circle(ax, 2, y=0.55)
ray_right(ax, 2.15, 5.5, y=0.55, color=C_BLUE)
ax.text(4, 0.78, 'x > 2', ha='center', fontsize=10, color=C_BLUE)
# 下：x ≤ 4
closed_circle(ax, 4, y=-0.55)
ray_left(ax, 3.85, 0, y=-0.55, color=C_BLUE)
ax.text(1.5, -0.78, 'x ≤ 4', ha='center', fontsize=10, color=C_BLUE)
# 重叠
ray_right(ax, 2, 4, y=0, color=C_RED)
ax.text(3, 0.22, '重叠', ha='center', fontsize=9, color=C_RED, fontweight='bold')
ax.text(3, -0.3, '解集: 2 < x ≤ 4', ha='center', fontsize=11, color=C_RED,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9))
save(fig, 'numline_system')

# ===== 图4: 四种基本类型 =====
fig, axes = plt.subplots(4, 1, figsize=(7, 4.5))
for i, ax_i in enumerate(axes):
    ax_i.set_xlim(-0.8, 8.5); ax_i.set_ylim(-0.7, 0.7); ax_i.axis('off')
    draw_axis(ax_i, 0, 8)
    if i == 0:   # 大大取大
        for (x, yo) in [(5,0.45),(3,-0.45)]: open_circle(ax_i, x, y=yo)
        ray_right(ax_i,5.15,7.8,y=0.45,color=C_BLUE); ray_right(ax_i,3.15,7.8,y=-0.45,color=C_BLUE)
        closed_circle(ax_i,5,y=0); ray_right(ax_i,5,7.8,y=0,color=C_RED)
        ax_i.text(0.2,0.42,'① 大大取大：x>5 且 x>3 → x>5',ha='left',fontsize=10)
    # ... (其余类型类似)
plt.tight_layout(pad=0.3)
save(fig, 'numline_four_types')
