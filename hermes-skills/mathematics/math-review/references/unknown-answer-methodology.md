# 无答案可查时的数学验证方法论

## 核心原则：证据群（Swarm of Evidence）

不要依赖单一证明链。构建多重独立证据，每种证据有不同的失效模式：

- 人类手推 → 代数跳步、漏分类
- SymPy 符号验证 → 问题编码有误
- 数值随机采样 → 漏窄反例区域
- Z3 SMT 检查 → 逻辑编码不完整
- WolframScript → 与 SymPy 共享的数学误解
- 穷举枚举 → 空间太大无法全枚（仅适用小空间）

## 七种独立验证策略

### 1. 穷举枚举（Exhaustive Enumeration）

最硬的证据——不是"采样"，是"全检"。

**条件**：搜索空间 ≤ 10⁷

```python
import itertools
count = 0
for perm in itertools.permutations(range(1, 10)):
    if check_condition(perm):
        count += 1
```

**注意**：枚举代码可能有 bug。必须配合策略 2 交叉验证。

### 2. 双方法交叉验证（Two-Method Cross-Validation）

同一问题用两种代数结构完全不同的方法求解。

```python
# 方法 A：组合计数
ans_a = count_groupings() * factorial(3)**3  # 9 × 216 = 1944

# 方法 B：暴力枚举
ans_b = brute_force()  # 1944

assert ans_a == ans_b  # CERT
```

### 3. 临界边界枚举（Critical Boundary Enumeration）

全空间枚举不可行时，在"最危险区域"密集枚举。

```python
# 只枚举 mA+mB < 1 的临界区域（空间比全集小很多）
for alpha in critical_region:
    if not inequality_holds(alpha):
        report_counterexample()
```

### 4. 退化极限检验（Limit Case Testing）

将问题退化到已知答案的极限情形。

| 极限 | 退化为 | 验证结论 |
|------|--------|---------|
| α→0 | sin(mα) ≈ mα | n+m > 1 ✅ |
| α→π/m | A→0 | 1/A 主导 ✅ |
| C=0 | sin(mnα)=0 | A+B > 1/m ✅ |
| m=1 | 直接展开 | A²B+AB²+B² > 0 ✅ |

### 5. 三轨工具链独立验证（Triple-Track Toolchain）

三种完全独立的计算引擎：

| 轨道 | 引擎 | 语言 |
|------|------|------|
| SymPy | Python 符号计算 | Python |
| WolframScript | Mathematica 引擎 | Wolfram Language |
| 数值扫描 | NumPy 数值计算 | Python（纯数值） |

### 6. Z3 SMT 逻辑链检查

将推导链编码为一阶逻辑约束：

```python
solver.add(premises)
solver.add(Not(conclusion))
assert solver.check() == unsat
```

### 7. 形式化证明（Formal Proof）

使用 Lean/Coq 编写机器可检查的 deduction。

## CERT 条件（无答案对照时）

当以下条件全部满足时，答案置信度可达 CERT：

1. ✅ 至少两种代数结构不同的推导路径（双方法交叉）
2. ✅ 所有退化极限检验通过
3. ✅ 临界边界零违反
4. ✅ 至少两个独立计算引擎一致（三轨验证）
5. ✅ 逻辑链经机械化检查（Z3 unsat）

不需要"标准答案"来对照——证据群本身足够强。
