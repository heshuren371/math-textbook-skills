"""生成第14章所有数学图，保存为矢量PDF — 已验证的完整示例"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Polygon, Circle, FancyArrowPatch
import os

OUT = 'figures'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS'],
    'font.size': 12,
    'axes.linewidth': 1.0,
    'axes.unicode_minus': False,
})

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.05)
    fig.savefig(path + '.png', format='png', dpi=150, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    print(f'  ✓ {name}')

def new_fig(w=4.5, h=3.5):
    return plt.subplots(figsize=(w, h))

# ===== 角度示意图 =====
fig, ax = new_fig(3, 2.5)
ax.set_xlim(-0.3, 3); ax.set_ylim(-0.3, 2.7); ax.axis('off')
ax.annotate('', xy=(3,0), xytext=(0,0), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.annotate('', xy=(1.5,2.5), xytext=(0,0), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(3.05, 0, '$OA$', va='center', fontsize=11)
ax.text(1.6, 2.55, '$OB$', ha='left', fontsize=11)
ax.text(-0.15, -0.15, '$O$', ha='right', va='top', fontsize=11)
arc = Arc((0,0), 1.0, 1.0, theta1=0, theta2=np.degrees(np.arctan2(2.5,1.5)), lw=1.5, color='blue')
ax.add_patch(arc)
ax.text(0.85, 0.32, '$60^{\\circ}$', fontsize=10, color='blue')
save(fig, 'ch14_angle_demo')

# ===== 三角形分类（按角）=====
labels_by_angle = [
    ('锐角三角形', '三个角都 $<90^\\circ$', [(0,0), (2.5,0), (1.8,2)]),
    ('直角三角形', '有一个角 $=90^\\circ$', [(0,0), (2.5,0), (0,2)]),
    ('钝角三角形', '有一个角 $>90^\\circ$', [(0,0), (2.5,0), (0.5,1.5)]),
]
for i, (title, sub, verts) in enumerate(labels_by_angle):
    fig, ax = new_fig(3, 3)
    ax.set_xlim(-0.5, 3.2); ax.set_ylim(-0.5, 2.5); ax.axis('off')
    tri = Polygon(verts, closed=True, fill=None, edgecolor='black', lw=1.5)
    ax.add_patch(tri)
    if i == 1:  # 直角标记
        ax.plot([0.3,0.3], [0,0.3], 'k-', lw=1)
        ax.plot([0,0.3], [0.3,0.3], 'k-', lw=1)
    ax.text(1.25, -0.8, f'{title}\n{sub}', ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none'))
    save(fig, f'ch14_tri_angle_{i}')

# ===== 同位角与内错角 =====
fig, ax = new_fig(5, 4)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.axis('off')
ax.plot([-3.5,3.5], [2,2], 'k-', lw=1.5)
ax.plot([-3.5,3.5], [-2,-2], 'k-', lw=1.5)
ax.text(3.6, 2, '$a$', va='center', fontsize=11)
ax.text(3.6, -2, '$b$', va='center', fontsize=11)
xs = np.linspace(-3, 3, 50); ax.plot(xs, xs, 'k-', lw=1.5)
arc = Arc((2,2), 0.8, 0.8, theta1=45, theta2=90, lw=1.5, color='blue')
ax.add_patch(arc); ax.text(1.55, 2.2, '$1$', fontsize=10, color='blue')
arc = Arc((-2,-2), 0.8, 0.8, theta1=45, theta2=90, lw=1.5, color='blue')
ax.add_patch(arc); ax.text(-2.45, -1.8, "$1'$", fontsize=10, color='blue')
arc = Arc((2,2), 0.8, 0.8, theta1=270, theta2=315, lw=1.5, color='red')
ax.add_patch(arc); ax.text(2.3, 1.6, '$2$', fontsize=10, color='red')
arc = Arc((-2,-2), 0.8, 0.8, theta1=90, theta2=135, lw=1.5, color='red')
ax.add_patch(arc); ax.text(-2.3, -1.6, "$2'$", fontsize=10, color='red')
ax.text(0, -3.2, '同位角相等：$\\angle 1 = \\angle 1\'$\qquad 内错角相等：$\\angle 2 = \\angle 2\'$',
        ha='center', fontsize=10)
save(fig, 'ch14_angle_relations')

print('✅ 所有图生成完毕')
