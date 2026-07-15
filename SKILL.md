---
name: report-writing
description: |
  按学术规范生成课程论文 LaTeX 源文件并用 xelatex 编译为 PDF。
  适用于中文学术课程论文（封面页、摘要页、目录、正文、参考文献），
  兼容三线表、LaTeX 标准公式符号、PyCharm/IDEA 风格代码高亮、学术页眉页脚。
  Trigger: 用户要求 "用 report-writing 写一篇课程论文 …"、"按课程论文版式生成 …"、
  "把这篇内容用课程论文模板排版 …"，或直接 @report-writing。
---

# report-writing

按中文学术规范排版课程论文，输出 `.tex` 源文件并编译为 PDF。

## 1. 使用条件

- **编译器**：必须用 `xelatex`（不要用 `pdflatex`），因为模板依赖 `xeCJK` 与 `fontspec`。
- **字体**：默认在导言区声明了常见 Linux/Mac/Windows 都可能命中的 CJK 字体
  `Noto Serif CJK SC`、`Noto Sans CJK SC`、`Noto Sans Mono CJK SC`；
  若用户的 TeX 环境中字体名不同，会自动回退到 `ctex` 默认字体，无需改 `.tex`。
- **logo/底图**：默认使用模板所在目录的 `assets/header_logo.png`（页眉）与
  `assets/cover_bg.png`（封面底图）。调用方可在每次请求里显式指定替代路径，
  或声明 "不要 logo / 不要封面底图"，模板会按 §3 策略回退。

## 2. 必填与选填信息

调用方在请求里需要提供以下信息。**未提供且未使用默认** 的项，模板留空（封面个人信息
行只有横线，无内容；不影响版式）。

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `title_zh` | 是 | 中文标题 |
| `title_en` | 是 | 英文标题（同时作为英文摘要页标题） |
| `author` | 是 | 姓名 |
| `class` | 是 | 班级，例如 信管T2401 |
| `student_id` | 是 | 学号 |
| `college` | 否 | 学院，例如 信息管理与人工智能学院 |
| `advisor` | 否 | 指导教师 |
| `date` | 否 | 提交日期；默认 `\today` |
| `abstract_zh` | 是 | 中文摘要正文 |
| `keywords_zh` | 是 | 中文关键词，分号分隔 |
| `classification_zh` | 否 | 中图分类号 |
| `abstract_en` | 是 | 英文摘要正文 |
| `keywords_en` | 是 | 英文关键词，分号分隔 |
| `classification_en` | 否 | 英文中图分类号 |
| `figure_count` | 否 | "图 X 表 Y 参 Z 篇" 中的 X，默认 0 |
| `table_count` | 否 | 同上 Y，默认按正文 `\caption` 自动计算；本模板采用手动填写 |
| `ref_count` | 否 | 同上 Z，默认按 `\begin{thebibliography}` 手动填写 |
| `sections` | 是 | 章节正文，按 §5 的小标题体系 |
| `tables` / `figures` | 否 | 表格与图片的占位内容 |
| `bibitems` | 是 | 参考文献条目，见 §6 |
| `code_blocks` | 否 | 代码段；如有则 §7 |
| `cover_bg` | 否 | 自定义封面底图绝对路径；空则用默认 `assets/cover_bg.png`，再无则 §3 策略 |
| `header_logo` | 否 | 自定义页眉 logo 绝对路径；空则用默认 `assets/header_logo.png`，再无则 §3 策略 |

## 3. Logo / 底图的回退策略

- **页眉 logo**：
  - 有 → 左侧显示，高度 0.86cm，右上角写论文题目。
  - 无 → 整个页眉改为"居中显示论文中文标题"，不再保留左上角空位。
- **封面底图 (`cover_bg`)**：
  - 有 → 整页铺满底图，再用白底矩形覆盖原题目/个人信息位置，绘制新版面。
  - 无 → 不使用任何底图，标题与个人信息按页面黄金比例垂直居中分布，填满整页。

## 4. 版式特征（继承自参考论文）

以下参数已经写死在 `templates/main.tex.tmpl` 中，调用方一般不需要改：

