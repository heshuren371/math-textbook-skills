# Geometry Plotting with matplotlib (高考解析几何)

## Overview

Use the `mathplot` module (auto-configures Chinese fonts) + standard matplotlib patches to draw geometry figures for 高考 conic section problems.

## Setup

```python
import sys; sys.path.insert(0, '.')
import mathplot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Arc, FancyArrowPatch
import math
```

## Drawing an Ellipse

```python
a, b, c = 2, math.sqrt(3), 1  # a=半长轴, b=半短轴, c=焦距
theta = np.linspace(0, 2*math.pi, 400)
ell_x = a * np.cos(theta)
ell_y = b * np.sin(theta)
ax.plot(ell_x, ell_y, 'b-', linewidth=2, label='椭圆 C')
```

## Drawing a Line with Parameter m

For line through focus F(-c, 0) with slope parameter `m` (in form x = my - c):

```python
m = 2 / math.sqrt(5)  # example
y_range = np.linspace(-2, 2, 100)
x_line = m * y_range - c
ax.plot(x_line, y_range, 'g-', linewidth=1.5, label='l')
```

## Computing Ellipse-Line Intersections

Substitute x = my - c into ellipse x²/a² + y²/b² = 1:

```python
# (3m²+4)y² - 6my - 9 = 0  (for a²=4, b²=3, c=1)
coeff_a = 3*m**2 + 4
coeff_b = -6*m
coeff_c = -9
disc = coeff_b**2 - 4*coeff_a*coeff_c
y1 = (-coeff_b + math.sqrt(disc)) / (2*coeff_a)  # P (y > 0)
y2 = (-coeff_b - math.sqrt(disc)) / (2*coeff_a)  # Q (y < 0)
x1 = m*y1 - c
x2 = m*y2 - c
```

## Drawing Triangles (Polygon patches)

```python
# Triangle PQR
tri = Polygon(np.array([[x1, y1], [x2, y2], [x3, y3]]),
              fill=True, alpha=0.12, color='blue')
ax.add_patch(tri)
```

## Point and Line Annotations

```python
# Points
ax.scatter(x1, y1, color='red', s=60, zorder=6)
ax.text(x1+0.2, y1+0.1, 'P', fontsize=12, fontweight='bold', color='red')

# Dashed lines
ax.plot([x1, x3], [y1, y3], 'purple', lw=1, linestyle='--')

# Axis lines
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)

# Text boxes
ax.text(0.5, 0.5, r'$3S_{\\triangle PFO}=S_{\\triangle PQR}$', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
```

## Key Settings for Geometry Plots

```python
ax.set_aspect('equal')                    # Important! Keeps circles circular
ax.set_xlim(-a*1.4, a*1.4)               # Slightly wider than ellipse
ax.set_ylim(-b*1.4, b*1.4)
ax.set_title('描述性标题', fontsize=13)
ax.legend(fontsize=9, loc='upper right')
ax.grid(True, alpha=0.3)
```

## Common高考 Geometry Configurations

### Ellipse Parameters

| Given | Formulas |
|-------|----------|
| Focus F(-c,0), eccentricity e | a = c/e, b² = a² - c² |
| Ellipse: x²/a² + y²/b² = 1 | Vertex (-a,0), (a,0), (0,-b), (0,b) |

### Line Through Focus

Two parameterizations:
- `y = k(x + c)` (slope form, k > 0 for upward)
- `x = my - c` (y-as-param form, m = 1/k)

The y-as-param form avoids needing to handle vertical line cases.

### Symmetry Properties

- If a line passes through origin O and hits ellipse at P, the other intersection R is at **R = -P** (vector from O). This is the key to area ratio problems: S(△PQR) = 2·S(△PQO).

### tan∠PQR Formula

For ∠Q in triangle PQR with vertices P(x₁,y₁), Q(x₂,y₂), R = -P:

```
tan∠PQR = |det(QP, QR)| / (QP · QR)

det(QP, QR) = 2(y₂ - y₁)     [after simplification using x=my-c]
QP · QR = (1/3)(y₁² - y₂²)   [after simplification using ellipse eq]

tan∠PQR = 6 / (y₁ + y₂)      [simplified]
         = 6(3m²+4) / (6m)
         = 3m + 4/m
```

Minimize using AM-GM: `3m + 4/m ≥ 4√3`, equality when `3m = 4/m → m = 2/√3`.

## Completed Example: 高考第18题

Full solution available at `/tmp/math-viz-cn.png` (from session). Key results:

| Part | Answer |
|------|--------|
| (1) | x²/4 + y²/3 = 1 |
| (2)(i) | y = (√5/2)(x + 1) |
| (2)(ii) | min tan∠PQR = 4√3 |
