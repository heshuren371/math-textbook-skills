# 实战参考：《自学高数》项目

## 产出数据

| 指标 | 值 |
|------|----|
| 总页数 | 88 页 |
| 章节 | 10 章（函数 → 无穷级数） |
| 练习 | 62 道（含难度标注 [易]/[中]/[难]） |
| 矢量配图 | 8 张（Python → PDF） |
| 数值验证 | 每章附 Python lstlisting 代码段 |
| 附录答案 | 62 题全部解答 |
| 编译引擎 | tectonic（零错误） |

## 项目路径

```
~/zixue-gaoshu/
├── book.tex
├── compile.sh
├── book.pdf
├── shared/
│   └── preamble.tex
├── part1/
│   ├── ch01-hanshu.tex       # 函数
│   ├── ch02-jixian.tex       # 极限
│   ├── ch03-lianxu.tex       # 连续
│   ├── ch04-daoshu.tex       # 导数
│   ├── ch05-daoshu-yingyong.tex # 导数应用
│   ├── ch06-buding-jifen.tex    # 不定积分
│   ├── ch07-ding-jifen.tex      # 定积分
│   ├── ch08-ding-jifen-yingyong.tex # 定积分应用
│   ├── ch09-weifen-fangcheng.tex   # 微分方程
│   └── ch10-wuqiong-jishu.tex     # 无穷级数
├── appendix/
│   └── answers.tex
└── figures/                  # 8 张矢量图
```

## 编译命令

```bash
cd ~/zixue-gaoshu
tectonic book.tex    # 单次编译，自动下载缺失包
```

## 本次编译中修复的问题

1. `figure` 环境不能嵌套在 `tcolorbox` 内 → 裸用 `\includegraphics`
2. `\symbolitem` 宏转义复杂 → 改用 3 列简化版 + `\verb`
3. `\\` 在 `\[...\]` 中非法 → 用 `gathered` 环境
4. `\end{exercise}` 遗漏 → 脚本批量检查 begin/end 计数
5. `_` 在 tabular 文本列中触发 `Missing $` → `$a_n$`
6. `\times` 在文本模式 → `\( \times \)`
7. emoji 字符在 LaTeX 中不可渲染 → `[OK]` 替代 `✅`
8. `\displaystyle` 在 matplotlib 中不可用 → 省略
9. `\xrightarrow` 在 matplotlib mathtext 中不支持 → 用 `\to`
