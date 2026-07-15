章节正文构建器（sections builder）说明
======================================

调用方按以下格式提供 sections（plain text），skill 按行解析：

  # 1 引言
  正文段……
  正文段……

  # 1.1 背景
  正文段……

  # 1.1.1 子节
  正文段……

  # 2 模型
  ……

转换规则：

  - `# N 标题`    → `\section{标题}`
  - `# N.M 标题`  → `\subsection{标题}`
  - `# N.M.K 标题` → `\subsubsection{标题}`

  - 段与段之间用一个空行分隔
  - 段内允许 inline 数学 `$...$`、引用 `\cite{key}`、强调 `\emph{}`、加粗 `\textbf{}`
  - 独立公式块用 `$$ ... $$`
  - 表格插入用占位符：

      [TABLE: 标题
        col widths: 1.5cm Y Y
        rows:
          | 符号 | 含义 | 解释 |
          | R   | 收益 | 数值 |
      ]

    skill 渲染为：

      \begin{table}[H]
      \centering
      \caption{标题}
      \small
      \begin{tabularx}{\textwidth}{>{\centering\arraybackslash}p{1.5cm}Y Y}
        \toprule
        \textbf{符号} & \textbf{含义} & \textbf{解释} \\
        \midrule
        R   & 收益 & 数值 \\
        \bottomrule
      \end{tabularx}
      \end{table}

  - 图片插入用占位符：

      [FIGURE: 标题 | path/to/fig.png | width=0.6\textwidth]

    skill 渲染为：

      \begin{figure}[H]
      \centering
      \includegraphics[width=0.6\textwidth]{path/to/fig.png}
      \caption{标题}
      \end{figure}

  - 代码段插入用占位符：

      [CODE: language=python caption="示例代码"
        x = 1
        print(x)
      ]

    skill 渲染为：

      \begin{codeframebox}
      \begin{lstlisting}[style=ide-dark]
      x = 1
      print(x)
      \end{lstlisting}
      \end{codeframebox}

注意：

- 章节中的所有数学符号、希腊字母（如 $\alpha$ $\beta$ $\Delta$）应使用标准 LaTeX 写法
- 单位、变量名、函数名要使用 `$...$` inline 数学包裹
- 长公式使用 `equation` 或 `aligned` 环境，由 skill 自动判定