# 线性代数泛化测试记录

**目标**: 验证 `math-textbook-authoring` 技能从数学分析领域泛化到线性代数领域的能力

**日期**: 2026-07-17

## 测试流程

1. `init "线性代数"` → ✅
2. `chapter new ch01 "向量——从箭头到坐标"` → ✅
3. 写完整 LaTeX 内容（含应用引导、定义框、例题5道、符号卡片、代码验证、小结、习题30道）
4. 生成 6 幅矢量图（Python + matplotlib → PDF）
5. `audit structural ch01` → 捕获环境配对、数学模式、Unicode 毒瘤
6. `fix all ch01` → 自动修复 10 处 `→` 转 `$\to$`
7. `tectonic book.tex` → 首次编译报错，修复后零错误输出

## 遇到的问题

| # | 问题 | 根因 | 修复 |
|---|------|------|------|
| 1 | `exercise` 环境未定义 | 管线 preamble 模板只定义了 tcolorbox | 补 `\newenvironment{exercise}` 到 pipeline 的 init 模板 |
| 2 | `figure` 在 tcolorbox 内 → Not in outer par mode | 图放在了定义框/例题框里 | 技能陷阱表补 #12 |
| 3 | `\overrightarrow` 在 `\caption` → Illegal parameter number | 脆弱命令需要 `\protect` | 技能陷阱表补 #13 |
| 4 | emoji `🔓🔒🔥` 在 examplebox 标题 → Missing character | tcolorbox 标题用 Latin Modern Roman 字体不含 emoji | 技能陷阱表补 #14 |
| 5 | `，` 在 `\[...\]` 中无 `\text{}` | 中文逗号在数学模式被视为符号，lmroman 字体不含 | `\text{}` 包裹或移到数学模式外 |

## 结论

- **核心管线 100% 可用**: init/chapter new/audit/fix/build 全部在代数领域工作正常
- **MATHBOOK_LANG 和 MATHBOOK_EXERCISES** 环境变量正确控制中文标签和习题数量
- **3 个 LaTeX 陷阱** 是从测试中发现的技能缺口，已补入 SKILL.md
- **1 个代码修复**: pipeline 的 preamble 模板补了 exercise/answer 环境
- **评分**: PASS+ —— 一个新手拿到 SKILL.md 后可以写出质量相近的教材，但需要留意 3 个陷阱和 preamble 补全

## 产出

- `book.pdf` (275KB, 20+ 页, 6 幅图, 30 道习题)
- 所有修正已合并到 `math-analysis/SKILL.md` 和 `mathbook-pipeline.py`
