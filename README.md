# report-writing

按中文学术规范排版课程论文 / 校内报告的 LaTeX 模板与渲染工具。输入结构化元数据，输出符合学术规范的 `.tex` 源文件并用 `xelatex` 编译为 PDF。

封面、摘要页（中文一页 + 英文一页）、目录、正文、参考文献一次生成，无需再手工调整版式。

## 实际输出效果

下面是使用仓库脚本和模板实际生成的课程论文封面。标题、作者信息、学校素材与日期均由结构化配置自动填充：

![课程论文生成效果](./docs/screenshots/cover.png)

## 特性

- **封面页**：可选 logo 与封面底图；无图时自动按页面比例居中分布，填满整页
- **个人信息**：姓名 / 班级 / 学号（必填），学院 / 指导教师 / 日期（可选）；冒号左侧等宽对齐，右侧下划线宽度固定、内容居中
- **摘要页**：中文摘要一页，英文摘要一页，含关键词与中图分类号
- **目录**：黑体小三居中标题，`第 X 章` 前缀，点引线
- **正文**：宋体正文、黑体标题，三线表（表注在上）、图注在下，标准 LaTeX 公式符号
- **代码**：PyCharm / IDEA 风格高亮（Darcula 配色），`tcolorbox` 圆角边框
- **页眉页脚**：左侧校徽（可选）+ 右侧论文题名 + 横线；页脚居中页码
- **参考文献**：`thebibliography` 手工条目，上角标方括号引用

## 目录结构

```
report-writing/
├── SKILL.md                    # skill 入口与调用协议
├── README.md
├── LICENSE
├── assets/
│   ├── header_logo.png         # 默认页眉 logo（可替换）
│   ├── cover_bg.png            # 默认封面底图（可替换）
│   └── README.md
├── scripts/
│   └── render.py               # 渲染脚本：meta.json -> .tex -> .pdf
├── templates/
│   ├── main.tex.tmpl           # 主模板
│   ├── cover.tmpl
│   ├── abstract-zh.tmpl
│   ├── abstract-en.tmpl
│   ├── sections.tmpl
│   ├── _cover-builder.md       # 封面构建器规范
│   ├── _abstract-builder.md
│   └── _sections-builder.md
└── examples/
    └── demo.md                 # 完整调用示例
```

## 环境要求

- **TeX 发行版**：TeX Live 或 MiKTeX，需包含 `xelatex`、`xeCJK`、`ctex`、`tcolorbox`、`listings`
- **Python**：3.8+（仅标准库，无第三方依赖）
- **字体**：默认尝试 `Noto Serif/Sans/Mono CJK SC`，缺失时自动回退 `SimSun` / `SimHei` / `FangSong`

## 快速开始

1. 准备一个 `meta.json`（字段说明见 `examples/demo.md`）：

```json
{
  "paper_id": "demo_course_paper",
  "title_zh": "基于强化学习的资源调度策略研究",
  "title_en": "A Study on Resource Scheduling Based on Reinforcement Learning",
  "author": "张三",
  "class": "信管T2401",
  "student_id": "8304240101",
  "advisor": "李四",
  "abstract_zh": "……",
  "keywords_zh": "强化学习；资源调度；云计算",
  "abstract_en": "……",
  "keywords_en": "reinforcement learning; resource scheduling; cloud computing",
  "figure_count": 1,
  "table_count": 1,
  "ref_count": 3,
  "sections": "# 1 引言\n\n正文……\n\n# 2 模型\n\n## 2.1 假设\n\n……\n\n[TABLE: 性能对比]\n| 策略 | 时间 | 利用率 |\n| Heuristic | 12.4s | 78% |\n| Q-Learning | 9.7s | 85% |\n\n[CODE: language=python caption=\"核心更新\"]\nQ[s, a] += alpha * (r + gamma * max(Q[s_next]) - Q[s, a])\n",
  "bibitems": [
    ["sutton", "SUTTON R S, BARTO A G. Reinforcement Learning[M]. MIT Press, 2018."]
  ]
}
```

2. 渲染并编译：

```bash
python scripts/render.py --json meta.json --out build/
```

产物：`build/<paper_id>.tex` 与 `build/<paper_id>.pdf`。

## 章节正文的写法

sections 字段是纯文本，按行解析：

| 写法 | 渲染为 |
| --- | --- |
| `# 1 引言` | `\section{引言}` |
| `## 2.1 假设` | `\subsection{假设}` |
| `### 2.1.1 子节` | `\subsubsection{子节}` |
| 空行分隔 | 段落 |
| `[TABLE: 标题]` + `| col \| col |` 行 | 三线表，表注在上 |
| `[FIGURE: 标题 \| path \| width=0.6\textwidth]` | 图片，图注在下 |
| `[CODE: language=python caption="..."]` + 代码行 | 带高亮的代码框 |

行内数学用 `$...$`，独立公式块用 `$$ ... $$`，引用用 `\cite{key}`。

## Logo 与封面底图

- 把校徽保存为 `assets/header_logo.png`，封面底图保存为 `assets/cover_bg.png`
- 也可在 `meta.json` 里指定 `header_logo` / `cover_bg` 的绝对路径临时覆盖
- 不提供 logo 时，页眉自动改为居中显示论文题目；不提供封面底图时，封面不铺底图、标题与个人信息按比例居中分布

## 作为 Codex Skill 使用

本仓库同时是一个 Codex skill。将仓库克隆到 `~/.codex/skills/` 下即可：

```bash
git clone https://github.com/xingchenyd/report-writing.git ~/.codex/skills/report-writing
```

随后在对话中说「用 report-writing 写一篇课程论文……」即可触发。

## License

MIT
