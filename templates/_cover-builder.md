封面构建器（cover builder）说明
================================

skill 在替换主模板的 {{COVER}} 占位符时，会按以下分支选择注入片段：

------------------------------------------------------------------------
分支 A:  有 cover_bg（用户提供 cover_bg 路径，或默认 assets/cover_bg.png 存在）
------------------------------------------------------------------------

\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=south west,inner sep=0pt] at (current page.south west)
    {\includegraphics[width=\paperwidth,height=\paperheight]{{{COVER_BG_PATH}}}};

  % 题目行白底矩形
  \fill[white] ($(current page.south west)+(39mm,111.0mm)$)
    rectangle ($(current page.south west)+(178mm,137.8mm)$);
  \node[anchor=west,font=\heiti\zihao{-3}]
    at ($(current page.south west)+(42.5mm,124.7mm)$) {题\quad 目：};
  \node[align=center,font=\heiti\zihao{-3}]
    at ($(current page.south west)+(125mm,124.7mm)$)
    {\shortstack{ {{TITLE_ZH_LINES}} }};

  % 个人信息行白底矩形
  \fill[white] ($(current page.south west)+(39mm,42mm)$)
    rectangle ($(current page.south west)+(178mm,85.0mm)$);

  % ===== 个人信息行（tabularx 模式：左侧标签列等宽，右侧下划线随内容长度）=====
  \node[anchor=north west,inner sep=0pt] at ($(current page.south west)+(39mm,82mm)$) {
    \begin{tabularx}{139mm}{@{}p{32mm}@{\hspace{1em}}X@{}}
      \heiti\zihao{-3} 姓\hspace{2em}名： & \heiti\zihao{-3} \underline{\makebox[60mm][c]{{AUTHOR}}} \\[1.6em]
      \heiti\zihao{-3} 班\hspace{2em}级： & \heiti\zihao{-3} \underline{\makebox[60mm][c]{{CLASS}}}   \\[1.6em]
      \heiti\zihao{-3} 学\hspace{2em}号： & \heiti\zihao{-3} \underline{\makebox[60mm][c]{{STUDENT_ID}}} \\[1.6em]
      {{INFO_ROWS_EXTRA}}
    \end{tabularx}
  };
\end{tikzpicture}

------------------------------------------------------------------------
分支 B:  无 cover_bg（无底图，按页面黄金比例居中分布）
------------------------------------------------------------------------

\begin{tikzpicture}[remember picture,overlay]
  % 题目：页面 1/3 高度处居中
  \node[align=center,font=\heiti\zihao{2}]
    at ($(current page.north)+(0,-0.33\paperheight)$)
    {\shortstack{ {{TITLE_ZH_LINES}} }};

  % 个人信息：页面 2/3 高度处居中
  \node[anchor=north] at ($(current page.north)+(0,-0.62\paperheight)$) {
    \begin{tabularx}{130mm}{@{}p{34mm}@{\hspace{1em}}X@{}}
      \heiti\zihao{3} 姓\hspace{2em}名： & \heiti\zihao{3} \underline{\makebox[60mm][c]{{AUTHOR}}} \\[1.6em]
      \heiti\zihao{3} 班\hspace{2em}级： & \heiti\zihao{3} \underline{\makebox[60mm][c]{{CLASS}}}   \\[1.6em]
      \heiti\zihao{3} 学\hspace{2em}号： & \heiti\zihao{3} \underline{\makebox[60mm][c]{{STUDENT_ID}}} \\[1.6em]
      {{INFO_ROWS_EXTRA}}
    \end{tabularx}
  };
\end{tikzpicture}

------------------------------------------------------------------------
{{INFO_ROWS_EXTRA}} 追加规则
------------------------------------------------------------------------

如果用户额外提供 college / advisor / date，依次追加如下行（在学号之后）：

  \heiti\zihao{-3} 学\hspace{2em}院： & \heiti\zihao{-3} \underline{\makebox[60mm][c]{{COLLEGE}}}    \\[1.6em]
  \heiti\zihao{-3} 指导教师：        & \heiti\zihao{-3} \underline{\makebox[60mm][c]{{ADVISOR}}}    \\[1.6em]
  \heiti\zihao{-3} 提交日期：        & \heiti\zihao{-3} \underline{\makebox[60mm][c]{{DATE}}}       \\

字号规则：

- 有 cover_bg：字号 -3（小四 之上），与题目字号匹配
- 无 cover_bg：字号 3（小三），让个人信息更醒目

------------------------------------------------------------------------
{{TITLE_ZH_LINES}} 处理规则
------------------------------------------------------------------------

如果中文标题超过 24 字，自动按 `\shortstack{...\\...}` 在视觉上换行
（语义上仍是同一行）。换行点优先选在"基于/的/与/对"等连接词之后。

------------------------------------------------------------------------
页眉 logo 区域（主模板 {{HEADER_LOGO}}）的两种分支
------------------------------------------------------------------------

分支 A:  有 header_logo → 保留
\fancyhead[L]{\raisebox{-0.12cm}{\includegraphics[height=0.86cm]{{{HEADER_LOGO_PATH}}}}}

分支 B:  无 header_logo → 整个 fancyhead 居中显示题目
\fancyhead[L]{\hfill\fontsize{10.5pt}{12pt}\selectfont {{TITLE_ZH}}\hfill}