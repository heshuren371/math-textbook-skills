# 外部 Skill 评估记录（2026-07-15）

评估了 skillsmp.com 和 skills.sh 上的 6 个数学相关 skill，结论：**均不需要集成**。

## 评估标准

若满足以下任一条件则集成：
1. 产出可直接用于 LaTeX 教材的图/内容
2. 工作流与已有管线互补而非重叠
3. 填补已有工具链的明确缺口

## 逐项评估

### skillsmp.com — jihe520/MathModelAgent

**仓库定位**：数学建模竞赛（国赛/美赛）72 小时工作流

| Skill | 功能 | 对教材？ | 原因 |
|-------|------|:--------:|------|
| `mathmodel-figure-templates` | 11 个科研图模板（SHAP/ROC/泰勒图/和弦图） | ❌ | AI/ML 论文插图，非教材教学插图 |
| `1start-mathmodel` | 竞赛工作流入口 | ❌ | 竞赛流程，非教材编写 |
| `3coding-visual` | 代码+可视化 | ❌ | 竞赛用，理念已被 mathplot.py 覆盖 |
| `4drawio` | DrawIO 流程图 | ⚠️ | 知识依赖图等可参考，但非必需 |
| `5writing` | Typst/LaTeX 双引擎论文 | ⚠️ | Typst 方向对但模板为竞赛定制 |
| `6verity` | 论文验证 | ❌ | 竞赛论文检查项 |

**唯一收获**：从脚本中提取了 4 个值得融入的 matplotlib 技术，均已落地：

| 技术 | 落地位置 |
|------|---------|
| `pdf.fonttype: 42` | `mathplot.py` rcParams（两份） |
| `fig.add_gridspec()` | 备注，等用到时参考 |
| 自包含 `kde_1d()` | `workspace/math-templates/utils_kde.py` |
| `set_box_aspect()` + 透明 pane | 备注，等多元微积分章节时用 |

### skills.sh — jamesrochabrun/math-teacher

**定位**：交互式 HTML/JS 数学教具生成器

生成浏览器可玩的可视化演示（滑块、动画、Canvas 绘图），覆盖小学到实分析。

**对教材**：❌ 目前用不上。产出是 HTML 文件而非 PDF/LaTeX。可考虑未来为教材做配套交互网站时参考。

**记住它的理由**：ε-δ 收敛拖滑块、梯度下降小球滚动、黎曼和分区数调节——这些概念在静态 PDF 中只能画示意图，在 HTML 中可以做真正交互的。教材出在线版时再回头看。

## 核心教训

1. **竞赛工具≠教材工具**。竞赛是 72 小时 sprint，教材是长期系统工程，工作流不兼容。
2. **科研插图≠教学插图**。SHAP 图、ROC 曲线对教材读者没有意义，函数图像、ε-δ 带形图才是需要的。
3. **学代码风格比学工具更有价值**。`make_taylor_diagram.py` 的 polar→xy 映射技巧、`make_correlation_pairgrid.py` 的自包含 KDE，比集成整个 skill 有用。
4. **已有工具链已经很完整**。`latex-math-book-authoring` + `math-review` + `mathplot.py` + `mathkit` 覆盖了教材编写的全部需求，外部 skill 引入会破坏一致性。
