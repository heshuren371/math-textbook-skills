"""第16章 勾股定理——几何图生成参考（面积切割法/梯子/数轴）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Polygon, Ellipse
import os

OUT = './figures'
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC'],
    'font.size': 12, 'axes.linewidth': 1.0, 'axes.unicode_minus': False,
})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name+'.pdf'), format='pdf', bbox_inches='tight', pad_inches=0.05)
    fig.savefig(os.path.join(OUT, name+'.png'), format='png', dpi=150, bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)

def fig(w=4, h=3.5): return plt.subplots(figsize=(w, h))

# === 直角三角形标注 ===
f, ax = fig(4, 3.5)
ax.set_xlim(-0.5, 4.5); ax.set_ylim(-0.5, 3.5); ax.axis('off')
verts = [(0,0), (4,0), (0,3)]
from matplotlib.patches import Polygon as Pg
ax.add_patch(Pg(verts, closed=True, fill=None, edgecolor='black', lw=2))
ax.plot([0.4,0.4],[0,0.4],'k-',lw=1.2); ax.plot([0,0.4],[0.4,0.4],'k-',lw=1.2)
ax.text(2, -0.35, '$a$', ha='center', fontsize=14)
ax.text(-0.35, 1.5, '$b$', va='center', fontsize=14)
ax.text(2.2, 1.7, '$c$', ha='center', va='center', fontsize=14, rotation=-37)
ax.text(-0.1, -0.1, '$A$', ha='right', va='top', fontsize=12)
ax.text(4.1, -0.1, '$B$', ha='left', va='top', fontsize=12)
ax.text(-0.1, 3.1, '$C$', ha='right', va='bottom', fontsize=12)
save(f, 'right_triangle')

# === 面积切割法证明 ===
f, ax = fig(5.5, 5.5)
ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.5, 5.5); ax.axis('off')
a, b, s = 4, 3, 7
ax.plot([0,s,s,0,0],[0,0,s,s,0],'k-',lw=2)
tri_verts = [[(0,0),(0,b),(a,b)],[(a,b),(s,b),(s,0)],[(a,b),(a,s),(0,s)],[(s,0),(s,s-b),(a,s-b)]]
colors = ['#ffcccc','#ccffcc','#ccccff','#ffffcc']
for tri, c in zip(tri_verts, colors):
    ax.add_patch(Pg(tri, closed=True, fill=True, color=c, alpha=0.5, lw=1.5))
ax.add_patch(Pg([(a,b),(s,b),(a,s),(0,s-b)], closed=True, fill=None, edgecolor='red', lw=2.5, linestyle='--'))
ax.text(2, -0.4, '$a=4$', ha='center'); ax.text(4.5, -0.4, '$b=3$', ha='center')
ax.text(-0.4, 2, '$a=4$', va='center'); ax.text(-0.4, 4.5, '$b=3$', va='center')
ax.text(2.1, 2.1, '$c$', ha='center', va='center', fontsize=16, color='red',
        bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.8))
save(f, 'area_proof')