- 页面：A4，`left=2.65cm right=2.65cm top=1.58cm bottom=2.45cm includehead`
- 正文字号：小四 (`\zihao{-4}`)，行距 1.54，段首缩进 2 字符
- 字体：宋体正文、黑体标题、Latin Modern 西文
- 章节标题：黑体，section=小三，subsection=四号，subsubsection=小四
- 目录：宋体，"目  录" 黑体小三居中，"第 X 章" 前缀，页码前点引线
- 表格：三线表（`booktabs`），表注在表上方，字体 `small`
- 公式：标准 `equation` / `aligned`，不加方框
- 引用：`natbib` 的 `\cite{}`，上角标方括号样式
- 页眉：左侧 logo（如有） + 右侧论文题目 + 横线 0.4pt
- 页脚：页码居中
- 参考文献：`thebibliography` 手工条目，编号上角标方括号

## 5. 章节标题体系

| 层级 | LaTeX | 字号 | 字体 |
| --- | --- | --- | --- |
| 一级 | `\section{}` | 小三 | 黑体 |
| 二级 | `\subsection{}` | 四号 | 黑体 |
| 三级 | `\subsubsection{}` | 小四 | 黑体 |

正文使用自然段，`\par` 换段；不需要再额外写 `\par`。

## 6. 参考文献

每条格式：

```tex
\bibitem{key} 作者. 题名[J/专著/报告/网页]. 出版地: 出版者, 年: 页码.
```

模板会按出现顺序编号。

## 7. 代码段

如有代码，使用 `listings` 宏包 + PyCharm/IDEA 风格的配色（Darcula 主题近似），
外加 `tcolorbox` 圆角边框（边框粗细 0.4pt，圆角 1pt），与正文区分。
调用方只需传入 `code_blocks = [{lang:"python", caption:"...", body:"..."}]`，
模板会自动渲染。

## 8. 表格与图

- 表注在表上方，使用 `\caption{...}`。
- 图注在图下方，使用 `\caption{...}`。
- 表格默认三线表，列宽由 `tabularx` 自动撑开。
- 图片用 `figure[H]` 浮于原位。

## 9. 调用协议

调用方按以下顺序发送请求：

1. 触发词（"用 report-writing 写课程论文 …"）
2. 课程论文元数据（标题中英、姓名、班级、学号、可选学院/指导教师/日期）
3. 摘要中英、关键词中英、分类号（如有）
4. 各章节正文（按 §5 标题层级）
5. 表格 / 图片 / 代码段（如有）
6. 参考文献列表（按 §6 格式）
7. 封面底图与页眉 logo 的特殊声明（如有）

**示例**：

> 用 report-writing 写一篇课程论文。
> 中文标题：基于 XXX 的 YYY 研究
> 英文标题：A Study of YYY Based on XXX
> 作者：张三
> 班级：信管T2401
> 学号：8304240101
> 学院：信息管理与人工智能学院
> 指导教师：李四
> 摘要（中文）：……（一段）
> 关键词（中文）：XXX；YYY；ZZZ
> 摘要（英文）：……（一段）
> 关键词（英文）：XXX; YYY; ZZZ
> 章节：
> 1 引言
> 2 模型
>   2.1 假设
>   2.2 构建
> 3 结论
> 参考文献：
> [1] 作者. 题名[J]. 期刊, 年, 卷(期): 页码.
> ……

## 10. 模板渲染流程

调用方提供完整信息后，本 skill 会：

1. 把信息合并进 `templates/main.tex.tmpl`（封面 + 摘要 + 目录 + 正文 + 参考文献
   全部在同一 `.tex` 中），把结果写到 `OUT_DIR/<paper>.tex`。
2. 用 `xelatex -interaction=nonstopmode` 编译两遍以解决目录与引用。
3. 失败时给出 `*.log` 中的关键错误，常见原因：缺字体、缺 `assets/header_logo.png`
   / `assets/cover_bg.png` 时又未声明 §3 回退、参考文献 key 与 `\cite{}` 不一致。

## 11. 不在范围内

- PPT、Word、报告类排版（学校内部报告用本 skill 显得过重）——请用其他 skill。
- 硕博学位论文（章节体系、声明页、独创性声明、致谢、答辩页等需要额外模板，
  本 skill 不覆盖）。
- 英文论文（标题层级、字体、页眉都不一样，参数需重写）。