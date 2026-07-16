# Trigonometric高考 Problem Analysis (第19题 class)

源自 2026-07-06 会话。第19题: f(x) = 5cos x - cos 5x + 证明存在 y 使 cos y ≤ cos θ + 求 b_min。

## 核心技巧总结

### 1. cos 5x 的展开

使用余弦五倍角公式将 cos 5x 展开为 cos x 的多项式:

$$ \cos 5x = 16\cos^5 x - 20\cos^3 x + 5\cos x $$

代入 f(x) = 5cos x - cos 5x 化简为:

$$ f(x) = -16\cos^5 x + 20\cos^3 x = 4\cos^3 x(5 - 4\cos^2 x) $$

换元 t = cos x 将三角函数问题转化为多项式最值问题。

### 2. 驻点分类法（Part 3 的关键）

对 f_φ(x) = 5cos x - cos(5x+φ) 求导:

$$ f_φ'(x) = 5(\sin(5x+\varphi) - \sin x) = 0 $$

sin A = sin B 有两族解:

- **族(I)**: A = B + 2kπ → 5x+φ = x+2kπ → x = (2kπ-φ)/4, f = 5cos x - cos x = 4cos x
- **族(II)**: A = π-B+2kπ → 5x+φ = π-x+2kπ → x = (π+2kπ-φ)/6, f = 5cos x - (-cos x) = 6cos x

这样 f_φ 的全部驻点被归类为两个简单家族，其函数值直接由 cos x 给出。

### 3. Minimax下界论证

要证明 b_min ≤ 3√3 (上界)，直接取 φ = 0 代入 Part (1) 结果。

要证明 b_min ≥ 3√3 (下界)，利用**族(II)** 的值:

令 θ = (π-φ)/6，族(II) 的值包含:

$$ 6\cos\theta,\ 6\cos(\theta+\tfrac{\pi}{3}),\ 6\cos(\theta-\tfrac{\pi}{3}),\ -6\cos\theta $$

三个 cos 值在单位圆上间隔 π/3，其最大值的**最小值**在 θ = π/6 时达到，为 cos(π/6) = √3/2。因此:

$$ \max_x f_\varphi(x) \geq 6 \times \frac{\sqrt{3}}{2} = 3\sqrt{3} $$

### 4. cos 单调性证明 (Part 2)

要证: ∀θ ∈ (0,π), a ∈ ℝ, ∃y ∈ [a-θ, a+θ] 使 cos y ≤ cos θ.

分两类:
- **θ > π/2**: 区间长度 > π, 必含 cos 的最小值点 π+2kπ → cos y = -1 ≤ cos θ ✓
- **θ ≤ π/2**: 平移 a 到 [-π,π]。若 a ≥ 0, 取 y = a+θ, 由 cos 在 [0,π] 递减得 cos(a+θ) ≤ cos θ。若 a < 0, 由偶函数性 + 同理。

## 可扩展的模式

这种"两族驻点 → 一族给出明显的下界"结构可以推广到任何形如:

$$ A\cos x + B\cos(nx+\varphi) $$

的函数，其中 x 和 nx 的相位差可以分类为 A = B + 2kπ 和 A = π - B + 2kπ 两个族。
